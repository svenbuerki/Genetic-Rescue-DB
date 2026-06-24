"""
06_phenotyping_schema.py — introduce a dedicated `Phenotyping` table.

Image-based plant morphometrics are an *observation derived from a specific
image by a specific method*, not an intrinsic column of the `Occurrences`
entity. This step moves them into their own table so each measurement carries
full provenance (source `multimediaID`, method, confidence) and so an
occurrence can be measured more than once (multiple images, future campaigns,
extra traits) without a schema change. It mirrors the Darwin Core
MeasurementOrFact pattern and the BrAPI "observations are separate from the
entity" convention the rest of the DB already follows.

In one transaction (backup first; dry-run by default, `--apply` to write):

  1. CREATE TABLE Phenotyping (wide format, with unit companions).
  2. Migrate the measured sample from work/05_measurements.csv (+ the
     occurrenceSizeClass already on Occurrences), resolving each row's
     multimediaID via Multimedia.identifier (the source image).
  3. Register Phenotyping in TableModules (tableID 23) and re-home / add the
     Terms-dictionary entries (the DwC height/crown definitions move with it).
  4. DROP the now-duplicated columns from Occurrences.
  5. (optional, --with-view) CREATE VIEW vOccurrenceTraits joining Occurrences
     + Phenotyping + summed Germplasm seed quantity for analysis.

Run:
  python3 06_phenotyping_schema.py            # dry run — prints the plan
  python3 06_phenotyping_schema.py --apply    # writes (backs up the DB first)
  python3 06_phenotyping_schema.py --apply --with-view
"""
import argparse
import csv
import shutil
import sqlite3
import sys
from datetime import datetime

import config

# --- new-table conventions -------------------------------------------------
PHENO_TABLE          = "Phenotyping"
PHENO_TABLEMODULE_ID = 23                 # next free TableModules.tableID
PHENO_MODULE         = "Demography"       # trait/condition data (adjust to taste)
PHENO_MODULE_DESC    = (
    "Stores image-based morphometric observations of individual occurrences "
    "(see `Occurrences`): plant height and crown width estimated against the "
    "field whiteboard rulers, plus a robust size class. Each row links to the "
    "source image (see `Multimedia`) and records the measurement method and "
    "confidence. Derived by the Multimedia_pipeline."
)
DETERMINED_BY   = "Claude vision (in-session)"
DETERMINED_DATE = ""        # campaign date if known (MM-DD-YYYY); blank = unknown

# Columns made redundant on Occurrences once Phenotyping exists.
OCC_DROP_COLUMNS = [
    "occurrenceHeight", "occurrenceHeightUnit",
    "occurrenceCrownSize", "occurrenceCrownSizeUnit",
    "occurrenceSizeClass",
]

CREATE_PHENO_SQL = f"""
CREATE TABLE {PHENO_TABLE} (
  phenotypingID             INTEGER PRIMARY KEY AUTOINCREMENT,
  occurrenceID              INTEGER NOT NULL REFERENCES Occurrences(occurrenceID),
  multimediaID              INTEGER REFERENCES Multimedia(multimediaID),
  occurrenceHeight          NUMERIC,
  occurrenceHeightUnit      TEXT,
  occurrenceCrownSize       NUMERIC,
  occurrenceCrownSizeUnit   TEXT,
  occurrenceSizeClass       TEXT,
  measurementMethod         TEXT,
  measurementConfidence     TEXT,
  measurementDeterminedBy   TEXT,
  measurementDeterminedDate TEXT,
  remarks                   TEXT
)
"""

# Terms-dictionary rows for the NEW columns (the 4 height/crown terms are
# re-homed from Occurrences rather than recreated). dwc URLs where they exist.
DWC = "http://rs.tdwg.org/dwc/terms/"
NEW_TERMS = [
    # term, termOriginal, dataType, standard, URL, definitionDB
    ("phenotypingID", "", "Integer", "", "",
     "Primary key: one row per image-based measurement of an occurrence."),
    ("occurrenceID", "occurrenceID", "Integer", "Darwin Core", DWC + "occurrenceID",
     "Foreign key to the measured occurrence (see `Occurrences`)."),
    ("multimediaID", "", "Integer", "", "",
     "Foreign key to the source image the measurement was read from (see `Multimedia`)."),
    ("occurrenceSizeClass", "measurementValue", "Text", "Darwin Core", DWC + "measurementValue",
     "Coarse plant size class (small/medium/large) derived from crown width and the "
     "exceeds-ruler flag. The robust phenotyping output, reliable even when exact cm is uncertain."),
    ("measurementMethod", "measurementMethod", "Text", "Darwin Core", DWC + "measurementMethod",
     "How the measurement was estimated: 'ruler' (plant within the in-frame ruler span) or "
     "'1cm-tile' (one graduation used as cm/pixel and extrapolated for plants exceeding the ruler)."),
    ("measurementConfidence", "", "Text", "", "",
     "Qualitative confidence in the measurement: high / medium / low."),
    ("measurementDeterminedBy", "measurementDeterminedBy", "Text", "Darwin Core", DWC + "measurementDeterminedBy",
     "Agent that determined the measurement (e.g., Claude vision, in-session)."),
    ("measurementDeterminedDate", "measurementDeterminedDate", "Text", "Darwin Core", DWC + "measurementDeterminedDate",
     "Date the measurement was determined from the image."),
    ("remarks", "", "Text", "", "",
     "Free-text notes on the measurement (plant visibility, occlusion, exceeds-ruler, etc.)."),
]

