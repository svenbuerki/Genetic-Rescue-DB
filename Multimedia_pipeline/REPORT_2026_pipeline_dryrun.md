# LEPA 2026 — Image-driven data-entry pipeline (Steps A–C dry-run)

**Prepared for:** Buerki Lab team
**Subject:** Processing the first 2026-campaign uploads as a *pre-population* dry-run, and validating the OCR + phenotyping technique before the adapted-board protocol begins.
**Status:** **No database writes.** All outputs are staged for human review (`staging_2026/`).

---

## 0. What changed in 2026 (and why this is a dry-run)

In 2025 the workflow was *image → link to an already-digitized occurrence*: every board number matched a hand-entered `Occurrences` row, and the board read was **cross-checked** against that row. In 2026 the goal is the reverse — **the image becomes the data-entry source**: field sheets are not hand-digitized first, so the OCR creates the records (Locations → Occurrences → Phenotyping → Multimedia). That removes the 2025 cross-check, so before trusting OCR to *create* records we measured how well it *reproduces* records we already trust.

This batch is a **mixture**, and only part of it is genuinely new:

| Group | n images | What it is | Role here |
|---|---|---|---|
| **New 2026** `EO## NNNN` | 59 | EO70/EO68/EO69 boards dated 6/22/26, photo-sequence numbers, **no occurrence ID and no h/w on the board** | the pre-population dry-run (need new IDs; EO69 is a new EO) |
| **Existing 2025** `… Occurrence NNN` | 69 | EO27/EO68/EO70/EO72 boards already in the DB | **blind validation set** (known answers) + phenotyping gap-fill |
| **BC exemplars** `BC-A…J` | 10 | EO26 "Alkali Crk" boards, occ 336–345, dated 6/24/25 | curated exemplars; also a phenotyping gap |
| **Context/parking** | 5 | trucks, pullouts, slick-spot habitat | EO/location-level multimedia |

> **Important for the team:** the adapted boards (printed `O=`, `EO=`, `L=`, `h=`, `w=`) are **not in this batch** — they arrive next week. **0 of 128** boards here carry on-board `h/w`, so plant-size **validation against field-written h/w is deferred to that batch.** What we *could* validate now is the technique itself, against the 2025 records.

## 1. Method

All 128 plant boards were read by **read-only vision agents, one per image, fully blind** — each image was symlinked to an opaque name (`plant_001.jpg`…) so the agent could not see the EO/occurrence in the filename and reported **only what is physically on the whiteboard**. Each agent returned: the OCR'd board number / EO / date / locality, whether `h/w`/`O=`/`L=` labels are present, and a measured **height**, **crown width**, **method** (`ruler` vs `1cm-tile`) and **size class** scaled from the taped rulers. Results were then joined back to the database to score accuracy and build the staging set.

## 2. Step B — does the technique reproduce what we already trust?

**B1. OCR accuracy (blind board read vs the 2025 database):**

- **occurrence ID: 66/69 correct (96%).** The 3 misses (EO70 occ 450, 461, 464) were *partial* reads ("4…") — exactly the kind of low-confidence read the human gate is designed to stop.
- **EO code: 64/69 match the database** — but the 5 "mismatches" are **the database being wrong, not the OCR.** See §4.1: occ 226–230 read `EO27 Figgins 7/8/25` on the board (high confidence) *and* in the filename *and* in the locality, while the DB stores them as `EO38 / 06-17-25`. The blind read was right; it **surfaced a real mis-linkage.**

**B2. Measurement repeatability (re-measured blind vs the stored 2025 cm):**

- height Δ = **median +2.0 cm** (mean +1.8, n=44); crown Δ = **median +2.0 cm** (mean +2.4, n=46).
- **size class agreed on 38/47 (81%)**; every disagreement was an *adjacent* class straddling the 10/20 cm thresholds.
- Large plants (DB crown 38–60 cm) drove the only big deltas (up to ±10–22 cm) — the taped ruler is too short for them, the same limitation flagged in 2025.

