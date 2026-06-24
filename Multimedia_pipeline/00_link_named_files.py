#!/usr/bin/env python3
"""
STEP 00 (optional) - Link photos whose filename already carries the occurrenceID.

Some images are named like "EO70 Occurrence 444.jpg" / "EO72_2 Occurrence 0764.jpg"
(occurrenceID in the filename) instead of the JCN whiteboard format. These need no
OCR: parse the number, take the EXIF date, validate the occurrenceID exists, and
insert a Multimedia row using the same conventions as the JCN pipeline.

Skips: anything already in Multimedia (idempotent), 'parking'/setup shots, and any
parsed occurrenceID not present in Occurrences (reported, not inserted).

Usage:
  python3 00_link_named_files.py            # dry run
  python3 00_link_named_files.py --apply    # backup + insert
"""
import argparse
import csv
import re
import shutil
import sqlite3
import sys
from datetime import datetime

from PIL import Image

import config as C

TAG_DATETIME_ORIGINAL, TAG_DATETIME = 36867, 306
# "...Occurrence 444.jpg" / "...Occurrence 0764.jpg"  (case-insensitive)
OCC_RE = re.compile(r"occurrence[ _]*0*(\d+)", re.IGNORECASE)


def exif_date(path):
    try:
        with Image.open(path) as im:
            ex = im.getexif()
            raw = ex.get(TAG_DATETIME_ORIGINAL) or ex.get(TAG_DATETIME)
        if raw:
            y, m, d = str(raw).split(" ")[0].split(":")
            return f"{m}-{d}-{y}"
    except Exception:
        pass
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--db", default=str(C.DB_PATH))
    args = ap.parse_args()

    con = sqlite3.connect(args.db, timeout=3.0)
    con.row_factory = sqlite3.Row
    have_remarks = any(r["name"] == C.REMARKS_COLUMN
                       for r in con.execute("PRAGMA table_info(Multimedia)"))
    existing = {r["identifier"] for r in con.execute(
        "SELECT identifier FROM Multimedia WHERE identifier IS NOT NULL")}
    occ_ids = {r[0] for r in con.execute("SELECT occurrenceID FROM Occurrences")}
    next_id = con.execute("SELECT COALESCE(MAX(multimediaID),0) FROM Multimedia").fetchone()[0] + 1

    plan, skipped = [], []
    for path in sorted(C.IMAGE_DIR.glob("*.jpg")):       # lowercase .jpg = the named set
        name = path.name
        if name in existing:
            continue                                      # already linked
        if "parking" in name.lower() or name.upper().startswith("BC-"):
            skipped.append((name, "setup/parking or pre-existing edited image"))
            continue
        m = OCC_RE.search(name)
        if not m:
            skipped.append((name, "no 'Occurrence NNN' in filename"))
            continue
        occ = int(m.group(1))
        if occ not in occ_ids:
            skipped.append((name, f"occurrenceID {occ} not in Occurrences"))
            continue
        plan.append((name, occ, exif_date(path)))

    print(f"DB: {args.db}\nTo INSERT: {len(plan)}  Skipped: {len(skipped)}  next multimediaID: {next_id}")
    for n, why in skipped:
        print(f"   skip  {n}: {why}")
    for name, occ, d in plan[:8]:
        print(f"   link  {name} -> occurrenceID {occ}  createDate {d}")
    if len(plan) > 8:
        print(f"   ... ({len(plan)} total)")

    if not args.apply:
        con.close()
        print("\nDRY RUN - nothing written. Re-run with --apply.")
        return

    backup = f"{args.db}.bak-{datetime.now():%Y%m%d-%H%M%S}-named"
    shutil.copy2(args.db, backup)
    print(f"Backup: {backup}")
    try:
        with con:
            if not have_remarks:
                con.execute(f"ALTER TABLE Multimedia ADD COLUMN {C.REMARKS_COLUMN} TEXT")
            mid = next_id
            for name, occ, d in plan:
                con.execute(
                    f"""INSERT INTO Multimedia
                        (multimediaID, identifier, type, format, createDate, title,
                         license, rightsHolder, multimediaStorage, tableID, occurrenceID, {C.REMARKS_COLUMN})
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (mid, name, C.MM_TYPE, C.MM_FORMAT, d, C.TITLE_OCCURRENCE,
                     C.MM_LICENSE, C.MM_RIGHTSHOLDER, C.MM_STORAGE, C.TABLEID_OCCURRENCE, occ,
                     "valid; occurrenceID parsed from filename"))
                mid += 1
        print(f"Inserted {len(plan)} rows (multimediaID {next_id}..{mid-1}).")
    except sqlite3.OperationalError as e:
        con.close()
        sys.exit(f"ABORTED ({e}). DB likely open/locked - close it and retry. Backup: {backup}")
    con.close()


if __name__ == "__main__":
    main()
