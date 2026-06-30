#!/usr/bin/env python3
"""verify_event_barcodes.py — confirm each Event's eventID against its sticker BARCODE.

WHY (data-quality protocol, added 2026-06). The printed Event stickers on the field
forms carry a machine-readable CODE128 barcode with the number written beneath it.
Digit-OCR of that printed number is error-prone (e.g. 6->8 misreads); decoding the
barcode itself is ground truth. A 2026 audit run this way caught 5 mis-entered events
(stored 265/281/282/285/288 -> true 263/261/262/265/269).

MODES
  --audit         (default) for every Event that has a linked form image
                  (Multimedia.type='field form', tableID=11), decode the sticker and
                  compare it to the stored eventID. Prints MATCH / MISMATCH / NO-DECODE.
  --image PATH    decode the Event sticker on a single image and print the value.
                  Use on a new batch's event page-1 images BEFORE loading, so events
                  enter the DB with barcode-verified numbers.

This script only READS. Apply any correction deliberately: renumber the eventID with a
two-phase update (old -> temp -> true) so chained swaps can't collide, cascading
Events + Occurrences + Multimedia, and back up LEPA_SQL.db first.

REQUIREMENTS: Pillow, pyzbar, and the zbar system library (see requirements.txt /
"Requirements & setup" in IMAGE_PIPELINE_GUIDE.md). On macOS run with
  DYLD_LIBRARY_PATH=/opt/homebrew/lib python3 Multimedia_pipeline/verify_event_barcodes.py
"""
import argparse, re, sqlite3
from pathlib import Path

try:
    from PIL import Image
    from pyzbar.pyzbar import decode
except Exception as e:                                              # pragma: no cover
    raise SystemExit(
        "Missing dependency: %s\n"
        "  pip install -r Multimedia_pipeline/requirements.txt\n"
        "  and install the zbar system lib (macOS: brew install zbar; Debian: apt-get install libzbar0).\n"
        "  On macOS also export DYLD_LIBRARY_PATH=/opt/homebrew/lib" % e)

DB = "LEPA_SQL.db"
MAIN = Path("Multimedia_main")          # collision-proof copies live here (identifier == filename)


def read_sticker(path):
    """Return the integer encoded in the Event-sticker CODE128 barcode, or None."""
    try:
        im = Image.open(path).convert("RGB")
    except Exception:
        return None
    W, H = im.size
    # the sticker sits top-right of the event page: crop that region first (full res),
    # then fall back to the whole frame; try the 4 right-angle rotations for sideways scans.
    for region in (im.crop((int(W * 0.42), 0, W, int(H * 0.58))), im):
        for rot in (0, 90, 270, 180):
            for d in decode(region.rotate(rot, expand=True)):
                s = d.data.decode("ascii", "ignore")
                if d.type == "CODE128" and re.fullmatch(r"0*\d{2,4}", s):
                    return int(s)
    return None


def audit(db):
    cur = sqlite3.connect(db).cursor()
    rows = cur.execute(
        "SELECT m.eventID, m.identifier FROM Multimedia m JOIN Events e ON m.eventID = e.eventID "
        "WHERE m.type = 'field form' AND m.tableID = 11 ORDER BY m.eventID").fetchall()
    decoded = {}
    for ev, ident in rows:
        v = read_sticker(MAIN / ident)
        decoded.setdefault(ev, set())
        if v is not None:
            decoded[ev].add(v)
    mism, nod = [], []
    for ev in sorted(decoded):
        vals = sorted(decoded[ev])
        if vals == [ev]:
            status = "MATCH"
        elif vals:
            status = "MISMATCH"; mism.append((ev, vals))
        else:
            status = "NO-DECODE"; nod.append(ev)
        print(f"  event {ev:>4} -> barcode {str(vals or '—'):<10} {status}")
    print(f"\n{len(decoded)} events | {len(decoded) - len(mism) - len(nod)} MATCH | "
          f"{len(mism)} MISMATCH | {len(nod)} NO-DECODE")
    if mism:
        print("MISMATCH (stored eventID -> true barcode) — fix with a backed-up two-phase renumber:")
        for ev, vals in mism:
            print(f"  {ev} -> {vals}")
    if nod:
        print("NO-DECODE (re-crop / re-image):", nod)


def main():
    ap = argparse.ArgumentParser(description="Verify Event eventIDs against their sticker barcodes (read-only).")
    ap.add_argument("--audit", action="store_true", help="audit every loaded event vs its form-image barcode (default)")
    ap.add_argument("--image", help="decode the Event sticker on a single image and print the number")
    ap.add_argument("--db", default=DB)
    a = ap.parse_args()
    if a.image:
        print(read_sticker(a.image))
    else:
        audit(a.db)


if __name__ == "__main__":
    main()
