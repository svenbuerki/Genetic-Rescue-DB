# LEPA 2026 — field season processing (campaign report)

**Prepared for:** Buerki Lab team
**Subject:** Digitizing the 2026 field sheets, plant photos, and genotyping data into `LEPA_SQL.db`
**Pipeline:** three stages — **A: forms → records**, **B: plant images → multimedia + phenotyping**, then **C: seed sheets → seed accessions (`Germplasm`)**
(full method: [`IMAGE_PIPELINE_GUIDE.md`](IMAGE_PIPELINE_GUIDE.md); live data-quality status: [`DATA_QUALITY.md`](DATA_QUALITY.md))

**Companion project — SRK genotyping & mate limitation:** [`svenbuerki/SRK_bioinformatics`](https://github.com/svenbuerki/SRK_bioinformatics) analyses the self-incompatibility (SRK) genotypes of the plants recorded here. Its **Phase 5** uses this database's occurrences and seed accessions to test **fragmentation → genetic drift → mate limitation**. Start with the [Phase 5 summary for colleagues](https://github.com/svenbuerki/SRK_bioinformatics/blob/main/Phase5_SRK_summary_for_colleagues.md); full method in [Phase 5 — sampling and prediction](https://github.com/svenbuerki/SRK_bioinformatics/blob/main/Phase5_SRK_sampling_and_prediction.md). The seed-cleaning priorities in §1 are linked to that design.

*Last refreshed: 2026-10-04 — **seed processing (Stage C) added**: 410 of the 1,581 plants now have a seed accession; the cleaned-vs-remaining tally and the Phase 5 (SRK) cleaning priorities are below. Field-season figures unchanged since 2026-07-21 (through the FINAL July-21 load — EO30 Simco Rd loc 51/52 + a new 2026 population loc 53, 30 plants. The 2026 collection season is COMPLETE: 20 field days, 1,581 occurrences, 19 EOs, 13 new locations. §8 has Ian's full 2026 site-visit checklist with occurrence yields folded in.)*

---

## 1. The 2026 field season so far (DB deltas)

| | 2026 total | Notes |
|---|---|---|
| **Occurrences** (field-collected) | **1,581** | across 19 EOs (below) |
| **Events** (slick spots) | **486** | each with GPS + habitat/condition + associated taxa (incl. a few data-only, seedless slick spots at EO61 and EO30-3) |
| **Locations** | revisits + 13 new: EO69 (41), EO30-2 (42), EO27-5 (43), EO27 (44), EO27-1 (45, 46), EO8 (47), EO26 (48, 49), EO27 (50), EO30-3 (51), EO30-4 (52), new 2026 population (53) | thirteen genuinely new sites this season; the rest are revisits (link, no insert). |
| **Plant images** phenotyped | **1,571 / 1,581 (99%)** | each has a linked board image; measured height/crown/size class |
| **Seed accessions** (`Germplasm`) | **410 / 1,581 (26%)** | seeds cleaned, weighed and given a germplasmID; 73.0 g ≈ 171,000 seeds. 15 of 43 locations imaged so far (11 complete). Tally and priorities: below. |

The **1,581 occurrences span 19 EOs**; the full per-EO yield, together with every site the crew visited or skipped and its location number, is in the single season-coverage roster in **§8** (Ian's 2026 checklist, with the occurrence counts folded in). The season's largest EO was **EO27** (Red Tie South, EO27-5, Figgins, Pleasant Valley, Region 3 loc 37/50, and new sites); the eastern **EO8** (Hammett Hills) was next. The 19th EO is a **new 2026 population (loc 53)** with no official EO number yet — databased under a provisional code (`EO_NEW2026`).

The 2026 story from the field (Ian Robertson's reports): the **New Plymouth EOs** (70/68/69, late June), **EO118** near Firebird Raceway, then the large **EO18 complex** (EO18-7 severely cheatgrass/harvester-ant degraded; EO18-8 productive), **EO25** (Melba Butte, EO25-B badly cheatgrass-invaded) and **EO24** (Kuna Butte, very low) in early July, **EO32** ("10 Mile Creek", July 3 — 137 plants across 36 slick spots), and then a sustained week-long push through the **EO27 complex** (Red Tie, EO27-5, Figgins, Pleasant Valley and a new site) that made EO27 the season's largest EO at 418 plants (Red Tie South, EO27-5, Figgins, Pleasant Valley, plus new locations 44/45/46), finishing 2026-07-10 with a Range-Fire-burned wrap-up (loc 45/46) and a brief EO67 revisit. The crew then moved to the **eastern populations**, starting 2026-07-13 with a big single-day haul at **EO8 (Hammett Hills, loc 28 — 123 plants across 54 slick spots)**, continuing 2026-07-14 by completing **loc 28 and loc 27** (55 more plants) and opening a **new location 47**, and finishing **EO8** on 2026-07-15 by completing loc 47 (94 plants total, spanning both days) before moving to **EO26 (Glenns Ferry)** — loc 30 was visited but its plants had all dropped seed (nothing to sample), while loc 31 and loc 32 yielded 44 plants. loc 29 (07-14) was likewise visited-but-not-sampled. **EO26 was completed 2026-07-16** (loc 33/34 + new loc 48/49, 54 plants). The crew then worked **EO27 "Region 3" on 2026-07-17** (new loc 50 + loc 37, 55 plants — no field email that day), and closed out at **Mountain Home on 2026-07-20**: **EO61 (loc 38)** and **EO29 (loc 8)** where the plants were far gone (34 plants; at EO61 several occupied slick spots were documented with full data but no collectable seed, for effective-population-size analysis). The season **ended 2026-07-21 in the Simco Rd area (EO30)**: two new sub-EO sites, **EO30-3 (loc 51)** and **EO30-4 (loc 52)**, plus a **brand-new population (loc 53)** found on a BLM tip (nearest EO112 held no Lepa in 2026 or 2013) — 30 plants (occ 3843–3872) across three new locations, closing the 2026 collection at **20 field days**. Recurring theme all season: cheatgrass inundation of slick spots — and, at the OCTC, the 2025 Range Fire.

### Per-location tally — 2026 events & occurrences, by EO

Every location with 2026 records, ordered by EO, with its event, fertile-plant and occurrence counts, seed-processing completion and cleaning priority (from the database; a data-only slick spot with no seed collected still counts as an event). Subtotals shown for EOs spanning more than one location.

| EO | Location | Events | Fertile plants (counted) | Occurrences (sampled) | % sampled | Seed accessions | Completion | Priority |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **EO8** | loc 27 (EO8) | 9 | 39 | 15 | 38% | 15 | 100% | done |
|  | loc 28 (EO8) | 73 | 681 | 163 | 24% | 122 | 75% | **4** (finish) |
|  | loc 47 (EO8) | 27 | 1,494 | 94 | 6% | — | 0% | **1** |
| | *EO8 subtotal — 3 locations* | **109** | **2,214** | **272** | **12%** | **137** | **50%** | |
| **EO18** | loc 16 (EO18-7) | 25 | 365 | 76 | 21% | — | 0% | **8** |
|  | loc 17 (EO18-7) | 32 | 409 | 103 | 25% | — | 0% | **7** (cleaned — not yet imaged) |
|  | loc 18 (EO18-8) | 18 | 264 | 59 | 22% | 57 | 97% | **11** (finish) |
|  | loc 19 (EO18-7) | 1 | 2 | 1 | 50% | 1 | 100% | done |
| | *EO18 subtotal — 4 locations* | **76** | **1,040** | **239** | **23%** | **58** | **24%** | |
| **EO24** | loc 23 (EO24-2) | 1 | 2 | 1 | 50% | — | 0% | **30** |
|  | loc 24 (EO24) | 2 | 27 | 5 | 19% | 5 | 100% | done |
| | *EO24 subtotal — 2 locations* | **3** | **29** | **6** | **21%** | **5** | **83%** | |
| **EO25** | loc 20 (EO25-A) | 20 | ≥ 887 | 98 | ≤ 11% | — | 0% | **3** |
|  | loc 21 (EO25-B) | 3 | 16 | 8 | 50% | 8 | 100% | done |
| | *EO25 subtotal — 2 locations* | **23** | **≥ 903** | **106** | **≤ 12%** | **8** | **8%** | |
| **EO26** | loc 31 (EO26-3) | 4 | 12 | 7 | 58% | — | 0% | **29** |
|  | loc 32 (EO26-3) | 9 | 258 | 37 | 14% | — | 0% | **12** |
|  | loc 33 (EO26-3) | 5 | 14 | 11 | 79% | — | 0% | **28** |
|  | loc 34 (EO26-3) | 7 | 82 | 18 | 22% | — | 0% | **18** |
|  | loc 48 (EO26) | 10 | 35 | 18 | 51% | — | 0% | **23** |
|  | loc 49 (EO26) | 4 | 19 | 7 | 37% | — | 0% | **26** |
| | *EO26 subtotal — 6 locations* | **39** | **420** | **98** | **23%** | **0** | **0%** | |
| **EO27** | loc 9 (EO27) | 24 | 301 | 79 | 26% | — | 0% | **10** |
|  | loc 10 (EO27-3) | 2 | 44 | 7 | 16% | 7 | 100% | done |
|  | loc 11 (EO27-1) | 32 | 784* | 125 | 16%* | 113 | 90% | envelopes missing (#22) |
|  | loc 12 (EO27RT) | 34 | 455* | 126 | 28%* | — | 0% | **6** |
|  | loc 37 (EO27-1) | 17 | 191 | 38 | 20% | — | 0% | **14** |
|  | loc 43 (EO27-5) | 9 | 173 | 33 | 19% | — | 0% | **15** |
|  | loc 44 (EO27) | 6 | 85 | 17 | 20% | — | 0% | **17** |
|  | loc 45 (EO27-1) | 7 | 44 | 21 | 48% | — | 0% | **21** |
|  | loc 46 (EO27-1) | 2 | 53 | 10 | 19% | — | 0% | **19** |
|  | loc 50 (EO27) | 4 | 42 | 17 | 40% | — | 0% | **22** |
| | *EO27 subtotal — 10 locations* | **137** | **2,172*** | **473** | **22%*** | **120** | **25%** | |
| **EO29** | loc 8 (EO29) | 1 | 167 | 9 | 5% | — | 0% | **16** |
| **EO30** | loc 13 (EO30-1) | 2 | 154 | 16 | 10% | 16 | 100% | done |
|  | loc 42 (EO30-2) | 9 | 138 | 34 | 25% | 34 | 100% | done |
|  | loc 51 (EO30-3) | 6 | 152 | 16 | 11% | 11 | 69% | envelopes missing (#22) |
|  | loc 52 (EO30-4) | 2 | 27 | 7 | 26% | 7 | 100% | done |
| | *EO30 subtotal — 4 locations* | **19** | **471** | **73** | **15%** | **68** | **93%** | |
| **EO32** | loc 6 (EO32) | 36 | 1,285 | 137 | 11% | — | 0% | **2** |
| **EO38** | loc 1 (EO38) | 15 | 254 | 37 | 15% | — | 0% | **13** |
| **EO52** | loc 3 (EO52) | 1 | 3 | 1 | 33% | 1 | 100% | done |
| **EO61** | loc 38 (EO61) | 8 | 523 | 25 | 5% | — | 0% | **5** |
| **EO67** | loc 39 (EO67) | 2 | 12 | 6 | 50% | 6 | 100% | done |
| **EO68** | loc 5 (EO68-3) | 2 | 23 | 10 | 43% | — | 0% | **25** |
| **EO69** | loc 41 (EO69) | 1 | 26 | 7 | 27% | — | 0% | **24** |
| **EO70** | loc 26 (EO70) | 6 | 334 | 42 | 13% | — | 0% | **9** |
| **EO76** | loc 2 (EO76) | 2 | 16 | 8 | 50% | — | 0% | **27** |
| **EO118** | loc 4 (EO118) | 5 | 50 | 25 | 50% | — | 0% | **20** |
| **EO_NEW2026** | loc 53 (EO_NEW2026) | 1 | 27 | 7 | 26% | 7 | 100% | done |
| | **TOTAL — 43 locations across 19 EOs** | **486** | **≥ 9,969*** | **1581** | **≤ 16%*** | **410** | **26%** | |

*Completion* = seed accessions ÷ occurrences: the share of sampled plants whose seeds are cleaned, weighed and loaded with a germplasmID (Stage C). *Priority* = cleaning order for the locations still to finish, **ranked by fertile plants counted** (1 = largest population), so large locations come first. "done" = all sampled plants have a seed accession. "finish" = partly loaded, with the rest actionable. "cleaned — not yet imaged" = seeds already cleaned (loc 17), but the envelopes have not been photographed yet, so nothing is loaded. "envelopes missing (#22)" = the remaining plants' event envelopes are not in hand, so there is nothing to clean or image until they are found.

**Two different numbers.** *Fertile plants (counted)* = **every** fertile (flowering/fruiting) plant counted at the event, summed per location (`Events.organismQuantityFertile`). This is the local census of potential mothers and pollen donors. *Occurrences (sampled)* = the plants we actually **sampled** (barcoded, photographed and seed-collected), one row each in `Occurrences`. *% sampled* = occurrences ÷ fertile plants: the share of the breeding population we hold seed from. ≥ = one event recorded as ">200" (loc 20, event 356), counted as 200. \* = total excludes events with no fertile count on the form (loc 11: events 503, 504, 520, 521; loc 12: event 424). Their sampled plants are still counted, so % sampled for \* rows is an **overestimate**. For ≥ rows, % sampled is an upper bound. Free-text counts were read from their leading number (loc 26, e.g. "98 - 17 failed, 81 fruited" → 98).

*Locations visited in 2026 but with no collection (0 events, 0 occurrences — not in the table above): loc 15 (EO18-7, no plants found), loc 29 (EO8), loc 30 (EO26-1), loc 36 (EO26-4, 2 plants too far gone). loc 35 (EO26-2) was not visited. **Note:** Ian's site-visit checklist (§8) marks **loc 15 and loc 30 as seeds-collected (✓)**, but both have **zero 2026 records** in the database — consistent with his own field emails (loc 15, June 29: "found no plants to sample"; loc 30, July 15: seeds already dropped). Worth confirming with Ian which is correct before the checklist is treated as final.*

### Per-location tally — 2026 seed accessions (cleaned vs remaining)

Seed processing runs after the season: each plant's seeds are cleaned and weighed, given a **germplasmID**, and both are written on the event envelope. The envelope pages are then photographed and loaded (Stage C, §3b). *Seed accessions* = plants with a germplasmID and seed weight in the database. *Remaining* = 2026 plants without one yet. *Phase 5 gap* = mothers still needed at that location under the [SRK Phase 5 design](https://github.com/svenbuerki/SRK_bioinformatics/blob/main/Phase5_SRK_summary_for_colleagues.md) (next subsection).

| EO | Location | Occurrences (sampled) | Seed accessions | Remaining | Seed (g) | Status | Phase 5 gap |
|---|---|---:|---:|---:|---:|---|---:|
| **EO8** | loc 27 (EO8) | 15 | 15 | 0 | 2.29 | complete | 3 |
|  | loc 28 (EO8) | 163 | 122 | 41 | 15.50 | partial — occ 3412 no germplasmID (#21); July-14 events 592–610 not yet imaged | 5 |
|  | loc 47 (EO8) | 94 | — | 94 | — | not yet imaged |  |
| | *EO8 subtotal — 3 locations* | **272** | **137** | **135** | **17.79** | | |
| **EO18** | loc 16 (EO18-7) | 76 | — | 76 | — | not yet imaged | 1 |
|  | loc 17 (EO18-7) | 103 | — | 103 | — | cleaned — not yet imaged |  |
|  | loc 18 (EO18-8) | 59 | 57 | 2 | 12.47 | partial — event 328 not cleaned (#23) | 2 |
|  | loc 19 (EO18-7) | 1 | 1 | 0 | 0.18 | complete |  |
| | *EO18 subtotal — 4 locations* | **239** | **58** | **181** | **12.65** | | |
| **EO24** | loc 23 (EO24-2) | 1 | — | 1 | — | not yet imaged |  |
|  | loc 24 (EO24) | 5 | 5 | 0 | 0.23 | complete |  |
| | *EO24 subtotal — 2 locations* | **6** | **5** | **1** | **0.23** | | |
| **EO25** | loc 20 (EO25-A) | 98 | — | 98 | — | not yet imaged | 1 |
|  | loc 21 (EO25-B) | 8 | 8 | 0 | 1.01 | complete |  |
| | *EO25 subtotal — 2 locations* | **106** | **8** | **98** | **1.01** | | |
| **EO26** | loc 31 (EO26-3) | 7 | — | 7 | — | not yet imaged |  |
|  | loc 32 (EO26-3) | 37 | — | 37 | — | not yet imaged | 7 |
|  | loc 33 (EO26-3) | 11 | — | 11 | — | not yet imaged |  |
|  | loc 34 (EO26-3) | 18 | — | 18 | — | not yet imaged | 1 |
|  | loc 48 (EO26) | 18 | — | 18 | — | not yet imaged |  |
|  | loc 49 (EO26) | 7 | — | 7 | — | not yet imaged |  |
| | *EO26 subtotal — 6 locations* | **98** | **0** | **98** | **0.00** | | |
| **EO27** | loc 9 (EO27) | 79 | — | 79 | — | not yet imaged | 1 |
|  | loc 10 (EO27-3) | 7 | 7 | 0 | 0.03 | complete |  |
|  | loc 11 (EO27-1) | 125 | 113 | 12 | 28.38 | partial — 3 envelopes missing (#22) | 5 |
|  | loc 12 (EO27RT) | 126 | — | 126 | — | not yet imaged | 7 |
|  | loc 37 (EO27-1) | 38 | — | 38 | — | not yet imaged | 14 |
|  | loc 43 (EO27-5) | 33 | — | 33 | — | not yet imaged |  |
|  | loc 44 (EO27) | 17 | — | 17 | — | not yet imaged |  |
|  | loc 45 (EO27-1) | 21 | — | 21 | — | not yet imaged |  |
|  | loc 46 (EO27-1) | 10 | — | 10 | — | not yet imaged |  |
|  | loc 50 (EO27) | 17 | — | 17 | — | not yet imaged |  |
| | *EO27 subtotal — 10 locations* | **473** | **120** | **353** | **28.41** | | |
| **EO29** | loc 8 (EO29) | 9 | — | 9 | — | not yet imaged |  |
| **EO30** | loc 13 (EO30-1) | 16 | 16 | 0 | 2.43 | complete |  |
|  | loc 42 (EO30-2) | 34 | 34 | 0 | 7.91 | complete |  |
|  | loc 51 (EO30-3) | 16 | 11 | 5 | 0.42 | partial — 1 envelope missing (#22) |  |
|  | loc 52 (EO30-4) | 7 | 7 | 0 | 0.79 | complete |  |
| | *EO30 subtotal — 4 locations* | **73** | **68** | **5** | **11.55** | | |
| **EO32** | loc 6 (EO32) | 137 | — | 137 | — | not yet imaged | 6 |
| **EO38** | loc 1 (EO38) | 37 | — | 37 | — | not yet imaged | 2 |
| **EO52** | loc 3 (EO52) | 1 | 1 | 0 | 0.25 | complete |  |
| **EO61** | loc 38 (EO61) | 25 | — | 25 | — | not yet imaged |  |
| **EO67** | loc 39 (EO67) | 6 | 6 | 0 | 0.53 | complete | 2 |
| **EO68** | loc 5 (EO68-3) | 10 | — | 10 | — | not yet imaged |  |
| **EO69** | loc 41 (EO69) | 7 | — | 7 | — | not yet imaged |  |
| **EO70** | loc 26 (EO70) | 42 | — | 42 | — | not yet imaged |  |
| **EO76** | loc 2 (EO76) | 8 | — | 8 | — | not yet imaged | 10 |
| **EO118** | loc 4 (EO118) | 25 | — | 25 | — | not yet imaged |  |
| **EO_NEW2026** | loc 53 (EO_NEW2026) | 7 | 7 | 0 | 0.61 | complete |  |
| | **TOTAL — 43 locations** | **1581** | **410** | **1171** | **73.04** | | **76** |

*Phase 5 gap total (76) also counts locations with no 2026 records: loc 35 (EO26-2, 5), loc 29 (EO8, 2), loc 30 (EO26-1, 2).*

**Status at a glance (2026-10-04):**
- **410 plants cleaned and loaded, 1,171 remaining.**
- **11 locations complete:** loc 3, 10, 13, 19, 21, 24, 27, 39, 42, 52, 53.
- **4 partial** (60 plants), each with a known reason:
  - **loc 28:** July-14 events 592–610 (40 plants) not yet imaged, plus occ 3412, which has a weight but no germplasmID (#21).
  - **loc 11:** 3 event envelopes missing (12 plants, #22).
  - **loc 51:** 1 event envelope missing (5 plants, #22).
  - **loc 18:** event 328 not yet cleaned (2 plants, #23).
- **Loc 17:** cleaned, not yet imaged (103 plants).
- **27 other locations:** not yet imaged (1,008 plants). Whether their seeds have been cleaned is not yet recorded.
- **Who cleaned:** the cleaner's initials are recorded wherever they're written on the envelope (60 accessions so far). This is part of the protocol change in #20.

### Where to clean next — priorities from the SRK Phase 5 design

The SRK pipeline's Phase 5 ([`svenbuerki/SRK_bioinformatics`](https://github.com/svenbuerki/SRK_bioinformatics); read the [Phase 5 summary for colleagues](https://github.com/svenbuerki/SRK_bioinformatics/blob/main/Phase5_SRK_summary_for_colleagues.md), or the [full Phase 5 method](https://github.com/svenbuerki/SRK_bioinformatics/blob/main/Phase5_SRK_sampling_and_prediction.md) for formulas and scripts) tests the chain **fragmentation → drift → mate limitation**. Its key outcome regresses **per-mother seed set on predicted pollen compatibility**, within 50 m demes. The design genotypes **15 seedlings per mother** (25 seeds germinated at ~60 %). It needs **505 mothers across 39 locations**. The 2025 seed bank already supplies 431 of them, leaving **76 mothers short across 35 demes**, which Phase 5 flags as the **2026 top-up**.

**Fertile plants** (from the event forms) is shown alongside, because it is the local census that Phase 5's deme model uses (`component_N_fertile`). Where the 2026 fertile count is small, the gap may not be closable from 2026 alone. Every cleaned 2026 envelope gives exactly the data this analysis needs: a mother (`occurrenceID`), its seed lot (`germplasmID`), and its **seed set**, as weight and estimated seed number. **Cleaning order:** largest locations first, ranked by **fertile plants counted** (the same ranks as the Priority column above). Large populations hold the most mothers and the most of the local SRK allele pool, so each envelope from them adds the most to the seed bank and the Phase 5 analyses. The Phase 5 gap and pilot roles are shown alongside, to break ties or move a location up when a specific analysis needs it (e.g. loc 8 for the B1 pilot).

| Rank | Location | Fertile plants counted | Sampled plants still to process | Phase 5 gap (mothers) | Note |
|---:|---|---:|---:|---:|---|
| **1** | loc 47 (EO8) | 1,494 | 94 | — | New 2026 location (not in Phase 5's 2025 list) |
| **2** | loc 6 (EO32) | 1,285 | 137 | 6 |  |
| **3** | loc 20 (EO25-A) | ≥ 887 | 98 | 1 | Includes one event counted as ">200" |
| **4** | loc 28 (EO8) | 681 | 41 | 5 | July-14 events 592–610 (119 fertile); plus occ 3412 (#21) |
| **5** | loc 38 (EO61) | 523 | 25 | — |  |
| **6** | loc 12 (EO27RT) | 455* | 126 | 7 | One of the six locations Phase 5 names as short |
| **7** | loc 17 (EO18-7) | 409 | 103 | — | Seeds already cleaned (Sven); envelopes not yet photographed — next step is imaging |
| **8** | loc 16 (EO18-7) | 365 | 76 | 1 |  |
| **9** | loc 26 (EO70) | 334 | 42 | — | EO70 validation site: observed pollen compatibility below prediction |
| **10** | loc 9 (EO27) | 301 | 79 | 1 |  |
| **11** | loc 18 (EO18-8) | 264 | 2 | 2 | Event 328 not yet cleaned (#23) |
| **12** | loc 32 (EO26-3) | 258 | 37 | 7 | Same EO as pilot partner B2 (loc 34) |
| **13** | loc 1 (EO38) | 254 | 37 | 2 |  |
| **14** | loc 37 (EO27-1) | 191 | 38 | 14 | Largest Phase 5 gap (14 mothers, 4 demes) |
| **15** | loc 43 (EO27-5) | 173 | 33 | — |  |
| **16** | loc 8 (EO29) | 167 | 9 | — | Anchor of recommended pilot B1 (417 adults in one deme) |
| **17** | loc 44 (EO27) | 85 | 17 | — |  |
| **18** | loc 34 (EO26-3) | 82 | 18 | 1 | Partner in pilot option B2 |
| **19** | loc 46 (EO27-1) | 53 | 10 | — |  |
| **20** | loc 4 (EO118) | 50 | 25 | — |  |
| **21** | loc 45 (EO27-1) | 44 | 21 | — |  |
| **22** | loc 50 (EO27) | 42 | 17 | — |  |
| **23** | loc 48 (EO26) | 35 | 18 | — |  |
| **24** | loc 41 (EO69) | 26 | 7 | — |  |
| **25** | loc 5 (EO68-3) | 23 | 10 | — |  |
| **26** | loc 49 (EO26) | 19 | 7 | — |  |
| **27** | loc 2 (EO76) | 16 | 8 | 10 | EO76 validation site; only 16 fertile plants in 2026, so the gap can't close this year |
| **28** | loc 33 (EO26-3) | 14 | 11 | — |  |
| **29** | loc 31 (EO26-3) | 12 | 7 | — |  |
| **30** | loc 23 (EO24-2) | 2 | 1 | — |  |
| — | loc 11 (EO27-1), loc 51 (EO30-3) | 784* / 152 | 12 / 5 | 5 / — | Envelopes missing (#22) |
| — | loc 35 (EO26-2, pilot partner **B1**), loc 29, loc 30 | — | 0 | 5 / 2 / 2 | **No 2026 collection** (loc 35 not visited; 29 and 30 had no seed). B1 still relies on its 8 mothers from 2025 |

*Phase 5 gap "—" = no shortfall, or a location not in Phase 5's 2025 list (new 2026 locations 41–53).*

**Caveats.**
- **2026 mothers only close a gap if they fall in a short deme.** Phase 5's 50 m demes come from 2025 event positions (`step29c_event_to_component_50m.tsv`), so each 2026 event needs mapping to its 50 m component before the counts are final. The next step is to re-run the Phase 5 selection with 2026 accessions included.
- **Locations missing from the tally.** The Phase 5 location list is a 2025 snapshot of the Snake River Plain range, so new 2026 locations (41–53) aren't in it.

## 2. Stage A — field forms → Locations / Events / Occurrences

Paper Location + Event forms (2 pages each) are OCR'd by a **read-only agent sweep** (subscription, no API cost), pages classified by their printed header, and the hierarchy rebuilt from barcodes + capture order. **Event IDs are ground-truthed by decoding the CODE128 sticker barcode** (`verify_event_barcodes.py`) — the printed/handwritten event numbers are frequently wrong, so the decoded barcode is authoritative (this caught mis-entries all season). Table-only columns auto-fill; human fixes go through three persistent override files (occurrence ranges, reused event stickers, new-site GPS). Form photos are filed into `Multimedia` as evidence (`type='field form'`).

**`associatedTaxa`** is auto-homogenized to `Taxonomy.taxonID` lists (verbatim kept in `associatedTaxaOriginal`); the season added several taxa to the lexicon (Descurainia, Physaria, and spelling variants).

## 3. Stage B — plant images → multimedia + phenotyping

Board photos are ingested under collision-proof content-addressed names (`LEPA_<date>_<sha8>.jpg`; camera `JCN_####` names reset yearly and are **not** a stable key). A read-only sweep reads each board (OC# = occurrenceID) + measures the plant against the board's own ruler, cross-checking the written date to catch stray images from other field days. `stageB_load.py` links each image to its **existing** Stage-A occurrence (`tableID 13`) and inserts Phenotyping.

### 3a. h/w validation (the headline result)

Where boards carry **field-written height/width**, the **image-measured** value matches the **field tape** to a **median of ≈±1 cm** (the large majority within ±2 cm) for both height and width — a true ground-truth check, not self-consistency. Conclusion: the low-cost photo phenotyping reproduces the tape; keep using it, with **size class as the primary metric and cm as supporting**. (Boards with no clear image scale are scored straight from the field-written h/w — `measurementMethod = field tape`.)

### 3b. Stage C — seed sheets → seed accessions (added 2026-10-04)

After seed processing, the back of each event envelope (form page 2) carries each plant's **germplasmID** and **seed weight (g)**, and ideally a date and the cleaner's initials. These pages are photographed into `Field_forms/2026/`, with each location's **location form first**, and read by the same read-only agent sweep as Stage A. `germplasm_seeds.py` then:
- validates every row against the DB: the plant exists, belongs to the sheet's event, and sits at the right location;
- keeps a cumulative **germplasmID registry**, so an ID used twice or a plant given two IDs is caught across batches;
- **holds ambiguous handwriting** (overwritten digits) until someone checks the physical envelope, rather than guessing;
- computes seed-number estimates from the 1000-seed-weight equation;
- records the **cleaner** (`Germplasm.personID`, from the initials) and the written **acquisition date**;
- appends seed-quality notes (e.g. "many broken plants") to the event remarks.

Each sheet photo is copied under a collision-proof name and linked to its event as evidence. Method: Stage C section of [`IMAGE_PIPELINE_GUIDE.md`](IMAGE_PIPELINE_GUIDE.md).

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
- **#20** — seed processing protocol: write the **date and initials** on every envelope (most 2026 envelopes carry neither, so the photo date stands in as the acquisition date).
- **#21** — occ 3412 (loc 28): seed weight recorded but **no germplasmID**.
- **#22** — **missing event envelopes**, by location (loc 11: events 504, 516, 523; loc 51: event 719).
- **#23** — events whose **seeds are not yet cleaned**, by location (loc 18: event 328).
- *Resolved this season:* #7, #8 (EO38/EO118 forms located), #12 (genotyping status gaps), #14 (occ 2714 envelope reuse), **#18** (loc-50 event latitudes finalized against the manilla), **#19** (event 718 page-1 recovered → loaded as a data-only event).

## 7. Data products

- `LEPA_SQL.db` — **Locations 52, Events 723, Occurrences 3,797, Multimedia 3,558, Phenotyping 2,312, Germplasm 1,195** (785 from 2025 + 410 from 2026), including all prior-year data, the full 2026 season, the genotyping integration and the 2026 seed accessions so far.
- `staging_2026/` — reviewed staging + the 3 override files + `stageB_*` staging.
- Scripts: `germplasm_seeds.py` (Stage C, seed sheets → `Germplasm`, with registry and `--report`), `field_forms_ocr.py` (Stage A), `stageB_load.py` (Stage B linking — the forms-first loader), `verify_event_barcodes.py` (event barcode ground-truthing), `01_ingest_register.py` (image ingest).

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
- The checklist groups **location 50 under EO27-1 (Red Tie area OCTC)**, whereas the July-17 load labelled loc 50 as EO27 "Region 3" (reconstructed with no field email). Ian's roster is the authoritative sub-EO assignment. *(The loc-50 event latitudes flagged in GitHub **#18** were finalized against the manilla 2026-07-23 — 687/688 confirmed, 689 corrected; #18 resolved.)*
- **Location 44** is resolved by the checklist as **EO27-? "between Figgins and Pleasant Valley"** (previously flagged as within EO27 but outside any official sub-EO boundary).
- **EO48 (loc 7)** and **EO26-2 (loc 35)** are confirmed **DNV** (time-skipped, both low-prospect) — matching Ian's July-21 email.
- **EO30-3 (loc 51)**, **EO30-4 (loc 52)**, and the **New-2026 BLM-found population (loc 53)** are the July-21 final-day additions (30 plants, occ 3843–3872), now loaded; **EO112 was visited but held no Lepa** (Ø).
- **loc 53 has no official EO** (Ian marked "No EO"; nearest EO112 held no Lepa in 2026 or 2013). It is databased under a **provisional EO, EOID 21 / `EO_NEW2026`** so its 7 plants (occ 3866–3872) are fully attributed — rename the EOCode when IDFG assigns an official number.
- **One seedless slick spot on 2026-07-21 (loc 51, event 718)** was initially unrecordable (only its page 2 had been imaged). Peggy provided the missing page 1 (2026-07-22), and it is now loaded as a **data-only event** — 62 fruiting individuals, 25 rosettes, condition 2.5, 0 seed collections (the EO61-style effective-population-size case). GitHub **#19 resolved**.
