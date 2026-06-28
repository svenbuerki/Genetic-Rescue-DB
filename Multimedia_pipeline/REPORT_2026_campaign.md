# LEPA 2026 — field-form + plant-image processing (campaign report)

**Prepared for:** Buerki Lab team
**Subject:** Digitizing the 2026 field sheets and plant photos into `LEPA_SQL.db`
**Pipeline:** two stages — **A: forms → records**, then **B: plant images → multimedia + phenotyping**
(full method: [`IMAGE_PIPELINE_GUIDE.md`](IMAGE_PIPELINE_GUIDE.md); data-quality status: [`DATA_QUALITY.md`](DATA_QUALITY.md))

---

## 1. What was loaded (DB deltas)

| Table | Added (2026) | Notes |
|---|---|---|
| `Locations` | **+1** | EO69 (loc 41, New Plymouth/Payette) — the one genuinely new site; the other 5 are revisits (link, no insert) |
| `Events` | **+17** | with GPS; one reused sticker (`0098`) reassigned to a free `eventID` 268 |
| `Occurrences` | **+84** | the seed-collected plants (forms' Section 4), IDs 2318–2416 |
| `Multimedia` | **+120** | 40 field-form images (evidence) + 80 plant images linked by board# |
| `Phenotyping` | **+76** | image-measured height/crown/size for the matched plants |

Every step ran staged + gated, with a DB backup and a `PIPELINE_LOG.md` entry.

## 2. Stage A — field forms → Locations / Events / Occurrences

40 form photos (Location form + Event forms, 2 pages each) were OCR'd by a read-only agent sweep,
pages classified by their printed header, and the hierarchy reconstructed from the barcodes + capture
order. Table-only columns (`EOID`, `taxonID`, units, `stateProvince`/`country`, …) were auto-filled;
human corrections went through three persistent override files (an OCR'd occurrence range corrected
`2354–2362`→`2359–2368`; a non-contiguous list confirmed real from the field note "went back to add
more samples"; the EO69 GPS/county/locality filled). The **40 form images are now in `Multimedia`** as
evidence (`type='field form'`, `tableID 9`→location / `tableID 11`→event).

## 3. Stage B — plant images → multimedia + phenotyping

135 plant photos were OCR'd + measured (read-only sweep). Board number = occurrence barcode, so each
was matched to the Stage-A occurrences:

- **80 matched** → linked as occurrence images (`tableID 13`) + **76 phenotyped** (4 had no
  measurable plant). Covers **77 distinct occurrences**.
- **46 photographed-but-not-collected** (board# not in the forms' Section 4) — staged for review in
  `staging_2026/stageB_unmatched_review.csv`, **not loaded**. Dominated by **33 EO38** plants (see §5).
- **7 collected occurrences have no image** in the batch (see §5).
- **8 context/setup frames** (no measurable plant; e.g. board-placement shots).

### 3a. h/w validation (the headline result)

23 boards carried **field-written height/width** (the EO118 adapted sheets). Comparing the
**image-measured** value to the **field-written** value — the first true ground-truth check we've had:

| | image − field (median) | within ±2 cm |
|---|---|---|
| **height** | **+1.0 cm** | **20 / 21** |
| **width / crown** | **+1.0 cm** | **20 / 21** |

The image phenotyping reproduces the field tape to **~±1 cm**. This validates the in-image
measurement technique against ground truth (not just self-consistency) and supports continuing to use
it at scale — with **size class as the primary metric, cm as supporting**.

## 4. Reused-barcode collisions handled

The recurring 2026 theme — IDs reused across years — appeared again and was caught by the gated load:
the event sticker `0098` clashed with a 2025 event and was reassigned to **eventID 268**; the new
EO69 location barcode `0041` is a genuinely new `locationID 41`. (Same root cause as the JCN filename
collisions; the pipeline collision-checks every ID against the DB.)

## 5. Open items (tracked on GitHub)

- **[#7](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/7) — EO38 forms missing.** 33 EO38
  (EO38-6) plants were photographed (boards ~2281–2317) but no EO38 Location/Event form was in the
  batch, so they have no hierarchy to attach to. Awaiting the EO38 field sheets, then they run A→B.
- **[#6](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/6) — 7 collected occurrences without
  an image** (EO76 ×5 event 244; EO69 ×1 event 285; EO118 ×1 event 266). Possibly un-photographed, or
  a board# mis-read among the unmatched set — to confirm.
- The 9 EO118 photographed-not-collected plants + the 8 context frames are minor review items.

## 6. Data products

- `LEPA_SQL.db` — Locations 40, Events 254, Occurrences 894, Multimedia 930, **Phenotyping 817**.
- `staging_2026/` — the reviewed staging + the 3 override files + `stageB_*` staging (incl. the
  unmatched-review list).
- `field_forms_ocr.py` (Stage A: `--worklist/--load/--commit/--forms-mm`) + `stageB_load.py`.
