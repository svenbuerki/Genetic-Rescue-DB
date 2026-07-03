# LEPA database — data-quality status

Single source of truth for the data-quality state of `LEPA_SQL.db`. Last QA pass: **2026-07-02**
(genotyping/biobanking pipeline integrated + validated).
Tracked issues live on GitHub (**svenbuerki/Genetic-Rescue-DB**); each item below links to its issue.

## Integrity — clean ✅

A full audit (2026-06-27) found no structural problems:

| Check | Result |
|---|---|
| Orphan/broken FKs (Multimedia, Phenotyping, Germplasm → Occurrences) | **0** |
| `Phenotyping.multimediaID` → missing Multimedia | **0** |
| Duplicate Phenotyping rows (per occurrence) | **0** |
| Duplicate images (same SHA-256 content) | **0** |
| Locations missing GPS (`locationDecimalLatitude/Longitude`) | **0** of 39 |
| Locations with null `EOID` | **0** |
| Tables documented in `TableModules` | **30 / 30** (all real tables) |
| Photo-date (EXIF) vs `occurrenceDate`, where EXIF present | **0 mismatches** of 77 checkable |
| Genotyping FK chain: `GenotypingStatus`/`TissueBank` → Occurrences; `MolecularBank` → TissueBank; `Sequencing` → MolecularBank | **0** orphans |

## Coverage

- **Occurrences:** 2698. **Events:** 371. **Locations:** 40.
- **Phenotyping:** 1212. **Multimedia:** 1570 (incl. field-form images).

## July 1–2 2026 campaign (EO18-8 / EO18-7 / EO25 / EO24 — loaded 2026-07-03)

