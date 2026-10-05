#!/usr/bin/env python3
"""Stage C - Seed sheets → Germplasm (germplasmID + seed weight per occurrence).

Runs AFTER Stage A (forms → Locations/Events/Occurrences) — the occurrences must already exist,
because each Germplasm row is attached to its plant through the FK Germplasm.occurrenceID.

SOURCE. After seed processing, event-sheet PAGE 2 (Section 4 "Fruiting Plants Collection Details",
the plant-barcode list) gets two extra hand-written columns per plant: **Germ** (the germplasmID given
to that plant's seed envelope) and **Weight (g)**. The page is re-photographed and stored like every
other form page, FLAT in Field_forms/<year>/ (e.g. PXL_20261004_*.jpg). Page 2 carries NO event
sticker, so eventID + locationID are taken from the occurrences in the DB (and checked for consistency).
germplasmIDs continue from the previous season but are assigned as envelopes are processed, so they are
NOT in sheet order — gaps / out-of-order IDs are reported for information only.

FLOW (each DB-writing step is dry-run by default, backs up LEPA_SQL.db, appends to PIPELINE_LOG.md)
  --worklist --glob PAT  work/germplasm_worklist.csv: the sheet images matching PAT in Field_forms/<year>/
                         (scope it to the batch, e.g. "PXL_20261004_*") + each image's EXIF capture date.
  (in-session sweep)     read-only agents read each sheet → results JSON (schema below).
  --load FILE            validate every row against the DB + overrides → staging_2026/germplasm_staging.csv
                         (status OK / FLAG / NO_SEED / LOADED / SKIP, with reasons). NO DB writes.
  --commit [--apply]     insert the OK rows into Germplasm (+ derived seed-count estimates). FLAG rows are
                         HELD — fix them in staging_2026/germplasm_overrides.csv and re-run --load.
  --sheets-mm [--apply]  link the sheet images to their Event in Multimedia (tableID 11, type 'germplasm sheet').
  --report               germplasmID REGISTRY check across all batches + DB: duplicate IDs, occurrences with >1 ID,
                         numbers not yet seen, and per-location coverage of 2026 events/occurrences.

REGISTRY  staging_2026/germplasm_registry.csv — every row --load has ever read (all batches), sorted by
germplasmID. Each --load replaces the rows of its own sheet files and checks the rest, so a germplasmID or
occurrence that turns up again on a sheet imaged days later is caught even if neither row is loaded yet.

RESULTS JSON (list; one object per image, in capture order) expected by --load:
  location form:  {file, idx, page_type: "location_form", location_id (barcode / written locationID), confidence}
  seed sheet:     {file, idx, page_type: "seed_sheet", acquisition_date (as written, else null), initials, confidence,
                   seed_notes (seed-quality remark written on the sheet, verbatim, else null),
                   rows: [{occurrenceID, germplasmID, seedWeight, initials, acquisition_date, note}]}

LOCATION FORM RULE (Sven, 2026-10-04). Each location in a batch is introduced by a photo of its Location form;
every seed sheet photographed after it must belong to that location. Rows of a location with no location-form
photo in the batch, or of a sheet whose plants belong to a different location than the preceding form, are
FLAGged (held). --allow-missing-location-form exempts batches imaged before the rule (the 2026-10-04 pilot).

WHO + WHEN (Sven, 2026-10-04). Initials written next to the Germ | Weight columns identify who cleaned the
seeds / assigned the germplasmID → Germplasm.personID, resolved through staging_2026/initials_persons.csv.
ONE CLEANER PER GERMPLASM (Sven 2026-10-05): a germplasm = all seeds of one mother plant, so it has exactly one
cleaner, while an envelope (event) can have several. Several initials written once for a whole envelope (e.g.
"SB/TG") are recorded as "envelope: SB/TG" in staging and leave personID empty until the lab says who cleaned
which plant. Initials not in that file get a PLACEHOLDER Persons row at --commit --apply (firstName = initials,
lastName "[unidentified - seed cleaning <year>]") for the team to identify later. Dates are American
(MM/DD/YY) and become acquisitionDate. Both can be per row (rows[].initials / rows[].acquisition_date) or
per sheet (sheet-level initials / acquisition_date); the row value wins. --commit also BACKFILLS personID and
a written acquisitionDate onto rows already in the DB (status LOADED) when they are newly read.

SEED-QUALITY NOTES. Notes on the sheet about seed quality (e.g. "many too late", "germplasm 1266 has large
seeds") are transcribed into seed_notes and, at --commit, APPENDED to Events.eventRemarks of the sheet's event
as "Seed processing (<date>): <note>" (staged in staging_2026/germplasm_event_notes.csv; never overwrites).
  - transcribe exactly what is written; leave germplasmID/seedWeight null where the cell is blank or "—"
    (a plant with no seeds collected) — never infer or carry a value down.
  - seedWeight in grams as written (keep every decimal; do NOT round). Where a value is crossed out and
    rewritten, take the final value and say so in `note`.

ACQUISITION DATE (Germplasm.acquisitionDate = seed processing/accession date, NOT the field date).
  Priority: override column > date written on the sheet > EXIF capture date of the sheet photo.
  The photo date is a PROXY (issue #20 asks the lab to write the date on the envelope); such rows are
  marked acq_source=photo in staging and counted in the log so they can be revised.

OVERRIDES  staging_2026/germplasm_overrides.csv  (edit THIS, never the generated staging CSV):
  occurrenceID,correctedOccurrenceID,germplasmID,seedWeight,acquisitionDate,note
  - keyed by the occurrenceID AS READ; any non-blank column replaces the OCR value.  germplasmID=SKIP drops
    the row; germplasmID=HOLD keeps the read values but holds the row (FLAG) until the envelope is checked. correctedOccurrenceID fixes a mis-written plant barcode (the as-read value stays in occurrenceID_raw).

Germplasm row filled at --commit (2025 conventions): biologicalStatus='Wild', storageCondition='Fresh',
germplasmStorageLocation='Fridge_lab205', germplasmWeightUnit='gr.', taxonID=1, eventID + locationID
FROM THE OCCURRENCE, and germplasmQuantityEstimate/Low/Upr from the 1000-seed-weight regression
(Documentation/LEPA_DB_Documentation.md; Protocols/1000_Seed_Weight.zip).

Usage:
  python3 Multimedia_pipeline/germplasm_seeds.py --worklist --glob "PXL_20261004_*" [--year 2026]
  python3 Multimedia_pipeline/germplasm_seeds.py --load work/germplasm_results.json [--locations 11,28,52,53]
  python3 Multimedia_pipeline/germplasm_seeds.py --commit [--apply]
  python3 Multimedia_pipeline/germplasm_seeds.py --sheets-mm [--apply]
  python3 Multimedia_pipeline/germplasm_seeds.py --report
"""
import argparse, csv, hashlib, json, re, shutil, sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "Field_forms"
MAIN = ROOT / "Multimedia_main"
WORK = ROOT / "Multimedia_pipeline" / "work"; WORK.mkdir(parents=True, exist_ok=True)
STAGE = ROOT / "Multimedia_pipeline" / "staging_2026"; STAGE.mkdir(parents=True, exist_ok=True)
LOG = ROOT / "Multimedia_pipeline" / "PIPELINE_LOG.md"
WORKLIST = WORK / "germplasm_worklist.csv"
STAGING = STAGE / "germplasm_staging.csv"
NOTES = STAGE / "germplasm_event_notes.csv"     # seed-quality notes → Events.eventRemarks
LOCFORMS = STAGE / "germplasm_location_forms.csv"
SHEETS = STAGE / "germplasm_sheets.csv"             # every seed sheet of the batch -> its event (incl. sheets with no plant rows)
INITIALS = STAGE / "initials_persons.csv"           # seed-cleaner initials -> Persons.personID (Sven-curated)   # location-form photos of the batch → Multimedia (tableID 9)
OVERRIDES = STAGE / "germplasm_overrides.csv"
REGISTRY = STAGE / "germplasm_registry.csv"   # cumulative list of every germplasmID read, across ALL batches
REG_COLS = ["germplasmID", "occurrenceID", "eventID", "locationID", "seedWeight", "acquisitionDate", "acq_source", "initials",
            "status", "flags", "file", "batch"]
