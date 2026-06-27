#!/usr/bin/env python3
"""03 - Phenotyping: worklist of images still needing measurement, then load measurements.

Pipeline step 3 of 3   (01 ingest/rename -> 02 OCR -> 03 phenotype).

IDEMPOTENCY RULE (Sven): only phenotype an occurrence image that has NO Phenotyping row yet.
So this never re-measures work already done; re-running just shrinks the worklist.

TWO MODES
  --worklist   Write work/phenotype_worklist.csv = every occurrence image (Multimedia row with
               an occurrenceID) that has no Phenotyping row, joined to its file in Multimedia_main/.
               -> hand this list to the in-session measurement agent sweep (subscription, not API),
                  which reads each image and emits a results CSV with the columns below.
  --load FILE  Insert the agent results into Phenotyping (backup + dry-run first), link each to its
               source image (multimediaID) and occurrence, then append to PIPELINE_LOG.md.

RESULTS CSV columns expected by --load:
  occurrenceID, multimediaID, occurrenceHeight, occurrenceCrownSize, occurrenceSizeClass,
  measurementMethod(ruler|1cm-tile), measurementConfidence(high|med|low),
  [optional] boardHeight, boardWidth   (field-written h/w, for the validation case study)

Usage:
  python3 Multimedia_pipeline/03_phenotype.py --worklist
  python3 Multimedia_pipeline/03_phenotype.py --load work/phenotype_results.csv          # dry-run
  python3 Multimedia_pipeline/03_phenotype.py --load work/phenotype_results.csv --apply
"""
import argparse, csv, shutil, sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "Multimedia_pipeline" / "work"; WORK.mkdir(parents=True, exist_ok=True)
MAIN = ROOT / "Multimedia_main"
DETERMINED_BY = "Claude vision (in-session)"

def worklist(db):
    con = sqlite3.connect(db); con.row_factory = sqlite3.Row
    rows = con.execute("""SELECT m.occurrenceID, m.multimediaID, m.identifier, m.fileYear, e.EOCode
        FROM Multimedia m
        LEFT JOIN Phenotyping p ON m.occurrenceID = p.occurrenceID
        LEFT JOIN Occurrences o ON m.occurrenceID = o.occurrenceID
        LEFT JOIN EOs e ON o.EOID = e.EOID
        WHERE m.occurrenceID IS NOT NULL AND p.occurrenceID IS NULL
        ORDER BY m.occurrenceID""").fetchall()
    con.close()
    out = WORK / "phenotype_worklist.csv"
    present, missing = [], []
    for r in rows:
        p = MAIN / (r["identifier"] or "")
        (present if p.exists() else missing).append((r, p))
    with open(out, "w", newline="") as fh:               # only rows with a real file go to the sweep
        w = csv.writer(fh)
        w.writerow(["occurrenceID", "multimediaID", "EO", "image_path", "identifier"])
        for r, p in present:
            w.writerow([r["occurrenceID"], r["multimediaID"], r["EOCode"], str(p), r["identifier"]])
    print(f"phenotyping worklist: {len(present)} occurrence images to measure -> {out}")
    if missing:
        print(f"  EXCLUDED {len(missing)} with no image on disk (image lost): "
              f"{[r['occurrenceID'] for r, _ in missing]}")
    print("  Next: run the in-session measurement agent sweep over image_path, then --load the results.")

def load(db, results, apply):
    rows = list(csv.DictReader(open(results)))
    con = sqlite3.connect(db); cur = con.cursor()
    have = {r[0] for r in cur.execute("SELECT occurrenceID FROM Phenotyping WHERE occurrenceID IS NOT NULL")}
    ins, skip = [], 0
    for r in rows:
        occ = int(r["occurrenceID"])
        if occ in have:                                  # idempotency: never duplicate
            skip += 1; continue
        ins.append(r)
    print(f"results: {len(rows)}; to insert: {len(ins)}; skipped (already phenotyped): {skip}")
    if not apply:
        print("DRY-RUN. Re-run with --apply to insert."); con.close(); return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    bak = Path(db).with_name(Path(db).name + f".bak-pheno-{stamp}"); shutil.copy2(db, bak)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for r in ins:
        cur.execute("""INSERT INTO Phenotyping
            (occurrenceID, multimediaID, occurrenceHeight, occurrenceHeightUnit,
             occurrenceCrownSize, occurrenceCrownSizeUnit, occurrenceSizeClass,
             measurementMethod, measurementConfidence, measurementDeterminedBy,
             measurementDeterminedDate, remarks)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (int(r["occurrenceID"]), int(r["multimediaID"]) if r.get("multimediaID") else None,
             r.get("occurrenceHeight") or None, "cm",
             r.get("occurrenceCrownSize") or None, "cm",
             r.get("occurrenceSizeClass") or None,
             r.get("measurementMethod") or None, r.get("measurementConfidence") or None,
             DETERMINED_BY, now,
             (f"board h={r.get('boardHeight')} w={r.get('boardWidth')}" if r.get("boardHeight") else None)))
    con.commit(); con.close()
    with open(ROOT / "Multimedia_pipeline" / "PIPELINE_LOG.md", "a") as fh:
        fh.write(f"\n## {stamp} — 03_phenotype --load {Path(results).name} --apply\n"
                 f"- inserted {len(ins)} Phenotyping rows; skipped {skip} already-measured; backup `{bak.name}`\n")
    print(f"APPLIED: inserted {len(ins)} Phenotyping rows. Backup {bak.name}. Logged.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "LEPA_SQL.db"))
    ap.add_argument("--worklist", action="store_true")
    ap.add_argument("--load")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if a.worklist: worklist(a.db)
    elif a.load: load(a.db, a.load, a.apply)
    else: ap.print_help()

if __name__ == "__main__":
    main()
