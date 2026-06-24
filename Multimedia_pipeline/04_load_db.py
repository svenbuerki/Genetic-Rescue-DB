#!/usr/bin/env python3
"""
STEP 04 - Load validated rows into the database.

Three actions, all gated behind --apply (default is a DRY RUN that changes nothing):
  1. BACKUP   the DB to LEPA_SQL.db.bak-YYYYMMDD-HHMMSS before any write.
  2. FIX      existing Multimedia rows: tableID 9 -> 13 (occurrence images mislabelled
              as Locations). Controlled by FIX_EXISTING_TABLEID_* in config.
  3. INSERT   one Multimedia row per validated image:
                - status ok / date_mismatch_ok  -> Occurrence image (occurrenceID, tableID 13)
                - needs_location / needs_event   -> only if a locationID/eventID is present
                  in the CSV (use --include-special); otherwise skipped and reported.

Idempotent: an image whose `identifier` already exists in Multimedia is skipped.
multimediaID continues from the current MAX.

Usage:
  python3 04_load_db.py                 # dry run: print the plan
  python3 04_load_db.py --apply         # backup + write occurrence rows + fix tableIDs
  python3 04_load_db.py --apply --include-special   # also write location/event rows that have an id

IMPORTANT: close any SQLite GUI holding the DB first; the script aborts on a write lock.
"""
import argparse
import csv
import shutil
import sqlite3
import sys
from datetime import datetime

import config as C

INSERT_OK = {"ok", "date_mismatch_ok"}
SPECIAL = {"needs_location", "needs_event"}


def load_validated():
    with open(C.VALIDATED_CSV) as f:
        return list(csv.DictReader(f))


def col_or_none(v):
    return int(v) if str(v).strip() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually write (default: dry run)")
    ap.add_argument("--include-special", action="store_true",
                    help="also insert needs_location/needs_event rows that have an id")
    ap.add_argument("--db", default=str(C.DB_PATH))
    args = ap.parse_args()

    rows = load_validated()
    con = sqlite3.connect(args.db, timeout=2.0)
    con.row_factory = sqlite3.Row

    has_remarks = any(r["name"] == C.REMARKS_COLUMN
                      for r in con.execute("PRAGMA table_info(Multimedia)"))
    existing_ids = {r["identifier"] for r in con.execute(
        "SELECT identifier FROM Multimedia WHERE identifier IS NOT NULL")}
    next_id = (con.execute("SELECT COALESCE(MAX(multimediaID),0) FROM Multimedia").fetchone()[0]) + 1
    n_fix = con.execute(
        "SELECT COUNT(*) FROM Multimedia WHERE tableID=?",
        (C.FIX_EXISTING_TABLEID_FROM,)).fetchone()[0]

    plan, skipped = [], []
    for r in rows:
        if r["filename"] in existing_ids:
            skipped.append((r["filename"], "already in Multimedia"))
            continue
        st = r["status"]
        if st in INSERT_OK:
            target = ("occurrenceID", col_or_none(r["occurrenceID"]))
        elif st in SPECIAL and args.include_special and (r["locationID"] or r["eventID"]):
            target = ("locationID", col_or_none(r["locationID"])) if r["locationID"] \
                else ("eventID", col_or_none(r["eventID"]))
        else:
            skipped.append((r["filename"], f"status={st} (not loaded)"))
            continue
        plan.append((r, target))

    print(f"DB: {args.db}")
    print(f"'{C.REMARKS_COLUMN}' column exists: {has_remarks}"
          + ("" if has_remarks else "  (will ADD COLUMN on --apply)"))
    print(f"Existing Multimedia rows: {len(existing_ids)} | tableID {C.FIX_EXISTING_TABLEID_FROM}->"
          f"{C.FIX_EXISTING_TABLEID_TO}: {n_fix} rows")
    print(f"To INSERT: {len(plan)}  |  Skipped: {len(skipped)}  |  next multimediaID: {next_id}")
    for fn, why in skipped:
        print(f"   skip  {fn}: {why}")

    if not args.apply:
        print("\nDRY RUN - nothing written. Re-run with --apply to commit.")
        for r, (col, val) in plan[:5]:
            print(f"   would insert {r['filename']} -> {col}={val}, tableID={r['tableID']}, "
                  f"createDate={r['createDate']}")
        print(f"   ... ({len(plan)} total)")
        con.close()
        return

    # --- APPLY ---
    backup = f"{args.db}.bak-{datetime.now():%Y%m%d-%H%M%S}"
    shutil.copy2(args.db, backup)
    print(f"Backup written: {backup}")

    try:
        with con:
            if not has_remarks:
                con.execute(f"ALTER TABLE Multimedia ADD COLUMN {C.REMARKS_COLUMN} TEXT")
            # Fix mislabelled tableIDs and stamp the corrected rows' remarks
            con.execute(
                f"UPDATE Multimedia SET tableID=?, {C.REMARKS_COLUMN}=? WHERE tableID=?",
                (C.FIX_EXISTING_TABLEID_TO, C.REMARKS_FIX_TABLEID, C.FIX_EXISTING_TABLEID_FROM))
            mid = next_id
            for r, (col, val) in plan:
                con.execute(
                    f"""INSERT INTO Multimedia
                        (multimediaID, identifier, type, format, createDate, title,
                         license, rightsHolder, multimediaStorage, tableID, {col}, {C.REMARKS_COLUMN})
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (mid, r["filename"], C.MM_TYPE, C.MM_FORMAT, r["createDate"], r["title"],
                     C.MM_LICENSE, C.MM_RIGHTSHOLDER, C.MM_STORAGE, int(r["tableID"]), val,
                     r["remarks"]))
                mid += 1
        print(f"Applied: fixed {n_fix} tableIDs, inserted {len(plan)} rows "
              f"(multimediaID {next_id}..{mid-1}); remarks populated.")
    except sqlite3.OperationalError as e:
        con.close()
        sys.exit(f"\nABORTED ({e}). The DB is likely open/locked in another app - "
                 f"close it and retry. No partial write (transaction rolled back); "
                 f"backup at {backup}.")
    con.close()


if __name__ == "__main__":
    main()
