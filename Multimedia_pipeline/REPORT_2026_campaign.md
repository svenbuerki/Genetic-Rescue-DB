# LEPA 2026 — field season processing (campaign report)

**Prepared for:** Buerki Lab team
**Subject:** Digitizing the 2026 field sheets, plant photos, and genotyping data into `LEPA_SQL.db`
**Pipeline:** two stages — **A: forms → records**, then **B: plant images → multimedia + phenotyping**
(full method: [`IMAGE_PIPELINE_GUIDE.md`](IMAGE_PIPELINE_GUIDE.md); live data-quality status: [`DATA_QUALITY.md`](DATA_QUALITY.md))

*Last refreshed: 2026-07-16 (through the July 13 EO8 Hammett Hills loc 28 load — eastern populations begun).*

---

## 1. The 2026 field season so far (DB deltas)

| | 2026 total | Notes |
|---|---|---|
| **Occurrences** (field-collected) | **1,215** | across 15 EOs (below) |
| **Events** (slick spots) | **353** | each with GPS + habitat/condition + associated taxa |
| **Locations** | revisits + **EO69** (41) + **EO30-2** (42) + **EO27-5** (43) + **EO27** (44) + **EO27-1** (45, 46) | six genuinely new sites this season; the rest are revisits (link, no insert) |
| **Plant images** phenotyped | **1,205 / 1,215 (99%)** | each has a linked board image; measured height/crown/size class |

**By Element Occurrence:**

| EO | occ | EO | occ |
|---|---|---|---|
| **EO27** (Red Tie South 11/12/45/46, 27-5, Figgins, PV, new site) | 418 | EO38 | 37 |
| **EO18** (7 & 8) | 239 | EO118 | 25 |
| **EO32** (10 Mile Creek) | 137 | EO68 | 10 |
| **EO8** (Hammett Hills, loc 28 — eastern) | 123 | EO76 | 8 |
| **EO25** (A & B) | 106 | EO69 | 7 |
| **EO30** (Simco Rd, 1 & 2) | 50 | EO67 | 6 |
| EO70 | 42 | EO24 | 6 |
| | | EO52 | 1 |

