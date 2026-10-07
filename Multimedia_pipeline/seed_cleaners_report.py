#!/usr/bin/env python3
"""Seed-cleaner leaderboard for a season → Multimedia_pipeline/SEED_CLEANERS_<year>.md

Built from LEPA_SQL.db: one germplasm (= all seeds of one mother plant) has exactly one cleaner
(`Germplasm.personID`, from the initials on the event envelope; see germplasm_seeds.py). Germplasm without
a cleaner are counted separately, with the envelopes they come from, so they can be assigned later.

Usage:  python3 Multimedia_pipeline/seed_cleaners_report.py [--year 2026]
"""
import argparse, sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def mdy(d):  # "MM-DD-YYYY" -> sortable "YYYY-MM-DD"
    return f"{d[6:]}-{d[:2]}-{d[3:5]}" if d and len(d) == 10 else ""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--year", default="2026"); a = ap.parse_args()
    con = sqlite3.connect(ROOT / "LEPA_SQL.db"); cur = con.cursor()
    rows = cur.execute("""SELECT g.germplasmID, g.personID, COALESCE(p.firstName||' '||p.lastName,''), g.locationID,
                                 g.eventID, g.germplasmWeight, g.germplasmQuantityEstimate, g.acquisitionDate
                          FROM Germplasm g LEFT JOIN Persons p USING(personID)
                          WHERE g.acquisitionDate LIKE ?""", (f"%{a.year}",)).fetchall()
    proxy = {"10-04-2026", "10-05-2026", "10-06-2026"}          # photo / posting dates used as proxies (#20)
    by = {}
    for gid, pid, name, loc, ev, w, est, d in rows:
        k = pid or 0
        b = by.setdefault(k, dict(name=name or "— not yet assigned —", n=0, g=0.0, seeds=0.0, locs=set(), evs=set(), dates=set()))
        b["n"] += 1; b["g"] += w or 0; b["seeds"] += max(est or 0, 0); b["locs"].add(loc); b["evs"].add(ev)
        if d and d not in proxy: b["dates"].add(mdy(d))
    total = len(rows); assigned = total - by.get(0, {}).get("n", 0)
    ranked = sorted((k for k in by if k), key=lambda k: -by[k]["n"])
    out = [f"# {a.year} seed cleaning — leaderboard",
           "",
           f"*Generated {datetime.now():%Y-%m-%d} from `LEPA_SQL.db` by `seed_cleaners_report.py`. "
           "A **germplasm** is all the seeds of one mother plant (occurrence); each has exactly one cleaner, "
           "recorded from the initials on the event envelope (`Germplasm.personID`).*",
           "",
           f"**{total} germplasm** cleaned and loaded for {a.year}; **{assigned}** have a known cleaner, "
           f"**{total - assigned}** are not yet assigned (no initials on the envelope, or several initials "
           "written once for the whole envelope).",
           "",
           "| Rank | Cleaner | Germplasm | Share of assigned | Seed (g) | Est. seeds | Locations | Envelopes (events) | Dates written on envelopes |",
           "|---:|---|---:|---:|---:|---:|---:|---:|---|"]
    for i, k in enumerate(ranked, 1):
        b = by[k]; dr = (f"{min(b['dates'])} → {max(b['dates'])}" if b["dates"] else "—")
        out.append(f"| {i} | {b['name']} | {b['n']} | {100 * b['n'] / assigned:.0f}% | {b['g']:.2f} | {b['seeds']:,.0f} | "
                   f"{len(b['locs'])} | {len(b['evs'])} | {dr} |")
    if 0 in by:
        b = by[0]
        out.append(f"| — | *{b['name']}* | {b['n']} | — | {b['g']:.2f} | {b['seeds']:,.0f} | {len(b['locs'])} | {len(b['evs'])} | — |")
    out += ["", "## By location", "", "| Location | Germplasm | " + " | ".join(by[k]["name"] for k in ranked) + " | Not assigned |",
            "|---|---:|" + "---:|" * (len(ranked) + 1)]
    locs = sorted({r[3] for r in rows})
    for l in locs:
        code = cur.execute("SELECT locationCode FROM Locations WHERE locationID=?", (l,)).fetchone()[0]
        cnt = {}
        for r in rows:
            if r[3] == l: cnt[r[1] or 0] = cnt.get(r[1] or 0, 0) + 1
        out.append(f"| loc {l} ({code}) | {sum(cnt.values())} | " + " | ".join(str(cnt.get(k, "")) for k in ranked)
                   + f" | {cnt.get(0, '')} |")
    out += ["", "**Notes**",
            "- *Est. seeds* comes from seed weight via the 1000-seed-weight equation (negative estimates for very "
            "light lots are counted as 0).",
            "- *Dates written on envelopes* covers only envelopes where the cleaner wrote a date. Photo or posting "
            "dates used as stand-ins are excluded (see issue #20).",
            "- Germplasm without initials were attributed from **handwriting samples** where possible (Ian; "
            "Peggy for location 27), and each match was confirmed by Sven. The rest are tracked in "
            "[issue #24](https://github.com/svenbuerki/Genetic-Rescue-DB/issues/24).",
            "- To assign the remaining germplasm, fill in `staging_2026/cleaner_assignment.csv` (one row per "
            "envelope) and run `germplasm_seeds.py --assign-cleaners`.",
            "- Campaign context: [`REPORT_2026_campaign.md`](REPORT_2026_campaign.md)."]
    dst = ROOT / "Multimedia_pipeline" / f"SEED_CLEANERS_{a.year}.md"
    dst.write_text("\n".join(out) + "\n")
    print(f"wrote {dst}  ({total} germplasm, {assigned} assigned, {len(ranked)} cleaners)")

if __name__ == "__main__":
    main()
