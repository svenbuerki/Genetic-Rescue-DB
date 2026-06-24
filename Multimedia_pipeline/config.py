"""
Central configuration for the LEPA Multimedia ingestion pipeline.

Every tunable path / convention lives here so the same scripts run unchanged
on the 95-image sample and on the full multi-thousand-image dataset.
Adjust IMAGE_DIR / DB_PATH for a new batch; nothing else needs to change.
"""
from pathlib import Path

# --- Locations -------------------------------------------------------------
ROOT       = Path(__file__).resolve().parent.parent          # .../SQL_DB
IMAGE_DIR  = ROOT / "Multimedia_images"                       # source JPGs
DB_PATH    = ROOT / "LEPA_SQL.db"                             # target SQLite DB
WORK_DIR   = Path(__file__).resolve().parent / "work"        # all intermediate artefacts
FULL_DIR   = WORK_DIR / "full"                                # downscaled whole frames
CROP_DIR   = WORK_DIR / "crop"                                # top-of-board crops (header w/ ID + date)

# --- Pipeline data files (one row per image, joined across steps) ----------
METADATA_CSV  = WORK_DIR / "01_metadata.csv"    # filename, exif_date, width, height
BOARDS_CSV    = WORK_DIR / "02_boards.csv"      # filename, board_id, board_date, has_board, confidence, notes
VALIDATED_CSV = WORK_DIR / "03_validated.csv"   # + status, matched occurrenceID/locationID
MEASURE_DIR   = WORK_DIR / "measure"            # plant+ruler crops for measurement
MEASUREMENTS_CSV = WORK_DIR / "05_measurements.csv"  # occurrenceID, height_cm, crown_cm, confidence, ...

# --- Image processing ------------------------------------------------------
IMAGE_GLOB      = "*.JPG"      # source extension (case-sensitive on this disk)
FULL_MAX_PX     = 1300         # long edge of the context downscale
CROP_TOP_FRAC   = 0.45         # keep the top 45% of the frame (the whiteboard header lives here)
CROP_OUT_WIDTH  = 1500         # width to upscale the header crop to, for legible OCR

# --- Multimedia row conventions (mirror the 52 pre-existing rows) ----------
MM_TYPE              = "field image"
MM_FORMAT            = "jpeg"
MM_STORAGE           = "Google Drive"
MM_LICENSE           = ""               # left blank in existing rows
MM_RIGHTSHOLDER      = ""               # left blank in existing rows
TITLE_OCCURRENCE     = "fruiting plant in the field"   # whiteboard images
TITLE_LOCATION       = "field site / location image"   # whiteboard-less images

# tableID semantics come from the TableModules table:
#   9  -> Locations   (whiteboard-less site / context photos)
#   13 -> Occurrences (a whiteboard documenting one occurrence)
TABLEID_OCCURRENCE   = 13
TABLEID_LOCATION     = 9
TABLEID_EVENT        = 11

# Human-confirmed targets for images the validator can't resolve on its own
# (filename -> {locationID|eventID}). Applied in step 03, so the decision is
# recorded here rather than hand-edited into a CSV.
MANUAL_TARGETS = {
    "JCN_0055.JPG": {"eventID": 14},   # board reads "Event 14" (eventDate 06-16-2025, locationID 2)
}

# Existing occurrence images were mistakenly stored as tableID 9; fix them to 13.
FIX_EXISTING_TABLEID_FROM = 9
FIX_EXISTING_TABLEID_TO   = 13

# A free-text validation column added to Multimedia: "valid", or the reason to review.
REMARKS_COLUMN = "remarks"
REMARKS_FIX_TABLEID = "valid; tableID corrected 9->13 (occurrence image)"
