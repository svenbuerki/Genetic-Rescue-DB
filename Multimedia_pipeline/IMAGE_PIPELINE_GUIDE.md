# LEPA image → database pipeline (2026)

Turns field whiteboard photos of *Lepidium papilliferum* into linked database records, with a
**collision-proof naming system** so camera files can never overwrite each other again, and a
**human review gate** before any occurrence is created.

> **Why this was rebuilt.** Cameras reset their `JCN_####` numbering every season, so when 2026
> photos were dropped beside the 2025 set they silently overwrote 56 of them (see
> [`ISSUE_filename_collision.md`](ISSUE_filename_collision.md)). The fix: every image gets a
> globally unique, content-addressed name at ingest, and the original name + date are kept as
> provenance.

---

## Requirements & setup (deploying to another computer)

Plain **Python 3** (developed on 3.14, 3.9+ is fine) + **SQLite**, with two third-party packages and
one system library. On a fresh machine:

1. **Python deps** — `pip install -r Multimedia_pipeline/requirements.txt` (**Pillow** + **pyzbar**).
   Everything else is the standard library (`sqlite3`, `csv`, `json`, `re`, `argparse`, `shutil`,
   `hashlib`, `pathlib`).
2. **zbar system library** — pyzbar needs it to decode the Event-sticker barcodes:
   - macOS: `brew install zbar`, then run python with `DYLD_LIBRARY_PATH=/opt/homebrew/lib …`
   - Debian/Ubuntu: `sudo apt-get install libzbar0` · Fedora: `sudo dnf install zbar`
3. **HEIC → JPG** — board/form photos sometimes arrive as `.heic`: macOS `sips` (built-in); on Linux
   use ImageMagick (`magick`) or libheif (`heif-convert`).
4. **git + GitHub CLI (`gh`)** — for syncing docs/code to the public repo.
5. **OCR & plant measurement run in-session in Claude Code** (subscription) — there are **no local ML
   dependencies**; read-only agent sweeps read the boards/forms and the scripts ingest the results.

| Component | Version used | Purpose |
|---|---|---|
| Python | 3.14 (3.9+) | run the scripts |
| SQLite | 3.51 (bundled with Python) | the database (`LEPA_SQL.db`) |
| Pillow | ≥ 10 | image IO |
| pyzbar + zbar | 0.1.9 / 0.23 | decode CODE128 Event-sticker barcodes |
| git / gh | 2.39 / 2.89 | repo sync |

Run every script from the **`SQL_DB/`** directory (all paths are relative to it).

---

## The full pipeline — two stages (run in order)

**Stage A — Field forms → core records.** OCR the paper field sheets (one Location form, then
Event forms — each over two photos) to create the `Locations`, `Events`, and `Occurrences`
records, *with GPS*. This is the authoritative source for the occurrence hierarchy and **runs first**.

**Stage B — Plant images → multimedia + phenotyping.** Ingest/rename the whiteboard plant photos,
link each to the occurrence its board number names, and measure the plant. The occurrences already
exist (from Stage A), so the board number is just a lookup.

---

## The field board (what each plant photo carries)

Plants are photographed against the field board, which comes in **two sizes** identified by **sticker
colour**: a **standard** board (blue sticker, rulers **1–24 cm**) and a **large** board (orange
sticker, rulers **to 40 cm** on the x-axis, ~33 cm on the y-axis) for big plants. **Both boards carry
the identical labels** — only the ruler range differs.

| Standard (blue) — rulers 1–24 cm | Large (orange) — rulers to 40 cm |
|---|---|
| ![Standard blue board](../Documentation/Figures/LEPA_board_2026.jpg) | ![Large orange board](../Documentation/Figures/LEPA_large_board_2026.jpg) |

The printed labels are the keys the OCR sweep reads, and each maps to one database field — so a single
photo carries the link **and** the measurement:

| Board label | Database field | Notes |
|---|---|---|
| **OC** | `occurrenceID` | unique plant barcode — one per plant, never reused (the Stage B lookup key) |
| **EV** | `eventID` | sampling event (slick spot) |
| **EO** | `EOCode` | Element Occurrence code |
| **L#** | `locationID` | site — resolves to GPS |
| **D** | `eventDate` | |
| **W:** | `occurrenceCrownSize` (cm) | crown width |
| **H:** | `occurrenceHeight` (cm) | plant height |
| colour **sticker** | board size | encodes which board: **blue = standard**, **orange = large** |
| two **rulers** | scale | `x` and `y` axes for image measurement — **read the board's own graduations** (24 cm on the standard board, 40 cm on the large board) |

**For OCR + phenotyping:** first identify the board from its sticker colour / ruler range, then measure
the plant **against that board's own graduations** — the standard board tops out at 24 cm, the large
board at 40 cm, so a plant read against the wrong scale would be badly mis-sized. The field-written
**W/H** double as ground truth (2026 check: within **±1 cm** of the tape; **size class primary, cm
supporting**).

---

## Stage A — Field forms (`field_forms_ocr.py`)

Field crews fill paper forms (templates in `Protocols/`; the `…_with_terms` / `…_w_Terms` versions
annotate each field with its DB column). Photograph them into **`Field_forms/<year>/` in order**:
the **Location form first**, then each **Event over two images** — page 1 = event id / GPS / size /
condition / counts; **page 2 = the occurrenceID (plant barcode) list**. There can be several events
per location and (sometimes) more than one location.

What each form harvests:

| Form page | → table | key fields |
|---|---|---|
| Location | `Locations` | `locationID` (barcode), EO (locality), `locationDecimalLatitude/Longitude`, `landscapeHealth`, DSCN image #, `locationRemarks` |
| Event p1 | `Events` (all new) | `eventID` (barcode), `eventDate`, `locationID`, `eventDecimalLatitude/Longitude`, `eventSizeValue`, `eventDefinition`, `eventCondition`, `organismQuantityFertile/Vegetative`, `measurementValuePlantArea` (2026+), `associatedTaxa` |
| Event p2 | `Occurrences` (all new) | the plant barcodes → `occurrenceID`s, linked to event + location + EO |

**Location revisit vs new:** if a location barcode already exists in `Locations`, **link to it (no
insert)** — most 2026 forms are revisits; only genuinely new sites get a new `Locations` row.
**Events and occurrences are always new.** The plant board number written in the field **equals the
occurrenceID**, so Stage B's photos attach to the records created here.

**Stage A command flow** (`field_forms_ocr.py`, each step dry-run by default + DB backup + log):

```
--worklist                       # ordered list of form images for the in-session OCR sweep
   (run the read-only OCR sweep → results JSON)
--load results.json              # reconstruct hierarchy → review staging (no DB writes)
   (review staging_2026/, put fixes in the override files below)
--commit [--apply]               # GATED LOAD: insert Locations → Events → Occurrences
--forms-mm [--apply]             # link each form image into Multimedia as evidence
```

`--load` writes the review staging (`staging_2026/` Locations/Events/Occurrences) with
`REVISIT` / `NEW_LOCATION` flags and the `_src_image(s)` column (the form photo behind each row).
`--commit` reads the **reviewed** staging and inserts in dependency order (table-only columns already
filled — `taxonID`, units, `stateProvince`/`country`, etc.; dates normalised to `MM-DD-YYYY`); it
**blocks on collisions** (a staged event/occurrence ID already in the DB = a reused barcode) until
resolved. `--forms-mm` ingests the form images under collision-proof names and links them
(`tableID 9`→location, `tableID 11`→event, `type='field form'`) — durable evidence for every record.

### How pages are detected and grouped (robust to ordering)

Detection does **not** rely on image order alone — three independent signals are cross-checked:

1. **Header self-identification (primary).** Each page is classified by its *printed* header —
   "Location Data Collection" (location), "Section 1: Event Identification" (event p1), or
   "Section 4: Fruiting Plants Collection Details" (event p2). A page says what it is, regardless
   of where it falls in the sequence.
2. **Capture order.** Walking the photos in order, the loader tracks the *current location* and
   attaches every following event to it — **a location can have many events** — until the next
   Location form starts a new group. Event p1 + p2 pair as consecutive pages.
3. **Barcode fallback (most robust).** Every Event page 1 also carries its own "Location Unique
   Barcode #", so each event links to its location *by barcode* even if the order is disturbed; the
   loader prefers the stated barcode and only falls back to order-by-current-location when it's missing.

`--load` also **flags anomalies** for review rather than silently mis-pairing — e.g. an event
page-2 with no page-1 before it, an `occurrenceID` ≤ the current max (possible collision), or a
location barcode that doesn't resolve. Nothing is written until you clear the staging.

### Corrections — edit the override files, NOT the generated staging

`--load` regenerates `*_staging.csv` from the OCR each run, so **manual edits to those files are
overwritten.** Put human corrections in two small override files in `staging_2026/`, which `--load`
re-applies every time (so the staging stays reproducible *and* corrected):

- **`occurrence_overrides.csv`** (`eventID, occurrenceIDs, note`) — fix a mis-read plant-barcode
  list. `occurrenceIDs` accepts ranges and lists, e.g. `2359-2368` or `2394,2412-2416`. The event's
  occurrences are replaced and flagged `OVERRIDE`. (A real non-contiguous list with a field note —
  e.g. "went back to add more samples" — is *not* an error; leave it as the OCR read it.)
- **`location_overrides.csv`** (`barcode, locationID, …Location columns…, note`) — fill the
  table-only / GPS-derived fields for a new site (`county`, `locality`, `verbatimElevation`, cleaned
  lat/long). A new location's `locationID` defaults to its barcode; blank cells keep the staged value.
- **`event_overrides.csv`** (`barcode, eventID, note`) — reassign a **reused event sticker** to a
  free `eventID` (e.g. a 2026 sticker `0098` that clashes with a 2025 event → `268`); the event and
  its occurrences are remapped to the new ID.

### Form images as evidence (`--forms-mm`)

After the records are loaded, `field_forms_ocr.py --forms-mm --apply` files each **field form photo**
into `Multimedia` as durable evidence, so every Location and Event can be traced back to the paper
sheet it came from:

- Each form image is **ingested under the collision-proof name** (`LEPA_<date>_<sha8>.jpg`), copied
  into `Multimedia_main/`, with `originalFilename` (the `PXL_…` name), `captureTimestamp`, `sha256`
  kept as provenance — exactly like plant photos.
- **Location form** → one `Multimedia` row, `tableID 9`, `locationID`. **Event form (2 pages)** → two
  rows, `tableID 11`, `eventID`. All carry `type='field form'` and a descriptive `title`.
- Idempotent (skips images already linked) and dry-run by default; backs up the DB on `--apply`.

```sql
SELECT * FROM Multimedia WHERE type='field form';     -- all field-sheet evidence
SELECT identifier, title FROM Multimedia WHERE eventID = 268 AND type='field form';   -- a given event's sheets
```

### Barcode verification — ground-truth the event numbers (`verify_event_barcodes.py`)

Each **Event sticker** carries a printed **CODE128 barcode** with the event number written beneath it.
Reading the *digits* by OCR is error-prone (6→8 and similar misreads); **decoding the barcode itself is
ground truth.** This is now a standard data-quality step.

- **Before loading a new batch:** read the barcode on each event page-1 image so events enter the DB
  with verified numbers, instead of trusting the digit-OCR:
  ```bash
  DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 Multimedia_pipeline/verify_event_barcodes.py \
      --image Field_forms/2026/PXL_20260630_171632194.MP.jpg     # -> prints the true event number
  ```