FIRST_NEW_ID = 871                            # 2026 IDs continue after the last 2025 accession in the DB

# plausibility window for one plant's seed weight (g). 2025 wild accessions: 0.0032–2.4176 g.
WEIGHT_MIN, WEIGHT_MAX = 0.0001, 3.0
# 1000-seed-weight regression (weight = a + b*nSeeds; ±95% PI half-width) — see LEPA_DB_Documentation.md
REG_A, REG_B, REG_PI = 0.0003681555, 0.0004252451, 0.01926434
GERM_DEFAULTS = dict(biologicalStatus="Wild", storageCondition="Fresh", germplasmStorageLocation="Fridge_lab205",
                     germplasmWeightUnit="gr.", taxonID=1)

def as_int(s):
    m = re.search(r"\d+", str(s if s is not None else "")); return int(m.group()) if m else None

def as_weight(s):   # "0.0213" / ".0213" / "0,0213" / "0.0213 g" -> float; None if blank; "BAD" if unparseable
    if s is None or str(s).strip() in ("", "-", "—", "–", "null", "None"): return None
    t = str(s).strip().lower().replace(",", ".").replace("gr", "").replace("g", "").strip()
    try: return float(t)
    except ValueError: return "BAD"

def norm_date(s):    # "10/4/26" / "10-04-2026" -> "MM-DD-YYYY" (DB convention); None if blank/unparseable
    m = re.match(r"\s*(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})\s*$", str(s or ""))
    if not m: return None
    mo, d, y = m.groups(); y = ("20" + y) if len(y) == 2 else y
    return f"{int(mo):02d}-{int(d):02d}-{y}"

def stamp(): return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

def backup(db, tag):
    bk = Path(db).parent / "db_backups"; bk.mkdir(exist_ok=True)
    bak = bk / f"{Path(db).name}.bak-{tag}-{stamp()}"; shutil.copy2(db, bak); return bak

def log(title, line):
    with open(LOG, "a") as fh: fh.write(f"\n## {stamp()} — {title}\n- {line}\n")

