# ISSUE (major) — camera filenames repeat across years; 2026 frames overwrote 2025 images

**Severity:** high (data-management; no *database* data lost, but local image files were overwritten).
**Found:** 2026 dry-run, by comparing each `Multimedia.identifier` file's EXIF capture year to its occurrence's year.

## What happened
The field camera **resets its `JCN_####` numbering each season**. When the 2026 images were
copied into the same flat `Multimedia_images/` folder as the 2025 set, **57 frames reused a 2025
filename** and overwrote it. So a row like `Multimedia.identifier = 'JCN_0294.JPG' → occ 326
(EO18, 7/10/25)` now points at a file that on disk is a **2026 EO118 plant**.

The same root cause produced the named-file deletion: **`EO27 Figgins - Occurrence 220.jpg`
(occ 220) is gone** from Google Drive (deleted inadvertently) and has no local copy.

## Impact
- **56 occurrence images overwritten** — occ **1–34** (EO38/EO76, 6-17-2025, `JCN_0017–0050`)
  and occ **298–326** (EO18, 7-10-2025, `JCN_0263–0294`). Full list + per-file recoverability:
  [`staging_2026/REIMPORT_2025_from_backup.csv`](staging_2026/REIMPORT_2025_from_backup.csv).
- **No measurement/data loss:** all 56 occurrences were already phenotyped in 2025, and the
  **original images survive locally** at full resolution in `Multimedia_pipeline/work/full/`
  (the 2025 crop-pipeline copies; EXIF stripped but boards fully readable — verified
  `work/full/JCN_0294.jpg` = board `0326 EO18-7 7/10/25`).
- **1 image truly lost:** occ **220** (`EO27 Figgins - Occurrence 220.jpg`) — not in `work/full/`,
  not on Drive. Keep the occurrence record; flag the image as lost.

## What to reimport from 2025
- **56 files** → restore the 2025 originals. **Two options:**
  1. **Local, immediate** — copy from `Multimedia_pipeline/work/full/<JCN>.jpg` into
     `Multimedia_images/2025/` (full-res, board-readable, but EXIF was stripped in 2025).
  2. **Pristine** — re-pull the 56 from the Google Drive 2025 archive (keeps original EXIF).
- **occ 220** → unrecoverable; record kept, image flagged lost.

## Fix (going forward) — already started + tooling added
1. **Year folders (done by Sven):** `Multimedia_images/2025/` (755) and `2026/` (135). After the
   split there are **0 cross-year duplicate basenames**, so the live collision is contained.
2. **Unique names at ingest:** `Multimedia_pipeline/01_ingest_register.py` copies each image from a
   `<year>/<date>/` folder into the flat main folder `Multimedia_main/` under a **globally unique
   name** `LEPA_<YYYY-MM-DD>_<sha8>.jpg` (SHA-256 prefix → deterministic, auto-dedups identical
   re-uploads). **EXIF is preserved** (verbatim byte copy — no re-encode); the capture timestamp,
   original filename, year, folderDate and sha256 are all stored on the `Multimedia` row and in
   `Multimedia_main/file_registry.csv`. `Multimedia.identifier` was migrated to these names.
3. **Content-addressed = collision-proof:** two different images can never share a name (different
   bytes → different hash), so the 2025/2026 `JCN_0294` pair now resolve to distinct names.

## Action items
- [ ] Restore the 56 (option 1 now, or option 2 for pristine EXIF).
- [ ] Mark occ 220 image as lost in `Multimedia.remarks`; raise on GitHub.
- [ ] Migrate `Multimedia.identifier` to unique `<year>_<id>.jpg` names via `00b_ingest_uuid.py`.
