# LEPA Multimedia ingestion pipeline

Reproducible pipeline that inspects field photos of *Lepidium papilliferum*
whiteboards, reads the handwritten **occurrenceID** and **date**, validates each
against the `Occurrences` table of `LEPA_SQL.db`, and writes linked rows into the
`Multimedia` table.

Built and verified on the **95-image sample** (`Multimedia_images/JCN_0016.JPG` …
`JCN_0110.JPG`); designed to run unchanged on the full multi-thousand-image dataset
by pointing `config.py` at a new folder.

## The whiteboard

Each occurrence photo shows a blue-framed whiteboard held in the field:

```
 ┌───────────────────────────────┐
 │  0001                6/17/25   │   top-left  = occurrenceID
 │                                │   top-right = date (M/D/YY)
 │            [ ruler ]           │
 │            the LEPA plant      │
 └───────────────────────────────┘
```

**Validation principle (two-factor):** the board number must equal an
`Occurrences.occurrenceID`, and the board date is cross-checked against that row's
`occurrenceDate`. The number is the link; the date is an independent confirmation.

## Pipeline steps

| Step | Script | Input → Output |
|---|---|---|
| 0 *(optional)* | `00_link_named_files.py` | photos named `… Occurrence NNN.jpg` (occurrenceID in the filename, no whiteboard) → Multimedia rows, no OCR. Dry-run by default; `--apply` to write. |
| 1 | `01_extract_and_crop.py` | source JPGs → `work/01_metadata.csv` (EXIF capture date) + `work/full/` (context downscales) + `work/crop/` (header crops with the ID + date) |
| 2 | *(in-session, preferred)* / `02_ocr_boards.py` | `work/crop/` → `work/02_boards.csv` (board_id, board_date, has_board, confidence). **Preferred for this lab:** Claude Code reads the crops in-session — this is included in the Claude Code subscription, so there is **no extra per-image charge**, and every read is validated against the DB. `02_ocr_boards.py` is an **optional** headless alternative that OCRs each crop via the **Anthropic API** (separate pay-as-you-go account, `ANTHROPIC_API_KEY`) — use only for fully-unattended runs. Both write the same `02_boards.csv`. |
| 3 | `03_validate.py` | `01_metadata.csv` + `02_boards.csv` + DB → `work/03_validated.csv` (resolved occurrenceID/locationID/eventID, `tableID`, `createDate`, `remarks`, `status`) |
| 4 | `04_load_db.py` | `03_validated.csv` → `LEPA_SQL.db` (backup, fix existing tableIDs, insert Multimedia rows). **Dry-run by default; `--apply` to write.** |
| 5 *(optional)* | `05_measure.py` | occurrence images → `work/05_measurements.csv` (plant **height** + **crown** in cm, read off the board rulers via Claude vision). **Review-only by default; `--write` populates `Occurrences.occurrenceHeight`/`occurrenceCrownSize` for high-confidence, non-`exceeds_ruler` rows.** |

Run order:

```bash
cd Multimedia_pipeline
python3 01_extract_and_crop.py
python3 02_ocr_boards.py          # or hand-author work/02_boards.csv for a sample
python3 03_validate.py
python3 04_load_db.py             # dry run — prints the plan
python3 04_load_db.py --apply     # writes (backs up DB first)
```

## What gets written to `Multimedia`

Per inserted row (conventions in `config.py`, mirroring the 52 pre-existing rows):

| column | value |
|---|---|
| `identifier` | filename, e.g. `JCN_0017.JPG` |
| `type` / `format` | `field image` / `jpeg` |
| `createDate` | **EXIF capture date** of the photo (per image, MM-DD-YYYY) |
| `title` | `fruiting plant in the field` (occurrence) / `field site / location image` (location) |
| `multimediaStorage` | `Google Drive` |
| `tableID` | **13 = Occurrences** (occurrence images) / **9 = Locations** (whiteboard-less) |
| `occurrenceID` | the validated board number (occurrence images) |
| `remarks` | **`valid`**, or a `REVIEW - …` explanation (see below) |

The loader also:
- **fixes the 51 pre-existing occurrence rows** stored as `tableID = 9` → `13`
  (9 is *Locations*, 13 is *Occurrences* per `TableModules`), stamping their `remarks`;
- **adds the `remarks` column** to `Multimedia` if it doesn't exist.

