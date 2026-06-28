#!/usr/bin/env python3
"""Stage A - OCR the paper field forms → stage Locations / Events / Occurrences.

This is the FRONT of the full pipeline (runs before the Stage B plant-image steps 00–03).
Field crews photograph the forms into Field_forms/<year>/ IN ORDER:
    Location form (1 page)  then  each Event over TWO pages
        event page 1 = id / GPS / size / condition / counts / plant-area / associated taxa
        event page 2 = the occurrenceID (plant barcode) list  + event remarks
There can be several events per location and (sometimes) more than one location.

TWO MODES
  --worklist   Write work/field_forms_worklist.csv = the form images in capture order (the order
               matters: it pairs event page1+page2 and attaches events to the preceding location).
               Hand this to the in-session OCR sweep, which classifies each page and extracts the
               mapped fields → a results JSON (one object per image; schema in --load below).
  --load FILE  Reconstruct the hierarchy from the barcodes (+ order) and write review staging to
               staging_2026/ : locations_staging.csv, events_staging.csv, occurrences_staging.csv.
               Locations are matched to existing rows → REVISIT (link, no insert) or NEW_LOCATION.
               Events + Occurrences are always new. NO DB writes — gated load happens after review.

RESULTS JSON (list; one object per image, in worklist order) expected by --load:
  {file, idx, page_type: location|event_p1|event_p2|other,
   # location:
   location_barcode, eo, locality, lat, long, landscape_health, dscn, location_remarks,
   # event_p1:
   event_barcode, event_date, location_barcode, event_lat, event_long, size_value, defined,
   condition, fertile, vegetative, plant_area, associated_taxa,
   # event_p2:
   occurrence_ids: [..], event_remarks,
   confidence}

Usage:
  python3 Multimedia_pipeline/field_forms_ocr.py --worklist [--year 2026]
  python3 Multimedia_pipeline/field_forms_ocr.py --load work/field_forms_results.json
"""
import argparse, csv, json, re, shutil, sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT / "Field_forms"
WORK = ROOT / "Multimedia_pipeline" / "work"; WORK.mkdir(parents=True, exist_ok=True)
STAGE = ROOT / "Multimedia_pipeline" / "staging_2026"; STAGE.mkdir(parents=True, exist_ok=True)

def barcode_int(s):
    m = re.search(r"\d+", str(s or "")); return int(m.group()) if m else None

