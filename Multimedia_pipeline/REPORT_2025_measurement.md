# LEPA 2025 — Image-based occurrence linking & plant measurement

**Prepared for:** Buerki Lab team
**Subject:** Linking field whiteboard photos to the database, and estimating plant size from the photos
**Data:** full 2025 campaign — `JCN_0016`–`JCN_0753` (731 frames)

> **Status update (2026-06).** This 2025 campaign report has been refreshed for the June-2026
> gap-fill sweep (`Phenotyping` now **741**) and the occ 226–230 correction. For the current,
> living data-quality state and the full tracked-issue list, see **[`DATA_QUALITY.md`](DATA_QUALITY.md)**
> and the rebuilt pipeline guide **[`IMAGE_PIPELINE_GUIDE.md`](IMAGE_PIPELINE_GUIDE.md)**.

---

## 1. Objective

Each fruiting *Lepidium papilliferum* plant was photographed in the field with a blue
whiteboard giving its **occurrenceID** (top-left) and **date** (top-right), plus two
rulers for scale. Two goals:

1. **Link** every photo to its `Occurrences` record in `LEPA_SQL.db` and store it in the
   `Multimedia` table.
2. **Measure** plant **height** and **crown width**, and assign a **size class**, stored in
   the dedicated **`Phenotyping`** table.

## 2. Approach

A documented, reproducible pipeline (`Multimedia_pipeline/`):

- **Read the board** — each photo's header is cropped and the handwritten occurrenceID +
  date are read, then validated against `Occurrences` (number must match; date cross-checked).
- **Load** — linked rows inserted into `Multimedia` (backup + `remarks` note).
- **Measure** — the board's two rulers give scale: the horizontal ~15 cm Zukamo ruler
  (crown width) and the vertical ~30 cm edge ruler (height). Plants larger than the ruler are
  measured by a **"1 cm tile"** (read one graduation → cm-per-pixel → tile across the plant).
  Measurement reads a **high-resolution crop of the lower frame** (the plant + rulers).
- **Phenotyping** — each measurement is its own record (DwC *MeasurementOrFact*), linked to
  the occurrence **and** its source image (`06_phenotyping_schema.py`).

**Reading at scale.** Board reads and measurements were done **in-session by Claude Code**
(covered by the subscription — no per-image API cost), parallelised across many subagents.
Board IDs were established two ways and cross-checked: **manual reads** for `JCN_0111–0513`
and an **alignment-proof single-image agent pass** for `JCN_0514–0753` (one agent per crop, so
the filename↔ID mapping cannot drift). Agreement on the overlap with an independent agent
sweep was 91.8%; all sampled disagreements were the agent's batch-boundary off-by-one, with
the manual read confirmed correct against the board.

## 3. Results

### Linking (Multimedia)

- **587** new occurrence images linked (boards `0111`–`0753` → occurrenceIDs **94–763**);
  **760** occurrence images in `Multimedia` total (incl. the original 95-image sample).
- **1** board-number conflict held back (board `289` reused on two plants — see Issues).
- **47** no-board frames (transit / landscape / sky) not linked.
- All **587** board numbers matched an existing `Occurrences` record.

### Image coverage (Occurrences ↔ Multimedia)

- **760 of 810** occurrences have an image. **50** do not:
  **5 in-situ field plants** (occ 213, 214, 215, 236, 379 — photo-sequence gaps) and
  **45 ex-situ** greenhouse/breeding accessions (not field-imaged by design).
- Reusable view **`vUnimagedOccurrences`** lists them.

### Measurement (Phenotyping)

**741** measurement records (all image-linked; all 19 EOs represented):

| Size class | n | crown width |
|---|---|---|
| small  | 387 | < 10 cm |
| medium | 241 | 10–20 cm |
| large  | 113 | > 20 cm / exceeds the board ruler |

- Height ≈ 1.8–35 cm (mean ~10.7); crown ≈ 1.5–70 cm (mean ~11.7; the upper extreme is a single
  very large individual).
- Method: **661** read within the ruler, **80** by the 1 cm-tile (exceeds-ruler).