### `remarks` values

- `valid` — board number = occurrenceID and board date = occurrenceDate.
- `valid - occurrenceID N confirmed; board/photo date … differs from occurrenceDate …`
  — number confirmed; the plant was **observed** on one day and **photographed** the
  next (the Event-14 occurrences: observed 06-16, photographed 06-17). Still linked.
- `REVIEW - …` — needs a human decision: no whiteboard (Location image, locationID to
  confirm), an `Event N` marker board (Event image, eventID to confirm), or a board
  number with no matching occurrenceID. These are **not** auto-inserted.

## Sample results (95 images)

| outcome | n | action |
|---|---|---|
| `valid` (ok) | 77 | inserted as occurrence images |
| `valid` w/ 1-day observe-vs-photo note | 16 | inserted as occurrence images |
| `REVIEW` needs_location (`JCN_0016`, landscape) | 1 | held for locationID |
| `REVIEW` needs_event (`JCN_0055`, "Event 14") | 1 | held for eventID |

→ 93 occurrence images (boards 0001–0093) link cleanly to occurrenceIDs 1–93.

**Filename ↔ board offset is not constant** (JCN_0017→0001 is +16; after the
`JCN_0055` "Event 14" insert it becomes +17, so JCN_0110→0093). Every board is read;
the offset is never assumed.

## Plant measurement (step 05) — accuracy

The board carries two rulers: the **horizontal Zukamo ruler** (~15 cm, across the
board) for **crown width**, and the **vertical steel ruler** (~30 cm, right edge) for
**height**. `05_measure.py` reads them via Claude vision and estimates each plant.

Accuracy is **inherently limited** — there is no field-measured ground truth in the
DB to calibrate against (`occurrenceHeight`/`occurrenceCrownSize` were empty):

- **Clean cases** — plant in front of the white board, base visible, within the ruler
  span — roughly **±2–3 cm**.
- **Bushy plants that exceed the board/ruler** (`exceeds_ruler=yes`) — measured by the
  **"1 cm tile"** method: read one graduation to fix cm-per-pixel, then extend that unit
  past the ruler's end to estimate the full extent. This gives a real estimate (not just a
  lower bound) but with **wider error (~±5–8 cm / ~20%)** — parallax (plant in front of the
  board) and amplified calibration error.

**Size class is the robust output.** A plant that overflows the board is reliably
*large* even when its exact cm is uncertain, so `sizeClass` (small/medium/large) is derived
from crown width + `exceeds_ruler` and written to `Occurrences.occurrenceSizeClass`. The
cm values stay review-only until signed off.

Prototype on 4 sample images (`work/05_measurements.csv`):

| occ | height | crown | confidence | |
|---|---|---|---|---|
| 0046 | ~11 cm | ~9 cm | high | clean |
| 0001 | ~14 cm | ~7 cm | medium | wispy single stem |
| 0084 | ~13 cm | ~12 cm | medium | base occluded |
| 0048 | ~22 cm | ~28 cm | low | exceeds ruler — lower bound |

Sanity anchor: `Events.measurementValueCrownAvg` = 10 cm (Event 14), consistent with
the small/medium estimates. **Recommendation:** treat results as coarse size classes;
review before `--write`, and only auto-write high-confidence, non-`exceeds_ruler` rows.

## Reading method & cost

Board reading (step 2) can run two ways:
- **In-session via Claude Code (preferred here)** — Claude reads the crops directly; this
  is part of the Claude Code subscription, so there is **no extra per-image cost**. Slower
  (interactive, batched) but every read is cross-checked against the database. This is the
  method used for the 2025 dataset.
- **Anthropic API via `02_ocr_boards.py`** — a separate **pay-as-you-go** account
  (`ANTHROPIC_API_KEY`), **not** included in the Claude Code subscription. Faster and
  fully unattended; use only when a headless run is needed.

## Notes / requirements

- **Close the DB in any SQLite GUI before `--apply`** — an open write-lock makes the
  loader abort cleanly (transaction rolled back, backup kept). Reading is unaffected.
- `04_load_db.py` is **idempotent**: an image whose `identifier` already exists is skipped.
- Dependencies: Python 3 + Pillow (steps 1) and the `anthropic` SDK (step 2 automated
  OCR only). `sqlite3` is in the standard library.
- `work/` holds only regenerable intermediates and can be deleted.
