#!/usr/bin/env python3
"""Stage B load — link matched 2026 plant images to their occurrences + insert Phenotyping.

Reads the Stage B staging (board# already matched to an existing occurrenceID) and:
  1. inserts one Multimedia occurrence-image row per matched image (tableID 13, occurrenceID),
     pulling provenance (originalFilename / sha256 / captureTimestamp / folderDate) from the
     ingest file_registry;
  2. inserts one Phenotyping row per occurrence (linked to its image), with the image-measured
     height/crown/size + the field-written board h/w noted in remarks.

Idempotent (skips occurrences already imaged / phenotyped); dry-run by default; backs up the DB.
Usage:  python3 Multimedia_pipeline/stageB_load.py [--apply]
"""
import argparse, csv, shutil, sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGE = ROOT / "Multimedia_pipeline" / "staging_2026"
REG = ROOT / "Multimedia_main" / "file_registry.csv"
DB = ROOT / "LEPA_SQL.db"
DETERMINED_BY = "Claude vision (in-session)"

def iso_to_dbdate(s):   # 2026-06-22 -> 06-22-2026
    s = str(s or "")
    return f"{s[5:7]}-{s[8:10]}-{s[0:4]}" if len(s) >= 10 and s[4] == "-" else None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    reg = {r["new_name"]: r for r in csv.DictReader(open(REG))}
    mm = list(csv.DictReader(open(STAGE / "stageB_multimedia_staging.csv")))
    ph = {r["occurrenceID"]: r for r in csv.DictReader(open(STAGE / "stageB_phenotyping_staging.csv"))}  # 1/occ (last wins)
    con = sqlite3.connect(DB); cur = con.cursor()
    imaged = {r[0] for r in cur.execute("SELECT occurrenceID FROM Multimedia WHERE occurrenceID IS NOT NULL AND tableID=13")}
    phenod = {r[0] for r in cur.execute("SELECT occurrenceID FROM Phenotyping")}
    maxmm = cur.execute("SELECT MAX(multimediaID) FROM Multimedia").fetchone()[0] or 0

    new_mm = [m for m in mm if int(m["occurrenceID"]) not in imaged]
    occ_seen, new_ph = set(), []
    for m in new_mm:
        occ = m["occurrenceID"]
        if occ in ph and int(occ) not in phenod and occ not in occ_seen:
            occ_seen.add(occ); new_ph.append(occ)
    print(f"Stage B load — to INSERT: {len(new_mm)} Multimedia occurrence-images, {len(new_ph)} Phenotyping rows")
    print(f"  skipped (already imaged): {len(mm)-len(new_mm)}; occurrences covered: {len({m['occurrenceID'] for m in new_mm})}")
    if not a.apply:
        print("DRY-RUN. Re-run with --apply to write (DB backed up first)."); con.close(); return

    _bk = DB.parent / "db_backups"; _bk.mkdir(exist_ok=True); bak = _bk / (DB.name + ".bak-stageB-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")); shutil.copy2(DB, bak)
    occ_to_mmid = {}
    for m in new_mm:
        occ = int(m["occurrenceID"]); ident = m["identifier"]; rr = reg.get(ident, {})
        maxmm += 1
        cur.execute("""INSERT INTO Multimedia (multimediaID,identifier,type,format,createDate,title,multimediaStorage,
                       tableID,occurrenceID,remarks,originalFilename,fileYear,folderDate,captureTimestamp,sha256)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (maxmm, ident, "field image", "jpeg", iso_to_dbdate(rr.get("folderDate")), m["title"], "Google Drive",
                     13, occ, "valid; 2026 plant image linked by board#=occurrenceID (Stage B)",
                     rr.get("original_name"), rr.get("year"), rr.get("folderDate"), rr.get("capture") or None, rr.get("sha256")))
        occ_to_mmid.setdefault(occ, maxmm)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for occ in new_ph:
        p = ph[occ]; o = int(occ)
        rmk = (f"field board h={p['board_h_cm']} w={p['board_w_cm']}" if p.get("board_has_hw") == "True" else None)
        cur.execute("""INSERT INTO Phenotyping (occurrenceID,multimediaID,occurrenceHeight,occurrenceHeightUnit,
                       occurrenceCrownSize,occurrenceCrownSizeUnit,occurrenceSizeClass,measurementMethod,
                       measurementConfidence,measurementDeterminedBy,measurementDeterminedDate,remarks)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (o, occ_to_mmid.get(o), p.get("occurrenceHeight") or None, "cm", p.get("occurrenceCrownSize") or None, "cm",
                     p.get("occurrenceSizeClass") or None, p.get("measurementMethod") or None,
                     p.get("measurementConfidence") or None, DETERMINED_BY, now, rmk))
    con.commit(); con.close()
    with open(ROOT / "Multimedia_pipeline" / "PIPELINE_LOG.md", "a") as fh:
        fh.write(f"\n## {datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')} — stageB_load --apply\n"
                 f"- linked {len(new_mm)} 2026 plant images to occurrences (Multimedia tableID 13) + {len(new_ph)} Phenotyping rows. Backup `{bak.name}`.\n")
    print(f"APPLIED: +{len(new_mm)} Multimedia, +{len(new_ph)} Phenotyping. Backup {bak.name}. Logged.")

if __name__ == "__main__":
    main()
