#!/usr/bin/env python3
"""
STEP 01 - Extract metadata and produce review crops.

For every source image this script:
  1. reads the EXIF capture timestamp (DateTimeOriginal) -> createDate (MM-DD-YYYY),
  2. writes a downscaled whole-frame copy to work/full/   (context: is there a board?),
  3. writes an upscaled top-of-frame crop to work/crop/   (the whiteboard header that
     carries the handwritten occurrenceID and date).

Output: work/01_metadata.csv  (filename, exif_date, width, height)

The crops are what step 02 (OCR) reads. Cropping to the header makes the
handwritten number/date large and isolated, which is what makes reading it
reliable at scale.

Usage:  python3 01_extract_and_crop.py
Idempotent: re-running overwrites the crops and CSV.
"""
import csv
import sys
from PIL import Image

import config as C

# EXIF tag ids (avoids importing the whole ExifTags name map)
TAG_DATETIME_ORIGINAL = 36867   # 'DateTimeOriginal'  -> 'YYYY:MM:DD HH:MM:SS'
TAG_DATETIME          = 306     # 'DateTime' (fallback)


def exif_date(img):
    """Return capture date as MM-DD-YYYY, or '' if unavailable."""
    exif = img.getexif()
    raw = exif.get(TAG_DATETIME_ORIGINAL) or exif.get(TAG_DATETIME)
    if not raw:
        return ""
    try:
        date_part = str(raw).split(" ")[0]          # 'YYYY:MM:DD'
        y, m, d = date_part.split(":")
        return f"{m}-{d}-{y}"                        # 'MM-DD-YYYY' (matches DB convention)
    except ValueError:
        return ""


def process(path):
    with Image.open(path) as img:
        w, h = img.size
        date = exif_date(img)
        img = img.convert("RGB")

        # 1) context downscale (full frame)
        full = img.copy()
        full.thumbnail((C.FULL_MAX_PX, C.FULL_MAX_PX))
        full.save(C.FULL_DIR / f"{path.stem}.jpg", quality=85)

        # 2) header crop: top CROP_TOP_FRAC of the frame, upscaled for legibility
        crop = img.crop((0, 0, w, int(h * C.CROP_TOP_FRAC)))
        if crop.width != C.CROP_OUT_WIDTH:
            ratio = C.CROP_OUT_WIDTH / crop.width
            crop = crop.resize((C.CROP_OUT_WIDTH, int(crop.height * ratio)))
        crop.save(C.CROP_DIR / f"{path.stem}.jpg", quality=88)

    return {"filename": path.name, "exif_date": date, "width": w, "height": h}


def main():
    for d in (C.WORK_DIR, C.FULL_DIR, C.CROP_DIR):
        d.mkdir(parents=True, exist_ok=True)

    images = sorted(C.IMAGE_DIR.glob(C.IMAGE_GLOB))
    if not images:
        sys.exit(f"No images matching {C.IMAGE_GLOB} in {C.IMAGE_DIR}")

    rows = []
    for i, path in enumerate(images, 1):
        rows.append(process(path))
        if i % 10 == 0 or i == len(images):
            print(f"  {i}/{len(images)} processed", flush=True)

    with open(C.METADATA_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "exif_date", "width", "height"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {C.METADATA_CSV} ({len(rows)} rows)")
    print(f"Crops in {C.CROP_DIR}, full frames in {C.FULL_DIR}")


if __name__ == "__main__":
    main()
