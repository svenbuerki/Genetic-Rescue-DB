# LEPA Fieldwork Protocol & Seed Collection Database

**Species:** *Lepidium papilliferum* (slickspot peppergrass, LEPA)
**Status:** Federally threatened (Endangered Species Act)
**Institution:** Boise State University — Buerki Lab
**Contact:** Sven BUERKI, Ph.D. — svenbuerki@boisestate.edu

---

## Overview

This repository supports a **genetic rescue program** for slickspot peppergrass (*Lepidium papilliferum*), a federally threatened plant endemic to southwestern Idaho's sagebrush-steppe ecosystem.

The core goal is to develop a transferable framework for genetic rescue of threatened plants: restoring functionally viable and genetically diverse seed banks across a species' range through informed breeding and targeted reintroduction. The program is implemented in a spatially-oriented SQLite database that tracks individual plants from field collection through biobanking, breeding trials, and restoration.

The six-step genetic rescue pipeline:

1. Determine genetic diversity across the landscape
2. Conduct targeted fieldwork and seed collection
3. Characterize seeds (weight → estimated seed count)
4. Build bulked seed lots for restoration
5. Execute controlled breeding trials to increase diversity
6. Reintroduce material to under-represented populations

---

## Repository Structure

```
SQL_DB/
├── LEPA_SQL.db                          # Core SQLite3 database
├── README.md                            # This file
├── Multimedia_images/<year>/<date>/     # RAW field images (immutable source; one folder per field day)
├── Multimedia_main/                     # Renamed unique-name copies (LEPA_<date>_<sha8>.jpg) + file_registry.csv
├── Multimedia_pipeline/                 # Image → database pipeline
│   ├── IMAGE_PIPELINE_GUIDE.md          # ▶ how the pipeline works (start here)
│   ├── DATA_QUALITY.md                  # ▶ data-quality status + tracked issues
│   ├── 00_sort_by_date.py … 03_phenotype.py   # the four pipeline scripts
│   ├── PIPELINE_LOG.md                  # running log of every --apply
│   ├── REPORT_2025_measurement.md, REPORT_2026_pipeline_dryrun.md, ISSUE_filename_collision.md
│   └── legacy_2025/                     # archived 2025 pipeline scripts
├── Documentation/
│   ├── LEPA_DB_Documentation.md        # Database & protocol documentation (GitHub-facing)
│   ├── Documentation_LEPA_fieldwork.Rmd # Full project report source (R/bookdown)
│   ├── Documentation_LEPA_fieldwork.html
│   └── Figures/                         # Maps, diagrams, workflow figures
├── Protocols/
│   ├── 01_Location_LEPA fieldwork 2025_PM.docx  # Location/EO data-entry form
│   ├── 02_Event_LEPA fieldwork 2025_PM.docx     # Slick spot & plant data-entry form
│   └── 1000_Seed_Weight.zip             # R script + calibration data for seed-weight model
├── Queries/                             # Analysis scripts + pre-computed query results
└── Not_GitHub/                          # Local development files (not versioned)
```

**Full database and protocol documentation:** [`Documentation/LEPA_DB_Documentation.md`](Documentation/LEPA_DB_Documentation.md)

---

## Database

- **Engine:** SQLite 3
- **File:** `LEPA_SQL.db`
- **Tables:** 22 (plus two system tables: `TableModules`, `Terms`)

The database is organized into seven modules:

| Module | Purpose |
|--------|---------|
| **Admin** | Staff, project metadata, QC notes, multimedia |
| **Environment** | Spatial hierarchy, taxonomy, EO rankings |
| **Demography** | Population size and habitat condition per event/EO |
| **Biobanking** | Seed accessions, transactions, tissue and molecular samples |
| **Genetics** | Sequencing metadata and quality metrics |
| **Breeding** | Hand-pollination records and trial design |
| **Restoration** | Restoration trial outcomes (planned for 2027) |

### Spatial Hierarchy

```
EO (Element Occurrence — federally designated population)
 └── Location (discrete site within an EO)
      └── Event (individual slick spot)
           └── Occurrence (individual fruiting plant)
                └── Germplasm (seed accession from that plant)
```

### Summer 2025 Snapshot

| Entity | Count |
|--------|-------|
| Element Occurrences (EOs) sampled | 19 |
| Locations | 39 |
| Events (slick spots) | 237 |
| Occurrences (fruiting plants) | 810 |
| Germplasm accessions | 785 |
| Seeds biobanked (estimated) | 476,140 |
| Hand-pollination crosses | 43 |

---

## Image → Database Pipeline (field photo to record)

Every fruiting plant is photographed in the field with a whiteboard (ID + date + rulers).
Those photos are the entry point for three tables — **Multimedia**, **Phenotyping**, and (from
2026) **Occurrences** themselves. This section is the shared reference for the team before the
**new adapted-board imaging protocol** begins.

> 📖 **Full pipeline guide:** [`Multimedia_pipeline/IMAGE_PIPELINE_GUIDE.md`](Multimedia_pipeline/IMAGE_PIPELINE_GUIDE.md) (folder convention, the four scripts, naming, idempotency). &nbsp; 🩺 **Data-quality status:** [`Multimedia_pipeline/DATA_QUALITY.md`](Multimedia_pipeline/DATA_QUALITY.md).

### Two operating modes

