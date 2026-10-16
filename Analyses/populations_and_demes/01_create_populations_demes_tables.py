"""01_create_populations_demes_tables.py

Add the spatial-genetic framework from the LEPA mate-limitation pipeline
(https://github.com/svenbuerki/LEPA_mate_limitation) to the LEPA SQLite
database: Bottleneck Lineages (BLs), Populations, Demes — plus three new
columns on the existing Events table (populationID, demeID, eventYear)
that make the full chain `Germplasm → Occurrences → Events → Populations
→ BottleneckLineages` queryable in one join path.

Two targets
-----------
Production DB — `/SQL_DB/LEPA_SQL.db` on the local machine (default):
  loads schema + mate-limitation TSV data. NEVER committed; contains
  ESA-sensitive GPS data.

Schema-shell DB — `Genetic_Rescue_DB/Genetic_Rescue_SQL.db` (the shared
copy on GitHub): run with `--schema-only` to add tables + columns +
TableModules rows + Terms rows WITHOUT loading data.

Pipeline
--------
1.  Back the target DB up to a timestamped sibling file.
2.  Pre-flight migration (idempotent, safe to re-run):
      - DROP any legacy junction tables (PopulationEvents,
        PopulationLocations, DemeLocations) from an earlier design.
      - If Populations has the old columns nSlickspots / nSlickspotsBothYears,
        rename them to nEvents / nEventsBothYears.
      - If Events is missing populationID / demeID / eventYear, add them.
3.  Create (or keep) the three new tables + indexes:
      BottleneckLineages, Populations, Demes.
4.  Unless --schema-only, load data:
      - BottleneckLineages   ← SRK_bioinformatics/tables/EO_BL_summary.csv
      - Populations          ← LEPA_mate_limitation/tables/
                                    step29a_population_summary.tsv
                                 + step30g_populations_classified.tsv
                                 + step30g_prediction_population_year.tsv
      - Demes                ← inline 50 m single-linkage clustering on
                                 Events.eventDecimalLatitude/Longitude
                                 within each (populationID, eventYear) group.
      - Events UPDATE        ← populationID + demeID + eventYear from the
                                 crosswalk + inline clustering, keyed on
                                 eventID.
5.  Clean up Terms / TableModules rows for the removed tables and
    renamed columns, then insert controlled-vocabulary rows for every
    column of every new table + the three new columns on Events.

Hierarchy produced
------------------
  BottleneckLineages
     └── Populations                      (Populations.BLID → BottleneckLineages)
          └── Demes                       (within-year 50 m clusters)
  Events (existing, +3 new columns)       (Events.populationID → Populations;
                                           Events.demeID + eventYear join to Demes
                                           on (populationID, demeID, year))

Deme assignment note: the mate-limitation pipeline exports only the
per-deme summary (step29a_demes_per_population_year.tsv), not the
per-event deme membership. This script re-derives it inline, using 50 m
haversine single-linkage within each (populationID, eventYear) group on
the full-precision Events.eventDecimalLatitude/Longitude from the DB.
In one borderline case (population 39, year 2025) the exported TSV
splits a single 50 m component into two sub-components via a secondary
criterion that this DB does not use (eventID is the project-standard
identifier for a slickspot). The inline single-linkage result is
authoritative.

Running
-------
Local, loads data into the production DB:
    python 01_create_populations_demes_tables.py --apply

Schema-shell (no data), for GitHub share:
    python 01_create_populations_demes_tables.py \
        --db ../../Genetic_Rescue_SQL.db --schema-only --apply

Author: Sven Buerki, Buerki Lab, Boise State University.
"""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
import sqlite3
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
CURRENT_PROJECTS = REPO_ROOT.parent.parent

DEFAULT_DB = CURRENT_PROJECTS / "LEPA_fieldwork_protocol" / "SQL_DB" / "LEPA_SQL.db"
DEFAULT_TABLES_DIR = CURRENT_PROJECTS / "LEPA_mate_limitation" / "tables"
DEFAULT_BL_SUMMARY = (
    CURRENT_PROJECTS
    / "SRK_bioinformatics"
    / "SRK_bioinformatics_GitHub"
    / "tables"
    / "EO_BL_summary.csv"
)

BL_PALETTE = {
    "BL1": "#984EA3",
    "BL2": "#377EB8",
    "BL3": "#4DAF4A",
    "BL4": "#E41A1C",
    "BL5": "#FF7F00",
}
BL_DISPLAY_ORDER = {"BL4": 1, "BL5": 2, "BL3": 3, "BL1": 4, "BL2": 5}

OBSOLETE_TABLES = ("PopulationEvents", "PopulationLocations", "DemeLocations")
RENAMED_POP_COLUMNS = (
    ("nSlickspots", "nEvents"),
    ("nSlickspotsBothYears", "nEventsBothYears"),
    ("populationIDOld", "populationName"),
    ("populationIDPx",  "populationName"),
)
EVENTS_NEW_COLUMNS = (
    ("populationID", "INTEGER REFERENCES Populations(populationID)"),
    ("demeID",       "INTEGER"),
    ("eventYear",    "INTEGER"),
)


SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS BottleneckLineages (
        BLID                     INTEGER PRIMARY KEY AUTOINCREMENT,
        BLCode                   TEXT    NOT NULL UNIQUE,
        BLDisplayOrder           INTEGER,
        nGroups                  INTEGER,
        nLocations               INTEGER,
        nEOs                     INTEGER,
        totalAreaHa              REAL,
        meanAreaHa               REAL,
        totalCensusPopulationSize INTEGER,
        meanCensusPerGroup       INTEGER,
        meanDriftIndex           REAL,
        nPopulations             INTEGER,
        nPopulationsBothYears    INTEGER,
        nPopulations2025Only     INTEGER,
        nPopulations2026Only     INTEGER,
        totalFertile2025         INTEGER,
        totalFertile2026         INTEGER,
        paletteHex               TEXT,
        definitionSource         TEXT,
        BLRemarks                TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Populations (
        populationID             INTEGER PRIMARY KEY,
        populationLabel          TEXT    NOT NULL,
        BLID                     INTEGER REFERENCES BottleneckLineages(BLID),
        populationName           TEXT,
        locationCodes            TEXT,
        locationIDs              TEXT,
        nEvents                  INTEGER,
        nEventsBothYears         INTEGER,
        nFertile2025             INTEGER,
        nFertile2026             INTEGER,
        nFertileTotal            INTEGER,
        nEvents2025              INTEGER,
        nEvents2026              INTEGER,
        nDemes2025               INTEGER,
        nDemes2026               INTEGER,
        occupancy                TEXT,
        presentBothYears         INTEGER,
        ratio2026Over2025        REAL,
        trendClass               TEXT,
        predDiversity2025        REAL,
        predDiversity2026        REAL,
        predDiversity2025Lo95    REAL,
        predDiversity2025Hi95    REAL,
        predDiversity2026Lo95    REAL,
        predDiversity2026Hi95    REAL,
        predPcompat2025          REAL,
        predPcompat2026          REAL,
        predPcompat2025Lo95      REAL,
        predPcompat2025Hi95      REAL,
        predPcompat2026Lo95      REAL,
        predPcompat2026Hi95      REAL,
        deltaDiversity           REAL,
        deltaPcompat             REAL,
        diversityCIOverlap       INTEGER,
        pcompatCIOverlap         INTEGER,
        stableAcrossYears        INTEGER,
        crashRatioNfert          REAL,
        populationRemarks        TEXT,
        definitionSource         TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Demes (
        demeKey            INTEGER PRIMARY KEY AUTOINCREMENT,
        populationID       INTEGER NOT NULL REFERENCES Populations(populationID),
        demeID             INTEGER NOT NULL,
        year               INTEGER NOT NULL,
        nEvents            INTEGER,
        componentNFertile  INTEGER,
        demeRemarks        TEXT,
        UNIQUE(populationID, demeID, year)
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_populations_bl   ON Populations(BLID)",
    "CREATE INDEX IF NOT EXISTS idx_demes_pop        ON Demes(populationID)",
    "CREATE INDEX IF NOT EXISTS idx_events_pop       ON Events(populationID)",
    "CREATE INDEX IF NOT EXISTS idx_events_pop_deme  ON Events(populationID, demeID, eventYear)",
]


TABLE_MODULES_ROWS = [
    (
        "BottleneckLineages",
        "Environment",
        (
            "Species-wide Bottleneck Lineages (BLs): clusters of Element "
            "Occurrences / locations that share a landscape-connectivity "
            "signature and act as the top-level stratum for mate-limitation "
            "analyses. Source: LEPA_EO_spatial_clustering (Buerki & Robertson "
            "2026); 5 BLs (BL1..BL5) sorted area-first then connectivity."
        ),
    ),
    (
        "Populations",
        "Demography",
        (
            "Operational populations from the LEPA mate-limitation pipeline: "
            "500 m stable spatial units built on pooled 2025+2026 event "
            "centroids + historical locationID centroids. Each population "
            "sits inside one BL (Populations.BLID) and is linked to Events "
            "via Events.populationID. Columns include across-year dynamic "
            "(trendClass), per-year predictions of SRK allele diversity and "
            "pollen compatibility with 95% CIs, and the stability flags used "
            "by the conservation-priority classifier."
        ),
    ),
    (
        "Demes",
        "Demography",
        (
            "Within-year, 50 m operational breeding units (demes) within a "
            "population. The deme is a working-hypothesis genetic neighbourhood "
            "calibrated to Wright 1943/1946 (not a Nb estimate; the 50 m "
            "threshold is a step-function stand-in for sigma^2). Each row is "
            "a rollup; the per-event deme membership is on Events "
            "(populationID + demeID + eventYear)."
        ),
    ),
]


TERMS_ROWS = [
    # BottleneckLineages — full coverage
    ("BottleneckLineages", "BLID", None, None, "Integer", "Local", None,
     "Surrogate primary key for a Bottleneck Lineage."),
    ("BottleneckLineages", "BLCode", None, None, "Text", "Local", None,
     "Human-readable BL code (BL1..BL5). Project-standard identifier."),
    ("BottleneckLineages", "BLDisplayOrder", None, None, "Integer", "Local", None,
     "Figure-ordering key: area-first then connectivity (BL4, BL5, BL3, BL1, BL2)."),
    ("BottleneckLineages", "nGroups", None, None, "Integer", "Local", None,
     "Number of LEPA_EO_spatial_clustering sub-groups in this BL."),
    ("BottleneckLineages", "nLocations", None, None, "Integer", "Local", None,
     "Number of member locationIDs in this BL."),
    ("BottleneckLineages", "nEOs", None, None, "Integer", "Local", None,
     "Number of member Element Occurrences (EOs) in this BL."),
    ("BottleneckLineages", "totalAreaHa", None, None, "Numeric", "Local", None,
     "Total slickspot habitat area across all member locations (ha)."),
    ("BottleneckLineages", "meanAreaHa", None, None, "Numeric", "Local", None,
     "Mean slickspot habitat area per LEPA_EO_spatial_clustering sub-group within this BL (ha)."),
    ("BottleneckLineages", "totalCensusPopulationSize", None, None, "Integer", "Local", None,
     "Total census (demographic) plant count summed across member locations, from LEPA_EO_spatial_clustering. "
     "NOT the count of operational Populations — see nPopulations for that."),
    ("BottleneckLineages", "meanCensusPerGroup", None, None, "Integer", "Local", None,
     "Mean census plant count per LEPA_EO_spatial_clustering sub-group within this BL."),
    ("BottleneckLineages", "meanDriftIndex", None, None, "Numeric", "Local", None,
     "Mean drift index (0-1); higher = more drift pressure."),
    ("BottleneckLineages", "nPopulations", None, None, "Integer", "Local", None,
     "Count of operational mate-limitation Populations assigned to this BL (derived from Populations.BLID)."),
    ("BottleneckLineages", "nPopulationsBothYears", None, None, "Integer", "Local", None,
     "Count of Populations in this BL with occupancy = 'both_years'."),
    ("BottleneckLineages", "nPopulations2025Only", None, None, "Integer", "Local", None,
     "Count of Populations in this BL with occupancy = '2025_only'."),
    ("BottleneckLineages", "nPopulations2026Only", None, None, "Integer", "Local", None,
     "Count of Populations in this BL with occupancy = '2026_only'."),
    ("BottleneckLineages", "totalFertile2025", None, None, "Integer", "Local", None,
     "Sum of nFertile2025 across all Populations in this BL (observed-year 2025 fertile adult total)."),
    ("BottleneckLineages", "totalFertile2026", None, None, "Integer", "Local", None,
     "Sum of nFertile2026 across all Populations in this BL (observed-year 2026 fertile adult total)."),
    ("BottleneckLineages", "paletteHex", None, None, "Text", "Local", None,
     "Set1 colour used across the SRK pipeline for this BL."),
    ("BottleneckLineages", "definitionSource", None, None, "Text", "Local", None,
     "Provenance string recording the file + date the BL definition was imported from."),
    ("BottleneckLineages", "BLRemarks", None, None, "Text", "Local", None,
     "Free-text analyst remarks on this BL (nullable)."),

    # Populations — full coverage (nEvents / nEventsBothYears replace nSlickspots*)
    ("Populations", "populationID", None, None, "Integer", "Local", None,
     "Primary key — mate-limitation populationID (1..44)."),
    ("Populations", "populationLabel", None, None, "Text", "Local", None,
     "Project-standard display label: comma-separated `{locationCode}_{locationID}`. "
     "NOT UNIQUE — multiple populationIDs can share a label when a locationID is split "
     "across populations by the >500 m pooled-event threshold."),
    ("Populations", "BLID", None, None, "Integer", "Local", None,
     "Foreign key to BottleneckLineages — the BL this population sits in."),
    ("Populations", "populationName", None, None, "Text", "Local", None,
     "Figure-facing short name — the integer populationID prefixed with 'P' (P1, P2, ..., P44). "
     "Matches the per-population identifiers used in every figure in the LEPA_mate_limitation repo."),
    ("Populations", "locationCodes", None, None, "Text", "Local", None,
     "Comma-separated locationCode list for this population (may be >1)."),
    ("Populations", "locationIDs", None, None, "Text", "Local", None,
     "Comma-separated locationID list for this population. For a proper relational lookup, "
     "use `SELECT DISTINCT locationID FROM Events WHERE populationID = ?`."),
    ("Populations", "nEvents", None, None, "Integer", "Local", None,
     "Total count of events (eventIDs = slickspot visits) assigned to this population across all years."),
    ("Populations", "nEventsBothYears", None, None, "Integer", "Local", None,
     "Count of physical slickspot sites within this population that were visited in BOTH 2025 and 2026 "
     "(cross-year persistence; 10 m haversine match between year-specific eventIDs)."),
    ("Populations", "nFertile2025", None, None, "Integer", "Local", None,
     "Sum of fertile adults across all events in this population in 2025."),
    ("Populations", "nFertile2026", None, None, "Integer", "Local", None,
     "Sum of fertile adults across all events in this population in 2026."),
    ("Populations", "nFertileTotal", None, None, "Integer", "Local", None,
     "Sum of fertile adults across all events in this population across all years (= nFertile2025 + nFertile2026)."),
    ("Populations", "nEvents2025", None, None, "Integer", "Local", None,
     "Count of events (slickspots visited) within this population in 2025."),
    ("Populations", "nEvents2026", None, None, "Integer", "Local", None,
     "Count of events (slickspots visited) within this population in 2026."),
    ("Populations", "nDemes2025", None, None, "Integer", "Local", None,
     "Count of within-year 50 m demes in 2025."),
    ("Populations", "nDemes2026", None, None, "Integer", "Local", None,
     "Count of within-year 50 m demes in 2026."),
    ("Populations", "occupancy", None, None, "Text", "Local", None,
     "Occupancy class: 'both_years', '2025_only', or '2026_only'."),
    ("Populations", "presentBothYears", None, None, "Boolean", "Local", None,
     "1 = population had at least one fertile-adult observation in BOTH 2025 and 2026."),
    ("Populations", "ratio2026Over2025", None, None, "Numeric", "Local", None,
     "nFertile2026 / nFertile2025 — the across-year fold change. Feeds trendClass thresholds "
     "(crash <= 0.25, growth >= 4). Null for single-year populations."),
    ("Populations", "trendClass", None, None, "Text", "Local", None,
     "Across-year dynamic: crash / stable / growth / ambiguous / 2025_only / 2026_only. "
     "Thresholds: crash = ratio <=0.25 + delta_div<0 + CI mismatch; growth = ratio >=4; "
     "stable = both CIs overlap + N_fert_total >=20."),
    ("Populations", "predDiversity2025", None, None, "Numeric", "Local", None,
     "Predicted mean SRK allele diversity per 50 m deme, unioned across the population, 2025."),
    ("Populations", "predDiversity2026", None, None, "Numeric", "Local", None,
     "Predicted mean SRK allele diversity per 50 m deme, unioned across the population, 2026."),
    ("Populations", "predDiversity2025Lo95", None, None, "Numeric", "Local", None,
     "Lower 95 % CI bound on predicted SRK allele diversity, 2025."),
    ("Populations", "predDiversity2025Hi95", None, None, "Numeric", "Local", None,
     "Upper 95 % CI bound on predicted SRK allele diversity, 2025."),
    ("Populations", "predDiversity2026Lo95", None, None, "Numeric", "Local", None,
     "Lower 95 % CI bound on predicted SRK allele diversity, 2026."),
    ("Populations", "predDiversity2026Hi95", None, None, "Numeric", "Local", None,
     "Upper 95 % CI bound on predicted SRK allele diversity, 2026."),
    ("Populations", "predPcompat2025", None, None, "Numeric", "Local", None,
     "Predicted species-wide pollen-compatibility probability (sporophytic SI, Class I/II dominance), 2025."),
    ("Populations", "predPcompat2026", None, None, "Numeric", "Local", None,
     "Predicted species-wide pollen-compatibility probability (sporophytic SI, Class I/II dominance), 2026."),
    ("Populations", "predPcompat2025Lo95", None, None, "Numeric", "Local", None,
     "Lower 95 % CI bound on predicted species-wide pollen-compatibility probability, 2025."),
    ("Populations", "predPcompat2025Hi95", None, None, "Numeric", "Local", None,
     "Upper 95 % CI bound on predicted species-wide pollen-compatibility probability, 2025."),
    ("Populations", "predPcompat2026Lo95", None, None, "Numeric", "Local", None,
     "Lower 95 % CI bound on predicted species-wide pollen-compatibility probability, 2026."),
    ("Populations", "predPcompat2026Hi95", None, None, "Numeric", "Local", None,
     "Upper 95 % CI bound on predicted species-wide pollen-compatibility probability, 2026."),
    ("Populations", "deltaDiversity", None, None, "Numeric", "Local", None,
     "predDiversity2026 - predDiversity2025 (positive = allele richness grew)."),
    ("Populations", "deltaPcompat", None, None, "Numeric", "Local", None,
     "predPcompat2026 - predPcompat2025 (positive = pollen compatibility improved)."),
    ("Populations", "diversityCIOverlap", None, None, "Boolean", "Local", None,
     "1 = 2025 and 2026 95% CIs on predicted diversity overlap (stable under drift)."),
    ("Populations", "pcompatCIOverlap", None, None, "Boolean", "Local", None,
     "1 = 2025 and 2026 95% CIs on pollen compatibility overlap (buffering holds)."),
    ("Populations", "stableAcrossYears", None, None, "Boolean", "Local", None,
     "1 = population passes BOTH CI-overlap tests AND the N_fert_total >= 20 size filter."),
    ("Populations", "crashRatioNfert", None, None, "Numeric", "Local", None,
     "Same as ratio2026Over2025 but retained under the project-standard 'crash' name used by the "
     "conservation-priority classifier."),
    ("Populations", "populationRemarks", None, None, "Text", "Local", None,
     "Free-text analyst remarks on this population (nullable)."),
    ("Populations", "definitionSource", None, None, "Text", "Local", None,
     "Provenance string recording which pipeline version and inputs produced this population row."),

    # Demes — full coverage
    ("Demes", "demeKey", None, None, "Integer", "Local", None,
     "Surrogate primary key for a deme row; AUTOINCREMENT. Use (populationID, demeID, year) for joins."),
    ("Demes", "populationID", None, None, "Integer", "Local", None,
     "Foreign key to Populations — the population this deme sits inside."),
    ("Demes", "demeID", None, None, "Integer", "Local", None,
     "Within-population deme ordinal (1..n_demes_year); not globally unique."),
    ("Demes", "year", None, None, "Integer", "Local", None,
     "Year of the deme partition. Demes are strictly within-year, re-computed each year."),
    ("Demes", "nEvents", None, None, "Integer", "Local", None,
     "Count of events (slickspots) that fall inside this deme in this year."),
    ("Demes", "componentNFertile", None, None, "Integer", "Local", None,
     "Sum of fertile adults across all events in the deme that year."),
    ("Demes", "demeRemarks", None, None, "Text", "Local", None,
     "Free-text analyst remarks on this deme (nullable)."),

    # Events — three new columns documented here
    ("Events", "populationID", None, None, "Integer", "Local", None,
     "Foreign key to Populations — the mate-limitation operational population this event belongs to. "
     "Added 2026-10-15. Together with Events.locationID, Events.eventID this gives the full chain from "
     "germplasmID back to BL."),
    ("Events", "demeID", None, None, "Integer", "Local", None,
     "The within-year, 50 m deme (in the same year as eventYear) this event belongs to. "
     "Joins to Demes on (populationID, demeID, year). Added 2026-10-15."),
    ("Events", "eventYear", None, None, "Integer", "Local", None,
     "Year of the event (2025 or 2026), derived from eventDate. Added 2026-10-15 for fast "
     "year-stratified queries without having to CAST(substr(eventDate, 1, 4) AS INT) each time."),
]


def log(msg: str, *, dry: bool) -> None:
    tag = "[DRY-RUN]" if dry else "[APPLY  ]"
    print(f"{tag} {msg}", flush=True)


def backup_db(db_path: Path, *, dry: bool) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = db_path.with_suffix(f".db.bak-{stamp}")
    if dry:
        log(f"would copy  {db_path}  ->  {dst}", dry=True)
    else:
        shutil.copy2(db_path, dst)
        log(f"backup written: {dst}", dry=False)
    return dst


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone() is not None


def column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    return column in cols


def migrate_old_schema(conn: sqlite3.Connection, *, dry: bool) -> None:
    """Pre-flight migration for DBs that carry the earlier six-table design or
    the old nSlickspots column names. Idempotent — safe on a fresh DB too."""
    # 1. Drop obsolete junction tables.
    for t in OBSOLETE_TABLES:
        if table_exists(conn, t):
            log(f"migration: DROP TABLE {t}", dry=dry)
            if not dry:
                conn.execute(f"DROP TABLE {t}")

    # 2. Rename old column names on Populations if present (and if Populations itself exists).
    if table_exists(conn, "Populations"):
        for old, new in RENAMED_POP_COLUMNS:
            if column_exists(conn, "Populations", old) and not column_exists(conn, "Populations", new):
                log(f"migration: ALTER TABLE Populations RENAME COLUMN {old} TO {new}", dry=dry)
                if not dry:
                    conn.execute(f"ALTER TABLE Populations RENAME COLUMN {old} TO {new}")

    # 3. Add the three new columns to Events if missing.
    if table_exists(conn, "Events"):
        for col, spec in EVENTS_NEW_COLUMNS:
            if not column_exists(conn, "Events", col):
                log(f"migration: ALTER TABLE Events ADD COLUMN {col} {spec}", dry=dry)
                if not dry:
                    conn.execute(f"ALTER TABLE Events ADD COLUMN {col} {spec}")

    # 4. Clean up stale Terms + TableModules rows from the obsolete tables.
    for t in OBSOLETE_TABLES:
        n = conn.execute("SELECT COUNT(*) FROM Terms WHERE tableName=?", (t,)).fetchone()[0]
        if n:
            log(f"migration: DELETE {n} stale Terms row(s) for {t}", dry=dry)
            if not dry:
                conn.execute("DELETE FROM Terms WHERE tableName=?", (t,))
        n = conn.execute("SELECT COUNT(*) FROM TableModules WHERE tableName=?", (t,)).fetchone()[0]
        if n:
            log(f"migration: DELETE {n} stale TableModules row for {t}", dry=dry)
            if not dry:
                conn.execute("DELETE FROM TableModules WHERE tableName=?", (t,))

    # 5. Clean up stale Terms rows for renamed columns on Populations.
    for old, _new in RENAMED_POP_COLUMNS:
        n = conn.execute(
            "SELECT COUNT(*) FROM Terms WHERE tableName='Populations' AND term=?", (old,)
        ).fetchone()[0]
        if n:
            log(f"migration: DELETE stale Terms row Populations.{old}", dry=dry)
            if not dry:
                conn.execute("DELETE FROM Terms WHERE tableName='Populations' AND term=?", (old,))


def create_schema(conn: sqlite3.Connection, *, dry: bool) -> None:
    for stmt in SCHEMA:
        head = " ".join(stmt.strip().split()[:4])
        log(f"schema: {head}...", dry=dry)
        if not dry:
            conn.execute(stmt)


def load_bl(conn: sqlite3.Connection, bl_csv: Path, *, dry: bool) -> dict[str, int]:
    df = pd.read_csv(bl_csv)
    log(f"BottleneckLineages: {len(df)} rows from {bl_csv.name}", dry=dry)
    bl_to_id: dict[str, int] = {}
    for i, row in enumerate(df.itertuples(index=False), start=1):
        bl_to_id[row.BL] = i
        if dry:
            continue
        conn.execute(
            """
            INSERT OR REPLACE INTO BottleneckLineages
              (BLID, BLCode, BLDisplayOrder, nGroups, nLocations, nEOs,
               totalAreaHa, meanAreaHa, totalCensusPopulationSize,
               meanCensusPerGroup, meanDriftIndex, paletteHex,
               definitionSource, BLRemarks)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                i, row.BL, BL_DISPLAY_ORDER.get(row.BL),
                int(row.n_groups), int(row.n_locations), int(row.n_EOs),
                float(row.total_area_ha), float(row.mean_area_ha),
                int(row.total_pop_size), int(row.mean_pop_per_group),
                float(row.mean_drift_index), BL_PALETTE.get(row.BL),
                "EO_BL_summary.csv (LEPA_EO_spatial_clustering, 2026-05-18)",
                None,
            ),
        )
    return bl_to_id


def update_bl_from_populations(conn: sqlite3.Connection, *, dry: bool) -> None:
    """After Populations is loaded, roll per-population stats up to each BL."""
    log("Updating BottleneckLineages with population-derived stats", dry=dry)
    if dry:
        return
    conn.execute(
        """
        WITH p AS (
          SELECT BLID,
                 COUNT(*)                                   AS nPopulations,
                 SUM(CASE WHEN occupancy = 'both_years' THEN 1 ELSE 0 END) AS nPopulationsBothYears,
                 SUM(CASE WHEN occupancy = '2025_only'  THEN 1 ELSE 0 END) AS nPopulations2025Only,
                 SUM(CASE WHEN occupancy = '2026_only'  THEN 1 ELSE 0 END) AS nPopulations2026Only,
                 SUM(COALESCE(nFertile2025, 0))             AS totalFertile2025,
                 SUM(COALESCE(nFertile2026, 0))             AS totalFertile2026
            FROM Populations
           GROUP BY BLID
        )
        UPDATE BottleneckLineages
           SET nPopulations          = (SELECT nPopulations          FROM p WHERE p.BLID = BottleneckLineages.BLID),
               nPopulationsBothYears = (SELECT nPopulationsBothYears FROM p WHERE p.BLID = BottleneckLineages.BLID),
               nPopulations2025Only  = (SELECT nPopulations2025Only  FROM p WHERE p.BLID = BottleneckLineages.BLID),
               nPopulations2026Only  = (SELECT nPopulations2026Only  FROM p WHERE p.BLID = BottleneckLineages.BLID),
               totalFertile2025      = (SELECT totalFertile2025      FROM p WHERE p.BLID = BottleneckLineages.BLID),
               totalFertile2026      = (SELECT totalFertile2026      FROM p WHERE p.BLID = BottleneckLineages.BLID)
         WHERE BLID IN (SELECT BLID FROM p);
        """
    )


def load_populations(
    conn: sqlite3.Connection,
    tables_dir: Path,
    bl_to_id: dict[str, int],
    *,
    dry: bool,
) -> None:
    summary = pd.read_csv(tables_dir / "step29a_population_summary.tsv", sep="\t")
    classified = pd.read_csv(tables_dir / "step30g_populations_classified.tsv", sep="\t")
    preds = pd.read_csv(tables_dir / "step30g_prediction_population_year.tsv", sep="\t")

    pred_wide = preds.pivot_table(
        index="populationID", columns="year",
        values=["pred_srk_diversity_lo95", "pred_srk_diversity_hi95",
                "pred_pcompat_lo95", "pred_pcompat_hi95"],
        aggfunc="first",
    )
    pred_wide.columns = [f"{a}_{int(b)}" for a, b in pred_wide.columns]
    pred_wide = pred_wide.reset_index()

    df = (
        summary.merge(
            classified[["populationID", "population_label", "trend_class",
                        "pred_diversity_2025", "pred_diversity_2026",
                        "pred_pcompat_2025", "pred_pcompat_2026",
                        "delta_diversity", "delta_pcompat",
                        "diversity_CI_overlap", "pcompat_CI_overlap",
                        "stable_across_years", "crash_ratio_nfert"]],
            on="populationID", how="left",
        )
        .merge(pred_wide, on="populationID", how="left")
    )

    log(f"Populations: {len(df)} rows", dry=dry)
    missing_label = df["population_label"].isna().sum()
    if missing_label:
        log(f"  {missing_label} populations missing from classified TSV", dry=dry)

    for row in df.itertuples(index=False):
        bl_id = bl_to_id.get(row.BL)
        label = row.population_label if pd.notna(row.population_label) else None
        if label is None:
            codes = str(row.locationCodes) if pd.notna(row.locationCodes) else ""
            ids = str(row.locationIDs) if pd.notna(row.locationIDs) else ""
            label = f"P{int(row.populationID)}:{codes}|{ids}"
        if dry:
            continue
        conn.execute(
            """
            INSERT OR REPLACE INTO Populations VALUES (
              :populationID, :populationLabel, :BLID, :populationName,
              :locationCodes, :locationIDs,
              :nEvents, :nEventsBothYears,
              :nFertile2025, :nFertile2026, :nFertileTotal,
              :nEvents2025, :nEvents2026,
              :nDemes2025, :nDemes2026,
              :occupancy, :presentBothYears, :ratio2026Over2025,
              :trendClass,
              :predDiversity2025, :predDiversity2026,
              :predDiversity2025Lo95, :predDiversity2025Hi95,
              :predDiversity2026Lo95, :predDiversity2026Hi95,
              :predPcompat2025, :predPcompat2026,
              :predPcompat2025Lo95, :predPcompat2025Hi95,
              :predPcompat2026Lo95, :predPcompat2026Hi95,
              :deltaDiversity, :deltaPcompat,
              :diversityCIOverlap, :pcompatCIOverlap,
              :stableAcrossYears, :crashRatioNfert,
              :populationRemarks, :definitionSource
            )
            """,
            {
                "populationID": int(row.populationID),
                "populationLabel": label,
                "BLID": bl_id,
                "populationName": f"P{int(row.populationID)}",
                "locationCodes": str(row.locationCodes) if pd.notna(row.locationCodes) else None,
                "locationIDs": str(row.locationIDs) if pd.notna(row.locationIDs) else None,
                "nEvents": int(row.n_slickspots) if pd.notna(row.n_slickspots) else None,
                "nEventsBothYears": int(row.n_slickspots_both_years) if pd.notna(row.n_slickspots_both_years) else None,
                "nFertile2025": int(row.n_fertile_2025) if pd.notna(row.n_fertile_2025) else None,
                "nFertile2026": int(row.n_fertile_2026) if pd.notna(row.n_fertile_2026) else None,
                "nFertileTotal": int(row.n_fertile_total) if pd.notna(row.n_fertile_total) else None,
                "nEvents2025": int(row.n_events_2025) if pd.notna(row.n_events_2025) else None,
                "nEvents2026": int(row.n_events_2026) if pd.notna(row.n_events_2026) else None,
                "nDemes2025": int(row.n_demes_2025) if pd.notna(row.n_demes_2025) else None,
                "nDemes2026": int(row.n_demes_2026) if pd.notna(row.n_demes_2026) else None,
                "occupancy": row.occupancy if pd.notna(row.occupancy) else None,
                "presentBothYears": int(bool(row.present_both_years)) if pd.notna(row.present_both_years) else None,
                "ratio2026Over2025": float(row.ratio_2026_over_2025) if pd.notna(row.ratio_2026_over_2025) and str(row.ratio_2026_over_2025) != "" else None,
                "trendClass": row.trend_class if pd.notna(row.trend_class) else None,
                "predDiversity2025": float(row.pred_diversity_2025) if pd.notna(row.pred_diversity_2025) else None,
                "predDiversity2026": float(row.pred_diversity_2026) if pd.notna(row.pred_diversity_2026) else None,
                "predDiversity2025Lo95": float(getattr(row, "pred_srk_diversity_lo95_2025", None)) if pd.notna(getattr(row, "pred_srk_diversity_lo95_2025", None)) else None,
                "predDiversity2025Hi95": float(getattr(row, "pred_srk_diversity_hi95_2025", None)) if pd.notna(getattr(row, "pred_srk_diversity_hi95_2025", None)) else None,
                "predDiversity2026Lo95": float(getattr(row, "pred_srk_diversity_lo95_2026", None)) if pd.notna(getattr(row, "pred_srk_diversity_lo95_2026", None)) else None,
                "predDiversity2026Hi95": float(getattr(row, "pred_srk_diversity_hi95_2026", None)) if pd.notna(getattr(row, "pred_srk_diversity_hi95_2026", None)) else None,
                "predPcompat2025": float(row.pred_pcompat_2025) if pd.notna(row.pred_pcompat_2025) else None,
                "predPcompat2026": float(row.pred_pcompat_2026) if pd.notna(row.pred_pcompat_2026) else None,
                "predPcompat2025Lo95": float(getattr(row, "pred_pcompat_lo95_2025", None)) if pd.notna(getattr(row, "pred_pcompat_lo95_2025", None)) else None,
                "predPcompat2025Hi95": float(getattr(row, "pred_pcompat_hi95_2025", None)) if pd.notna(getattr(row, "pred_pcompat_hi95_2025", None)) else None,
                "predPcompat2026Lo95": float(getattr(row, "pred_pcompat_lo95_2026", None)) if pd.notna(getattr(row, "pred_pcompat_lo95_2026", None)) else None,
                "predPcompat2026Hi95": float(getattr(row, "pred_pcompat_hi95_2026", None)) if pd.notna(getattr(row, "pred_pcompat_hi95_2026", None)) else None,
                "deltaDiversity": float(row.delta_diversity) if pd.notna(row.delta_diversity) else None,
                "deltaPcompat": float(row.delta_pcompat) if pd.notna(row.delta_pcompat) else None,
                "diversityCIOverlap": int(bool(row.diversity_CI_overlap)) if pd.notna(row.diversity_CI_overlap) else None,
                "pcompatCIOverlap": int(bool(row.pcompat_CI_overlap)) if pd.notna(row.pcompat_CI_overlap) else None,
                "stableAcrossYears": int(bool(row.stable_across_years)) if pd.notna(row.stable_across_years) else None,
                "crashRatioNfert": float(row.crash_ratio_nfert) if pd.notna(row.crash_ratio_nfert) and str(row.crash_ratio_nfert) != "" else None,
                "populationRemarks": None,
                "definitionSource": "step01_populations.py (LEPA_mate_limitation), pooled 2025+2026",
            },
        )


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    import math
    R = 6_371_000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def assign_demes(events_df: pd.DataFrame, radius_m: float = 50.0) -> pd.DataFrame:
    """50 m haversine single-linkage per (populationID, eventYear) group.
    Returns the same frame with an added 1-indexed `demeID` column
    (components ordered by total n_fertile DESC, tiebreak smallest eventID)."""
    out = events_df.copy()
    out["demeID"] = -1
    for (pid, yr), grp in events_df.groupby(["populationID", "event_year"], sort=False):
        n = len(grp)
        if n == 0:
            continue
        idx = grp.index.to_numpy()
        lat = grp["lat"].to_numpy(dtype=float)
        lon = grp["lon"].to_numpy(dtype=float)
        nf = grp["n_fertile"].fillna(0).to_numpy(dtype=float)
        eid = grp["eventID"].to_numpy()
        parent = list(range(n))

        def find(i: int) -> int:
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        for i in range(n):
            for j in range(i + 1, n):
                if haversine_m(lat[i], lon[i], lat[j], lon[j]) <= radius_m:
                    ra, rb = find(i), find(j)
                    if ra != rb:
                        parent[ra] = rb
        roots = [find(i) for i in range(n)]
        comps: dict[int, list[int]] = {}
        for i, r in enumerate(roots):
            comps.setdefault(r, []).append(i)
        ordered = sorted(
            comps.values(),
            key=lambda members: (-float(sum(nf[k] for k in members)), int(min(eid[k] for k in members))),
        )
        for d, members in enumerate(ordered, start=1):
            for k in members:
                out.at[idx[k], "demeID"] = d
    return out


def load_demes_and_update_events(
    conn: sqlite3.Connection,
    tables_dir: Path,
    *,
    dry: bool,
) -> None:
    crosswalk = pd.read_csv(tables_dir / "step29a_population_crosswalk.tsv", sep="\t")
    tsv_demes = pd.read_csv(tables_dir / "step29a_demes_per_population_year.tsv", sep="\t")

    # Full-precision coords from the DB (fall back to crosswalk 4-decimal coords on miss).
    event_ids = crosswalk["eventID"].astype(int).tolist()
    db_coords = pd.read_sql(
        f"SELECT eventID, eventDecimalLatitude AS lat_db, eventDecimalLongitude AS lon_db "
        f"FROM Events WHERE eventID IN ({','.join('?' * len(event_ids))})",
        conn, params=event_ids,
    )
    crosswalk = crosswalk.merge(db_coords, on="eventID", how="left")
    use_db = crosswalk["lat_db"].notna() & crosswalk["lon_db"].notna()
    crosswalk.loc[use_db, "lat"] = crosswalk.loc[use_db, "lat_db"]
    crosswalk.loc[use_db, "lon"] = crosswalk.loc[use_db, "lon_db"]
    crosswalk = crosswalk.drop(columns=["lat_db", "lon_db"])
    log(f"Using DB full-precision coords for {int(use_db.sum())}/{len(crosswalk)} events", dry=dry)

    log(f"Deme assignment: 50 m single-linkage on {len(crosswalk)} events", dry=dry)
    with_demes = assign_demes(crosswalk, radius_m=50.0)

    # Compare against the exported TSV; expected disagreement at P39 2025 (see docstring).
    mismatches = []
    for (pid, yr), grp in with_demes.groupby(["populationID", "event_year"]):
        mine = sorted(grp.groupby("demeID")["n_fertile"].sum().astype(int).tolist(), reverse=True)
        tsv = sorted(
            tsv_demes[(tsv_demes["populationID"] == pid) & (tsv_demes["year"] == yr)]["component_N_fertile"].astype(int).tolist(),
            reverse=True,
        )
        if mine != tsv:
            mismatches.append(f"  population {pid} year {yr}: inline={mine} vs TSV={tsv}")
    if mismatches:
        log(f"NOTE: {len(mismatches)} (populationID, year) group(s) disagree with the exported TSV "
            f"(inline single-linkage on eventID coords is authoritative):", dry=dry)
        for m in mismatches:
            print(m)

    # Demes rollup.
    rollup = (
        with_demes.groupby(["populationID", "event_year", "demeID"], sort=True)
        .agg(nEvents=("eventID", "count"), componentNFertile=("n_fertile", "sum"))
        .reset_index()
        .rename(columns={"event_year": "year"})
    )
    log(f"Demes: {len(rollup)} rows", dry=dry)
    for row in rollup.itertuples(index=False):
        if dry:
            continue
        conn.execute(
            "INSERT OR REPLACE INTO Demes (populationID, demeID, year, nEvents, componentNFertile, demeRemarks) "
            "VALUES (?,?,?,?,?,?)",
            (int(row.populationID), int(row.demeID), int(row.year),
             int(row.nEvents), int(row.componentNFertile), None),
        )

    # UPDATE Events with populationID / demeID / eventYear.
    log(f"Events UPDATE: setting populationID/demeID/eventYear on {len(with_demes)} rows", dry=dry)
    for row in with_demes.itertuples(index=False):
        if dry:
            continue
        conn.execute(
            "UPDATE Events SET populationID=?, demeID=?, eventYear=? WHERE eventID=?",
            (int(row.populationID), int(row.demeID), int(row.event_year), int(row.eventID)),
        )


def events_has_composite_fk_to_demes(conn: sqlite3.Connection) -> bool:
    """True iff Events already has the composite FK
    (populationID, demeID, eventYear) → Demes(populationID, demeID, year)."""
    fks: dict[int, list[tuple[str, str, str]]] = {}
    for row in conn.execute("PRAGMA foreign_key_list(Events)"):
        fk_id = row[0]
        fks.setdefault(fk_id, []).append((row[2], row[3], row[4]))  # (table, from, to)
    for parts in fks.values():
        if len(parts) != 3:
            continue
        tables = {t for t, _, _ in parts}
        froms = {f for _, f, _ in parts}
        tos = {o for _, _, o in parts}
        if (tables == {"Demes"}
                and froms == {"populationID", "demeID", "eventYear"}
                and tos == {"populationID", "demeID", "year"}):
            return True
    return False


def ensure_events_composite_fk(conn: sqlite3.Connection, *, dry: bool) -> None:
    """Add the composite FK FOREIGN KEY (populationID, demeID, eventYear)
    → Demes(populationID, demeID, year) to Events. No-op if already present.

    SQLite can't ALTER-add a composite FK, so this rebuilds Events: create a
    new Events_new with the FK, copy rows, drop old, rename. Must run OUTSIDE
    the main transaction (PRAGMA foreign_keys cannot be toggled inside one).
    """
    if events_has_composite_fk_to_demes(conn):
        log("Events: composite FK to Demes already present — skip rebuild", dry=dry)
        return

    orphans = conn.execute(
        """
        SELECT COUNT(*)
          FROM Events e
          LEFT JOIN Demes d
            ON d.populationID = e.populationID AND d.demeID = e.demeID AND d.year = e.eventYear
         WHERE e.populationID IS NOT NULL AND d.demeKey IS NULL
        """
    ).fetchone()[0]
    if orphans > 0:
        msg = (f"ERROR: {orphans} orphan Events row(s) have (populationID, demeID, eventYear) "
               f"not matching any Demes row. Composite FK would reject the rebuild. "
               f"Aborting without changes.")
        log(msg, dry=dry)
        if not dry:
            raise RuntimeError(msg)
        return

    log("Rebuilding Events to add composite FK → Demes(populationID, demeID, year)", dry=dry)
    if dry:
        return

    # Snapshot existing indexes/triggers on Events so we can recreate them.
    extra_sql = [
        r[0] for r in conn.execute(
            "SELECT sql FROM sqlite_master WHERE tbl_name='Events' "
            "  AND type IN ('index','trigger') AND sql IS NOT NULL"
        ).fetchall()
    ]
    cols = [r[1] for r in conn.execute("PRAGMA table_info(Events)").fetchall()]
    col_list = ", ".join(cols)

    conn.execute("PRAGMA foreign_keys=OFF")
    try:
        conn.execute("BEGIN")
        conn.execute(
            """
            CREATE TABLE Events_new (
                eventID                       INTEGER PRIMARY KEY UNIQUE NOT NULL,
                eventDate                     TEXT NOT NULL,
                eventDecimalLatitude          NUMERIC,
                eventDecimalLongitude         NUMERIC,
                eventSizeValue                NUMERIC,
                eventSizeUnit                 TEXT DEFAULT m2,
                eventDefinition               TEXT,
                eventCondition                INTEGER,
                organismQuantityFertile       NUMERIC,
                organismQuantityVegetative    NUMERIC,
                measurementValueCrownAvg      NUMERIC,
                measurementValueCrownAvgUnit  TEXT DEFAULT cm,
                associatedTaxa                TEXT,
                eventRemarks                  TEXT,
                locationID                    INTEGER REFERENCES Locations(locationID),
                measurementValuePlantArea     REAL,
                measurementValuePlantAreaUnit TEXT,
                associatedTaxaOriginal        TEXT,
                populationID                  INTEGER REFERENCES Populations(populationID),
                demeID                        INTEGER,
                eventYear                     INTEGER,
                FOREIGN KEY (populationID, demeID, eventYear)
                    REFERENCES Demes(populationID, demeID, year)
            )
            """
        )
        conn.execute(f"INSERT INTO Events_new ({col_list}) SELECT {col_list} FROM Events")
        conn.execute("DROP TABLE Events")
        conn.execute("ALTER TABLE Events_new RENAME TO Events")
        for sql in extra_sql:
            conn.execute(sql)
        # Run SQLite's own FK sanity check before committing.
        bad = conn.execute("PRAGMA foreign_key_check(Events)").fetchall()
        if bad:
            raise RuntimeError(f"FK check failed after rebuild: {bad}")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.execute("PRAGMA foreign_keys=ON")
    log("Events rebuild complete; composite FK is now enforced", dry=dry)


def load_terms(conn: sqlite3.Connection, *, dry: bool) -> None:
    cur = conn.cursor()
    max_table_id = cur.execute("SELECT MAX(tableID) FROM TableModules").fetchone()[0] or 0
    max_term_id = cur.execute("SELECT MAX(termID) FROM Terms").fetchone()[0] or 0
    log(f"TableModules max_id={max_table_id}  Terms max_id={max_term_id}", dry=dry)

    cur2 = conn.cursor()
    name_to_id: dict[str, int] = {}
    for name, module, definition in TABLE_MODULES_ROWS:
        existing = cur2.execute(
            "SELECT tableID FROM TableModules WHERE tableName = ?", (name,)
        ).fetchone()
        if existing:
            tid = int(existing[0])
            log(f"  TableModules exists: ({tid}, {name}) — updating definition", dry=dry)
            if not dry:
                cur2.execute(
                    "UPDATE TableModules SET tableModule = ?, definition = ? WHERE tableID = ?",
                    (module, definition, tid),
                )
        else:
            max_table_id += 1
            tid = max_table_id
            log(f"  TableModules += ({tid}, {name})", dry=dry)
            if not dry:
                cur2.execute(
                    "INSERT INTO TableModules (tableID, tableName, tableModule, definition) VALUES (?,?,?,?)",
                    (tid, name, module, definition),
                )
        name_to_id[name] = tid

    # Resolve Events's tableID too so Terms rows for Events columns carry the right FK.
    events_row = cur2.execute("SELECT tableID FROM TableModules WHERE tableName='Events'").fetchone()
    if events_row:
        name_to_id["Events"] = int(events_row[0])

    for tbl, term, term_orig, def_orig, dtype, standard, url, def_db in TERMS_ROWS:
        existing = cur2.execute(
            "SELECT termID FROM Terms WHERE tableName = ? AND term = ?", (tbl, term)
        ).fetchone()
        tid = name_to_id.get(tbl)
        if existing:
            term_id = int(existing[0])
            log(f"  Terms exists: ({term_id}, {tbl}.{term}) — updating", dry=dry)
            if not dry:
                cur2.execute(
                    "UPDATE Terms SET tableID=?, dataType=?, standard=?, URL=?, definitionDB=? "
                    "WHERE termID=?",
                    (tid, dtype, standard, url, def_db, term_id),
                )
        else:
            max_term_id += 1
            term_id = max_term_id
            log(f"  Terms += ({term_id}, {tbl}.{term})", dry=dry)
            if not dry:
                cur2.execute(
                    "INSERT INTO Terms "
                    "(termID, tableID, tableName, term, termOriginal, definitionOriginal, dataType, standard, URL, definitionDB) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (term_id, tid, tbl, term, term_orig, def_orig, dtype, standard, url, def_db),
                )


def summarise(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    for t in ("BottleneckLineages", "Populations", "Demes"):
        n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {n} rows")
    n_evt = cur.execute("SELECT COUNT(*) FROM Events").fetchone()[0]
    n_evt_pop = cur.execute("SELECT COUNT(*) FROM Events WHERE populationID IS NOT NULL").fetchone()[0]
    print(f"  Events: {n_evt} rows ({n_evt_pop} with populationID set)")
    print()
    print("  Trend-class breakdown:")
    for cls, n in cur.execute(
        "SELECT trendClass, COUNT(*) FROM Populations GROUP BY trendClass ORDER BY 2 DESC"
    ):
        print(f"    {cls or '(null)'}: {n}")
    print()
    print("  Populations per BL:")
    for bl, n in cur.execute(
        "SELECT b.BLCode, COUNT(*) FROM Populations p LEFT JOIN BottleneckLineages b ON b.BLID = p.BLID "
        "GROUP BY b.BLCode ORDER BY b.BLDisplayOrder"
    ):
        print(f"    {bl}: {n}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--db", type=Path, default=DEFAULT_DB,
                   help=f"target SQLite DB (default: {DEFAULT_DB})")
    p.add_argument("--tables-dir", type=Path, default=DEFAULT_TABLES_DIR)
    p.add_argument("--bl-summary", type=Path, default=DEFAULT_BL_SUMMARY)
    p.add_argument("--schema-only", action="store_true",
                   help="create tables + columns + Terms rows only; skip data loads")
    p.add_argument("--apply", action="store_true", help="write to DB (otherwise dry-run)")
    args = p.parse_args()

    dry = not args.apply

    print(f"DB:          {args.db}")
    print(f"Tables dir:  {args.tables_dir}")
    print(f"BL summary:  {args.bl_summary}")
    print(f"Schema-only: {args.schema_only}")
    print(f"Mode:        {'DRY-RUN' if dry else 'APPLY'}")
    print()

    required = [args.db]
    if not args.schema_only:
        required += [args.tables_dir, args.bl_summary]
    for pth in required:
        if not pth.exists():
            print(f"ERROR: not found: {pth}", file=sys.stderr)
            return 1

    backup_db(args.db, dry=dry)

    conn = sqlite3.connect(str(args.db))
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        if not dry:
            conn.execute("BEGIN")
        migrate_old_schema(conn, dry=dry)
        create_schema(conn, dry=dry)
        if not args.schema_only:
            bl_to_id = load_bl(conn, args.bl_summary, dry=dry)
            load_populations(conn, args.tables_dir, bl_to_id, dry=dry)
            load_demes_and_update_events(conn, args.tables_dir, dry=dry)
            update_bl_from_populations(conn, dry=dry)
        load_terms(conn, dry=dry)
        if not dry:
            conn.commit()

        # Composite FK must be added OUTSIDE the main transaction because
        # SQLite ignores PRAGMA foreign_keys toggles inside a BEGIN..COMMIT.
        ensure_events_composite_fk(conn, dry=dry)

        if not dry and not args.schema_only:
            print()
            print("Row counts after apply:")
            summarise(conn)
    except Exception:
        if not dry:
            conn.rollback()
        raise
    finally:
        conn.close()

    print()
    print("Done." if not dry else "Dry-run complete; re-run with --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