> **Takeaway:** the image technique reproduces the trusted data to **±2 cm typically**, **size-class ~80%**, and **OCR ~96%** — and where it "disagreed" it caught two real data-quality problems. It is good enough to *pre-populate* provided every record passes the human gate, and provided **size class (not raw cm) remains the primary size metric.**

## 3. Step C — staging the new records (no writes)

`staging_2026/occurrences_staging.csv` + `phenotyping_staging.csv`:

- **59 provisional Occurrences** (`prov_occID` 1498–1556) for the new 2026 boards — EO70 ×42, EO68 ×9, EO69 ×8 (by board OCR). No collision with the live max ID (1497).
- **EO69 (8 plants) is a NEW Element Occurrence** not in the `EOs` table → flagged `NEW_EO`. Per the controlled-vocabulary rule we do **not** auto-create it; it needs a deliberate EO record + a Location with GPS first.
- **All 59 flagged `NEEDS_LOCATION`** — 2026 boards carry no latitude/longitude, and `Locations` is *defined* by GPS, so no Location row can be created from the board alone.
- **77 phenotyping rows staged**: 59 new-2026 + 18 existing gap-fill (EO27 Figgins + EO72 plants that had images but no measurement).

## 4. Issues to raise / resolve before any load

1. **occ 226–230 — EO conflict (likely board-number reuse).** Board + filename + locality say `EO27 Figgins, 7/8/25`; DB says `EO38, loc 1, 6/17/25`. Either the DB rows are mis-assigned or board numbers 226–230 were reused across two sites/dates (cf. the 2025 board-289 case). **Needs human adjudication.**
2. **EO69 is new.** Requires a designated EO record and a GPS'd Location (two context images — habitat + parking — document the site and can be linked once EO69 exists).
3. **EO68 `2376` boundary read.** Filename says EO68; the board OCR'd `EO69` (medium confidence). Confirm visually which EO this plant belongs to.
4. **3 partial occ reads** (EO70 450/461/464) — re-read or confirm from the board.
5. **GPS gap (design).** Pre-population cannot create Locations from boards; either add GPS to the board (the adapted boards' `L=` plus a coordinate, ideally) or supply a Location lookup at load time.

## 5. Also identified (not yet processed)

- **occ 336–345 (BC-A…J, EO26 Alkali Crk):** 10 exemplar boards, all validate cleanly (board ↔ DB ↔ filename agree, dates match) but have **0 phenotyping** — a clean 10-plant gap-fill set, ready to measure.
- **5 context images** → Multimedia at EO/location level with content-describing titles (truck, parking pullout, slick-spot habitat); 2 document the new EO69 site.

## 6. Recommendations for the new imaging protocol (team)

1. **Put the occurrence ID, EO, and Location on the board** (the adapted `O=`/`EO=`/`L=` fields) — OCR of a *structured* field is far more reliable than free handwriting, and it removes the 226–230-type ambiguity.
2. **Record GPS with every board** (or print the Location code that resolves to GPS) — without it we cannot create `Locations`, which blocks Occurrences.
3. **Keep `h=`/`w=` on the board** — once present they give an independent field measurement to validate the image phenotyping (the check we could not run this batch).
4. **Add a taller scale** (the ~15/30 cm rulers cap below mature plants — the dominant measurement-error source) and **report size class as primary**, cm as supporting.
5. **One board number per plant, never reused** — the 226–230 conflict shows the cost of reuse.
6. **Every board passes the human gate** before load — the staging CSVs are that gate.

## 7. Data products

- `staging_2026/occurrences_staging.csv` — 59 provisional Occurrences + EO/Location resolution + flags.
- `staging_2026/phenotyping_staging.csv` — 77 measurement rows (new + gap-fill).
- `staging_2026/validation_ocr.tsv` — blind board read vs DB (per image).
- `staging_2026/validation_measure.tsv` — re-measured cm vs stored cm (per image).