VIEW_SQL = f"""
CREATE VIEW vOccurrenceTraits AS
SELECT  o.occurrenceID,
        o.taxonID,
        o.eventID,
        o.locationID,
        o.occurrenceDate,
        p.occurrenceHeight,
        p.occurrenceHeightUnit,
        p.occurrenceCrownSize,
        p.occurrenceCrownSizeUnit,
        p.occurrenceSizeClass,
        p.measurementMethod,
        p.measurementConfidence,
        g.seedQuantityTotal,
        g.nAccessions
FROM Occurrences o
LEFT JOIN {PHENO_TABLE} p ON p.occurrenceID = o.occurrenceID
LEFT JOIN (
    SELECT occurrenceID,
           SUM(germplasmQuantityEstimate) AS seedQuantityTotal,
           COUNT(*)                        AS nAccessions
    FROM Germplasm
    WHERE occurrenceID IS NOT NULL
    GROUP BY occurrenceID
) g ON g.occurrenceID = o.occurrenceID
"""


def _truthy(s):
    return str(s).strip().lower() in ("true", "1", "yes", "y")


def load_measurements():
    """Read 05_measurements.csv into Phenotyping-shaped dict rows."""
    rows = []
    with open(config.MEASUREMENTS_CSV, newline="") as fh:
        for r in csv.DictReader(fh):
            exceeds = _truthy(r.get("exceeds_ruler"))
            notes = (r.get("notes") or "").strip()
            bits = []
            if not _truthy(r.get("plant_visible")):
                bits.append("plant not clearly visible")
            if exceeds:
                bits.append("exceeds ruler (1cm-tile extrapolation)")
            if notes:
                bits.append(notes)
            rows.append({
                "filename": r["filename"].strip(),
                "occurrenceID": int(r["occurrenceID"]),
                "occurrenceHeight": r.get("height_cm") or None,
                "occurrenceHeightUnit": "cm" if r.get("height_cm") else None,
                "occurrenceCrownSize": r.get("crown_cm") or None,
                "occurrenceCrownSizeUnit": "cm" if r.get("crown_cm") else None,
                "occurrenceSizeClass": (r.get("sizeClass") or "").strip() or None,
                "measurementMethod": "1cm-tile" if exceeds else "ruler",
                "measurementConfidence": (r.get("confidence") or "").strip() or None,
                "remarks": "; ".join(bits) or None,
            })
    return rows


def resolve_multimedia_id(conn, filename):
    cur = conn.execute(
        "SELECT multimediaID FROM Multimedia WHERE identifier = ?", (filename,)
    )
    hit = cur.fetchone()
    return hit[0] if hit else None


def backup_db():
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = config.DB_PATH.with_suffix(config.DB_PATH.suffix + f".bak-{stamp}")
    shutil.copy2(config.DB_PATH, dst)
    return dst


