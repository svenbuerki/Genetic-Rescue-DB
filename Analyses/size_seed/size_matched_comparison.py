#!/usr/bin/env python3
"""
Model-free size-matched test: do EO27/EO70 plants yield less than SAME-SIZE plants elsewhere?
=============================================================================================

This makes NO allometric/functional-form assumption. For every plant we find its
k nearest neighbours in crown size drawn from *other EOs*, and take the ratio of the
plant's seed yield to the median yield of those size-matched controls. If a population's
ratios are systematically < 1, its plants under-produce relative to equally-sized plants
elsewhere — a direct answer that cannot be a size or curve-shape artifact.

  ratio_i      = yield_i / median(yield of k crown-nearest plants from other EOs)
  per-EO fold  = median(ratio) ; Wilcoxon signed-rank on log10(ratio) vs 0 ; BH-FDR across EOs

Cross-checks the model-based "fold-of-expectation" in size_seed_model.py (they should agree).

Usage:  python3 Queries/size_matched_comparison.py [--db PATH] [--bl-key PATH] [--k 15] [--min-n 10] [--no-plot]
"""
import argparse, csv, sqlite3
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multitest import fdrcorrection

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
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        for lid in str(r["Population_IDs"]).replace('"', "").split(","):
            if lid.strip().isdigit():
                loc[int(lid.strip())] = r["BL"]
    return loc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--bl-key", default=str(DEFAULT_BLKEY))
    ap.add_argument("--k", type=int, default=15)
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
    df = pd.DataFrame(rows, columns=["c", "y", "EO", "locID"]).reset_index(drop=True)
    df["BL"] = df.locID.map(lambda L: blkey.get(L, "Unassigned"))
    df["logc"] = np.log10(df.c)

    # per-plant ratio vs k crown-nearest controls from OTHER EOs
    ratios = np.full(len(df), np.nan); matchq = np.full(len(df), np.nan)
    logc = df.logc.values; yv = df.y.values; eo = df.EO.values
    for i in range(len(df)):
        mask = eo != eo[i]
        d = np.abs(logc[mask] - logc[i])
        order = np.argsort(d)[:args.k]
        ctrl = yv[mask][order]
        ratios[i] = yv[i] / np.median(ctrl)
        matchq[i] = np.median(d[order])           # median |Δ log10 crown| of the matches
    df["ratio"] = ratios; df["matchq"] = matchq
    print(f"n={len(df)} plants; k={args.k} size-matched controls per plant (from other EOs).")
    print(f"matching quality: median |Δlog10 crown| = {np.median(matchq):.3f} "
          f"(≈ ×/÷{10**np.median(matchq):.2f} in crown) — small = well matched.\n")

    out = []
    for e, g in df.groupby("EO"):
        if len(g) < args.min_n:
            continue
        lr = np.log10(g.ratio.values)
        W, p = stats.wilcoxon(lr) if len(lr) >= 6 else (np.nan, np.nan)
        out.append(dict(EO=e, BL=g.BL.iloc[0], n=len(g), fold=np.median(g.ratio), p=p))
    res = pd.DataFrame(out)
    res["q"] = fdrcorrection(res.p.fillna(1))[1]
    res["__o"] = res.BL.map(lambda b: BL_ORDER.index(b) if b in BL_ORDER else 9)
    res = res.sort_values(["__o", "fold"])

    print(f"{'EO':<7}{'BL':>4}{'n':>4}{'fold vs size-matched':>22}{'q(FDR)':>9}  verdict")
    for _, r in res.iterrows():
        v = "UNDER-produces" if (r.q < 0.05 and r.fold < 1) else ("over" if (r.q < 0.05 and r.fold > 1) else "~matches")
        print(f"{r.EO:<7}{r.BL:>4}{int(r.n):>4}{r.fold:>22.2f}{r.q:>9.1e}  {v}")
    flagged = list(res[(res.q < 0.05) & (res.fold < 1)].EO)
    print(f"\nUNDER-producing vs size-matched controls (FDR<0.05): {flagged or 'none'}")
    res.drop(columns="__o").to_csv(Path(__file__).resolve().parent / f"size_matched_comparison{suffix(YEAR)}.tsv", sep="\t", index=False)
    print(f"table -> Queries/size_matched_comparison{suffix(YEAR)}.tsv")

    if not args.no_plot:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(13, 5))
        rr = res.iloc[::-1]
        ax[0].barh(range(len(rr)), rr.fold, color=[BL_COLORS[b] for b in rr.BL])
        ax[0].axvline(1.0, color="k", ls="--")
        ax[0].set_yticks(range(len(rr))); ax[0].set_yticklabels([f"{e} ({b})" for e, b in zip(rr.EO, rr.BL)], fontsize=8)
        ax[0].set(xlabel="yield ÷ size-matched controls (fold)", title="Model-free: each EO vs same-crown plants elsewhere\n<1 = under-produces for its size")
        # EO27/EO70 ratio distributions vs the null (1.0)
        for j, tgt in enumerate(["EO27", "EO70"]):
            g = df[df.EO == tgt]
            ax[1].scatter(np.full(len(g), j) + np.random.uniform(-0.12, 0.12, len(g)), g.ratio, s=18, alpha=0.5,
                          color=BL_COLORS[g.BL.iloc[0]])
            ax[1].plot([j - 0.2, j + 0.2], [g.ratio.median()] * 2, "k-", lw=2)
        ax[1].axhline(1.0, color="k", ls="--", label="parity with size-matched controls")
        ax[1].set_yscale("log"); ax[1].set_xticks([0, 1]); ax[1].set_xticklabels(["EO27 (BL4)", "EO70 (BL2)"])
        ax[1].set(ylabel="yield ÷ size-matched controls", title="Per-plant ratios (bar = median)"); ax[1].legend(fontsize=8)
        fig.suptitle(f"Lepidium papilliferum — model-free size-matched seed-yield comparison ({YEAR})", y=1.02)
        fig.tight_layout()
        out = Path(__file__).resolve().parent / f"size_matched_comparison{suffix(YEAR)}.png"
        fig.savefig(out, dpi=130, bbox_inches="tight"); print(f"figure -> {out}")


if __name__ == "__main__":
    main()
