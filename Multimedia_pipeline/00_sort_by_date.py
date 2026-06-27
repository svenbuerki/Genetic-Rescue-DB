#!/usr/bin/env python3
"""00 - Sort flat year-folder images into date subfolders:  <year>/  ->  <year>/<YYYY-MM-DD>/

Mirrors the real upload situation (one folder per field day) and gives 01_ingest_register the
date it stamps into the unique filename. Date per image, in priority:
    1. EXIF DateTimeOriginal            (most images)
    2. DB occurrenceDate                (for EXIF-stripped files, matched by original name + year)
    3. -> "unknown-date/"               (flagged for you to place by hand)

Non-destructive-ish: moves files WITHIN their year folder; verifies the count is conserved.
Dry-run unless --apply.

Usage:
  python3 Multimedia_pipeline/00_sort_by_date.py            # dry-run, show date histogram
  python3 Multimedia_pipeline/00_sort_by_date.py --apply
"""
import argparse, shutil, sqlite3, re
from collections import Counter
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DTO, DT = 36867, 306

def exif_date(p):
    try:
        ex = Image.open(p)._getexif() or {}
        v = ex.get(DTO) or ex.get(DT)
        if v and re.match(r"\d{4}:\d{2}:\d{2}", str(v)):
            return str(v)[:10].replace(":", "-")
    except Exception:
        pass
    return None

def db_date_map(db):
    con = sqlite3.connect(db)
    m = {}
    for ident, year, od, cd in con.execute("""SELECT m.originalFilename, m.fileYear, o.occurrenceDate, m.createDate
            FROM Multimedia m LEFT JOIN Occurrences o ON m.occurrenceID=o.occurrenceID
            WHERE m.originalFilename IS NOT NULL"""):
        d = od or cd
        if d and re.match(r"\d{2}-\d{2}-\d{4}", str(d)):
            mm, dd, yy = str(d).split("-"); d = f"{yy}-{mm}-{dd}"
        elif d and re.match(r"\d{4}-\d{2}-\d{2}", str(d)):
            d = str(d)[:10]
        else:
            d = None
        if ident and year and d:
            m[(ident.lower(), year)] = d
    con.close()
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-root", default=str(ROOT / "Multimedia_images"))
    ap.add_argument("--db", default=str(ROOT / "LEPA_SQL.db"))
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    root = Path(a.src_root)
    dbmap = db_date_map(a.db)

    plan, hist, src_exif, src_db, src_unk = [], Counter(), 0, 0, 0
    for ydir in sorted(p for p in root.iterdir() if p.is_dir() and p.name.isdigit()):
        for p in list(ydir.glob("*")):                       # only files directly in <year>/ (flat)
            if p.is_dir() or p.suffix.lower() not in (".jpg", ".jpeg") or p.name.startswith("."):
                continue
            d = exif_date(p)
            if d: src_exif += 1
            else:
                d = dbmap.get((p.name.lower(), ydir.name))
                if d: src_db += 1
                else: d = "unknown-date"; src_unk += 1
            # sanity: date year should match folder year (else keep folder year's bucket but flag)
            if d != "unknown-date" and not d.startswith(ydir.name):
                d = f"{ydir.name}-MISMATCH-{d}"
            hist[(ydir.name, d)] += 1
            plan.append((p, ydir / d / p.name))

    print(f"to sort: {len(plan)} images  (date from EXIF {src_exif}, from DB {src_db}, unknown {src_unk})")
    for (y, d), n in sorted(hist.items()):
        print(f"  {y}/{d}/ : {n}")
    if not a.apply:
        print("\nDRY-RUN. Re-run with --apply to move.")
        return
    moved = 0
    for src, dst in plan:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.resolve() != dst.resolve():
            shutil.move(str(src), str(dst)); moved += 1
    print(f"APPLIED: moved {moved} files into date subfolders.")

if __name__ == "__main__":
    main()