The 2026 story from the field (Ian Robertson's reports): the **New Plymouth EOs** (70/68/69, late June), **EO118** near Firebird Raceway, then the large **EO18 complex** (EO18-7 severely cheatgrass/harvester-ant degraded; EO18-8 productive), **EO25** (Melba Butte, EO25-B badly cheatgrass-invaded) and **EO24** (Kuna Butte, very low) in early July, **EO32** ("10 Mile Creek", July 3 — 137 plants across 36 slick spots), and then a sustained week-long push through the **EO27 complex** (Red Tie, EO27-5, Figgins, Pleasant Valley and a new site) that made EO27 the season's largest EO at 418 plants (Red Tie South, EO27-5, Figgins, Pleasant Valley, plus new locations 44/45/46), finishing 2026-07-10 with a Range-Fire-burned wrap-up (loc 45/46) and a brief EO67 revisit. The crew then moved to the **eastern populations**, starting 2026-07-13 with a big single-day haul at **EO8 (Hammett Hills, loc 28 — 123 plants across 54 slick spots)**. Recurring theme: cheatgrass inundation of slick spots — and, at the OCTC, the 2025 Range Fire.

## 2. Stage A — field forms → Locations / Events / Occurrences

Paper Location + Event forms (2 pages each) are OCR'd by a **read-only agent sweep** (subscription, no API cost), pages classified by their printed header, and the hierarchy rebuilt from barcodes + capture order. **Event IDs are ground-truthed by decoding the CODE128 sticker barcode** (`verify_event_barcodes.py`) — the printed/handwritten event numbers are frequently wrong, so the decoded barcode is authoritative (this caught mis-entries all season). Table-only columns auto-fill; human fixes go through three persistent override files (occurrence ranges, reused event stickers, new-site GPS). Form photos are filed into `Multimedia` as evidence (`type='field form'`).

**`associatedTaxa`** is auto-homogenized to `Taxonomy.taxonID` lists (verbatim kept in `associatedTaxaOriginal`); the season added several taxa to the lexicon (Descurainia, Physaria, and spelling variants).

## 3. Stage B — plant images → multimedia + phenotyping

Board photos are ingested under collision-proof content-addressed names (`LEPA_<date>_<sha8>.jpg`; camera `JCN_####` names reset yearly and are **not** a stable key). A read-only sweep reads each board (OC# = occurrenceID) + measures the plant against the board's own ruler, cross-checking the written date to catch stray images from other field days. `stageB_load.py` links each image to its **existing** Stage-A occurrence (`tableID 13`) and inserts Phenotyping.

### 3a. h/w validation (the headline result)

Where boards carry **field-written height/width**, the **image-measured** value matches the **field tape** to a **median of ≈±1 cm** (the large majority within ±2 cm) for both height and width — a true ground-truth check, not self-consistency. Conclusion: the low-cost photo phenotyping reproduces the tape; keep using it, with **size class as the primary metric and cm as supporting**. (Boards with no clear image scale are scored straight from the field-written h/w — `measurementMethod = field tape`.)

## 4. Genotyping data integrated (2026-07-02)

The biobanking→genetics chain was loaded and validated against Peggy's master sheet:
**Occurrence → TissueBank (1,699) → MolecularBank (662 DNA extractions) → Sequencing (505 Nanopore libraries) → GenotypingStatus (885)**. `GenotypingStatus` tracks where each occurrence sits in the pipeline (DNA extraction → PCR → sequencing) with a derived next step; the `vSequencingOccurrence` view is the join point for the SRK genotyping pipeline (`SampleID` = `Sequencing.libraryName`). See `DATA_QUALITY.md` and the database documentation for detail.

## 5. Reused-ID handling

The recurring 2026 theme — IDs reused across years and across field days — kept appearing and was caught by the gated loads: event stickers reassigned to free IDs; the EO69 barcode as a genuinely new location; and **reused field envelopes** (e.g. occ 2714 written on two event forms → resolved to event 363 from the board evidence; occ **2897** written on an EO32 plant but already a wild EO69 plant → reassigned to fresh 2909). A companion failure mode surfaced at EO32: **OCR digit-errors on the plant numbers** (a looped hand-written 9 read as 4: 2404→2904, 2744→2794) — caught by reading the physical forms and cross-checking the plant boards, which carry the same number. Every ID is collision-checked against the DB before insert.

**Which source wins?** Neither, categorically. On July 6 the Red Tie *forms* were unreadable and the *boards* settled the occurrence↔event mapping; on July 8 a *board* was mis-written (JCN_1052 hand-labelled `3142`, a duplicate) and the *form* settled it as 3143. The rule the season has converged on: **cross-check forms against boards on every load, and treat the physical envelope number as the tie-breaker** — which is exactly what Ian confirmed for the July-8 case. Two independent, error-prone records of the same number are what make the errors visible at all.

## 6. Open items (tracked on GitHub — svenbuerki/Genetic-Rescue-DB)

- **#6** — a handful of collected occurrences without a plant image (un-photographed / board# mis-read).
- **#10** — 57 tissue samples missing a weight (lab to supply or confirm blank).
- **#11** — 6 tissue-sample cell errors in the master sheet (lab to correct online).
- **#13** — 5 impossible negative tissue weights + missing who/when/experiment metadata.
- *Resolved this season:* #7, #8 (EO38/EO118 forms located), #12 (genotyping status gaps), #14 (occ 2714 envelope reuse).

## 7. Data products

- `LEPA_SQL.db` — **Locations 45, Events 590, Occurrences 3,431, Multimedia 2,757, Phenotyping 1,946** (incl. all prior-year data + the 2026 season + the genotyping integration).
- `staging_2026/` — reviewed staging + the 3 override files + `stageB_*` staging.
- Scripts: `field_forms_ocr.py` (Stage A), `stageB_load.py` (Stage B linking — the forms-first loader), `verify_event_barcodes.py` (event barcode ground-truthing), `01_ingest_register.py` (image ingest).