| | **2025 mode — link & verify** | **2026 mode — pre-populate** |
|---|---|---|
| Records exist first? | Yes — field sheets hand-digitized into `Occurrences` | **No** — the image creates the record |
| Board read is… | **cross-checked** against the existing occurrence | the **source of truth** (no field-sheet to check against) |
| Validation comes from | matching the board number to a known row | **on-board redundancy + OCR ensemble + human gate** |
| Risk | low (two independent sources) | higher → mitigated by staging + review |

2026 mode removes the cross-check, so trust is rebuilt with **board structure** (printed
`O=`/`EO=`/`L=` fields), **independent on-board `h=`/`w=` measurements**, and a **mandatory
human review gate** — no record is written until a person approves the staged batch.

### The adapted 2026 board (what every field photo should carry)

```
 O  = occurrence (one unique number per plant, never reused)
 EO = Element Occurrence code            L = Location code (resolves to GPS)
 h  = height (cm)     w = crown width (cm)        date
 + two rulers for scale  + a taller scale for large plants
```

A coordinate (or a Location code that resolves to one) **must** accompany each board: a
`Location` is *defined* by its GPS, so without it no Occurrence can be created.

### Storage & collision-proof naming

Raw images live **only** in `Multimedia_images/<year>/<YYYY-MM-DD>/` (one folder per field day).
The pipeline copies each into a flat `Multimedia_main/` under a unique, content-addressed name
**`LEPA_<date>_<sha8>.jpg`**. This exists because camera filenames (`JCN_####`) reset every season
and once silently overwrote 56 of the 2025 images — content-addressing makes that impossible. The
original camera name, year, field-day date, EXIF capture time and SHA-256 are kept as provenance
(new `Multimedia` columns + `Multimedia_main/file_registry.csv`).

### The pipeline — four scripts (mapping to steps A → E)

| Script | Step | Role |
|---|---|---|
| `00_sort_by_date.py` | — | sort loose year-folder images into date subfolders |
| `01_ingest_register.py` | **A** | rename to `LEPA_<date>_<sha8>.jpg` → `Multimedia_main/`; update `Multimedia` identifier + provenance |
| `02_ocr.py` | **B/C** | worklist of un-linked images → OCR sweep → **review staging** (`NEW_EO`/`NEEDS_LOCATION` flags; nothing auto-created) |
| `03_phenotype.py` | **E** | worklist of unmeasured occurrences → measurement sweep → insert `Phenotyping` |

Each is **dry-run by default**, **backs up the DB** before any write, and logs to
[`Multimedia_pipeline/PIPELINE_LOG.md`](Multimedia_pipeline/PIPELINE_LOG.md). An **idempotency rule**
runs throughout: OCR only images not yet linked to an occurrence; phenotype only occurrences with no
measurement — so re-running never duplicates work. The OCR/measurement itself is an in-session
read-only agent sweep (subscription, no per-image API cost). Full details in the
[pipeline guide](Multimedia_pipeline/IMAGE_PIPELINE_GUIDE.md).

### How well does it work? (2026 blind dry-run, 128 boards)

A blind dry-run against records we already trust (full write-up:
[`Multimedia_pipeline/REPORT_2026_pipeline_dryrun.md`](Multimedia_pipeline/REPORT_2026_pipeline_dryrun.md)):

- **OCR:** occurrence ID **96%**, EO code reproduced the database except where the *database*
  was wrong — the blind read **caught a real mis-linkage** (5 plants stored under the wrong EO,
  since corrected).
- **Measurement repeatability:** median **±2 cm** (height & crown); **size class ~81%**.
- **Guidance:** **size class is the primary size metric; cm is supporting.** A taller in-frame
  scale is the highest-value field-kit fix.

**Current state (2026-06-27):** the pipeline is migrated and live — 948 images ingested under the
new scheme, 809 `Multimedia` identifiers renamed, **Phenotyping = 741** (every occurrence image with
a measurable plant), and a full integrity audit is clean. See
[`DATA_QUALITY.md`](Multimedia_pipeline/DATA_QUALITY.md) for the standing items and tracked issues.

> **For the field team:** structured board fields + GPS + on-board `h/w` + unique, never-reused
> occurrence numbers are what make automated pre-population safe. Everything still passes a human
> review gate before it enters the database.

---

## Data Sensitivity

*Lepidium papilliferum* is listed as threatened under the ESA. Per U.S. Fish and Wildlife Service guidelines, **precise GPS coordinates must not be made public**. The following fields must be excluded from any public-facing interface:

`locationDecimalLatitude`, `locationDecimalLongitude`, `eventDecimalLatitude`, `eventDecimalLongitude`

---

## Terminology and Standards

| Standard | Scope |
|----------|-------|
| [Darwin Core](https://dwc.tdwg.org/terms/) | Occurrence and location data |
| [Dublin Core](https://www.dublincore.org/specifications/dublin-core/) | Metadata |
| [PlantBreeding / BrAPI v2.1](https://github.com/plantbreeding/BrAPI) | Germplasm and breeding data |
| [BBMRI-ERIC / MIABIS](https://github.com/BBMRI-ERIC/miabis) | Biobank and sample data |

Custom terms are defined in the `Terms` table (54 entries).

---

## Key Publications

- Buerki et al. (2019) *Bioinformatics* — https://doi.org/10.1093/bioinformatics/btz190
- Buerki et al. (2022) *G3: Genes, Genomes, Genetics* — https://doi.org/10.1093/g3journal/jkac078

---

## Data Ownership

Buerki Lab, Department of Biological Sciences, Boise State University.
Contact svenbuerki@boisestate.edu before redistributing any subset of this database.
