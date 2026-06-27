#!/usr/bin/env python3
"""01 - Ingest & rename images to a collision-proof scheme, then update Multimedia.

Pipeline step 1 of 3   (01 ingest/rename -> 02 OCR -> 03 phenotype; each updates the DB
and appends to Multimedia_pipeline/PIPELINE_LOG.md).

WHY: camera filenames repeat across years (JCN_#### resets each season), which overwrote
2025 images when 2026 frames landed in the same folder. Fix = give every image a globally
unique, content-addressed name and keep the original name + date for provenance.

FOLDER CONVENTION (what users do)
    Multimedia_images/<year>/<YYYY-MM-DD>/<images>      e.g. 2026/2026-06-27/JCN_0294.JPG
  The date subfolder = one field day / upload batch. Flat <year>/<images> is also accepted
  (that is how the current 2025 & 2026 sets are stored), so this one script both migrates the
  existing images and ingests future dated batches.

WHAT IT DOES, per image
    year      = top-level year folder (authoritative)
    folderDate= the date subfolder name (verbatim; "" if the image sits straight in <year>/)
    sha256    = content hash;  sha8 = first 8 hex
    new_name  = "LEPA_<year>_<sha8>.jpg"     (unique; re-ingesting the same bytes = no-op)
    capture   = EXIF DateTimeOriginal (kept; null if a prior edit stripped it)
  Then COPIES the file verbatim into the MAIN folder (Multimedia_main/) — non-destructive,
  EXIF preserved; the year/date folders stay the immutable source. Writes the file registry
  (Multimedia_main/file_registry.csv) and updates Multimedia: rows already linked (matched by
  original filename + year) get identifier=<new_name> plus originalFilename / fileYear /
  folderDate / captureTimestamp / sha256. New images (no row yet) are only registered; their
  Multimedia row is created later by 02_ocr / load.

SAFE BY DEFAULT: dry-run unless --apply; backs up the DB before any write.

Usage:
  python3 Multimedia_pipeline/01_ingest_register.py            # dry-run, writes a preview registry
  python3 Multimedia_pipeline/01_ingest_register.py --apply    # copy + DB update + log
Options: --src-root DIR --main-dir DIR --db PATH --prefix LEPA
"""
import argparse, csv, hashlib, os, shutil, sqlite3, sys
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PROV_COLS = [("originalFilename", "TEXT"), ("fileYear", "TEXT"), ("folderDate", "TEXT"),
             ("captureTimestamp", "TEXT"), ("sha256", "TEXT")]
DTO, DT = 36867, 306

def sha256(path, buf=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(buf), b""):
            h.update(chunk)
    return h.hexdigest()

def capture(path):
    try:
        ex = Image.open(path)._getexif() or {}
        return ex.get(DTO) or ex.get(DT) or None
    except Exception:
        return None

def rec_year(createDate, occDate):
    for d in (occDate, createDate):
        if d and len(str(d)) >= 4 and str(d)[-4:].isdigit():
            return str(d)[-4:]
    return None