def parse_spec(s):   # "2359-2368" or "2394,2412-2416" -> sorted list of ints (ranges + explicit)
    out = []
    for part in re.split(r"[,;]", str(s or "")):
        part = part.strip()
        m = re.match(r"(\d+)\s*-\s*(\d+)$", part)
        if m: out += list(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit(): out.append(int(part))
    return sorted(set(out))

def norm_date(s):    # "06-15-26" / "6/22/2026" / "6/22/26" -> "MM-DD-YYYY" (DB convention)
    m = re.match(r"\s*(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\s*$", str(s or ""))
    if not m: return (str(s).strip() or None)
    mo, d, y = m.groups(); y = ("20" + y) if len(y) == 2 else y
    return f"{int(mo):02d}-{int(d):02d}-{y}"

def worklist(year):
    d = FORMS / year
    imgs = sorted(p for p in d.iterdir() if p.suffix.lower() in (".jpg", ".jpeg") and not p.name.startswith("."))
    out = WORK / "field_forms_worklist.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["idx", "file", "image_path"])
        for i, p in enumerate(imgs): w.writerow([i, p.name, str(p)])
    print(f"field-forms worklist: {len(imgs)} form images (in order) -> {out}")
    print("  Order matters: Location form first, then each Event over two pages (p2 = occurrenceIDs).")
    print("  Next: run the in-session OCR sweep over image_path → results JSON, then --load it.")

def load(db, results):
    items = sorted(json.load(open(results)), key=lambda r: r.get("idx", 0))
    con = sqlite3.connect(db); con.row_factory = sqlite3.Row; cur = con.cursor()
    loc_full = {row["locationID"]: dict(row) for row in cur.execute("SELECT * FROM Locations")}
    eo2id = {r[1]: r[0] for r in cur.execute("SELECT EOID, EOCode FROM EOs")}
    maxocc = cur.execute("SELECT MAX(occurrenceID) FROM Occurrences").fetchone()[0] or 0
    con.close()
    fname = {}                                              # idx -> source form image filename (traceability)
    wl = WORK / "field_forms_worklist.csv"
    if wl.exists():
        fname = {int(row["idx"]): row["file"] for row in csv.DictReader(open(wl))}

    overrides = {}                                          # eventID -> corrected occurrenceID list (manual fixes)
    ovf = STAGE / "occurrence_overrides.csv"
    if ovf.exists():
        for row in csv.DictReader(open(ovf)):
            ev = barcode_int(row.get("eventID")); spec = (row.get("occurrenceIDs") or "").strip()
            if ev and spec: overrides[ev] = parse_spec(spec)

    loc_overrides = {}                                      # location barcode -> filled/resolved Location fields (persists across re-runs)
    lovf = STAGE / "location_overrides.csv"
    if lovf.exists():
        for row in csv.DictReader(open(lovf)):
            bc = barcode_int(row.get("barcode"))
            vals = {k: v for k, v in row.items() if k not in ("barcode", "note") and v not in (None, "")}
            if bc and vals: loc_overrides[bc] = vals

    ev_id_overrides = {}                                    # event sticker barcode -> reassigned eventID (sticker collisions)
    evf = STAGE / "event_overrides.csv"
    if evf.exists():
        for row in csv.DictReader(open(evf)):
            bc = barcode_int(row.get("barcode")); nid = barcode_int(row.get("eventID"))
            if bc and nid: ev_id_overrides[bc] = nid

    # table-only DB columns NOT on the forms — filled here at data entry (per DB conventions)
    LOC_DEFAULTS = dict(stateProvince="Idaho", country="United States")   # constants for LEPA / Idaho
    EVT_DEFAULTS = dict(eventSizeUnit="m2")
    OCC_DEFAULTS = dict(taxonID=1, basisOfRecord="HumanObservation", reproductiveCondition="Fruiting", provenance="in situ")
    # county / locality / verbatimElevation are GPS-derived (Google-Maps lookup) -> left blank + flagged for new sites

    locs, events, occs = {}, [], []
    cur_loc = None; pending_event = None
    def norm_eo(s):
        m = re.search(r"(\d+)", str(s or "")); return f"EO{int(m.group(1))}" if m else None
    def sub_of(s):                                          # "68-3 New Plymouth" -> "3"
        m = re.search(r"\d+\s*-\s*(\d+)", str(s or "")); return m.group(1) if m else None

    for r in items:
        pt = r.get("page_type")
        src = fname.get(r.get("idx"), "")                    # source form image for this page
        if pt == "location":   # → Locations
            bc = barcode_int(r.get("location_barcode")); cur_loc = bc
            eo = norm_eo(r.get("eo") or r.get("locality")); eoid = eo2id.get(eo, "?")
            if bc in loc_full:                              # REVISIT — record exists; show it to confirm (no new entry)
                locs[bc] = {**loc_full[bc], "_barcode": bc, "_flag": "REVISIT", "_conf": r.get("confidence"),
                            "_src_image": src, "_dscn": r.get("dscn"), "_form_lat": r.get("lat"), "_form_long": r.get("long"),
                            "_form_landscapeHealth": r.get("landscape_health"), "_form_remarks": r.get("location_remarks")}
            else:                                           # NEW — locationID defaults to the barcode (next id); GPS-derived cols flagged
                sub = sub_of(r.get("locality"))
                locs[bc] = dict(locationID=bc, locationCode=(eo or "") + (f"-{sub}" if sub else ""),
                                EOID=eoid, subEOID=sub,
                                locationDecimalLatitude=r.get("lat"), locationDecimalLongitude=r.get("long"),
                                landscapeHealth=r.get("landscape_health"), locationRemarks=r.get("location_remarks"),
                                county="", locality="", verbatimElevation="", **LOC_DEFAULTS,
                                _barcode=bc, _src_image=src, _dscn=r.get("dscn"), _flag="NEW_LOCATION", _conf=r.get("confidence"),
                                _needs="county;locality;verbatimElevation (from GPS — manual)")
            if bc in loc_overrides:                          # apply human-filled fields (county/locality/elev, cleaned GPS, ...)
                for k, v in loc_overrides[bc].items(): locs[bc][k] = v
                locs[bc]["_flag"] = (str(locs[bc].get("_flag", "")) + " +RESOLVED").strip()
        elif pt == "event_p1":  # → Events (all new)
            stated = r.get("location_barcode"); sb = barcode_int(stated); loc = cur_loc   # ORDER primary
            locflag = f"LOC_REF={stated}?" if (sb and cur_loc and sb != cur_loc and sb in loc_full) else ""
            evid = barcode_int(r.get("event_barcode")); evid = ev_id_overrides.get(evid, evid)   # reassign reused sticker
            pending_event = dict(eventID=evid, eventDate=r.get("event_date"), locationID=loc,
                                 eventDecimalLatitude=r.get("event_lat"), eventDecimalLongitude=r.get("event_long"),
                                 eventSizeValue=r.get("size_value"), eventDefinition=r.get("defined"),
                                 eventCondition=r.get("condition"), organismQuantityFertile=r.get("fertile"),
                                 organismQuantityVegetative=r.get("vegetative"),
                                 measurementValuePlantArea=r.get("plant_area"), measurementValuePlantAreaUnit="",
                                 associatedTaxa=r.get("associated_taxa"), eventRemarks=None, **EVT_DEFAULTS,
                                 _stated_location=stated, _locflag=locflag, _conf=r.get("confidence"), _src_p1=src)
            events.append(pending_event)
        elif pt == "event_p2":  # → Occurrences (all new; section-4 plant barcodes)
            ev0 = pending_event["eventID"] if pending_event is not None else None
            if ev0 in overrides:                            # manual correction wins (e.g. mis-read endpoints)
                occ_list, rflag = overrides[ev0], "OVERRIDE"
            else:
                raw = sorted({barcode_int(x) for x in (r.get("occurrence_ids") or []) if barcode_int(x)})
                occ_list, rflag = raw, ""
                if len(raw) == 2 and raw[1] - raw[0] > 1:   # first+last shorthand -> expand the range
                    occ_list = list(range(raw[0], raw[1] + 1)); rflag = f"RANGE_EXPANDED({raw[0]}-{raw[1]})"
                elif len(raw) >= 2 and raw[-1] - raw[0] + 1 != len(raw):
                    rflag = "GAPPY_REVIEW"
            if pending_event is not None:
                pending_event["eventRemarks"] = r.get("event_remarks")
                pending_event["_src_images"] = ";".join(x for x in [pending_event.get("_src_p1"), src] if x)
                ev, loc = pending_event["eventID"], pending_event["locationID"]
                eo = norm_eo(locs.get(loc, {}).get("locationCode"))
            else:
                ev = loc = eo = None
            for oid in occ_list:
                fl = ";".join(f for f in [rflag, ("OCC_EXISTS" if oid <= maxocc else "")] if f)
                occs.append(dict(occurrenceID=oid, **OCC_DEFAULTS, eventID=ev, locationID=loc,
                                 EOID=eo2id.get(eo, "?"), occurrenceDate=(pending_event or {}).get("eventDate"),
                                 occurrenceRemarks="", _EO=eo, _flags=fl, _src_image=src))
            pending_event = None

    def w(path, header, rows):
        with open(path, "w", newline="") as fh:
            wr = csv.writer(fh); wr.writerow(header)
            for r in rows: wr.writerow([r.get(h, "") for h in header])
    # data columns = exact DB column names (incl. table-only ones now filled); staging helpers prefixed "_"
    w(STAGE / "locations_staging.csv",
      ["locationID","locationCode","EOID","subEOID","locationDecimalLatitude","locationDecimalLongitude","verbatimElevation","landscapeHealth","locationRemarks","locality","county","stateProvince","country","_src_image","_barcode","_flag","_needs","_dscn","_conf","_form_lat","_form_long"], list(locs.values()))
    w(STAGE / "events_staging.csv",
      ["eventID","eventDate","locationID","eventDecimalLatitude","eventDecimalLongitude","eventSizeValue","eventSizeUnit","eventDefinition","eventCondition","organismQuantityFertile","organismQuantityVegetative","measurementValuePlantArea","measurementValuePlantAreaUnit","associatedTaxa","eventRemarks","_src_images","_stated_location","_locflag","_conf"], events)
    w(STAGE / "occurrences_staging.csv",
      ["occurrenceID","taxonID","basisOfRecord","reproductiveCondition","provenance","eventID","locationID","EOID","occurrenceDate","occurrenceRemarks","_src_image","_EO","_flags"], occs)

    revisit = sum(1 for l in locs.values() if l["_flag"] == "REVISIT"); new = len(locs) - revisit
    coll = sum(1 for o in occs if "OCC_EXISTS" in o.get("_flags",""))
    rng = len({o["eventID"] for o in occs if "RANGE_EXPANDED" in o.get("_flags","")})
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    with open(ROOT / "Multimedia_pipeline" / "PIPELINE_LOG.md", "a") as fh:
        fh.write(f"\n## {stamp} — field_forms_ocr --load {Path(results).name}\n"
                 f"- staged {len(locs)} locations ({revisit} revisit / {new} new), {len(events)} events, "
                 f"{len(occs)} occurrences; occ collisions {coll}. Table-only cols auto-filled (EOID, taxonID, basisOfRecord, "
                 f"reproductiveCondition, provenance, eventSizeUnit, stateProvince, country, locationCode/subEOID). Review staging_2026/.\n")
    print(f"staged: {len(locs)} Locations ({revisit} REVISIT, {new} NEW_LOCATION), {len(events)} Events, {len(occs)} Occurrences")
    print("  table-only columns auto-filled — Occurrences: taxonID/basisOfRecord/reproductiveCondition/provenance; "
          "Events: eventSizeUnit; Locations: stateProvince/country + derived locationCode/subEOID/EOID")
    if new:  print("  NEW location: county/locality/verbatimElevation left blank for your manual GPS lookup (see _needs)")
    if rng:  print(f"  ⚠ {rng} events used first+last RANGE shorthand — occurrenceIDs expanded; confirm vs plant boards")
    if coll: print(f"  ⚠ {coll} occurrenceIDs ≤ current max ({maxocc}) — check collision")
    print("  -> staging_2026/{locations,events,occurrences}_staging.csv  (no DB writes)")

def commit(db, apply):   # GATED LOAD: reviewed staging -> DB (Locations -> Events -> Occurrences)
    def rd(p): return list(csv.DictReader(open(STAGE / p)))
    locs, events, occs = rd("locations_staging.csv"), rd("events_staging.csv"), rd("occurrences_staging.csv")
    con = sqlite3.connect(db); cur = con.cursor()
    cols = {t: [r[1] for r in cur.execute(f"PRAGMA table_info({t})")] for t in ("Locations", "Events", "Occurrences")}
    exist = {t: {r[0] for r in cur.execute(f"SELECT {k} FROM {t}")}
             for t, k in (("Locations", "locationID"), ("Events", "eventID"), ("Occurrences", "occurrenceID"))}

    def clean(row, table):   # keep real DB columns only; ""->None; normalise dates
        out = {}
        for k, v in row.items():
            if k.startswith("_") or k not in cols[table]: continue
            v = (v or "").strip()
            if k in ("eventDate", "occurrenceDate"): v = norm_date(v)
            out[k] = v if v not in ("", None) else None
        return out

    # events & occurrences must all be NEW; a staged ID already in the DB = sticker/barcode collision to resolve
    ev_coll  = sorted({int(e["eventID"]) for e in events if e.get("eventID") and int(e["eventID"]) in exist["Events"]})
    occ_coll = sorted({int(o["occurrenceID"]) for o in occs if o.get("occurrenceID") and int(o["occurrenceID"]) in exist["Occurrences"]})

    new_locs   = [clean(l, "Locations")   for l in locs   if "NEW_LOCATION" in l.get("_flag", "") and int(l["locationID"]) not in exist["Locations"]]
    new_events = [clean(e, "Events")      for e in events if e.get("eventID") and int(e["eventID"]) not in exist["Events"]]
    new_occs   = [clean(o, "Occurrences") for o in occs   if o.get("occurrenceID") and int(o["occurrenceID"]) not in exist["Occurrences"]]

    # validation — collisions + referential integrity (parent exists in DB or in this batch)
    loc_ids = exist["Locations"] | {int(l["locationID"]) for l in new_locs}
    ev_ids  = exist["Events"]    | {int(e["eventID"]) for e in new_events}
    problems = []
    for ev in ev_coll:  problems.append(f"eventID {ev} COLLIDES with an existing DB event (reused sticker) — reassign via event_overrides.csv")
    for oc in occ_coll: problems.append(f"occurrenceID {oc} COLLIDES with an existing DB occurrence")
    for e in new_events:
        if int(e["locationID"]) not in loc_ids: problems.append(f"event {e['eventID']} -> missing locationID {e['locationID']}")
    for o in new_occs:
        if o.get("eventID") and int(o["eventID"]) not in ev_ids: problems.append(f"occ {o['occurrenceID']} -> missing eventID {o['eventID']}")
        if o.get("locationID") and int(o["locationID"]) not in loc_ids: problems.append(f"occ {o['occurrenceID']} -> missing locationID {o['locationID']}")
    skipped = (len(locs)-len(new_locs), len(events)-len(new_events), len(occs)-len(new_occs))

    print(f"GATED LOAD plan (Stage A) — to INSERT: {len(new_locs)} Locations, {len(new_events)} Events, {len(new_occs)} Occurrences")
    print(f"  already in DB / skipped: {skipped[0]} loc, {skipped[1]} ev, {skipped[2]} occ")
    if new_locs: print(f"  new Location(s): " + ", ".join(f"{l['locationID']}={l.get('locationCode')}" for l in new_locs))
    def _rng(rows, key):  # guard min()/max() when a batch adds only some entity types
        ids = [int(r[key]) for r in rows]
        return f"{min(ids)}-{max(ids)}" if ids else "none"
    print(f"  eventID range {_rng(new_events, 'eventID')}; occurrenceID range {_rng(new_occs, 'occurrenceID')}")
    if problems:
        print("  ⚠ INTEGRITY PROBLEMS (fix before load):"); [print("     -", p) for p in problems[:20]]
        con.close(); return
    if not apply:
        print("\nDRY-RUN. Re-run with --commit --apply to write (DB backed up first)."); con.close(); return

    bak = Path(db).with_name(Path(db).name + ".bak-formsload-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    shutil.copy2(db, bak)
    def ins(table, rows):
        for r in rows:
            keys = list(r.keys())
            cur.execute(f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join('?'*len(keys))})", [r[k] for k in keys])
    ins("Locations", new_locs); ins("Events", new_events); ins("Occurrences", new_occs)
    con.commit(); con.close()
    with open(ROOT / "Multimedia_pipeline" / "PIPELINE_LOG.md", "a") as fh:
        fh.write(f"\n## {datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')} — field_forms_ocr --commit --apply\n"
                 f"- inserted {len(new_locs)} Locations, {len(new_events)} Events, {len(new_occs)} Occurrences from Stage A staging. Backup `{bak.name}`.\n")
    print(f"APPLIED: +{len(new_locs)} Locations, +{len(new_events)} Events, +{len(new_occs)} Occurrences. Backup {bak.name}. Logged.")

def forms_multimedia(db, apply):   # link the field-form images to their Location/Event records in Multimedia (evidence)
    import hashlib
    from PIL import Image
    FORMS = ROOT / "Field_forms" / "2026"; MAIN = ROOT / "Multimedia_main"
    def sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
        return h.hexdigest()
    def cap(p):
        try:
            ex = Image.open(p)._getexif() or {}; return ex.get(36867) or ex.get(306)
        except Exception: return None

    jobs = []   # (pxl_filename, tableID, fk_col, fk_id, title)
    for l in csv.DictReader(open(STAGE / "locations_staging.csv")):
        if l.get("_src_image"):
            jobs.append((l["_src_image"], 9, "locationID", l["locationID"], f"2026 Location field data sheet — {l['locationCode']}"))
    for e in csv.DictReader(open(STAGE / "events_staging.csv")):
        pages = [x for x in (e.get("_src_images") or "").split(";") if x]
        for i, img in enumerate(pages, 1):
            jobs.append((img, 11, "eventID", e["eventID"], f"2026 Event field data sheet (page {i} of {len(pages)}) — event {e['eventID']}"))

    con = sqlite3.connect(db); cur = con.cursor()
    have_ident = {r[0] for r in cur.execute("SELECT identifier FROM Multimedia WHERE identifier IS NOT NULL")}
    maxmm = cur.execute("SELECT MAX(multimediaID) FROM Multimedia").fetchone()[0] or 0
    plan, missing = [], []
    for pxl, tid, fkcol, fkid, title in jobs:
        src = FORMS / pxl
        if not src.exists(): missing.append(pxl); continue
        digest = sha(src); m = re.match(r"PXL_(\d{4})(\d{2})(\d{2})", pxl)
        fdate = f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else "2026-06-27"
        plan.append(dict(pxl=pxl, src=str(src), newname=f"LEPA_{fdate}_{digest[:8]}.jpg", digest=digest,
                         capture=cap(src), fdate=fdate, createDate=f"{fdate[5:7]}-{fdate[8:10]}-{fdate[0:4]}",
                         tableID=tid, fkcol=fkcol, fkid=int(fkid), title=title))
    todo = [p for p in plan if p["newname"] not in have_ident]
    nloc = sum(1 for p in todo if p["tableID"] == 9); nev = sum(1 for p in todo if p["tableID"] == 11)
    print(f"forms→Multimedia: {len(jobs)} links ({sum(p['tableID']==9 for p in plan)} Location, {sum(p['tableID']==11 for p in plan)} Event); to insert: {len(todo)} ({nloc} loc, {nev} ev)")
    if missing: print(f"  ⚠ {len(missing)} form images missing on disk: {missing[:5]}")
    if not apply:
        print("DRY-RUN. Re-run with --forms-mm --apply (copies images to Multimedia_main + inserts Multimedia rows)."); con.close(); return
    bak = Path(db).with_name(Path(db).name + ".bak-formsmm-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")); shutil.copy2(db, bak)
    MAIN.mkdir(exist_ok=True)
    for p in todo:
        dst = MAIN / p["newname"]
        if not dst.exists(): shutil.copy2(p["src"], dst)
        maxmm += 1
        cur.execute("""INSERT INTO Multimedia (multimediaID,identifier,type,format,createDate,title,multimediaStorage,
                       tableID,locationID,eventID,remarks,originalFilename,fileYear,folderDate,captureTimestamp,sha256)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (maxmm, p["newname"], "field form", "jpeg", p["createDate"], p["title"], "Google Drive", p["tableID"],
                     p["fkid"] if p["fkcol"] == "locationID" else None, p["fkid"] if p["fkcol"] == "eventID" else None,
                     "2026 field data sheet (evidence for the record)", p["pxl"], "2026", p["fdate"], p["capture"], p["digest"]))
    con.commit(); con.close()
    with open(ROOT / "Multimedia_pipeline" / "PIPELINE_LOG.md", "a") as fh:
        fh.write(f"\n## {datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')} — field_forms_ocr --forms-mm --apply\n"
                 f"- linked {len(todo)} field-form images to Multimedia ({nloc} Location tableID 9, {nev} Event tableID 11); copied to Multimedia_main. Backup `{bak.name}`.\n")
    print(f"APPLIED: linked {len(todo)} form images to Multimedia ({nloc} Location, {nev} Event). Backup {bak.name}. Logged.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "LEPA_SQL.db"))
    ap.add_argument("--year", default="2026")
    ap.add_argument("--worklist", action="store_true")
    ap.add_argument("--load")
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--forms-mm", dest="forms_mm", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if a.commit: commit(a.db, a.apply)
    elif a.forms_mm: forms_multimedia(a.db, a.apply)
    elif a.worklist: worklist(a.year)
    elif a.load: load(a.db, a.load)
    else: ap.print_help()

if __name__ == "__main__":
    main()