def capture_date(p):   # EXIF DateTimeOriginal -> "MM-DD-YYYY"; PXL_YYYYMMDD filename as fallback
    try:
        from PIL import Image
        ex = Image.open(p)._getexif() or {}; v = str(ex.get(36867) or ex.get(306) or "")
        m = re.match(r"(\d{4})[:\-](\d{2})[:\-](\d{2})", v)
        if m: return f"{m.group(2)}-{m.group(3)}-{m.group(1)}"
    except Exception: pass
    m = re.match(r"PXL_(\d{4})(\d{2})(\d{2})", Path(p).name)
    return f"{m.group(2)}-{m.group(3)}-{m.group(1)}" if m else None

# ---------------------------------------------------------------------------------------------------
def worklist(year, pattern):
    if not pattern: raise SystemExit("--glob is required (scope to the batch, e.g. \"PXL_20261004_*\") — "
                                     "Field_forms/<year>/ also holds every Stage A form page.")
    imgs = sorted(p for p in (FORMS / year).glob(pattern) if p.suffix.lower() in (".jpg", ".jpeg"))
    with open(WORKLIST, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["idx", "file", "capture_date", "image_path"])
        for i, p in enumerate(imgs): w.writerow([i, p.name, capture_date(p), str(p)])
    print(f"germplasm worklist: {len(imgs)} sheet images ({pattern}) -> {WORKLIST}")
    print("  Next: in-session READ-ONLY OCR sweep over image_path → results JSON, then --load it.")

# ---------------------------------------------------------------------------------------------------
def read_initials():
    return {r["initials"].strip().upper(): as_int(r["personID"]) for r in csv.DictReader(open(INITIALS))} if INITIALS.exists() else {}

def read_overrides():
    if not OVERRIDES.exists():
        with open(OVERRIDES, "w", newline="") as fh:
            csv.writer(fh).writerow(["occurrenceID", "correctedOccurrenceID", "germplasmID", "seedWeight", "acquisitionDate", "note"])
        return {}
    return {as_int(r.get("occurrenceID")): r for r in csv.DictReader(open(OVERRIDES)) if as_int(r.get("occurrenceID"))}

