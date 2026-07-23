# LEPA 2026 — field season processing (campaign report)

**Prepared for:** Buerki Lab team
**Subject:** Digitizing the 2026 field sheets, plant photos, and genotyping data into `LEPA_SQL.db`
**Pipeline:** two stages — **A: forms → records**, then **B: plant images → multimedia + phenotyping**
(full method: [`IMAGE_PIPELINE_GUIDE.md`](IMAGE_PIPELINE_GUIDE.md); live data-quality status: [`DATA_QUALITY.md`](DATA_QUALITY.md))

*Last refreshed: 2026-07-21 (through the FINAL July-21 load — EO30 Simco Rd loc 51/52 + a new 2026 population loc 53, 30 plants. The 2026 collection season is COMPLETE: 20 field days, 1,581 occurrences, 19 EOs, 13 new locations. §8 has Ian's full 2026 site-visit checklist with occurrence yields folded in.)*

---

## 1. The 2026 field season so far (DB deltas)

| | 2026 total | Notes |
|---|---|---|
| **Occurrences** (field-collected) | **1,581** | across 19 EOs (below) |
| **Events** (slick spots) | **486** | each with GPS + habitat/condition + associated taxa (incl. a few data-only, seedless slick spots at EO61 and EO30-3) |
| **Locations** | revisits + 13 new: EO69 (41), EO30-2 (42), EO27-5 (43), EO27 (44), EO27-1 (45, 46), EO8 (47), EO26 (48, 49), EO27 (50), EO30-3 (51), EO30-4 (52), new 2026 population (53) | thirteen genuinely new sites this season; the rest are revisits (link, no insert). |
| **Plant images** phenotyped | **1,571 / 1,581 (99%)** | each has a linked board image; measured height/crown/size class |

The **1,581 occurrences span 19 EOs**; the full per-EO yield, together with every site the crew visited or skipped and its location number, is in the single season-coverage roster in **§8** (Ian's 2026 checklist, with the occurrence counts folded in). The season's largest EO was **EO27** (Red Tie South, EO27-5, Figgins, Pleasant Valley, Region 3 loc 37/50, and new sites); the eastern **EO8** (Hammett Hills) was next. The 19th EO is a **new 2026 population (loc 53)** with no official EO number yet — databased under a provisional code (`EO_NEW2026`).

The 2026 story from the field (Ian Robertson's reports): the **New Plymouth EOs** (70/68/69, late June), **EO118** near Firebird Raceway, then the large **EO18 complex** (EO18-7 severely cheatgrass/harvester-ant degraded; EO18-8 productive), **EO25** (Melba Butte, EO25-B badly cheatgrass-invaded) and **EO24** (Kuna Butte, very low) in early July, **EO32** ("10 Mile Creek", July 3 — 137 plants across 36 slick spots), and then a sustained week-long push through the **EO27 complex** (Red Tie, EO27-5, Figgins, Pleasant Valley and a new site) that made EO27 the season's largest EO at 418 plants (Red Tie South, EO27-5, Figgins, Pleasant Valley, plus new locations 44/45/46), finishing 2026-07-10 with a Range-Fire-burned wrap-up (loc 45/46) and a brief EO67 revisit. The crew then moved to the **eastern populations**, starting 2026-07-13 with a big single-day haul at **EO8 (Hammett Hills, loc 28 — 123 plants across 54 slick spots)**, continuing 2026-07-14 by completing **loc 28 and loc 27** (55 more plants) and opening a **new location 47**, and finishing **EO8** on 2026-07-15 by completing loc 47 (94 plants total, spanning both days) before moving to **EO26 (Glenns Ferry)** — loc 30 was visited but its plants had all dropped seed (nothing to sample), while loc 31 and loc 32 yielded 44 plants. loc 29 (07-14) was likewise visited-but-not-sampled. **EO26 was completed 2026-07-16** (loc 33/34 + new loc 48/49, 54 plants). The crew then worked **EO27 "Region 3" on 2026-07-17** (new loc 50 + loc 37, 55 plants — no field email that day), and closed out at **Mountain Home on 2026-07-20**: **EO61 (loc 38)** and **EO29 (loc 8)** where the plants were far gone (34 plants; at EO61 several occupied slick spots were documented with full data but no collectable seed, for effective-population-size analysis). The season **ended 2026-07-21 in the Simco Rd area (EO30)**: two new sub-EO sites, **EO30-3 (loc 51)** and **EO30-4 (loc 52)**, plus a **brand-new population (loc 53)** found on a BLM tip (nearest EO112 held no Lepa in 2026 or 2013) — 30 plants (occ 3843–3872) across three new locations, closing the 2026 collection at **20 field days**. Recurring theme all season: cheatgrass inundation of slick spots — and, at the OCTC, the 2025 Range Fire.

### Per-location tally — 2026 events & occurrences, by EO

Every location with 2026 records, ordered by EO, with its event and occurrence counts (from the database; a data-only slick spot with no seed collected still counts as an event). Subtotals shown for EOs spanning more than one location.

| EO | Location | Events | Occurrences |
|---|---|---:|---:|
| **EO8** | loc 27 (EO8) | 9 | 15 |
|  | loc 28 (EO8) | 73 | 163 |
|  | loc 47 (EO8) | 27 | 94 |
| | *EO8 subtotal — 3 locations* | **109** | **272** |
| **EO18** | loc 16 (EO18-7) | 25 | 76 |
|  | loc 17 (EO18-7) | 32 | 103 |
|  | loc 18 (EO18-8) | 18 | 59 |
|  | loc 19 (EO18-7) | 1 | 1 |
| | *EO18 subtotal — 4 locations* | **76** | **239** |
| **EO24** | loc 23 (EO24-2) | 1 | 1 |
|  | loc 24 (EO24) | 2 | 5 |
| | *EO24 subtotal — 2 locations* | **3** | **6** |
| **EO25** | loc 20 (EO25-A) | 20 | 98 |
|  | loc 21 (EO25-B) | 3 | 8 |
| | *EO25 subtotal — 2 locations* | **23** | **106** |
| **EO26** | loc 31 (EO26-3) | 4 | 7 |
|  | loc 32 (EO26-3) | 9 | 37 |
|  | loc 33 (EO26-3) | 5 | 11 |
|  | loc 34 (EO26-3) | 7 | 18 |
|  | loc 48 (EO26) | 10 | 18 |
|  | loc 49 (EO26) | 4 | 7 |
| | *EO26 subtotal — 6 locations* | **39** | **98** |
| **EO27** | loc 9 (EO27) | 24 | 79 |
|  | loc 10 (EO27-3) | 2 | 7 |
|  | loc 11 (EO27-1) | 32 | 125 |
|  | loc 12 (EO27RT) | 34 | 126 |
|  | loc 37 (EO27-1) | 17 | 38 |
|  | loc 43 (EO27-5) | 9 | 33 |
|  | loc 44 (EO27) | 6 | 17 |
|  | loc 45 (EO27-1) | 7 | 21 |
|  | loc 46 (EO27-1) | 2 | 10 |
|  | loc 50 (EO27) | 4 | 17 |
| | *EO27 subtotal — 10 locations* | **137** | **473** |
| **EO29** | loc 8 (EO29) | 1 | 9 |
| **EO30** | loc 13 (EO30-1) | 2 | 16 |
|  | loc 42 (EO30-2) | 9 | 34 |
|  | loc 51 (EO30-3) | 6 | 16 |
|  | loc 52 (EO30-4) | 2 | 7 |
| | *EO30 subtotal — 4 locations* | **19** | **73** |
| **EO32** | loc 6 (EO32) | 36 | 137 |
| **EO38** | loc 1 (EO38) | 15 | 37 |
| **EO52** | loc 3 (EO52) | 1 | 1 |
| **EO61** | loc 38 (EO61) | 8 | 25 |
| **EO67** | loc 39 (EO67) | 2 | 6 |
| **EO68** | loc 5 (EO68-3) | 2 | 10 |
| **EO69** | loc 41 (EO69) | 1 | 7 |
| **EO70** | loc 26 (EO70) | 6 | 42 |
| **EO76** | loc 2 (EO76) | 2 | 8 |
| **EO118** | loc 4 (EO118) | 5 | 25 |
| **EO_NEW2026** | loc 53 (EO_NEW2026) | 1 | 7 |
| | **TOTAL — 43 locations across 19 EOs** | **486** | **1581** |

*Locations visited in 2026 but with no collection (0 events, 0 occurrences — not in the table above): loc 15 (EO18-7, no plants found), loc 29 (EO8), loc 30 (EO26-1), loc 36 (EO26-4, 2 plants too far gone). loc 35 (EO26-2) was not visited. **Note:** Ian's site-visit checklist (§8) marks **loc 15 and loc 30 as seeds-collected (✓)**, but both have **zero 2026 records** in the database — consistent with his own field emails (loc 15, June 29: "found no plants to sample"; loc 30, July 15: seeds already dropped). Worth confirming with Ian which is correct before the checklist is treated as final.*

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
- **#18** — EO27 loc 50: three event latitudes provisional (field-recording errors) — verify vs manilla.
- **#19** — July-21 EO30-3 (loc 51): one seedless slick-spot event (718) missing its page-1 form image — page-1 to be located/retaken so it can be entered as a data-only event.
- *Resolved this season:* #7, #8 (EO38/EO118 forms located), #12 (genotyping status gaps), #14 (occ 2714 envelope reuse).

## 7. Data products

- `LEPA_SQL.db` — **Locations 52, Events 723, Occurrences 3,797, Multimedia 3,403, Phenotyping 2,312** (incl. all prior-year data + the full 2026 season + the genotyping integration).
- `staging_2026/` — reviewed staging + the 3 override files + `stageB_*` staging.
- Scripts: `field_forms_ocr.py` (Stage A), `stageB_load.py` (Stage B linking — the forms-first loader), `verify_event_barcodes.py` (event barcode ground-truthing), `01_ingest_register.py` (image ingest).

## 8. 2026 season coverage & collections (Ian Robertson's checklist)

The single authoritative roster for the season — reproduced from Ian's *2026 Checklist of Seed Collections* and merged with the DB occurrence yield (this replaces the separate per-EO count table; the information appears once, here). Every EO / location the crew considered in 2026, with its outcome, location number, and — for sampled EOs — the occurrences collected. A blank **EO # (Name)** cell means the row is another location of the EO named in the row above. **Map** = a region map thumbnail accompanies that row in the source document (multi-region EOs).

**Legend:** ✓ = seeds collected · Ø = visited, but no plants found · **DNV** = did not visit. **occ** = occurrences collected, given as the whole-EO total on that EO's first sampled row (blank on its other rows and on Ø/DNV rows); `—` = none.

**Totals:** **45** locations with seeds collected · **11** visited-but-no-plants (Ø) · **15** did-not-visit (DNV). Occurrence total = **1,581** across 19 EOs (season complete through 2026-07-21).

| Status | EO # (Name) | Location | occ | Map |
|---|---|---|---|---|
| ✓ | 68 (S of New Plymouth) | 0005 | 10 | |
| ✓ | 69 (S of New Plymouth) | 0041 | 7 | |
| ✓ | 70 (W of Graveyard Gulch) | 0026 | 42 | |
| ✓ | 118 (Firebird Raceway) | 0004 | 25 | |
| ✓ | 76 (Hartley Rd) | 0002 | 8 | |
| ✓ | 52 (Woods Gulch) | 0003 | 1 | |
| ✓ | 38 (Eagle Bike Park) | 0001 | 37 | |
| ✓ | 32 (Ten Mile Creek) | 0006 | 137 | map |
| DNV | 48 (East Kuna Rd) | 0007 | — | |
| Ø | 24-1 (Kuna Butte) | 0022 | | map |
| ✓ | 24-2 (Kuna Butte) | 0023 | 6 | map |
| ✓ | 24- (Kuna Butte: no subEO) | 0024 | | map |
| Ø | 24-7 (Kuna Butte) | 0025 | | map |
| DNV | 24-12 (Kuna Butte) | | — | map |
| ✓ | 25 (Melba Butte) | 0020 | 106 | |
| ✓ | | 0021 | | |
| DNV | 18-2 | | — | map |
| Ø | 18-4 (Past Initial Point) | | | map |
| Ø | 18-5 | | | map |
| Ø | 18-6 (Swan Falls Rd) | | | map |
| ✓ | 18-7 (Kuna Butte SW) | 0019 | 239 | map |
| ✓ | | 0015 | | map |
| ✓ | | 0017 | | map |
| ✓ | | 0016 | | map |
| ✓ | 18-8 (W of EO18-7) | 0018 | | map |
| DNV | 18-9 | | — | map |
| DNV | 18-12 | | — | map |
| ✓ | 27-1 (Red Tie area OCTC) | 0012 | 473 | map |
| ✓ | | 0011 | | map |
| ✓ | | 0037 | | map |
| ✓ | | 0045 | | map |
| ✓ | | 0046 | | map |
| ✓ | | 0050 | | map |
| ✓ | 27-? (between Figgins and PV) | 0044 | | map |
| ✓ | 27-2 (Figgins OCTC) | 0009 | | map |
| ✓ | 27-3 (Pleasant Valley OCTC) | 0010 | | map |
| ✓ | 27-5 | 0043 | | map |
| ✓ | 67 (Powerline OCTC) | 0039 | 6 | map |
| Ø | 77 (Sand Creek) | | | |
| DNV | 104 (S of Leone) | | — | |
| DNV | 72-1 (SW of Leone) | | — | |
| DNV | 72-2 (SW of Leone) | | — | |
| DNV | 72-3 (SW of Leone) | 0040 | — | |
| Ø | 15 (Simco Rd) | | | |
| ✓ | 30-1 (Soles Rest Creek) | 0013 | 73 | map |
| ✓ | 30-2 | 0042 | | map |
| ✓ | 30-3 | 0051 | | map |
| ✓ | 30-4 | 0052 | | map |
| Ø | 112 | | | map |
| ✓ | New 2026 (no EO → prov. EO_NEW2026) | 0053 | 7 | map |
| DNV | 31 (Bown's Creek) | | — | |
| DNV | 20 (Soles Rest Creek) | | — | |
| DNV | 51-5 (Hot Creek) | | — | |
| ✓ | 29 (Mountain Home SE) | 0008 | 9 | |
| DNV | 120 (N of Transfer Station) | | — | |
| DNV | 121 (Gailey Reservoir) | | — | |
| ✓ | 61 (SE of Reverse) | 0038 | 25 | |
| Ø | 116 (I-84/Bennett Rd) | | | |
| ✓ | 8 (Hammett Hills) | 0027 | 272 | map |
| ✓ | | 0028 | | |
| Ø | | 0029 | | |
| ✓ | | 0047 | | |
| ✓ | 26-1 (Alkali Creek) | 0030 | 98 | |
| DNV | 26-2 (Alkali Creek) | 0035 | — | |
| ✓ | 26-3 (Alkali Creek) | 0031 | | map |
| ✓ | | 0032 | | map |
| ✓ | | 0033 | | map |
| ✓ | | 0034 | | map |
| ✓ | | 0048 | | map |
| ✓ | | 0049 | | map |
| Ø | 26-4 (Alkali Creek) | 0036 | | map |

**Reconciliation notes (checklist vs. the loaded DB):**
- The checklist groups **location 50 under EO27-1 (Red Tie area OCTC)**, whereas the July-17 load labelled loc 50 as EO27 "Region 3" (reconstructed with no field email). Ian's roster is the authoritative sub-EO assignment — relevant when finalizing GitHub **#18** (loc 50 provisional latitudes).
- **Location 44** is resolved by the checklist as **EO27-? "between Figgins and Pleasant Valley"** (previously flagged as within EO27 but outside any official sub-EO boundary).
- **EO48 (loc 7)** and **EO26-2 (loc 35)** are confirmed **DNV** (time-skipped, both low-prospect) — matching Ian's July-21 email.
- **EO30-3 (loc 51)**, **EO30-4 (loc 52)**, and the **New-2026 BLM-found population (loc 53)** are the July-21 final-day additions (30 plants, occ 3843–3872), now loaded; **EO112 was visited but held no Lepa** (Ø).
- **loc 53 has no official EO** (Ian marked "No EO"; nearest EO112 held no Lepa in 2026 or 2013). It is databased under a **provisional EO, EOID 21 / `EO_NEW2026`** so its 7 plants (occ 3866–3872) are fully attributed — rename the EOCode when IDFG assigns an official number.
- **One seedless slick spot on 2026-07-21 (loc 51, event 718)** was initially unrecordable (only its page 2 had been imaged). Peggy provided the missing page 1 (2026-07-22), and it is now loaded as a **data-only event** — 62 fruiting individuals, 25 rosettes, condition 2.5, 0 seed collections (the EO61-style effective-population-size case). GitHub **#19 resolved**.
