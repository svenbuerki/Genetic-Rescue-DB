#!/usr/bin/env python3
"""
STEP 05 (optional) - Estimate plant height + crown width from the whiteboard rulers.

For every occurrence image (has_board == 'yes' in 02_boards.csv) this:
  1. crops the lower part of the frame (plant + the board's rulers) at high resolution,
  2. asks the Claude vision API to read the rulers and estimate the plant's
     height (base -> tallest point) and crown width (widest horizontal spread) in cm,
  3. writes work/05_measurements.csv joined to occurrenceID.

The two scale references on the board:
  - horizontal "Zukamo" ruler taped across the board (~15 cm graduated)  -> crown width
  - vertical steel ruler on the right edge (~30 cm)                       -> height

ACCURACY IS LIMITED - read before trusting the numbers:
  - Clean cases (plant in front of the white board, base visible, within the ruler
    span) are good to ~+/-2-3 cm.
  - Bushy plants that exceed the board/ruler give only a rough LOWER BOUND
    (`exceeds_ruler=yes`); the ~15 cm ruler can't span them and the plant sits in
    front of the board (parallax). A large share of mature plants fall here.
  - There is no field-measured ground truth in the DB to calibrate against.

So this step is REVIEW-ONLY by default: it writes a CSV for a human to check.
`--write` will populate Occurrences.occurrenceHeight / occurrenceCrownSize, but ONLY
for rows at or above --min-confidence and not flagged exceeds_ruler, after a backup.

Usage:
  python3 05_measure.py                         # measure all occurrence images -> CSV
  python3 05_measure.py --limit 5               # smoke-test on 5
  python3 05_measure.py --write --min-confidence high   # write high-confidence rows to DB
"""
import argparse
import base64
import csv
import json
import shutil
import sqlite3
import sys
from datetime import datetime

from PIL import Image

import config as C

MODEL = "claude-opus-4-8"
CONF_RANK = {"low": 0, "medium": 1, "high": 2}


def size_class(crown_cm, exceeds_ruler):
    """Coarse size class from crown width. Robust even where exact cm is not:
    a plant that overflows the board is 'large' regardless of the (unreliable) number."""
    if exceeds_ruler or crown_cm >= 20:
        return "large"
    if crown_cm >= 10:
        return "medium"
    return "small"

SCHEMA = {
    "type": "object",
    "properties": {
        "plant_visible": {"type": "boolean",
                          "description": "is a measurable LEPA plant visible in front of the board?"},
        "height_cm": {"type": "number", "description": "base to tallest point, cm; 0 if not measurable"},
        "crown_cm": {"type": "number", "description": "widest horizontal spread, cm; 0 if not measurable"},
        "exceeds_ruler": {"type": "boolean",
                          "description": "true if the plant is larger than the board/ruler so the value is a lower bound"},
        "ruler_used": {"type": "string", "description": "which ruler(s) gave the scale"},
        "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        "notes": {"type": "string"},
    },
    "required": ["plant_visible", "height_cm", "crown_cm", "exceeds_ruler",
                 "ruler_used", "confidence", "notes"],
    "additionalProperties": False,
}

PROMPT = (
    "This is the lower part of a field photo of a Lepidium papilliferum plant in front of "
    "a blue-framed whiteboard. Two rulers give scale:\n"
    "- a horizontal black 'Zukamo' ruler taped across the board, graduated in cm (the "
    "numbers 1..15 are visible) - use it as the primary in-plane scale;\n"
    "- a vertical steel ruler down the right edge of the board, graduated in cm (~30 cm).\n"
    "Use the ruler as a SCALE CALIBRATION, not a stick the plant must fit inside: read one "
    "clear 1 cm graduation to fix centimetres-per-pixel, then 'tile' that unit across the "
    "plant to measure distances even BEYOND the ruler's length. Estimate:\n"
    "- height_cm: from the plant base (where it meets the ground) to its tallest point;\n"
    "- crown_cm: the widest horizontal spread of foliage/flowers.\n"
    "If the plant extends past the ruler, still give a real cm estimate by tiling the 1 cm "
    "unit, and set exceeds_ruler=true (this means 'extrapolated beyond the ruler — wider "
    "error from parallax/calibration', NOT unmeasurable). If no measurable plant is in front "
    "of the board, set plant_visible=false and height_cm=crown_cm=0. Note occlusion (grass, "
    "boot, hand) and that plants in front of the board read slightly large (parallax)."
)


def make_crop(src_jpg, out_jpg):
    with Image.open(src_jpg) as im:
        im = im.convert("RGB")
        w, h = im.size
        crop = im.crop((0, int(h * 0.28), w, h))          # lower ~72%: plant + rulers
        rw = 1600
        crop = crop.resize((rw, int(crop.height * rw / crop.width)))
        crop.save(out_jpg, quality=90)