def load(db, results, locations, allow_no_form=False, year="2026"):
    items = sorted(json.load(open(results)), key=lambda r: r.get("idx", 0))
    loc_forms_all = {as_int(it.get("location_id")) for it in items if it.get("page_type") == "location_form"}
    wl = {r["file"]: r for r in csv.DictReader(open(WORKLIST))}
    con = sqlite3.connect(db); cur = con.cursor()
    occ_db = {o: (e, l) for o, e, l in cur.execute(
        "SELECT o.occurrenceID, o.eventID, e.locationID FROM Occurrences o LEFT JOIN Events e ON e.eventID=o.eventID")}
    germ_db = {g: (o, w) for g, o, w in cur.execute("SELECT germplasmID, occurrenceID, germplasmWeight FROM Germplasm")}
    con.close()
    occ_has_germ = {}
    for g, (o, _) in germ_db.items(): occ_has_germ.setdefault(o, []).append(g)
    ev_occs = {}
    for o, (e, _) in occ_db.items(): ev_occs.setdefault(e, set()).add(o)
    occ_ov = read_overrides()
    ini_map = read_initials(); unknown_ini = set()
    batch_files = {it.get("file") for it in items}
    prior = [r for r in read_registry() if r["file"] not in batch_files]   # other batches / sheets
    prior_g, prior_occ = {}, {}
    for r in prior:
        if as_int(r["germplasmID"]) is not None: prior_g.setdefault(as_int(r["germplasmID"]), []).append(r)
        if as_int(r["occurrenceID"]) is not None and as_int(r["germplasmID"]) is not None:
            prior_occ.setdefault(as_int(r["occurrenceID"]), []).append(r)

    out, seen_germ, seen_occ, sheet_events = [], {}, {}, {}
    loc_forms, cur_form, sheet_form, notes, sheet_list = {}, None, {}, [], []
    for it in items:
        f = it.get("file")
        if f not in wl:                                   # results from an earlier batch: resolve the file directly
            p_ = FORMS / year / f
            if not p_.exists(): print(f"  ⚠ {f} not in worklist or {FORMS / year} — skipped"); continue
            wl[f] = {"file": f, "capture_date": capture_date(p_), "image_path": str(p_)}
        if it.get("page_type") == "location_form":
            cur_form = as_int(it.get("location_id")); loc_forms.setdefault(cur_form, f); continue
        sheet_form[f] = cur_form
        sheet_date = norm_date(it.get("acquisition_date")); photo_date = wl[f].get("capture_date") or None
        # the sheet's event = the event most of its listed occurrences belong to (page 2 has no sticker)
        fix = lambda o: as_int(occ_ov.get(o, {}).get("correctedOccurrenceID")) or o
        evs = Counter(occ_db[fix(as_int(r.get("occurrenceID")))][0] for r in it.get("rows", [])
                      if fix(as_int(r.get("occurrenceID"))) in occ_db)
        sheet_ev = as_int(it.get("event_id")) or (evs.most_common(1)[0][0] if evs else None)   # event_id: sheets with no plant rows
        sheet_events.setdefault(sheet_ev, set()); sheet_list.append((f, sheet_ev))
        if (it.get("seed_notes") or "").strip():
            notes.append(dict(eventID=sheet_ev, file=f, note=it["seed_notes"].strip(),
                              date=sheet_date or photo_date))
        for r in it.get("rows", []):
            occ = as_int(r.get("occurrenceID")); ov = occ_ov.get(occ, {})
            if as_int(ov.get("correctedOccurrenceID")):              # mis-written plant barcode (audit kept in occurrenceID_raw)
                occ = as_int(ov["correctedOccurrenceID"])
            g_raw = ov.get("germplasmID") or r.get("germplasmID")
            w_raw = ov.get("seedWeight") if (ov.get("seedWeight") or "").strip() else r.get("seedWeight")
            row_date = norm_date(r.get("acquisition_date")) or sheet_date
            acq, src = ((norm_date(ov["acquisitionDate"]), "override") if norm_date(ov.get("acquisitionDate"))
                        else (row_date, "sheet") if row_date else (photo_date, "photo"))
            row_ini = str(r.get("initials") or "").strip().upper()
            sheet_ini = str(it.get("initials") or "").strip().upper()
            # one cleaner per germplasm (Sven 2026-10-05): several initials written once for the whole envelope
            # (e.g. "SB/TG") name the envelope's cleaners, not this plant's -> leave unassigned, never a placeholder
            multi = lambda x: bool(re.search(r"[/,&+]|\s", x))
            ini = row_ini if row_ini and not multi(row_ini) else (sheet_ini if sheet_ini and not multi(sheet_ini) and not row_ini else "")
            envelope_cleaners = sheet_ini if multi(sheet_ini) else ""
            pid = ini_map.get(ini) if ini else None
            if ini and pid is None: unknown_ini.add(ini)
            row = dict(file=f, sheet_eventID=sheet_ev, occurrenceID=occ, occurrenceID_raw=r.get("occurrenceID"),
                       germplasmID_raw=r.get("germplasmID"), seedWeight_raw=r.get("seedWeight"),
                       germplasmID=None, seedWeight=None, eventID=None, locationID=None,
                       acquisitionDate=acq, acq_source=src, initials=ini or (("envelope: " + envelope_cleaners) if envelope_cleaners else ""), personID=pid,
                       override="yes" if ov else "", ocr_note=r.get("note") or "", confidence=it.get("confidence"))
            if str(g_raw).strip().upper() == "SKIP":
                out.append({**row, "status": "SKIP", "flags": "override SKIP"}); continue
            g, wt = as_int(g_raw), as_weight(w_raw)
            flags = []
            if occ is None: flags.append("no occurrenceID")
            elif occ not in occ_db: flags.append(f"occ {occ} not in DB")
            else:
                oe, ol = occ_db[occ]; row.update(eventID=oe, locationID=ol)
                sheet_events[sheet_ev].add(occ)
                if oe != sheet_ev: flags.append(f"occ {occ} is event {oe}; rest of sheet is event {sheet_ev}")
                if locations and ol not in locations: flags.append(f"occ {occ} is loc {ol}, not in batch {sorted(locations)}")
                if not allow_no_form:
                    if ol not in loc_forms_all: flags.append(f"no location-form photo for loc {ol} in this batch")
                    elif sheet_form.get(f) != ol:
                        flags.append(f"sheet follows location form of loc {sheet_form.get(f)}, but occ {occ} is loc {ol}")
            if str(g_raw).strip().upper() == "HOLD":                 # reviewer hold: keep the read values, don't load
                row.update(germplasmID=as_int(r.get("germplasmID")), seedWeight=as_weight(r.get("seedWeight")))
                out.append({**row, "status": "FLAG", "flags": f"held by reviewer: {ov.get('note', '')}"}); continue
            if g is None and wt is None:
                out.append({**row, "status": "NO_SEED", "flags": "; ".join(flags)}); continue
            if g is None: flags.append("weight but no germplasmID")
            if wt is None: flags.append("germplasmID but no weight")
            elif wt == "BAD": flags.append(f"unparseable weight {w_raw!r}"); wt = None
            elif not (WEIGHT_MIN <= wt <= WEIGHT_MAX): flags.append(f"weight {wt} g outside {WEIGHT_MIN}–{WEIGHT_MAX}")
            if not acq: flags.append("no acquisitionDate (no sheet date, no photo date)")
            row.update(germplasmID=g, seedWeight=wt)
            if g in germ_db:
                if germ_db[g][0] == occ and wt is not None and abs((germ_db[g][1] or 0) - wt) < 1e-9:
                    out.append({**row, "status": "LOADED", "flags": ""}); continue
                flags.append(f"germplasmID {g} already in DB (occ {germ_db[g][0]})")
            elif occ in occ_has_germ: flags.append(f"occ {occ} already has germplasm {occ_has_germ[occ]}")
            if g is not None:
                if g in seen_germ: flags.append(f"germplasmID {g} duplicated (also occ {seen_germ[g]})")
                seen_germ.setdefault(g, occ)
            if occ is not None:
                if occ in seen_occ: flags.append(f"occ {occ} listed twice (also {seen_occ[occ]})")
                seen_occ.setdefault(occ, f)
            for pr in prior_g.get(g, []) if g is not None else []:          # cross-batch checks (registry)
                if as_int(pr["occurrenceID"]) != occ:
                    flags.append(f"germplasmID {g} already read for occ {pr['occurrenceID']} ({pr['file']})")
                else:
                    flags.append(f"occ {occ} already read on {pr['file']} (re-photographed sheet? SKIP one)")
            for pr in prior_occ.get(occ, []) if occ is not None else []:
                if as_int(pr["germplasmID"]) != g:
                    flags.append(f"occ {occ} already has germplasmID {pr['germplasmID']} on {pr['file']}")
            out.append({**row, "status": "FLAG" if flags else "OK", "flags": "; ".join(flags)})

    cols = ["status", "flags", "file", "sheet_eventID", "occurrenceID", "germplasmID", "seedWeight", "eventID",
            "locationID", "acquisitionDate", "acq_source", "initials", "personID", "occurrenceID_raw", "germplasmID_raw", "seedWeight_raw", "override",
            "ocr_note", "confidence"]
    with open(STAGING, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(out)

    write_registry(prior + [{**r, "batch": Path(results).name} for r in out])
    with open(SHEETS, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["file", "eventID"]); w.writerows(sheet_list)
    with open(LOCFORMS, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["file", "locationID"])
        w.writerows([[it["file"], as_int(it.get("location_id"))] for it in items if it.get("page_type") == "location_form"])
    with open(NOTES, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["eventID", "file", "date", "note"]); w.writeheader(); w.writerows(notes)
    print(f"  location forms in batch: {sorted(x for x in loc_forms_all if x is not None) or 'NONE'}"
          + ("  (rule waived: --allow-missing-location-form)" if allow_no_form else ""))
    ini_n = Counter(r["initials"] or "—" for r in out if r["status"] in ("OK", "FLAG", "LOADED"))
    print("  initials (who cleaned): " + ", ".join(f"{k} {v}" for k, v in sorted(ini_n.items())))
    if unknown_ini: print(f"  new initials → placeholder Persons rows will be created at --commit --apply: {sorted(unknown_ini)}")
    for n_ in notes: print(f"  seed-quality note → event {n_['eventID']}: \"{n_['note']}\"")
    n = {s: sum(r["status"] == s for r in out) for s in ("OK", "FLAG", "NO_SEED", "LOADED", "SKIP")}
    print(f"Stage C staged {len(out)} rows from {len(items)} sheets -> {STAGING}")
    print("  " + "  ".join(f"{k}={v}" for k, v in n.items()))
    by_loc = Counter(r["locationID"] for r in out if r["status"] in ("OK", "FLAG"))
    print("  rows with seed by location: " + ", ".join(f"loc {k}: {v}" for k, v in sorted(by_loc.items(), key=lambda x: str(x[0]))))
    srcs = Counter(r["acq_source"] for r in out if r["status"] in ("OK", "FLAG"))
    print("  acquisitionDate source: " + ", ".join(f"{k} {v}" for k, v in srcs.items()) +
          ("   (photo = proxy, see issue #20)" if srcs.get("photo") else ""))
    # completeness: occurrences of the event in the DB that its sheet never lists
    missing = {e: sorted(ev_occs.get(e, set()) - s) for e, s in sheet_events.items() if e is not None and e in ev_occs}
    missing = {e: m for e, m in missing.items() if m}
    if missing:
        print(f"  ⚠ {len(missing)} events have DB occurrences absent from their sheet (photo cut-off / second sheet?):")
        for e, m in list(missing.items())[:20]: print(f"     event {e}: {m}")
    dup_ev = [e for e in sheet_events if len({r["file"] for r in out if r["sheet_eventID"] == e}) > 1]
    if dup_ev: print(f"  note: events photographed on >1 sheet image (re-shoot or 2 pages?): {dup_ev}")
    gids = sorted({r["germplasmID"] for r in out if r["status"] in ("OK", "FLAG", "LOADED") and r["germplasmID"] is not None})
    if gids:   # info only: IDs are assigned as envelopes are processed, not in sheet order
        gaps = [g for g in range(gids[0], gids[-1] + 1) if g not in set(gids)]
        print(f"  germplasmID range {gids[0]}–{gids[-1]} ({len(gids)} IDs; {len(gaps)} unused numbers in range — info only)")
    if any(r["status"] == "OK" for r in out):
        ws = [r["seedWeight"] for r in out if r["status"] == "OK"]
        print(f"  seed weight (OK rows): min {min(ws):.4f}  max {max(ws):.4f} g")
    for r in [r for r in out if r["status"] == "FLAG"][:40]: print(f"     FLAG occ {r['occurrenceID']} ({r['file']}): {r['flags']}")
    log(f"germplasm_seeds --load {Path(results).name}",
        f"staged {len(out)} rows ({', '.join(f'{k} {v}' for k, v in n.items())}); acquisitionDate sources {dict(srcs)}; "
        f"{len(missing)} events incomplete. Review staging_2026/germplasm_staging.csv.")

# ---------------------------------------------------------------------------------------------------
def read_registry():
    return list(csv.DictReader(open(REGISTRY))) if REGISTRY.exists() else []

def write_registry(rows):
    key = lambda r: (as_int(r.get("germplasmID")) is None, as_int(r.get("germplasmID")) or 0, as_int(r.get("occurrenceID")) or 0)
    with open(REGISTRY, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=REG_COLS, extrasaction="ignore"); w.writeheader(); w.writerows(sorted(rows, key=key))

def ranges(nums):   # [871,872,873,880] -> "871–873, 880"
    out, nums = [], sorted(nums)
    for n in nums:
        if out and n == out[-1][1] + 1: out[-1][1] = n
        else: out.append([n, n])
    return ", ".join(f"{a}–{b}" if a != b else f"{a}" for a, b in out)

def report(db, year):
    reg = read_registry()
    con = sqlite3.connect(db); cur = con.cursor()
    db_g = {g: o for g, o in cur.execute("SELECT germplasmID, occurrenceID FROM Germplasm")}
    # season = every event from the first one dated in <year> onward (eventIDs increase through the season;
    # robust to the July 16-21 rows whose dates were stored without a year, e.g. "07-16")
    first_ev = cur.execute("SELECT MIN(eventID) FROM Events WHERE eventDate LIKE ?", (f"%-{year}",)).fetchone()[0]
    occ26 = {o: (e, l) for o, e, l in cur.execute(
        "SELECT o.occurrenceID, o.eventID, e.locationID FROM Occurrences o JOIN Events e ON e.eventID=o.eventID "
        "WHERE e.eventID >= ?", (first_ev or 10**9,))}
    con.close()
    reg_live = [r for r in reg if r["status"] != "SKIP"]
    # every (germplasmID -> occurrence) claim: registry reads + DB rows
    claims = {}
    for r in reg_live:
        g = as_int(r["germplasmID"])
        if g is not None: claims.setdefault(g, set()).add((as_int(r["occurrenceID"]), r["file"]))
    for g, o in db_g.items():
        if g >= FIRST_NEW_ID or g in claims: claims.setdefault(g, set()).add((o, "DB"))
    dup_g = {g: c for g, c in claims.items() if len({o for o, _ in c}) > 1}
    occ_ids = {}
    for g, c in claims.items():
        for o, _ in c: occ_ids.setdefault(o, set()).add(g)
    multi_occ = {o: gs for o, gs in occ_ids.items() if len(gs) > 1}
    ids = sorted(claims)
    new_ids = [g for g in ids if g >= FIRST_NEW_ID]
    print(f"germplasmID REGISTRY — {len(reg)} sheet rows from {len({r['file'] for r in reg})} sheets "
          f"({len({r['batch'] for r in reg})} batches) -> {REGISTRY}")
    st = Counter(r["status"] for r in reg); print("  status: " + "  ".join(f"{k}={v}" for k, v in sorted(st.items())))
    print(f"  germplasmIDs claimed: {len(new_ids)} (≥{FIRST_NEW_ID})" + (f", range {new_ids[0]}–{new_ids[-1]}" if new_ids else ""))
    print(f"  ✖ DUPLICATE germplasmIDs (one ID → >1 occurrence): {len(dup_g)}")
    for g, c in sorted(dup_g.items()): print(f"     {g}: " + "; ".join(f"occ {o} [{f}]" for o, f in sorted(c, key=str)))
    print(f"  ✖ OCCURRENCES with >1 germplasmID: {len(multi_occ)}")
    for o, gs in sorted(multi_occ.items(), key=lambda x: x[0] or 0): print(f"     occ {o}: {sorted(gs)}")
    if new_ids:
        unseen = [g for g in range(FIRST_NEW_ID, new_ids[-1] + 1) if g not in claims]
        print(f"  not yet seen ({len(unseen)} numbers in {FIRST_NEW_ID}–{new_ids[-1]}; expected to fill as sheets are imaged):")
        print(f"     {ranges(unseen) or '—'}")
    # coverage of the season: which locations / events have had their seed sheet read
    read_occ = {as_int(r["occurrenceID"]) for r in reg}
    loaded_occ = {o for g, o in db_g.items() if g >= FIRST_NEW_ID}
    per = {}
    for o, (e, l) in occ26.items():
        d = per.setdefault(l, dict(ev=set(), ev_read=set(), occ=0, read=0, germ=0, loaded=0))
        d["ev"].add(e); d["occ"] += 1
        if o in read_occ: d["read"] += 1; d["ev_read"].add(e)
        if o in loaded_occ: d["loaded"] += 1
    germ_occ = {as_int(r["occurrenceID"]) for r in reg_live if as_int(r["germplasmID"]) is not None}
    for o, (e, l) in occ26.items():
        if o in germ_occ: per[l]["germ"] += 1
    print(f"\n  {year} coverage by location (events with sheet read / events; occurrences read / with germplasmID / loaded / total):")
    for l, d in sorted(per.items(), key=lambda x: x[0] or 0):
        tag = "done" if len(d["ev_read"]) == len(d["ev"]) else ("partial" if d["ev_read"] else "")
        print(f"     loc {l:>3}: events {len(d['ev_read']):>3}/{len(d['ev']):<3} occ read {d['read']:>3}  germ {d['germ']:>3}  "
              f"loaded {d['loaded']:>3} / {d['occ']:<3} {tag}")
        if tag == "partial":
            print(f"              events not yet read: {ranges(d['ev'] - d['ev_read'])}")
    todo = [l for l, d in per.items() if not d["ev_read"]]
    print(f"  locations not yet imaged: {len(todo)}/{len(per)}")

def commit(db, apply):
    rows = list(csv.DictReader(open(STAGING)))
    ok = [r for r in rows if r["status"] == "OK"]; held = [r for r in rows if r["status"] == "FLAG"]
    con = sqlite3.connect(db); cur = con.cursor()
    have = {g for (g,) in cur.execute("SELECT germplasmID FROM Germplasm")}
    clash = [r["germplasmID"] for r in ok if int(r["germplasmID"]) in have]
    proxy = sum(r["acq_source"] == "photo" for r in ok)
    print(f"GATED LOAD plan (Stage C) — to INSERT {len(ok)} Germplasm rows; HELD (FLAG) {len(held)}")
    if ok:
        ids = sorted(int(r["germplasmID"]) for r in ok)
        print(f"  germplasmID {ids[0]}–{ids[-1]}; acquisitionDate from photo (proxy, issue #20): {proxy}/{len(ok)}")
    if clash: print(f"  ⚠ germplasmIDs now in DB (re-run --load): {clash[:10]}"); con.close(); return
    nts = list(csv.DictReader(open(NOTES))) if NOTES.exists() else []
    if nts: print(f"  seed-quality notes to append to Events.eventRemarks: {len(nts)} (events {sorted({n['eventID'] for n in nts})})")
    lr = [r for r in rows if r["status"] == "LOADED" and (r.get("initials") or r["acq_source"] in ("sheet", "override"))]
    if lr: print(f"  loaded rows with who/when to backfill (if different in DB): {len(lr)}")
    if not apply: print("\nDRY-RUN. Re-run with --commit --apply to write (DB backed up first)."); con.close(); return
    bak = backup(db, "germplasm")
    # placeholder Persons for initials not yet in initials_persons.csv
    new_people = sorted({r["initials"] for r in rows if r.get("initials") and not r.get("personID")
                         and not r["initials"].startswith("envelope:")})
    if new_people:
        with open(INITIALS, "a", newline="") as fh:
            w = csv.writer(fh)
            for ini in new_people:
                cur.execute("INSERT INTO Persons (lastName, firstName, institution) VALUES (?,?,?)",
                            (f"[unidentified - seed cleaning {datetime.now().year}]", ini, "Boise State"))
                w.writerow([ini, cur.lastrowid, "placeholder", "Created automatically by germplasm_seeds --commit; identify with Peggy."])
    ini_map = read_initials()
    pid_of = lambda r: ini_map.get(r["initials"]) if r.get("initials") and not r["initials"].startswith("envelope:") else None
    for r in ok:
        wt = float(r["seedWeight"])
        rec = dict(germplasmID=int(r["germplasmID"]), occurrenceID=int(r["occurrenceID"]), eventID=int(r["eventID"]),
                   locationID=int(r["locationID"]), germplasmWeight=wt, acquisitionDate=r["acquisitionDate"],
                   germplasmQuantityEstimate=round((wt - REG_A) / REG_B, 2),
                   germplasmQuantityEstimateLow=round((wt - REG_PI - REG_A) / REG_B, 2),
                   germplasmQuantityEstimateUpr=round((wt + REG_PI - REG_A) / REG_B, 2), personID=pid_of(r), **GERM_DEFAULTS)
        cur.execute(f"INSERT INTO Germplasm ({','.join(rec)}) VALUES ({','.join('?' * len(rec))})", list(rec.values()))
    n_back = 0                                            # backfill who/when onto rows already in the DB
    for r in [r for r in rows if r["status"] == "LOADED"]:
        g = int(r["germplasmID"]); pid = pid_of(r)
        dbp, dbd = cur.execute("SELECT personID, acquisitionDate FROM Germplasm WHERE germplasmID=?", (g,)).fetchone()
        sets = {}
        if pid and pid != dbp: sets["personID"] = pid
        if r["acq_source"] in ("sheet", "override") and r["acquisitionDate"] and r["acquisitionDate"] != dbd:
            sets["acquisitionDate"] = r["acquisitionDate"]
        if sets:
            cur.execute(f"UPDATE Germplasm SET {', '.join(k + '=?' for k in sets)} WHERE germplasmID=?", [*sets.values(), g]); n_back += 1
    n_notes = 0
    for nt in (list(csv.DictReader(open(NOTES))) if NOTES.exists() else []):
        if not nt["eventID"]: continue
        text = f"Seed processing ({nt['date']}): {nt['note']}"
        old = cur.execute("SELECT eventRemarks FROM Events WHERE eventID=?", (int(nt["eventID"]),)).fetchone()
        if old is None or text in (old[0] or ""): continue        # idempotent: never append twice
        cur.execute("UPDATE Events SET eventRemarks=? WHERE eventID=?",
                    ((old[0] + " | " + text) if old[0] else text, int(nt["eventID"]))); n_notes += 1
    con.commit(); con.close()
    log("germplasm_seeds --commit --apply",
        f"inserted {len(ok)} Germplasm rows (seed sheets → occurrenceID FK); {len(held)} held as FLAG; "
        f"{n_notes} seed-quality notes appended to Events.eventRemarks; {n_back} loaded rows backfilled (personID/acquisitionDate); "
        f"new placeholder Persons {new_people or 'none'}; "
        f"acquisitionDate = photo-date proxy for {proxy} rows (issue #20). Backup `{bak.name}`.")
    print(f"APPLIED: +{len(ok)} Germplasm, {n_back} backfilled, {n_notes} event remarks, new Persons {new_people or 'none'}. "
          f"{len(held)} held. Backup {bak.name}. Logged.")

def sheets_multimedia(db, apply):   # sheet image -> Multimedia evidence row on its Event (tableID 11)
    rows = list(csv.DictReader(open(STAGING)))
    jobs = {}                                          # file -> (tableID, fk value, title)
    sheet_rows = list(csv.DictReader(open(SHEETS))) if SHEETS.exists() else [
        {"file": r["file"], "eventID": r["sheet_eventID"]} for r in rows]
    for r in sheet_rows:
        if r["eventID"] and r["file"] not in jobs:
            ev = int(r["eventID"])
            jobs[r["file"]] = (11, ev, f"Seed-collection sheet, event page 2 with germplasmIDs + seed weights — event {ev}")
    for lf in (list(csv.DictReader(open(LOCFORMS))) if LOCFORMS.exists() else []):
        if lf["locationID"]:
            jobs[lf["file"]] = (9, int(lf["locationID"]), f"Location form (seed-processing batch) — location {lf['locationID']}")
    paths = {r["file"]: Path(r["image_path"]) for r in csv.DictReader(open(WORKLIST))}
    con = sqlite3.connect(db); cur = con.cursor()
    have = {i for (i,) in cur.execute("SELECT identifier FROM Multimedia WHERE identifier IS NOT NULL")}
    maxmm = cur.execute("SELECT MAX(multimediaID) FROM Multimedia").fetchone()[0] or 0
    plan = []
    for f, (tid, fk, title) in jobs.items():
        p = paths.get(f)
        if not p or not p.exists(): print(f"  ⚠ missing on disk: {f}"); continue
        h = hashlib.sha256(p.read_bytes()).hexdigest(); cd = capture_date(p)   # MM-DD-YYYY
        iso = f"{cd[6:]}-{cd[:2]}-{cd[3:5]}" if cd else datetime.now(timezone.utc).strftime("%Y-%m-%d")
        name = f"LEPA_{iso}_{h[:8]}.jpg"
        if name not in have: plan.append((p, name, h, cd, iso, tid, fk, title))
    print(f"seed sheets→Multimedia: {sum(j[0]==11 for j in jobs.values())} sheets + "
          f"{sum(j[0]==9 for j in jobs.values())} location forms; to insert {len(plan)} (copied as LEPA_<date>_<sha8>.jpg)")
    if not apply: print("DRY-RUN. Re-run with --sheets-mm --apply."); con.close(); return
    bak = backup(db, "germplasmmm"); MAIN.mkdir(exist_ok=True)
    for p, name, h, cd, iso, tid, fk, title in plan:
        if not (MAIN / name).exists(): shutil.copy2(p, MAIN / name)
        maxmm += 1
        cur.execute("""INSERT INTO Multimedia (multimediaID,identifier,type,format,createDate,title,multimediaStorage,
                       tableID,eventID,locationID,remarks,originalFilename,fileYear,folderDate,captureTimestamp,sha256)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (maxmm, name, "germplasm sheet" if tid == 11 else "field form", "jpeg", cd, title, "Google Drive", tid,
                     fk if tid == 11 else None, fk if tid == 9 else None,
                     "evidence for the Germplasm rows of this event" if tid == 11 else "location form photographed with the seed sheets",
                     p.name, iso[:4], iso, cd, h))
    con.commit(); con.close()
    log("germplasm_seeds --sheets-mm --apply", f"linked {len(plan)} seed-sheet / location-form images to Multimedia (Event tableID 11 / Location tableID 9), copied as LEPA_<date>_<sha8>.jpg. Backup `{bak.name}`.")
    print(f"APPLIED: linked {len(plan)} seed-sheet images. Backup {bak.name}. Logged.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "LEPA_SQL.db"))
    ap.add_argument("--year", default="2026")
    ap.add_argument("--worklist", action="store_true")
    ap.add_argument("--glob", help='sheet-image pattern inside Field_forms/<year>/, e.g. "PXL_20261004_*"')
    ap.add_argument("--load")
    ap.add_argument("--locations", help="expected locationIDs for the batch, e.g. 11,28,52,53 (others are flagged)")
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--sheets-mm", dest="sheets_mm", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--allow-missing-location-form", dest="allow_no_form", action="store_true",
                    help="waive the location-form rule (only for batches imaged before it, e.g. the 2026-10-04 pilot)")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    locs = {int(x) for x in a.locations.split(",")} if a.locations else None
    if a.worklist: worklist(a.year, a.glob)
    elif a.load: load(a.db, a.load, locs, a.allow_no_form, a.year)
    elif a.commit: commit(a.db, a.apply)
    elif a.sheets_mm: sheets_multimedia(a.db, a.apply)
    elif a.report: report(a.db, a.year)
    else: ap.print_help()

if __name__ == "__main__":
    main()