Revisit of existing locations 18–25 (2025 data already present). Two-stage load, both stages verified 0-orphan:
- **Stage A** (`field_forms_ocr.py`): 96 forms → **+45 Events** (328–372, **CODE128 barcode-verified**, 44/45 decoded), **+172 Occurrences** (2596–2767), +96 form images. Counts matched Ian's field emails exactly (loc 20 = 98, loc 18 = 59, loc 21 = 8, EO24 = 6, loc 19 = 1). `associatedTaxa` auto-homogenized; **+2 taxa** (Descurainia 46, Physaria 47) + 14 lexicon variants added for the new tokens.
- **Stage B** (`stageB_load.py` — NOT `02_ocr --load`; see the guide's "which loader" note): 172 boards ingested → **+172 Multimedia** (tableID 13) **+172 Phenotyping** (48 large / 107 medium / 17 small). 15 board-only-unclassed re-scored from field-written h/w (field tape, high confidence). No stray/other-day images (date cross-check clean).
- **[#14](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/14) (CLOSED)** — occ 2714 reused across events 362 & 363 (field envelope reused); resolved by moving occ 2714 → event 363, so both events hold 4 plants matching the whiteboards.
- **Images:** unique `LEPA_<date>_<sha8>.jpg` scheme in `Multimedia_main/`; raw in `Multimedia_images/<year>/<date>/`.

## Genotyping & biobanking (integrated 2026-07-02)

Biobanking→genetics pipeline loaded and **validated against Peggy's master sheet** (full multiset match, 0 diffs):

- **TissueBank** 1,699 · **TissueTransactions** 33 · **MolecularBank** 662 DNA extractions (MP/Omega) ·
  **Sequencing** 505 Nanopore libraries (497 ingroup / 8 outgroup) · **GenotypingStatus** 885 rows.
- **Pipeline status** (885 rows): **Complete 259 · Failed 225 · Incomplete 401** (883 distinct occurrences; 258 Complete).
- **Taxonomy:** +9 *Lepidium* congeners (outgroups). **6 clone occurrences** flagged (`occurrenceRemarks LIKE '%CLONE%'`).
- **View** `vSequencingOccurrence` joins each library to its `occurrenceID` (SRK-pipeline entry point; `SampleID` = `libraryName`).
- **Terms** now document every genotyping field (140 total); `TissueTransactions` (Biobanking) + `GenotypingStatus` (Genetics) registered.
- **Issues:** #9–#13 filed for the lab team; **#12 closed** (status gaps reconciled; occ 1134 resolved to *L. montanum*). Open: **#10** (57 tissues no weight), **#11** (6 master-sheet tissue cells), **#13** (5 negative tissue weights).
- **Event-265 occurrence-ID collision fixed** — wild EO69 plants renumbered off the genotyping-bank IDs (2384/2385/2386→2894/2895/2896, +2897); clones/outgroups now hold 2383–2386; three board images annotated with corrected OccIDs. See `Notes` (Data Correction rows) + `PIPELINE_LOG.md`.

## 2026 campaign (processed June 2026) — see [`REPORT_2026_campaign.md`](REPORT_2026_campaign.md)

Two-stage load: **forms → records** (1 new Location EO69, 17 Events, 84 Occurrences, 40 form images as
evidence), then **plant images → multimedia + phenotyping** (80 linked, 76 phenotyped). **h/w validation:**
on the 23 boards with field-written h/w, image measurement matched the field tape to **median ±1 cm
(20/21 within ±2 cm)** for both height and width — the technique is validated against ground truth.
Reused-barcode collisions caught + fixed (event sticker `0098`→`268`).

**Follow-up load (2026-06-28) — closed [#7](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/7) + [#8](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/8):**
EO38 forms came in → +15 Events (239–241, 249–260), +37 Occurrences (2281–2317) on a **revisit of location 1**,
34 plant images + 33 phenotyped, 31 form images as evidence. EO118 envelope event located → occ 2395–2403
attached to **event 266**, 9 images + phenotyping linked. OCR section-4 fixes confirmed against plant boards
(234→2314, 2205→2285, 2708→2308, 7310→2310; Event 255 = 2292–2299 per review).

**EO18-7 load (2026-06-30):** +32 Events (270–302, gap at 277), +103 Occurrences (2417–2519) on a **revisit
of location 17**, +103 plant images, +103 phenotyped (3 from board-written W/H), +65 form sheets. Event
numbers **barcode-verified** (no collisions after the 5-event fix). Occurrence numbers anchored on the board
reads, which resolved the noisy form OCR (e.g. 7470→2430, 24465→2465, 501→2501). Also recovered occ **2379**
(EO69, collected + imaged but missed in the original load) and flagged occ **2386** as a no-image gap;
occ 2387–2391 confirmed as skipped barcodes.

**EO18-7 Location 16 load (2026-07-01, fieldwork 06-30):** +25 Events (303–327, barcode-verified — one "630"
was really 324), +76 Occurrences (2520–2595), all imaged + phenotyped, +51 form sheets, on a **revisit of
location 16**. Board reads corrected 4 form-OCR slips. **First live run of `associatedTaxa` auto-homogenization**
→ `Taxonomy` taxonIDs (verbatim kept in `associatedTaxaOriginal`); 1 run-together token reviewed by Sven.

## Standing items (known; not integrity faults)

| # | Item | Detail | GitHub |
|---|---|---|---|
| 0b | **2026 collected occ without image** | 7 occurrences (EO76 ×5, EO69 ×1, EO118 ×1) have no linked plant photo — un-photographed or a board# mis-read. | [#6](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/6) |
| 0d | **EO38 image residuals** | occ **2282** not photographed (board **2202** is an image with no occurrence — likely a 2282 misread, in `stageB_unmatched_review.csv` for a human check); occ **2288 & 2292** photographed but no plant in frame → linked board-only, tagged `NOT PHENOTYPED`. | (within #7) |
| 1 | **Un-phenotyped: plant below board** | 18 occurrence images where the plant was photographed on the ground below/beside the board (no scale reference) → size indeterminate. Tagged in `Multimedia.remarks` (`NOT PHENOTYPED`). | [#5](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/5) |
| 2 | **Un-phenotyped: image lost** | occ 220 (`EO27 Figgins - Occurrence 220.jpg`) deleted from Drive, no copy. Record retained, `IMAGE LOST` in remarks. | [#5](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/5) |
| 3 | **No-board context images** | 48 location-level images (transit/landscape/crew) auto-attached to the nearest site; need a human to confirm content + locationID. `Multimedia.remarks LIKE 'NEEDS CURATION%'`. | [#4](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/4) |
| 4 | **Image coverage gaps** | 50 occurrences with no image: **45 ex-situ** greenhouse accessions (image later, by design) + **5 in-situ** field gaps (occ 213, 214, 215, 236, 379 — no photo taken). View `vUnimagedOccurrences`. | [#3](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/3) |
| 5 | **Board-vs-DB mismatches (2025)** | 56 boards where board-date ≠ `occurrenceDate` (some are observed-vs-photographed next day; some may be entry errors) + 26 location-label candidates. **Not currently re-checkable** — see limitation below. | [#2](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/2) |
| 6 | **Board number 289 reused** | Board 289 used on two 2025 plants; one image (`JCN_0360`, now in `Multimedia_images/2025/unknown-date/`) needs the correct occurrenceID. | [#1](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/1) |

## Resolved this session (2026-06)

- **Event-barcode audit** (2026-06-30) — new protocol: decode the **CODE128 barcode** on each Event
  sticker instead of trusting digit-OCR (`Multimedia_pipeline/verify_event_barcodes.py`). The audit
  found **5 mis-entered 2026 events** (stored `265/281/282/285/288` → true `263/261/262/265/269`); all
  corrected by a backed-up two-phase renumber cascading Events/Occurrences/Multimedia. Now `32/32`
  loaded 2026 events match their barcode. (Setup: see "Requirements & setup" in the pipeline guide.)
- **#7 EO38 forms & #8 EO118 event** (2026-06-28) — both closed. EO38 forms OCR'd and loaded (revisit of
  location 1; +15 Events, +37 Occurrences, plant images + form evidence); EO118 occ 2395–2403 attached to
  event 266. See the 2026-campaign follow-up note above and the GitHub issues.
- **Filename collisions** — camera `JCN_####` numbering resets yearly; 2026 frames had overwritten 56
  of the 2025 images. Recovered all 56 from `work/full/`; root-caused and fixed by a content-addressed
  naming scheme. See [`ISSUE_filename_collision.md`](ISSUE_filename_collision.md).
- **occ 226–230 EO mis-entry** — were `EO38 / loc1 / 06-17-2025`; corrected to `EO27 / loc9 / 07-08-2025`
  (board OCR + EXIF capture 2025-07-08 + neighbours all agree). Audit note in `occurrenceRemarks`.
- **occ 220** — image confirmed lost and documented (above).

## Known limitation — date re-validation

The EXIF-vs-`occurrenceDate` cross-check (which caught the 226–230 error) only covers the **77 of 760**
occurrence images that still carry EXIF; the rest are EXIF-stripped 2025 crop-pipeline copies. So issue
**#2** (board-date mismatches) cannot be revisited from EXIF alone — it would need a re-OCR pass of the
boards (`02_ocr.py`). All 77 EXIF-bearing images currently agree with their `occurrenceDate`.

## How to query the flags

```sql
SELECT * FROM Multimedia WHERE remarks LIKE '%NOT PHENOTYPED%';   -- 18 below-board images (#5)
SELECT * FROM Multimedia WHERE remarks LIKE 'IMAGE LOST%';        -- occ 220 (#5)
SELECT * FROM Multimedia WHERE remarks LIKE 'NEEDS CURATION%';    -- 48 no-board images (#4)
SELECT * FROM vUnimagedOccurrences;                               -- 50 image-coverage gaps (#3)
```

Provenance of every image (original camera name, year, field-day date, EXIF capture, SHA-256) is in the
new `Multimedia` columns and in `Multimedia_main/file_registry.csv`; all renames are logged in
[`PIPELINE_LOG.md`](PIPELINE_LOG.md).
