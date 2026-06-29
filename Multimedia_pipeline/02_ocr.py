#!/usr/bin/env python3
"""02 - OCR: worklist of images whose board has not been read, then stage the readings.

Pipeline step 2 of 3   (01 ingest/rename -> 02 OCR -> 03 phenotype).

IDEMPOTENCY RULE (Sven): only OCR an image that is not yet linked to an occurrence — i.e. a
file registered by 01 with no Multimedia.occurrenceID. Re-running just shrinks the worklist.

TWO MODES
  --worklist   Write work/ocr_worklist.csv = every file in Multimedia_main/ that 01 marked
               'register_new' (in the registry) and is not yet an occurrence image.
               -> hand to the in-session OCR agent sweep (subscription, not API), which reads
                  each board and emits a results CSV with the columns below.
  --load FILE  Resolve the readings against the DB and write a HUMAN-REVIEW staging set
               (occurrences_staging + multimedia_staging) — board number, EO->EOID, date, and
               flags (NEW_EO / NEEDS_LOCATION / OCC_EXISTS / LOW_OCR). No occurrence rows are
               created here: that is the gated load step (review the staging first).

THE FIELD BOARD (revised 2026; photo: ../Documentation/Figures/LEPA_board_2026.jpg).
Each plant photo is taken against a whiteboard whose printed labels map 1:1 to DB fields:
  OC -> occurrenceID (the board_number = the Stage B lookup key)   EV -> eventID
  EO -> EOCode        L# -> locationID (resolves to GPS)           D  -> eventDate
  W: -> occurrenceCrownSize (cm)   H: -> occurrenceHeight (cm)
  colour sticker -> board SIZE: blue = standard (rulers 1-24 cm), orange = large (rulers to 40 cm x / ~33 cm y)
  two rulers, x & y axes -> the scale for image measurement; READ THE BOARD'S OWN graduations
                           (do not assume 24 cm — a large/orange board goes to 40 cm)
Read OC as board_number; EV/EO/L#/D are cross-checks against the Stage-A record; W/H are the
field-written board_w_cm/board_h_cm (ground truth for the image estimate).

RESULTS CSV columns expected by --load:
  new_name, board_number, eo_code, date_raw, locality, plant_present,
  [optional] board_h_cm, board_w_cm, ocr_confidence

Usage:
  python3 Multimedia_pipeline/02_ocr.py --worklist
  python3 Multimedia_pipeline/02_ocr.py --load work/ocr_results.csv
"""
import argparse, csv, re, sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "Multimedia_pipeline" / "work"; WORK.mkdir(parents=True, exist_ok=True)
MAIN = ROOT / "Multimedia_main"
STAGE = ROOT / "Multimedia_pipeline" / "staging_2026"; STAGE.mkdir(parents=True, exist_ok=True)
REG = MAIN / "file_registry.csv"

def norm_eo(s):
    m = re.search(r"(\d+)", str(s or "")); return f"EO{int(m.group(1))}" if m else None

def worklist(db):
    reg = {r["new_name"]: r for r in csv.DictReader(open(REG))} if REG.exists() else {}
    con = sqlite3.connect(db)
    linked = {r[0] for r in con.execute("SELECT identifier FROM Multimedia WHERE occurrenceID IS NOT NULL")}
    con.close()
    todo = [r for n, r in reg.items() if r["action"] == "register_new" and n not in linked]
    out = WORK / "ocr_worklist.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["new_name", "image_path", "year", "folderDate", "original_name"])
        for r in todo:
            w.writerow([r["new_name"], str(MAIN / r["new_name"]), r["year"], r["folderDate"], r["original_name"]])
    print(f"OCR worklist: {len(todo)} new images need board reading -> {out}")
    print("  Next: run the in-session OCR agent sweep over image_path, then --load the results.")

def load(db, results):
    rows = list(csv.DictReader(open(results)))
    con = sqlite3.connect(db); cur = con.cursor()
    eo2id = {c: i for i, c in cur.execute("SELECT EOID, EOCode FROM EOs")}
    occ_exist = {r[0] for r in cur.execute("SELECT occurrenceID FROM Occurrences")}
    maxocc = cur.execute("SELECT MAX(occurrenceID) FROM Occurrences").fetchone()[0] or 0
    con.close()
    occ_stage, mm_stage, pid = [], [], maxocc
    for r in rows:
        eo = norm_eo(r.get("eo_code")); eoid = eo2id.get(eo)
        bn = re.search(r"(\d+)", r.get("board_number") or ""); bn = int(bn.group(1)) if bn else None
        flags = []
        if eoid is None: flags.append("NEW_EO")
        flags.append("NEEDS_LOCATION")
        if bn in occ_exist: flags.append(f"OCC_{bn}_EXISTS")
        if (r.get("ocr_confidence") or "") == "low": flags.append("LOW_OCR")
        pid += 1
        occ_stage.append([pid, r["new_name"], bn, eo, eoid or "NEW_EO", "NEEDS_LOCATION", "NEEDS-EVENT",
                          r.get("date_raw"), r.get("locality"), ";".join(flags)])
        mm_stage.append([r["new_name"], pid, eo, r.get("board_h_cm"), r.get("board_w_cm")])
    def w(path, head, rws):
        with open(path, "w", newline="") as fh:
            wr = csv.writer(fh); wr.writerow(head); wr.writerows(rws)
    w(STAGE / "occurrences_staging.csv",
      ["prov_occID", "src_image", "board_num", "EO", "EOID", "locationID", "eventID", "date_raw", "locality", "flags"], occ_stage)
    w(STAGE / "multimedia_staging.csv", ["src_image", "prov_occID", "EO", "board_h_cm", "board_w_cm"], mm_stage)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    with open(ROOT / "Multimedia_pipeline" / "PIPELINE_LOG.md", "a") as fh:
        fh.write(f"\n## {stamp} — 02_ocr --load {Path(results).name}\n"
                 f"- staged {len(occ_stage)} provisional occurrences (IDs {maxocc+1}-{pid}); "
                 f"NEW_EO: {sum('NEW_EO' in o[-1] for o in occ_stage)}; review staging_2026/ before load\n")
    print(f"staged {len(occ_stage)} provisional occurrences (IDs {maxocc+1}-{pid}) -> staging_2026/")
    print("  Review occurrences_staging.csv (flags), resolve Locations/EOs, then run the gated load.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "LEPA_SQL.db"))
    ap.add_argument("--worklist", action="store_true")
    ap.add_argument("--load")
    a = ap.parse_args()
    if a.worklist: worklist(a.db)
    elif a.load: load(a.db, a.load)
    else: ap.print_help()

if __name__ == "__main__":
    main()
