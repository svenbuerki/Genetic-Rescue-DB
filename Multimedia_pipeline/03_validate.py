#!/usr/bin/env python3
"""
STEP 03 - Validate board reads against the database, classify every image.

Joins work/01_metadata.csv (EXIF date) + work/02_boards.csv (board reads) against
the live Occurrences / Events tables, and writes work/03_validated.csv with a
resolved target (occurrenceID / locationID / eventID), the Multimedia field values,
and a status the load step keys off.

Status values:
  ok                 - board_id matches an existing occurrenceID  -> INSERT as Occurrence image (tableID 13)
  date_mismatch_ok   - same, but board_date != occurrenceDate (still inserted; difference reported)
  missing_occurrence - board_id has NO matching occurrenceID       -> NOT inserted, needs review
  needs_location     - no whiteboard                               -> Location image, locationID must be set
  needs_event        - 'Event NN' marker board                     -> Event image, eventID must be set
  no_target          - could not classify                          -> review

Inference helpers (best-effort, never silently guessed into the DB):
  * needs_location / needs_event rows get a SUGGESTED id from the EXIF date when it is
    unambiguous (date maps to exactly one location/event), left blank otherwise.

Usage:  python3 03_validate.py
"""
import csv
import sqlite3
from collections import defaultdict

import config as C


def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def main():
    meta = {r["filename"]: r for r in load_csv(C.METADATA_CSV)}
    boards = load_csv(C.BOARDS_CSV)

    con = sqlite3.connect(C.DB_PATH)
    con.row_factory = sqlite3.Row

    # occurrenceID -> occurrenceDate
    occ_date = {r["occurrenceID"]: r["occurrenceDate"]
                for r in con.execute("SELECT occurrenceID, occurrenceDate FROM Occurrences")}
    # date -> set(locationID) and date -> set(eventID), for unambiguous inference
    loc_by_date = defaultdict(set)
    for r in con.execute("SELECT DISTINCT occurrenceDate, locationID FROM Occurrences WHERE locationID IS NOT NULL"):
        loc_by_date[r["occurrenceDate"]].add(r["locationID"])
    evt_by_date = defaultdict(set)
    for r in con.execute("SELECT eventID, eventDate FROM Events"):
        evt_by_date[r["eventDate"]].add(r["eventID"])
    con.close()

    out = []
    for b in boards:
        fn = b["filename"]
        exif = meta.get(fn, {}).get("exif_date", "")
        has = b["has_board"]
        row = {
            "filename": fn, "createDate": exif,
            "board_id": b["board_id"], "board_date": b["board_date"],
            "occurrenceID": "", "locationID": "", "eventID": "",
            "tableID": "", "title": "", "db_date": "", "date_match": "",
            "status": "", "remarks": "", "notes": b.get("notes", ""),
        }

        if has == "yes":
            oid = int(b["board_id"])
            if oid in occ_date:
                db_date = occ_date[oid]
                row.update(occurrenceID=oid, tableID=C.TABLEID_OCCURRENCE,
                           title=C.TITLE_OCCURRENCE, db_date=db_date)
                same = (b["board_date"] == db_date)
                row["date_match"] = "yes" if same else "no"
                if same:
                    row["status"] = "ok"
                    row["remarks"] = "valid"
                else:
                    row["status"] = "date_mismatch_ok"
                    row["remarks"] = (f"valid - occurrenceID {oid} confirmed; board/photo date "
                                      f"{b['board_date']} differs from occurrenceDate {db_date} "
                                      f"(observed {db_date}, photographed {b['board_date']})")
            else:
                row["status"] = "missing_occurrence"
                row["remarks"] = (f"REVIEW - board number {b['board_id']} has no matching "
                                  f"occurrenceID in Occurrences; not linked")
        elif has == "no":
            row.update(tableID=C.TABLEID_LOCATION, title=C.TITLE_LOCATION, status="needs_location")
            cand = loc_by_date.get(exif, set())
            if len(cand) == 1:
                row["locationID"] = next(iter(cand))
                row["remarks"] = (f"REVIEW - no whiteboard; Location image; suggested "
                                  f"locationID={row['locationID']} (sole location on {exif})")
            else:
                row["remarks"] = (f"REVIEW - no whiteboard; Location image; locationID "
                                  f"ambiguous on {exif}: {sorted(cand)} - confirm")
        elif has == "event":
            row.update(tableID=C.TABLEID_LOCATION, title=C.TITLE_LOCATION, status="needs_event")
            cand = evt_by_date.get(b["board_date"], set())
            row["remarks"] = (f"REVIEW - board labeled 'Event'; Event image; events on "
                              f"{b['board_date']}: {sorted(cand)} - confirm eventID")
        else:
            row["status"] = "no_target"
            row["remarks"] = "REVIEW - could not classify"

        # Apply any human-confirmed target (overrides the inferred classification)
        override = C.MANUAL_TARGETS.get(fn)
        if override:
            if "eventID" in override:
                row.update(eventID=override["eventID"], tableID=C.TABLEID_EVENT,
                           title=C.TITLE_LOCATION)
                row["remarks"] = f"valid - confirmed Event image; eventID={override['eventID']}"
            elif "locationID" in override:
                row.update(locationID=override["locationID"], tableID=C.TABLEID_LOCATION,
                           title=C.TITLE_LOCATION)
                row["remarks"] = f"valid - confirmed Location image; locationID={override['locationID']}"
        out.append(row)

    cols = ["filename", "createDate", "board_id", "occurrenceID", "locationID", "eventID",
            "tableID", "title", "board_date", "db_date", "date_match", "status", "remarks", "notes"]
    with open(C.VALIDATED_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    # summary
    counts = defaultdict(int)
    for r in out:
        counts[r["status"]] += 1
    print(f"Wrote {C.VALIDATED_CSV} ({len(out)} rows)")
    for k in sorted(counts):
        print(f"  {k:18s} {counts[k]}")


if __name__ == "__main__":
    main()