> **Recovered EOs (post-hoc).** 48 in-situ plants in **EO68, EO70, EO72** were imaged in 2025 but initially un-measured — their board numbers (179–199, 444–468, 764–767) fell in the photo-sequence gaps (board jumps 178→200 and 443→469). They were OCR-validated (board ID = filename, dates matched) and measured from the same crops, bringing the whole **Bottleneck Lineage BL2 (EO68+EO70)** into the dataset and giving phenotype coverage for **all 19 EOs**.

> **2026 gap-fill (June 2026).** A read-only agent sweep measured the 43 occurrence images that
> were linked but still un-measured, adding **25** records (716 → **741**): the EO27 Figgins run,
> the 10 EO26 "BC" exemplars (occ 336–345), and EO72. **18** images could not be measured (the
> plant was photographed below the board, so no in-frame scale) and occ **220**'s image was lost —
> both documented in `Multimedia.remarks` and GitHub issue #5. Separately, occ **226–230** were
> corrected from a data-entry error (`EO38` → `EO27`, confirmed by board OCR + EXIF + neighbours).

## 4. Accuracy & data quality

No field-measured ground truth exists, so these are estimates judged against the in-frame
rulers. Accuracy is tiered: **in-ruler plants ~±2–3 cm**; **plants beyond the ruler ~±5–8 cm**
(parallax + amplified calibration error).

**One consistent method.** The whole collection is now measured from the **same
high-resolution lower-frame crop** — occ 1–93 originally, and occ 94–763 re-measured in this
campaign from the sharper crop (which also recovered ~44 plants the earlier low-resolution
pass had missed). A cross-check of the two measurement passes over the same 524 plants showed
mean height Δ **+1.4 cm** and crown Δ **+0.2 cm** — the aggregate is stable — yet **size class
changed for ~33%** of plants, almost all *adjacent* classes near the 10/20 cm thresholds. So:

> **Size class is indicative; cm is supporting.** Size-class distributions and coarse trait
> data are reliable; treat individual cm values as ±2–8 cm vision estimates.

## 5. Data-quality issues raised (GitHub — svenbuerki/Genetic-Rescue-DB)

- **#1** — board `289` reused on two plants (one image held pending the correct ID).
- **#2** — 56 board-date ≠ `occurrenceDate`, plus 26 location-label candidates (blocks
  occ 122–144 `EO30-2`/`EO30-1`, occ 441–443 `EO24-7`/`EO24-1`).
- **#3** — 50 occurrences without images (the 5 in-situ field gaps + 45 ex-situ), requesting
  team support to source the field-plant photos.
- **#4** — 48 no-whiteboard context images (transit / landscape) added to `Multimedia` with
  inferred sites — flagged `NEEDS CURATION` for team confirmation.
- **#5** — 18 occurrence images that cannot be phenotyped (plant below the board, no scale) +
  occ 220 (image lost) — tagged `NOT PHENOTYPED` / `IMAGE LOST` in `Multimedia.remarks`.

The current status of all issues is consolidated in [`DATA_QUALITY.md`](DATA_QUALITY.md).

## 6. Recommendations

1. **Add a taller scale to the field kit** (meter stick / folding rule in frame) — the ~15 cm
   horizontal / ~30 cm vertical board rulers cap below mature plants; this is the main error
   source and the lowest-effort, highest-impact fix.
2. **Use size class as the primary size metric**; treat cm as supporting.
3. **Keep the board protocol** (number + date legible, two-factor validation) — it caught real
   field errors (the reused board number; date and location mismatches).
4. **One board number per plant** — the `289` reuse shows the value of unique board numbers.

## 7. Data products

- `LEPA_SQL.db` — `Phenotyping` (**741** rows), `Multimedia` (760 occurrence images), views
  `vOccurrenceTraits` (occurrence + phenotyping + summed germplasm yield) and
  `vUnimagedOccurrences` (image-coverage gaps).
- `Multimedia_pipeline/` — the 2025 linking + measurement scripts are archived in `legacy_2025/`;
  the current image→database pipeline is `00_sort_by_date.py … 03_phenotype.py`
  (see [`IMAGE_PIPELINE_GUIDE.md`](IMAGE_PIPELINE_GUIDE.md)) + this report.