- **Audit what's already loaded:** decode every event's linked form image and compare to its stored
  `eventID`:
  ```bash
  DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 Multimedia_pipeline/verify_event_barcodes.py --audit
  #   event  269 -> barcode [269]   MATCH      ...      32 events | 32 MATCH | 0 MISMATCH
  ```
- The script is **read-only**. This audit caught **5 mis-entered 2026 events** (stored
  `265/281/282/285/288` → true `263/261/262/265/269`); each was corrected with a backed-up **two-phase
  renumber** (old → temp → true) cascading `Events` + `Occurrences` + `Multimedia`, so chained swaps
  (e.g. 265↔263↔285) can't collide mid-update.
- **Scope:** only the **Event stickers** are barcoded. The plant-board `OC`/`EV` fields are *handwritten*
  (no barcode), so occurrence numbers still rely on board OCR + form reconciliation. And a *field note*
  about which number was skipped can still be wrong — trust the decoded barcode (it showed one 2026 gap
  was at event 277, not 271 as recalled in the field).

### Associated taxa — homogenized to the `Taxonomy` table

Field crews write `associatedTaxa` as free-text shorthand with heavy spelling variation (`cheatrgass`,
`crust`, `BSC`, `festuce`…). The loader **homogenizes it on `--load`** so the field becomes structured:

- Each token is mapped through **`taxa_lexicon.csv`** (a local `variant → standard_name → taxonID`
  table) to a **`Taxonomy.taxonID`**; the event's `associatedTaxa` is stored as a **`;`-separated list
  of taxonIDs** (e.g. `2;4;19`), and the **verbatim original is preserved in `associatedTaxaOriginal`**
  (Term 71) so nothing is lost and the mapping is auditable.
- Tokens not in the lexicon are left in a **`_taxa_unknown`** review column in the staging (never
  guessed) — review them, then add the taxon to `Taxonomy` + a row to `taxa_lexicon.csv`.
