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

## Folder convention (what the field team does)

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
