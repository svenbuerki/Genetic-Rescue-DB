#!/usr/bin/env python3
"""
Per-EO independent size->seed models (trends), with a size-RANGE diagnostic
===========================================================================

Fits an independent allometric model  log10(yield) ~ log10(crown)  separately for
each Element Occurrence, to inspect the within-population trend (slope) and level.

Critical caveat this script makes explicit: a population whose plants span only a
NARROW size range cannot reveal a slope even if one exists (range restriction
attenuates the slope toward 0). So a "flat" EO may be biologically decoupled OR
simply size-restricted that year. The report flags low-range EOs and tests whether
flat slopes track narrow crown ranges. (Motivated by the field note that EO27 plants
were unusually small in 2025 relative to prior years.)

Size = crown width (selected as best predictor in size_seed_model.py). Yield = summed
germplasmQuantityEstimate per occurrence (~viable seed; field viability >98%).

Usage:  python3 Queries/per_eo_trends.py [--db PATH] [--bl-key PATH] [--min-n 10] [--no-plot]
Outputs: console table + Queries/per_eo_trends.tsv + Queries/per_eo_trends.png (small multiples)
"""
import argparse, csv, sqlite3
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "LEPA_SQL.db"
DEFAULT_BLKEY = ROOT.parent.parent / "LEPA_EO_spatial_clustering" / "data" / "EO_group_BL_summary.csv"


def year_sql(year):
    """SQL filter on occurrence year ('all' = no filter). Dates stored as 'MM-DD' without a year
    (events 660-724, July 2026 -- known data issue) are counted as 2026."""
    return (" AND (? = 'all' OR substr(v.occurrenceDate, -4) = ? "
            "OR (? = '2026' AND length(v.occurrenceDate) = 5))"), (year, year, year)


def suffix(year):
    return "" if year == "all" else f"_{year}"
BL_ORDER = ["BL4", "BL5", "BL3", "BL1", "BL2"]
BL_COLORS = {"BL1": "#E41A1C", "BL2": "#377EB8", "BL3": "#4DAF4A", "BL4": "#984EA3", "BL5": "#FF7F00", "Unassigned": "#999999"}