- The **`Taxonomy`** table is Darwin Core (`family / genus / specificEpithet / taxonRank / WFOID /
  taxonomicStatus`) with a **`taxonRemarks`** column holding the common name + confidence + expert
  notes (e.g. *fescue = Vulpia microstachys, confirmed by Ian; NOT Festuca*). Lexicon variants and
  common names (incl. field experts') resolve to the same taxonID, so future forms normalize the same way.

---

## Stage B — Plant images

### Folder convention (what the field team does)

**All raw images MUST be saved under `Multimedia_images/`** — this is the single source of truth
for original photographs. Save each field day's images into a **date subfolder inside the year
folder**:

```
Multimedia_images/                       ← RAW images live here ONLY (one source of truth)
  2025/2025-07-10/  JCN_0294.JPG …       ← one folder per field day (ISO date, YYYY-MM-DD)
  2026/2026-06-22/  EO70 2327.jpg …
  2026/2026-06-24/  JCN_0294.JPG …       ← same camera name as 2025 — now harmless (different folder)
```

That's the only manual step. The scripts do the rest and **never modify `Multimedia_images/`** — it
is immutable. Everything in **`Multimedia_main/` is derived** (renamed copies the scripts generate);
never put raw images there by hand. (Flat `Multimedia_images/<year>/` is also accepted, e.g. for
legacy; `00_sort_by_date.py` will move them into date subfolders.)

## The scripts (run in order; each is dry-run by default and logs to `PIPELINE_LOG.md`)

| Step | Script | What it does |
|---|---|---|
| **00** | `00_sort_by_date.py` | Sorts loose images in a year folder into `<year>/<date>/` using EXIF (DB `occurrenceDate` fallback for EXIF-stripped files). One-time helper for already-flat folders. |
| **01** | `01_ingest_register.py` | The core. Copies every image into the flat main folder `Multimedia_main/` under a unique name **`LEPA_<YYYY-MM-DD>_<sha8>.jpg`** (date for sorting, SHA-256 prefix for uniqueness → re-ingesting the same bytes is a no-op). Preserves EXIF (verbatim copy). Updates `Multimedia`: existing images get their `identifier` migrated and `originalFilename / fileYear / folderDate / captureTimestamp / sha256` filled; new images are registered to await OCR. Writes `Multimedia_main/file_registry.csv`. |
| **02** | `02_ocr.py` | `--worklist` lists images not yet linked to an occurrence → the OCR sweep reads each board → `--load` resolves the readings and writes a **review staging set** (`staging_2026/`, with `NEW_EO`/`NEEDS_LOCATION`/`OCC_EXISTS` flags). Occurrences are **not** auto-created — that's the gated load. |
| **03** | `03_phenotype.py` | `--worklist` lists occurrence images with **no** `Phenotyping` row → the measurement sweep reads each plant → `--load --apply` inserts `Phenotyping` rows (linked to the source image), backing up the DB first. |

**Idempotency rule throughout:** an image is only OCR'd if it isn't linked to an occurrence yet,
and only phenotyped if its occurrence has no measurement yet. Re-running any step just shrinks its
worklist — nothing is ever redone or duplicated.

### The OCR / measurement step itself

Steps 02 and 03 split the work into **deterministic plumbing (Python)** + **the actual reading
(an in-session Claude Code agent sweep)**: the worklist gives the agents the image paths, they read
the boards / measure the plants **in-session under the subscription (no per-image API cost)**, and
emit a results CSV that `--load` ingests. Agents are **read-only** (no shell/PIL) to keep the run
clean. This is the same subscription-based method used for the 2025 dataset.

## Running it

```bash
cd Multimedia_pipeline
python3 01_ingest_register.py            # dry-run: preview the renames + DB updates
python3 01_ingest_register.py --apply    # copy to Multimedia_main/, migrate identifiers (backs up DB)

python3 02_ocr.py --worklist             # -> work/ocr_worklist.csv  (then run the OCR sweep)
python3 02_ocr.py --load work/ocr_results.csv     # -> staging_2026/ for human review

python3 03_phenotype.py --worklist       # -> work/phenotype_worklist.csv (then run the measure sweep)
python3 03_phenotype.py --load work/phenotype_results.csv --apply   # insert Phenotyping (backs up DB)
```

## Provenance & safety

- **`Multimedia` new columns:** `originalFilename`, `fileYear`, `folderDate`, `captureTimestamp`
  (EXIF), `sha256`. `identifier` is the unique `LEPA_…` name; the file lives in `Multimedia_main/`.
- **`Multimedia_main/file_registry.csv`** — the lookup table (`new_name ↔ original_name, year,
  folderDate, sha256, capture, source path, multimediaID, action`).
- **`PIPELINE_LOG.md`** — every `--apply` appends a dated entry (the running documentation).
- Every DB write **backs up `LEPA_SQL.db` first** (`*.bak-<step>-<timestamp>`); steps are dry-run
  until `--apply`. Year/date folders are copied from, never modified.

## Current state (2026-06-27)

- **948 images** ingested (2025: 805 across 17 field days; 2026: 143 across 4 days), **809
  `Multimedia` identifiers migrated** to the dated scheme. The one exception, occ **220**, is an
  image that was inadvertently deleted (record retained — [`ISSUE_filename_collision.md`]).
- Pending work (worklists ready): **139 new 2026 images** to OCR, **44 occurrence images** to
  phenotype. The h/w validation case study (board-written `h`/`w` vs image estimate) runs through
  these same steps — see [`REPORT_2026_pipeline_dryrun.md`](REPORT_2026_pipeline_dryrun.md).

## Legacy

The 2025 build (`00_link_named_files.py` … `06_phenotyping_schema.py`, `config.py`) is archived in
[`legacy_2025/`](legacy_2025/); it created the `Multimedia`/`Phenotyping` tables and loaded the
2025 campaign. The `work/` folder holds regenerable intermediates (incl. `work/full/`, which
served as the local backup that recovered the 56 overwritten 2025 images).
