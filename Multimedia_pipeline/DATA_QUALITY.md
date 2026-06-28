# LEPA database — data-quality status

Single source of truth for the data-quality state of `LEPA_SQL.db`. Last QA pass: **2026-06-27**.
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
| Tables documented in `TableModules` | **28 / 28** (all real tables) |
| Photo-date (EXIF) vs `occurrenceDate`, where EXIF present | **0 mismatches** of 77 checkable |

## Coverage

- **Occurrences:** 894 (810 2025 + 84 2026). **Events:** 254. **Locations:** 40 (+EO69, the new 2026 site).
- **Phenotyping:** 817 (741 2025 + 76 2026). **Multimedia:** 930 (incl. 40 2026 field-form images + 80 2026 plant images).
- **Images:** unique `LEPA_<date>_<sha8>.jpg` scheme in `Multimedia_main/`; raw in `Multimedia_images/<year>/<date>/`.

## 2026 campaign (processed June 2026) — see [`REPORT_2026_campaign.md`](REPORT_2026_campaign.md)

Two-stage load: **forms → records** (1 new Location EO69, 17 Events, 84 Occurrences, 40 form images as
evidence), then **plant images → multimedia + phenotyping** (80 linked, 76 phenotyped). **h/w validation:**
on the 23 boards with field-written h/w, image measurement matched the field tape to **median ±1 cm
(20/21 within ±2 cm)** for both height and width — the technique is validated against ground truth.
Reused-barcode collisions caught + fixed (event sticker `0098`→`268`).

## Standing items (known; not integrity faults)

| # | Item | Detail | GitHub |
|---|---|---|---|
| 0a | **EO38 forms missing (2026)** | 33 EO38 plants photographed (boards ~2281–2317) but no EO38 field form in the batch → no event/location to attach; staged in `stageB_unmatched_review.csv`, not loaded. | [#7](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/7) |
| 0b | **2026 collected occ without image** | 7 occurrences (EO76 ×5, EO69 ×1, EO118 ×1) have no linked plant photo — un-photographed or a board# mis-read. | [#6](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/6) |
| 0c | **EO118 plants missing their event form** | 9 EO118 plants photographed + field-measured (boards 2395–2403, with h/w) but absent from the loaded forms — their event envelope was pulled for seed cleaning. Staged in `stageB_unmatched_review.csv`, not loaded. | [#8](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/8) |
| 1 | **Un-phenotyped: plant below board** | 18 occurrence images where the plant was photographed on the ground below/beside the board (no scale reference) → size indeterminate. Tagged in `Multimedia.remarks` (`NOT PHENOTYPED`). | [#5](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/5) |
| 2 | **Un-phenotyped: image lost** | occ 220 (`EO27 Figgins - Occurrence 220.jpg`) deleted from Drive, no copy. Record retained, `IMAGE LOST` in remarks. | [#5](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/5) |
| 3 | **No-board context images** | 48 location-level images (transit/landscape/crew) auto-attached to the nearest site; need a human to confirm content + locationID. `Multimedia.remarks LIKE 'NEEDS CURATION%'`. | [#4](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/4) |
| 4 | **Image coverage gaps** | 50 occurrences with no image: **45 ex-situ** greenhouse accessions (image later, by design) + **5 in-situ** field gaps (occ 213, 214, 215, 236, 379 — no photo taken). View `vUnimagedOccurrences`. | [#3](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/3) |
| 5 | **Board-vs-DB mismatches (2025)** | 56 boards where board-date ≠ `occurrenceDate` (some are observed-vs-photographed next day; some may be entry errors) + 26 location-label candidates. **Not currently re-checkable** — see limitation below. | [#2](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/2) |
| 6 | **Board number 289 reused** | Board 289 used on two 2025 plants; one image (`JCN_0360`, now in `Multimedia_images/2025/unknown-date/`) needs the correct occurrenceID. | [#1](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/1) |

## Resolved this session (2026-06)

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
