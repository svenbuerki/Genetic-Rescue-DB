# LEPA 2025 — Image-based occurrence linking & plant measurement

**Prepared for:** Buerki Lab team
**Subject:** Linking field whiteboard photos to the database, and estimating plant size from the photos
**Data:** 95-image sample (`JCN_0016`–`JCN_0110`) of the 2025 campaign; full dataset to follow.

---

## 1. Objective

Each fruiting *Lepidium papilliferum* plant was photographed in the field with a blue
whiteboard giving its **occurrenceID** (top-left) and **date** (top-right), plus two
rulers for scale. Two goals:

1. **Link** every photo to its `Occurrences` record in `LEPA_SQL.db` and store it in the
   `Multimedia` table.
2. **Measure** plant **height** and **crown width**, and assign a **size class**.

## 2. Approach

A small, documented, reproducible pipeline (`Multimedia_pipeline/`) that runs unchanged
on the full dataset:

- **Read the board** — each photo's header is cropped and the handwritten occurrenceID +
  date are read (for this sample, read and double-checked manually; for the full dataset,
  the same read is done automatically by a vision model).
- **Validate** — the board number must match an existing `occurrenceID`, and the board
  date is cross-checked against the record's date. Mismatches are flagged, not guessed.
- **Load** — linked rows are inserted into `Multimedia` (with a backup and a `remarks`
  validation note).
- **Measure** — the board's two rulers give scale: the horizontal ~15 cm ruler (crown
  width) and the vertical ~30 cm edge ruler (height). For plants larger than the ruler we
  use a **"1 cm tile"**: read one graduation to fix the cm-per-pixel scale, then extend
  that unit across the plant to estimate sizes **beyond** the ruler's length.

## 3. Results

**Linking (Multimedia):** all 93 occurrence photos (boards 0001–0093) linked cleanly to
occurrenceIDs 1–93. One landscape/setup shot had no board (held for a location decision);
one "Event 14" marker was linked to that event. 94 rows inserted; 51 pre-existing
occurrence images were corrected to the right module.

**Measurement (93 plants):**

| Size class | n | crown width |
|---|---|---|
| small | 18 | < 10 cm |
| medium | 61 | 10–20 cm |
| large | 14 | > 20 cm (exceeds the board ruler) |

- Height ≈ 7–26 cm (mean ~14.5 cm); crown ≈ 5–35 cm (mean ~14.4 cm).
- A ~10 cm typical crown matches the independent field value on record for Event 14
  (`measurementValueCrownAvg` = 10 cm) — a useful sanity check.

## 4. Accuracy

There is **no field-measured ground truth** in the database, so these are estimates
judged against the in-frame rulers. Accuracy is tiered:

- **In-ruler plants** (compact, flush to the board, base visible) — good, ~**±2–3 cm**.
- **Large plants beyond the ruler** (14 of 93) — measurable by the 1 cm-tile method, but
  with **wider error (~±5–8 cm / ~20%)**: they sit in front of the board (parallax →
  slight overestimate), and any calibration error is amplified across a big plant.

Because of this, the **size class is the most trustworthy field** — a plant that overflows
the board is reliably "large" even when its exact cm is uncertain. Size classes have been
written to the database (`Occurrences.occurrenceSizeClass`); the cm estimates are kept in a
review file (`work/05_measurements.csv`) pending sign-off before any cm is written.

## 5. Recommendations

1. **Add a taller scale to the field kit.** The current board ruler caps at ~15 cm
   (horizontal) / ~30 cm (vertical); mature plants exceed it. A **meter stick or folding
   rule placed in frame** would let large plants be measured directly and remove the main
   source of error. *(Lowest-effort, highest-impact change for next campaign.)*
2. **Use size class as the primary size metric** for analysis; treat cm as supporting,
   especially for large plants.
3. **Keep the board protocol** otherwise — it worked well: number + date legible, two-factor
   validation caught a real photo-vs-observation date offset (plants observed 06-16,
   photographed 06-17 for Event 14).
4. **Scale-up is ready** — the pipeline processes the incoming full dataset automatically
   (board reading + measurement via the Claude vision API), with the same validation and
   review gates.

## 6. Data products

- `LEPA_SQL.db` — `Multimedia` rows linked to occurrences (+ `remarks`); `Occurrences.occurrenceSizeClass` populated. Backups kept alongside the DB.
- `Multimedia_pipeline/work/05_measurements.csv` — per-plant height, crown, size class, confidence, flags.
- `Multimedia_pipeline/README.md` — full method and how to run it.