def load_bl_key(path):
    loc = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            for lid in str(r["Population_IDs"]).replace('"', "").split(","):
                if lid.strip().isdigit():
                    loc[int(lid.strip())] = r["BL"]
    return loc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--bl-key", default=str(DEFAULT_BLKEY))
    ap.add_argument("--min-n", type=int, default=10)
    ap.add_argument("--no-plot", action="store_true")
    ap.add_argument("--year", default="all", help="2025, 2026 or all (default)")
    args = ap.parse_args(); YEAR = args.year
    blkey = load_bl_key(args.bl_key)

    con = sqlite3.connect(args.db)
    rows = con.execute("""SELECT v.occurrenceCrownSize c, v.seedQuantityTotal y, e.EOCode, o.locationID
        FROM vOccurrenceTraits v JOIN Occurrences o ON v.occurrenceID=o.occurrenceID
        LEFT JOIN EOs e ON o.EOID=e.EOID
        WHERE v.occurrenceCrownSize>0 AND v.seedQuantityTotal>0""" + year_sql(YEAR)[0], year_sql(YEAR)[1]).fetchall()
    con.close()
    df = pd.DataFrame(rows, columns=["c", "y", "EO", "locID"])
    df["BL"] = df.locID.map(lambda L: blkey.get(L, "Unassigned"))
    df["logc"], df["logy"] = np.log10(df.c), np.log10(df.y)

    out = []
    for eo, g in df.groupby("EO"):
        if len(g) < args.min_n:
            continue
        lr = stats.linregress(g.logc, g.logy)
        ci = 1.96 * lr.stderr
        # crown range diagnostic: log10 span and IQR (range restriction -> small span)
        span = g.logc.max() - g.logc.min()
        out.append(dict(EO=eo, BL=g.BL.iloc[0], n=len(g),
                        crown_min=g.c.min(), crown_med=g.c.median(), crown_max=g.c.max(),
                        logc_span=round(span, 2), slope=lr.slope, slope_lo=lr.slope - ci, slope_hi=lr.slope + ci,
                        intercept=lr.intercept, r2=lr.rvalue ** 2, p=lr.pvalue))
    res = pd.DataFrame(out)
    res["__o"] = res.BL.map(lambda b: BL_ORDER.index(b) if b in BL_ORDER else 9)
    res = res.sort_values(["__o", "EO"]).drop(columns="__o")

    print(f"n={len(df)} plants; per-EO independent models (crown -> yield), min-n={args.min_n}\n")
    print(f"{'EO':<7}{'BL':>4}{'n':>4}{'crown min/med/max':>20}{'logSpan':>8}{'slope[95%CI]':>20}{'R2':>6}{'p':>8}")
    for _, r in res.iterrows():
        print(f"{r.EO:<7}{r.BL:>4}{int(r.n):>4}"
              f"{f'{r.crown_min:.0f}/{r.crown_med:.0f}/{r.crown_max:.0f}':>20}{r.logc_span:>8.2f}"
              f"{f'{r.slope:+.2f}[{r.slope_lo:+.2f},{r.slope_hi:+.2f}]':>20}{r.r2:>6.2f}{r.p:>8.1e}")

    # diagnostic: do flat slopes track narrow crown ranges?
    rho, p = stats.spearmanr(res.logc_span, res.slope)
    print(f"\nRange-restriction check: Spearman(crown log-span, slope) = {rho:+.2f} (p={p:.2f})")
    print("  positive => EOs with a wider size range show steeper slopes (i.e. flat slopes can be range-restriction artifacts).")
    # EO27 size context vs the rest
    if "EO27" in set(res.EO):
        e = df[df.EO == "EO27"].c; others = df[df.EO != "EO27"].c
        pct = (others.median() and (e.median() / others.median()))
        u, pu = stats.mannwhitneyu(e, others, alternative="less")
        print(f"\nEO27 size context: median crown {e.median():.0f} cm vs {others.median():.0f} cm elsewhere "
              f"({100*pct:.0f}% of the rest); Mann-Whitney 'EO27 smaller' p={pu:.1e}.")
        eo27 = res[res.EO == "EO27"].iloc[0]
        narrow = res.logc_span.rank().loc[res.EO == "EO27"].iloc[0]
        print(f"  EO27 crown log-span = {eo27.logc_span:.2f} (rank {int(narrow)}/{len(res)} among EOs; low rank = narrow range).")

    res.to_csv(Path(__file__).resolve().parent / f"per_eo_trends{suffix(YEAR)}.tsv", sep="\t", index=False)
    print(f"\ntable -> Queries/per_eo_trends{suffix(YEAR)}.tsv")

    if not args.no_plot:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        eos = list(res.EO); ncol = 4; nrow = int(np.ceil(len(eos) / ncol))
        fig, axes = plt.subplots(nrow, ncol, figsize=(4 * ncol, 3 * nrow), squeeze=False)
        xall = np.log10(np.array([df.c.min(), df.c.max()]))
        for i, eo in enumerate(eos):
            ax = axes[i // ncol][i % ncol]; g = df[df.EO == eo]; r = res[res.EO == eo].iloc[0]
            ax.scatter(g.c, g.y, s=18, alpha=0.6, color=BL_COLORS[r.BL])
            xs = np.linspace(g.logc.min(), g.logc.max(), 20)
            ax.plot(10 ** xs, 10 ** (r.intercept + r.slope * xs), color=BL_COLORS[r.BL], lw=2)
            ax.set_xscale("log"); ax.set_yscale("log")
            ax.set_xlim(10 ** xall[0] * 0.8, 10 ** xall[1] * 1.2)
            ax.set_title(f"{eo} ({r.BL}) n={int(r.n)}\nslope={r.slope:+.2f}, R²={r.r2:.2f}", fontsize=9)
            ax.tick_params(labelsize=7)
        for j in range(len(eos), nrow * ncol):
            axes[j // ncol][j % ncol].axis("off")
        fig.supxlabel("crown width (cm, log) — note each panel's size RANGE"); fig.supylabel("seed yield (log)")
        fig.suptitle(f"Lepidium papilliferum — per-EO size→seed trends ({YEAR}); flat panels may be size-range-restricted", y=1.01)
        fig.tight_layout()
        out = Path(__file__).resolve().parent / f"per_eo_trends{suffix(YEAR)}.png"
        fig.savefig(out, dpi=120, bbox_inches="tight"); print(f"figure -> {out}")


if __name__ == "__main__":
    main()