def measure_one(client, crop_jpg):
    with open(crop_jpg, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode("utf-8")
    resp = client.messages.create(
        model=MODEL, max_tokens=1024,
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
            {"type": "text", "text": PROMPT},
        ]}],
    )
    return json.loads(next(b.text for b in resp.content if b.type == "text"))


def load_occurrence_images():
    """occurrence images (has_board==yes) joined to occurrenceID from the validated CSV."""
    rows = {r["filename"]: r for r in csv.DictReader(open(C.VALIDATED_CSV))}
    boards = {r["filename"]: r for r in csv.DictReader(open(C.BOARDS_CSV))}
    out = []
    for fn, b in boards.items():
        if b["has_board"] == "yes":
            occ = rows.get(fn, {}).get("occurrenceID", "")
            out.append((fn, occ))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--write", action="store_true", help="write results to Occurrences (backed up)")
    ap.add_argument("--min-confidence", choices=["low", "medium", "high"], default="high")
    ap.add_argument("--db", default=str(C.DB_PATH))
    args = ap.parse_args()

    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic Pillow")

    C.MEASURE_DIR.mkdir(parents=True, exist_ok=True)
    client = anthropic.Anthropic()
    items = load_occurrence_images()
    if args.limit:
        items = items[: args.limit]

    out = []
    for i, (fn, occ) in enumerate(items, 1):
        crop = C.MEASURE_DIR / f"{fn[:-4]}.jpg"
        make_crop(C.IMAGE_DIR / fn, crop)
        try:
            m = measure_one(client, crop)
        except Exception as e:
            m = {"plant_visible": False, "height_cm": 0, "crown_cm": 0, "exceeds_ruler": False,
                 "ruler_used": "", "confidence": "low", "notes": f"error: {e}"}
        m["sizeClass"] = size_class(m["crown_cm"], m["exceeds_ruler"]) if m["plant_visible"] else ""
        out.append({"filename": fn, "occurrenceID": occ, **m})
        print(f"  {i}/{len(items)} occ {occ}: h={m['height_cm']} crown={m['crown_cm']} "
              f"[{m['sizeClass']}] ({m['confidence']}{', exceeds' if m['exceeds_ruler'] else ''})",
              flush=True)

    cols = ["filename", "occurrenceID", "plant_visible", "height_cm", "crown_cm",
            "exceeds_ruler", "ruler_used", "sizeClass", "confidence", "notes"]
    with open(C.MEASUREMENTS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)
    print(f"Wrote {C.MEASUREMENTS_CSV} ({len(out)} rows)")

    if not args.write:
        print("Review-only (no DB write). Re-run with --write to populate Occurrences.")
        return

    # --- write to Occurrences (guarded) ---
    # Size class is robust -> write it for every measured plant.
    # Exact cm is only trustworthy for clean cases -> write occurrenceHeight/CrownSize
    # only at/above --min-confidence and not exceeds_ruler.
    classable = [r for r in out if r["plant_visible"] and r["occurrenceID"]]
    cm_writable = [r for r in classable if not r["exceeds_ruler"]
                   and CONF_RANK[r["confidence"]] >= CONF_RANK[args.min_confidence]]
    print(f"Writing sizeClass for {len(classable)}, cm for {len(cm_writable)} "
          f"(confidence >= {args.min_confidence}, not exceeds_ruler)...")
    backup = f"{args.db}.bak-{datetime.now():%Y%m%d-%H%M%S}"
    shutil.copy2(args.db, backup)
    print(f"Backup: {backup}")
    con = sqlite3.connect(args.db, timeout=2.0)
    try:
        with con:
            have = {r[1] for r in con.execute("PRAGMA table_info(Occurrences)")}
            if "occurrenceSizeClass" not in have:
                con.execute("ALTER TABLE Occurrences ADD COLUMN occurrenceSizeClass TEXT")
            for r in classable:
                con.execute("UPDATE Occurrences SET occurrenceSizeClass=? WHERE occurrenceID=?",
                            (r["sizeClass"], int(r["occurrenceID"])))
            for r in cm_writable:
                con.execute(
                    "UPDATE Occurrences SET occurrenceHeight=?, occurrenceHeightUnit='cm', "
                    "occurrenceCrownSize=?, occurrenceCrownSizeUnit='cm' WHERE occurrenceID=?",
                    (round(r["height_cm"], 1), round(r["crown_cm"], 1), int(r["occurrenceID"])))
        print(f"Updated {len(classable)} size classes, {len(cm_writable)} cm measurements.")
    except sqlite3.OperationalError as e:
        con.close()
        sys.exit(f"ABORTED ({e}). DB likely open/locked - close it and retry. Backup: {backup}")
    con.close()


if __name__ == "__main__":
    main()
