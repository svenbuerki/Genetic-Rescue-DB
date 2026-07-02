# Genetic Rescue Database Framework

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---

## Overview

This repository provides a **transferable framework for the genetic rescue of threatened plant species**: restoring functionally viable and genetically diverse seed banks across a species' range through informed breeding and targeted reintroduction. The framework is implemented in a spatially-oriented SQLite database that tracks individual plants from field collection through biobanking, breeding trials, and restoration.

The six-step genetic rescue pipeline:

1. Determine genetic diversity across the landscape
2. Conduct targeted fieldwork and seed collection
3. Characterize seeds (weight → estimated seed count)
4. Build bulked seed lots for restoration
5. Execute controlled breeding trials to increase diversity
6. Reintroduce material to under-represented populations

📖 **Full database documentation:** **[`Documentation/Documentation_DB.md`](Documentation/Documentation_DB.md)** — modules, tables, fields, and the data-acquisition workflow.

---

## Documentation Map

Use this map to navigate the project — *what has been done, and how.* Two operational pipelines turn raw
field/lab work into records in the database:

**① Field → Database (photos & forms → records).** How each plant becomes an `Occurrence` with images and
phenotypes.

```
Field forms + board photos ──▶ OCR / image pipeline ──▶ Locations · Events · Occurrences · Multimedia · Phenotyping
```
→ [`Multimedia_pipeline/IMAGE_PIPELINE_GUIDE.md`](Multimedia_pipeline/IMAGE_PIPELINE_GUIDE.md) (start here) ·
[Multimedia & Image-Based Phenotyping](#multimedia--image-based-phenotyping) (below)

**② Biobanking → Genetics (the genotyping pipeline).** How each occurrence moves from a tissue sample to a
sequenced genotype, and how we track where it is.

```
Occurrence ──▶ TissueBank ──▶ MolecularBank (DNA) ──▶ Sequencing ──▶ GenotypingStatus (tally)
                                                          └──▶ vSequencingOccurrence (view) ──▶ SRK pipeline
```
→ [`Documentation_DB.md` → **Biobanking**](Documentation/Documentation_DB.md#module-biobanking) ·
[→ **Genetics**](Documentation/Documentation_DB.md#module-genetics) ·
[Database](#database) and [Companion Repositories](#companion-repositories) (below)

### All documents

| Document | What you'll find | Read it to… |
|----------|------------------|-------------|
| [`Documentation/Documentation_DB.md`](Documentation/Documentation_DB.md) | Canonical reference — every module, table and field, with the data-acquisition workflow | Understand the schema and what each field means |
| [`LEPA_SQL_DB_overview.md`](LEPA_SQL_DB_overview.md) | Working-database + image-pipeline overview (LEPA instance) | See the live project at a glance |
| [`Multimedia_pipeline/IMAGE_PIPELINE_GUIDE.md`](Multimedia_pipeline/IMAGE_PIPELINE_GUIDE.md) | How field photos/forms become records (both stages) | Run or understand pipeline ① |
| [`Multimedia_pipeline/DATA_QUALITY.md`](Multimedia_pipeline/DATA_QUALITY.md) | Current data-quality status + tracked GitHub issues | Check what's clean and what's open |
| [`Multimedia_pipeline/REPORT_2026_campaign.md`](Multimedia_pipeline/REPORT_2026_campaign.md) | 2026 field-campaign results | Review the latest season |
| [`Multimedia_pipeline/REPORT_2025_measurement.md`](Multimedia_pipeline/REPORT_2025_measurement.md) · [`REPORT_2026_pipeline_dryrun.md`](Multimedia_pipeline/REPORT_2026_pipeline_dryrun.md) | Image-measurement validation + blind dry-run | See how well the method works |
| [`Multimedia_pipeline/PIPELINE_LOG.md`](Multimedia_pipeline/PIPELINE_LOG.md) | Running log of every applied load | Trace what changed and when |

---

## Author

**Sven Buerki, Ph.D.** (he/him)\
Associate Professor\
Dr. Christopher Davidson Endowed Chair in Botany\
Department of Biological Sciences\
Boise State University\
Boise, Idaho, USA

📧 [svenbuerki@boisestate.edu](mailto:svenbuerki@boisestate.edu)

**Co-authors:** Peggy Martinez, Mathew Geisler, Sam Billingsley, Isaac Carretero, Jim Beck & Ian Robertson\
Department of Biological Sciences, Boise State University

---

## Repository Structure

```
Genetic_Rescue_DB/
├── Genetic_Rescue_SQL.db                # Core SQLite3 database (schema + documentation tables)
├── README.md                            # This file
├── LEPA_SQL_DB_overview.md              # Working LEPA database + image-pipeline overview (companion)
├── Documentation/
│   ├── Documentation_DB.md             # Database documentation (canonical, GitHub-rendered)
│   └── Figures/                        # Workflow diagrams and figures
├── Protocols/
│   ├── 01_Location_fieldwork.docx      # Location/EO data-entry form
│   └── 02_Event_fieldwork.docx         # Event and individual plant data-entry form
└── Multimedia_pipeline/                # field-form + image → database pipeline (2026, collision-proof naming)
    ├── IMAGE_PIPELINE_GUIDE.md         # ▶ how the pipeline works, both stages (start here)
    ├── DATA_QUALITY.md                 # data-quality status + tracked issues
    ├── field_forms_ocr.py             # Stage A: forms → Locations/Events/Occurrences (+ form images)
    ├── 00_sort_by_date.py … 03_phenotype.py, stageB_load.py   # Stage B: plant images → Multimedia + Phenotyping
    ├── REPORT_2026_campaign.md, REPORT_2026_pipeline_dryrun.md, REPORT_2025_measurement.md, ISSUE_filename_collision.md
    └── legacy_2025/                    # archived 2025 pipeline scripts
```

> Field imagery, intermediate CSVs, and the working database are **not** versioned
> (ESA-protected locations) — only the `Multimedia_pipeline/` code and documentation are
> published. See [Data Sensitivity](#data-sensitivity).

| Resource | Description |
|----------|-------------|
| [Documentation_DB.md](Documentation/Documentation_DB.md) | Full database and workflow documentation |
| [LEPA_SQL_DB_overview.md](LEPA_SQL_DB_overview.md) | Working LEPA database + image-pipeline overview (companion to this README) |
| [01_Location_fieldwork.docx](Protocols/01_Location_fieldwork.docx) | Fieldwork data-entry form — Locations |
| [02_Event_fieldwork.docx](Protocols/02_Event_fieldwork.docx) | Fieldwork data-entry form — Events and individual plants |
| [Genetic_Rescue_SQL.db](Genetic_Rescue_SQL.db) | SQLite3 database (schema + `Terms` + `TableModules`) |
| [Multimedia_pipeline/](Multimedia_pipeline/) | Code + docs to link field photos to occurrences and derive plant size from them |

---

## Database

- **Engine:** SQLite 3
- **File:** [`Genetic_Rescue_SQL.db`](Genetic_Rescue_SQL.db)
- **Tables:** 30 — every table is registered in the `TableModules` documentation table — plus 4 SQL views (`vOccurrenceTraits`, `vUnimagedOccurrences`, `vSequencingOccurrence`, `GermplasmIDs_EO27`)
- **Full documentation:** [Documentation_DB.md](Documentation/Documentation_DB.md)

The database is organized into seven modules:

| Module | Purpose |
|--------|---------|
| **Admin** | Staff, project metadata, QC notes, multimedia |
| **Environment** | Spatial hierarchy, taxonomy, EO rankings |
| **Demography** | Population size and habitat condition per event/EO |
| **Biobanking** | Seed accessions and transactions; tissue samples (`TissueBank`) and tissue-weight transactions (`TissueTransactions`); DNA/RNA/protein extractions (`MolecularBank`) |
| **Genetics** | Sequencing metadata and quality metrics (`Sequencing`); per-occurrence genotyping-pipeline status (`GenotypingStatus`) |
| **Breeding** | Hand-pollination records and trial design |
| **Restoration** | Restoration trial outcomes |

**Genotyping pipeline (2026).** The biobanking-to-genetics chain is now populated end-to-end:
`Occurrence → TissueBank → MolecularBank (DNA extraction) → Sequencing (Oxford Nanopore) → GenotypingStatus`.
`GenotypingStatus` tracks where each occurrence sits in the pipeline (DNA extraction → PCR/library prep →
sequencing), the pass/fail of each round, and a derived next step to completion — the operational board for
completing genotyping across the collection.

### Spatial Hierarchy

```
EO (Element Occurrence — federally designated population)
 └── Location (discrete site within an EO)
      └── Event (individual sampling unit, e.g., microhabitat patch)
           └── Occurrence (individual fruiting plant)
                └── Germplasm (seed accession from that plant)
```

---

## Multimedia & Image-Based Phenotyping

Each fruiting plant (`Occurrence`) is photographed in the field with a whiteboard recording
its `occurrenceID` and date, plus two rulers for scale. The **[`Multimedia_pipeline/`](Multimedia_pipeline/)**
turns these photos into structured data — two capabilities from the **same images**:

**1. Occurrence linking (image → database).** The handwritten `occurrenceID` and date are
read from each board and validated against the `Occurrences` table (the number must match an
existing record; the date is cross-checked), then linked rows are written to the `Multimedia`
table with a `remarks` validation note.

**2. Image-based phenotyping (plant morphometrics).** From the same photos, plant **height**
and **crown width** are estimated against the board rulers — including a "1 cm tile"
calibration to measure plants larger than the ruler — and condensed into a robust **size
class** (small / medium / large). Each measurement is stored as its own record in the
dedicated **`Phenotyping`** table (linked to the occurrence and its source image), following
the Darwin Core *MeasurementOrFact* pattern. This yields low-cost phenotypic trait data
across the whole collection.

Board reading and plant-extent estimation use a vision-capable language model, with every
result cross-checked against the database; the workflow is fully scripted and scales from
tens to thousands of images.

From 2026 the pipeline runs in **two stages — field forms first**: **Stage A** OCRs the paper
Location/Event sheets to create the `Locations`, `Events`, and `Occurrences` (with GPS) and files each
form image as evidence; **Stage B** links the plant photos to those occurrences and measures them. It
uses a **collision-proof image-naming scheme** (`LEPA_<date>_<sha8>.jpg`, content-addressed) so camera
files that repeat across seasons can never overwrite one another, with a date-organised folder
convention and a human review gate before any record is created. In the 2026 campaign the on-board
field h/w **validated the image phenotyping to ~±1 cm**.

📖 **Full method and usage:** **[`Multimedia_pipeline/IMAGE_PIPELINE_GUIDE.md`](Multimedia_pipeline/IMAGE_PIPELINE_GUIDE.md)**
 — data-quality status: [`DATA_QUALITY.md`](Multimedia_pipeline/DATA_QUALITY.md); worked examples:
 [`REPORT_2026_campaign.md`](Multimedia_pipeline/REPORT_2026_campaign.md),
 [`REPORT_2026_pipeline_dryrun.md`](Multimedia_pipeline/REPORT_2026_pipeline_dryrun.md),
 [`REPORT_2025_measurement.md`](Multimedia_pipeline/REPORT_2025_measurement.md)

---

## Companion Repositories

This database is the integrative hub of a small ecosystem of repositories. Two companion projects feed specific modules:

| Repository | Feeds module | Role |
|------------|--------------|------|
| **[SRK_bioinformatics](https://github.com/svenbuerki/SRK_bioinformatics)** | **Genetics** | S-locus receptor kinase (**SRK**) genotyping pipeline. Consumes the sequencing outputs tracked in `Sequencing`/`GenotypingStatus` and produces the per-individual SRK genotypes that will populate the planned `Genotyping` table, each linked to an `occurrenceID` — the genetic-diversity basis for informed breeding. |
| **[LEPA_EO_spatial_clustering](https://github.com/svenbuerki/LEPA_EO_spatial_clustering)** | **Environment** | Spatial clustering of Element Occurrences (EOs) to define seed-transfer zones. Informs the `EOs`, `Locations`, and `EORankings` tables and the choice of source populations for translocation. |

Together they implement steps 1 (genetic diversity / seed zones) and 5 (informed breeding) of the genetic-rescue pipeline, with this database as the shared record.

> **How the SRK pipeline and this database intersect.** The two systems align on a single key: the SRK
> pipeline's per-sample identifier (`SampleID` in its `sampling_metadata.csv`) is **identical, 1:1, to
> `Sequencing.libraryName`** in the database. That shared key is the join between the flat sequencing file
> and the relational record. Crucially, occurrence identity — which the SRK CSV records only sparsely — is
> **recovered in one hop through the database**: `Sequencing.molecularID → MolecularBank.occurrenceID`. The
> convenience view **`vSequencingOccurrence`** exposes this directly (`libraryName`/`SampleID`,
> `molecularID`, `occurrenceID`, `tissueID`, `taxonID`, `ingroup`, flow cell, barcode, plate), so the
> pipeline can select an authoritative `occurrenceID` for every sequenced sample without re-joining. This
> lets the revised SRK pipeline **point at the database instead of the CSV and treat `occurrenceID` as the
> single source of truth**, tying each SRK genotype back to a specific plant (`Occurrences`) and, in turn,
> to the planned `Genotyping` table.

---

## Data Sensitivity

For threatened or endangered species listed under national legislation, **precise GPS coordinates must not be made public**. The following fields must be excluded from any public-facing interface:

`locationDecimalLatitude`, `locationDecimalLongitude`, `eventDecimalLatitude`, `eventDecimalLongitude`

---

## Terminology and Standards

| Standard | Scope |
|----------|-------|
| [Darwin Core](https://dwc.tdwg.org/terms/) | Occurrence and location data |
| [Dublin Core](https://www.dublincore.org/specifications/dublin-core/) | Metadata |
| [PlantBreeding / BrAPI v2.1](https://github.com/plantbreeding/BrAPI) | Germplasm and breeding data |
| [BBMRI-ERIC / MIABIS](https://github.com/BBMRI-ERIC/miabis) | Biobank and sample data |

Custom terms are defined in the `Terms` table (70 entries).

---

## Key Publications

- Selby et al. (2019) BrAPI—an application programming interface for plant breeding applications. *Bioinformatics* 35(20):4147–4155. https://doi.org/10.1093/bioinformatics/btz190
- Morales et al. (2022) Breedbase: a digital ecosystem for modern plant breeding. *G3: Genes|Genomes|Genetics* 12(7):jkac078. https://doi.org/10.1093/g3journal/jkac078

---

## License

This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).

You are free to share and adapt this material for non-commercial purposes, provided appropriate credit is given to the original author. See the [`LICENSE`](LICENSE) file for full terms.
