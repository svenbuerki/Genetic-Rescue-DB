#!/usr/bin/env python3
"""
STEP 02 - Read the whiteboard on each image (occurrenceID + date).

Reads the header crops produced by step 01 and writes work/02_boards.csv with one
row per image: filename, board_id, board_date, has_board, confidence, notes.

TWO WAYS TO PRODUCE THIS FILE
-----------------------------
1. Manual (used for the 95-image SAMPLE): a human (or Claude in-session) reads each
   crop and records the number/date. The sample's 02_boards.csv was produced this way
   and double-checked against the database, so every read is high-confidence.

2. Automated (this script — for the FULL multi-thousand-image dataset): each crop is
   sent to the Claude vision API, which returns the same fields as structured JSON.
   Handwriting OCR via Tesseract is unreliable; a vision model is the scalable
   equivalent of the manual read. Requires ANTHROPIC_API_KEY in the environment.

   Run:  pip install anthropic
         python3 02_ocr_boards.py            # OCR every crop -> 02_boards.csv
         python3 02_ocr_boards.py --limit 5  # smoke-test on 5 crops first

Whatever produces 02_boards.csv, step 03 (validate) then cross-checks every board
against the Occurrences table, so an OCR slip becomes a flagged mismatch, not a
silent bad insert.
"""
import argparse
import base64
import csv
import json
import sys

import config as C

MODEL = "claude-opus-4-8"   # latest, most capable; vision-capable

SCHEMA = {
    "type": "object",
    "properties": {
        "has_board": {"type": "string", "enum": ["yes", "no", "event"],
                      "description": "yes = a whiteboard with an occurrence number; "
                                     "no = no whiteboard (landscape/setup); "
                                     "event = a board labelled 'Event N'"},
        "board_id": {"type": "string",
                     "description": "the number in the TOP-LEFT of the board, digits only "
                                    "(e.g. '0001' -> '1'); empty string if none"},
        "board_date": {"type": "string",
                       "description": "the date in the TOP-RIGHT as MM-DD-YYYY "
                                      "(e.g. '6/17/25' -> '06-17-2025'); empty string if none"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "notes": {"type": "string", "description": "anything unusual, e.g. 'Event 14 written below'"},
    },
    "required": ["has_board", "board_id", "board_date", "confidence", "notes"],
    "additionalProperties": False,
}

PROMPT = (
    "This is a cropped top portion of a field photo. Most images show a blue-framed "
    "whiteboard: a handwritten occurrence NUMBER in the top-left corner and a DATE in "
    "the top-right (format M/D/YY). Some images have no whiteboard (landscape/setup shots), "
    "and a few show a board labelled 'Event N'. Read the board and return the fields. "
    "For board_id give digits only with leading zeros stripped (0007 -> 7). "
    "For board_date convert to MM-DD-YYYY. If there is no board, has_board='no' and leave "
    "board_id/board_date empty."
)


def normalize_board_id(raw):
    digits = "".join(ch for ch in str(raw) if ch.isdigit())
    return str(int(digits)) if digits else ""


def ocr_one(client, crop_path):
    with open(crop_path, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode("utf-8")
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{
            "role": "user",
            "content": [
                {"type": "image",
                 "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
                {"type": "text", "text": PROMPT},
            ],
        }],
    )
    text = next(b.text for b in resp.content if b.type == "text")
    data = json.loads(text)
    data["board_id"] = normalize_board_id(data.get("board_id", ""))
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="OCR only the first N crops (0 = all)")
    args = ap.parse_args()

    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic  (needed for the automated OCR step)")

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    crops = sorted(C.CROP_DIR.glob("*.jpg"))
    if args.limit:
        crops = crops[: args.limit]
    if not crops:
        sys.exit(f"No crops in {C.CROP_DIR}; run 01_extract_and_crop.py first")

    rows = []
    for i, crop in enumerate(crops, 1):
        try:
            d = ocr_one(client, crop)
        except Exception as e:                       # keep going; flag the row for review
            d = {"has_board": "", "board_id": "", "board_date": "",
                 "confidence": "low", "notes": f"OCR error: {e}"}
        rows.append({"filename": f"{crop.stem}.JPG", **d})
        print(f"  {i}/{len(crops)} {crop.stem}: {d['has_board']} "
              f"id={d['board_id']} date={d['board_date']} ({d['confidence']})", flush=True)

    with open(C.BOARDS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["filename", "board_id", "board_date",
                                          "has_board", "confidence", "notes"])
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {C.BOARDS_CSV} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