def collect(src_root):
    """Yield (year, folderDate, path) for every image under each <year>/ (flat or <year>/<date>/)."""
    out = []
    for ydir in sorted(p for p in src_root.iterdir() if p.is_dir() and p.name.isdigit()):
        for p in ydir.rglob("*"):
            if p.suffix.lower() not in (".jpg", ".jpeg") or p.name.startswith("."):
                continue
            rel = p.relative_to(ydir).parts
            folder_date = rel[0] if len(rel) > 1 else ""     # immediate subfolder, else flat
            out.append((ydir.name, folder_date, p))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-root", default=str(ROOT / "Multimedia_images"))
    ap.add_argument("--main-dir", default=str(ROOT / "Multimedia_main"))
    ap.add_argument("--db", default=str(ROOT / "LEPA_SQL.db"))
    ap.add_argument("--prefix", default="LEPA")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    src_root, main_dir, db = Path(args.src_root), Path(args.main_dir), Path(args.db)

    imgs = collect(src_root)
    if not imgs:
        sys.exit(f"No images under year subfolders of {src_root}")
    years = sorted({y for y, _, _ in imgs})

    con = sqlite3.connect(db); con.row_factory = sqlite3.Row; cur = con.cursor()
    have_cols = {r[1] for r in cur.execute("PRAGMA table_info(Multimedia)")}
    has_orig = "originalFilename" in have_cols
    mm = {}   # (camera_name.lower(), year) -> [multimediaID]  (re-runnable: match the persistent
    for r in cur.execute(f"""SELECT m.multimediaID, m.identifier,
                            {'m.originalFilename' if has_orig else 'NULL AS originalFilename'},
                            m.createDate, o.occurrenceDate
                            FROM Multimedia m LEFT JOIN Occurrences o ON m.occurrenceID=o.occurrenceID
                            WHERE m.identifier IS NOT NULL"""):
        yr = rec_year(r["createDate"], r["occurrenceDate"])
        # originalFilename survives renames; fall back to identifier on a first, un-migrated run
        for key in {(r["originalFilename"] or r["identifier"]).lower(), r["identifier"].lower()}:
            mm.setdefault((key, yr), set()).add(r["multimediaID"])
    mm = {k: sorted(v) for k, v in mm.items()}

    import re as _re
    seen_hash, reg, updates, ambig = {}, [], [], []
    dups = newfiles = 0
    for year, fdate, p in imgs:
        digest = sha256(p)
        # date stamped into the name = the date subfolder if it is a real date, else EXIF, else year
        stamp = fdate if _re.match(r"\d{4}-\d{2}-\d{2}$", fdate or "") else \
                (str(capture(p))[:10].replace(":", "-") if capture(p) and _re.match(r"\d{4}:\d{2}:\d{2}", str(capture(p))) else year)
        new_name = f"{args.prefix}_{stamp}_{digest[:8]}.jpg"
        if digest in seen_hash:
            dups += 1; continue
        seen_hash[digest] = new_name
        mids = mm.get((p.name.lower(), year), [])
        if len(mids) == 1:
            mid, action = mids[0], "update_identifier"
            updates.append((mid, new_name, p.name, year, fdate, capture(p), digest))
        elif len(mids) > 1:
            mid, action = "", "AMBIGUOUS"; ambig.append((p.name, year, mids))
        else:
            mid, action = "", "register_new"; newfiles += 1
        reg.append(dict(new_name=new_name, original_name=p.name, year=year, folderDate=fdate,
                        sha256=digest, capture=capture(p) or "", src_path=str(p),
                        multimediaID=mid, action=action))

    print(f"src {src_root}: {len(imgs)} images, years {years}")
    print(f"  dated subfolders present: {sorted({f for _,f,_ in imgs if f}) or 'none (flat layout)'}")
    print(f"  unique files: {len(reg)} (identical-bytes skipped: {dups})")
    print(f"  -> update existing Multimedia identifier: {len(updates)}")
    print(f"  -> new files (registered, await 02_ocr) : {newfiles}")
    if ambig:
        print(f"  ⚠ AMBIGUOUS (same name+year on >1 row): {len(ambig)} -> {ambig[:5]}")

    if not args.apply:
        main_dir.mkdir(parents=True, exist_ok=True)
        with open(main_dir / "file_registry_PREVIEW.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(reg[0].keys())); w.writeheader(); w.writerows(reg)
        print(f"\nDRY-RUN. preview -> {main_dir/'file_registry_PREVIEW.csv'}. Re-run with --apply.")
        con.close(); return

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    bak = db.with_name(db.name + f".bak-ingest-{stamp}"); shutil.copy2(db, bak)
    main_dir.mkdir(parents=True, exist_ok=True)
    for col, typ in PROV_COLS:
        if col not in have_cols:
            cur.execute(f"ALTER TABLE Multimedia ADD COLUMN {col} {typ}")
    copied = 0
    for r in reg:
        dest = main_dir / r["new_name"]
        if not dest.exists():
            shutil.copy2(r["src_path"], dest); copied += 1
    for mid, new_name, orig, year, fdate, cap, digest in updates:
        cur.execute("""UPDATE Multimedia SET identifier=?, originalFilename=?, fileYear=?,
                       folderDate=?, captureTimestamp=?, sha256=? WHERE multimediaID=?""",
                    (new_name, orig, year, fdate, cap, digest, mid))
    con.commit()
    regfile = main_dir / "file_registry.csv"
    existing = {r["new_name"]: r for r in csv.DictReader(open(regfile))} if regfile.exists() else {}
    for r in reg: existing[r["new_name"]] = r
    with open(regfile, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(reg[0].keys())); w.writeheader(); w.writerows(existing.values())
    con.close()

    log = ROOT / "Multimedia_pipeline" / "PIPELINE_LOG.md"
    with open(log, "a") as fh:
        fh.write(f"\n## {stamp} — 01_ingest_register --apply\n"
                 f"- source `{src_root}` years {years}; copied {copied} new files into `{main_dir.name}/` "
                 f"({len(reg)} unique, {dups} duplicate bytes)\n"
                 f"- Multimedia identifiers migrated to `{args.prefix}_<YYYY-MM-DD>_<sha8>.jpg`: {len(updates)}; "
                 f"new registered: {newfiles}; ambiguous: {len(ambig)}\n"
                 f"- DB backup `{bak.name}`; registry `{main_dir.name}/file_registry.csv`\n")
    print(f"\nAPPLIED: copied {copied}, updated {len(updates)} Multimedia rows. Backup {bak.name}. Logged.")

if __name__ == "__main__":
    main()
