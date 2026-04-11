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

---

## Author

**Sven Buerki, Ph.D.** (he/him)\
Associate Professor\
Dr. Christopher Davidson Endowed Chair in Botany\
Department of Biological Sciences\
Boise State University\
Boise, Idaho, USA

📧 [svenbuerki@boisestate.edu](mailto:svenbuerki@boisestate.edu)

---

## Repository Structure

```
Genetic_Rescue_DB/
├── Genetic_Rescue_SQL.db                # Core SQLite3 database (schema + documentation tables)
├── README.md                            # This file
├── Documentation/
│   ├── Documentation_DB.md             # Database documentation (GitHub-rendered)
│   ├── Documentation_DB.Rmd            # Documentation source (R/bookdown)
│   └── Figures/                        # Workflow diagrams and figures
├── Protocols/
│   ├── 01_Location_fieldwork.docx      # Location/EO data-entry form
│   └── 02_Event_fieldwork.docx         # Event and individual plant data-entry form
```

| Resource | Description |
|----------|-------------|
| [Documentation_DB.md](Documentation/Documentation_DB.md) | Full database and workflow documentation |
| [01_Location_fieldwork.docx](Protocols/01_Location_fieldwork.docx) | Fieldwork data-entry form — Locations |
| [02_Event_fieldwork.docx](Protocols/02_Event_fieldwork.docx) | Fieldwork data-entry form — Events and individual plants |
| [Genetic_Rescue_SQL.db](Genetic_Rescue_SQL.db) | SQLite3 database (schema + `Terms` + `TableModules`) |

---

## Database

- **Engine:** SQLite 3
- **File:** [`Genetic_Rescue_SQL.db`](Genetic_Rescue_SQL.db)
- **Tables:** 22 (plus two documentation tables: `TableModules`, `Terms`)
- **Full documentation:** [Documentation_DB.md](Documentation/Documentation_DB.md)

The database is organized into seven modules:

| Module | Purpose |
|--------|---------|
| **Admin** | Staff, project metadata, QC notes, multimedia |
| **Environment** | Spatial hierarchy, taxonomy, EO rankings |
| **Demography** | Population size and habitat condition per event/EO |
| **Biobanking** | Seed accessions, transactions, tissue and molecular samples |
| **Genetics** | Sequencing metadata and quality metrics |
| **Breeding** | Hand-pollination records and trial design |
| **Restoration** | Restoration trial outcomes |

### Spatial Hierarchy

```
EO (Element Occurrence — federally designated population)
 └── Location (discrete site within an EO)
      └── Event (individual sampling unit, e.g., microhabitat patch)
           └── Occurrence (individual fruiting plant)
                └── Germplasm (seed accession from that plant)
```

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

Custom terms are defined in the `Terms` table (54 entries).

---

## Key Publications

- Selby et al. (2019) BrAPI—an application programming interface for plant breeding applications. *Bioinformatics* 35(20):4147–4155. https://doi.org/10.1093/bioinformatics/btz190
- Morales et al. (2022) Breedbase: a digital ecosystem for modern plant breeding. *G3: Genes|Genomes|Genetics* 12(7):jkac078. https://doi.org/10.1093/g3journal/jkac078

---

## License

This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).

You are free to share and adapt this material for non-commercial purposes, provided appropriate credit is given to the original author. See the [`LICENSE`](LICENSE) file for full terms.