def main():
    ap = argparse.ArgumentParser(description="Create the Phenotyping table and migrate measurements.")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    ap.add_argument("--with-view", action="store_true", help="also create vOccurrenceTraits")
    args = ap.parse_args()

    conn = sqlite3.connect(config.DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    # Guard: table must not already exist.
    exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (PHENO_TABLE,)
    ).fetchone()
    if exists:
        print(f"!! {PHENO_TABLE} already exists — nothing to do. Aborting.")
        sys.exit(1)

    measurements = load_measurements()
    resolved = [(m, resolve_multimedia_id(conn, m["filename"])) for m in measurements]
    n_linked = sum(1 for _, mid in resolved if mid is not None)
    next_term_tableid = (conn.execute("SELECT COALESCE(MAX(tableID),0)+1 FROM Terms").fetchone()[0])
    next_term_id = (conn.execute("SELECT COALESCE(MAX(termID),0) FROM Terms").fetchone()[0])

    print("PLAN")
    print(f"  CREATE TABLE {PHENO_TABLE} (wide, 13 columns)")
    print(f"  INSERT {len(measurements)} measured plants  ({n_linked} linked to a multimediaID)")
    if n_linked < len(measurements):
        print(f"    !! {len(measurements) - n_linked} rows could not resolve a multimediaID (will store NULL)")
    print(f"  TableModules += (tableID {PHENO_TABLEMODULE_ID}, {PHENO_TABLE}, {PHENO_MODULE})")
    print(f"  Terms: re-home 4 height/crown terms -> {PHENO_TABLE} (Terms.tableID {next_term_tableid}); "
          f"add {len(NEW_TERMS)} new term rows")
    print(f"  Occurrences: DROP COLUMN {', '.join(OCC_DROP_COLUMNS)}")
    if args.with_view:
        print("  CREATE VIEW vOccurrenceTraits (Occurrences + Phenotyping + Germplasm quantity)")

    if not args.apply:
        print("\n(dry run — no changes written; re-run with --apply)")
        conn.close()
        return

    bak = backup_db()
    print(f"\nbackup -> {bak.name}")
    try:
        conn.execute("BEGIN IMMEDIATE")

        # 1. create
        conn.execute(CREATE_PHENO_SQL)

        # 2. migrate
        for m, mid in resolved:
            conn.execute(
                f"INSERT INTO {PHENO_TABLE} "
                "(occurrenceID, multimediaID, occurrenceHeight, occurrenceHeightUnit, "
                " occurrenceCrownSize, occurrenceCrownSizeUnit, occurrenceSizeClass, "
                " measurementMethod, measurementConfidence, measurementDeterminedBy, "
                " measurementDeterminedDate, remarks) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (m["occurrenceID"], mid, m["occurrenceHeight"], m["occurrenceHeightUnit"],
                 m["occurrenceCrownSize"], m["occurrenceCrownSizeUnit"], m["occurrenceSizeClass"],
                 m["measurementMethod"], m["measurementConfidence"], DETERMINED_BY,
                 DETERMINED_DATE or None, m["remarks"]),
            )

        # 3a. TableModules
        conn.execute(
            "INSERT INTO TableModules (tableID, tableName, tableModule, definition) VALUES (?,?,?,?)",
            (PHENO_TABLEMODULE_ID, PHENO_TABLE, PHENO_MODULE, PHENO_MODULE_DESC),
        )

        # 3b. Terms — re-home the 4 DwC height/crown definitions ...
        conn.execute(
            "UPDATE Terms SET tableID=?, tableName=? "
            "WHERE term IN ('occurrenceHeight','occurrenceHeightUnit',"
            "'occurrenceCrownSize','occurrenceCrownSizeUnit')",
            (next_term_tableid, PHENO_TABLE),
        )
        # ... and add the new ones.
        tid = next_term_id
        for term, term_orig, dtype, std, url, defdb in NEW_TERMS:
            tid += 1
            conn.execute(
                "INSERT INTO Terms (termID, tableID, tableName, term, termOriginal, "
                "definitionOriginal, dataType, standard, URL, definitionDB) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (tid, next_term_tableid, PHENO_TABLE, term, term_orig, "", dtype, std, url, defdb),
            )

        # 4. drop redundant Occurrences columns
        for col in OCC_DROP_COLUMNS:
            conn.execute(f"ALTER TABLE Occurrences DROP COLUMN {col}")

        # 5. optional analysis view
        if args.with_view:
            conn.execute("DROP VIEW IF EXISTS vOccurrenceTraits")
            conn.execute(VIEW_SQL)

        conn.commit()
    except sqlite3.OperationalError as e:
        conn.rollback()
        msg = str(e)
        if "locked" in msg.lower():
            print("!! DB is locked (close it in any SQLite GUI and retry). Rolled back; backup kept.")
        else:
            print(f"!! OperationalError: {msg}. Rolled back; backup kept.")
        sys.exit(1)
    except Exception as e:
        conn.rollback()
        print(f"!! {type(e).__name__}: {e}. Rolled back; backup kept.")
        sys.exit(1)
    finally:
        conn.close()

    print(f"OK — {PHENO_TABLE} created, {len(measurements)} rows migrated, "
          f"{len(OCC_DROP_COLUMNS)} columns dropped from Occurrences.")


if __name__ == "__main__":
    main()
