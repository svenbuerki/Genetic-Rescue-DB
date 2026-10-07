#!/usr/bin/env python3
"""
Year-to-year comparison of the size -> seed shortfall (2025 vs 2026)
=====================================================================

Run AFTER size_matched_comparison.py with --year 2025 and --year 2026.
Reads its per-year tables, recomputes the per-plant size-matched ratios (same method as
size_matched_comparison.py: yield / median yield of the k crown-nearest plants from OTHER EOs,
within the same year), and reports:

  - per-plant ratio distribution per year (IQR, share below 0.5x)
  - for EO27 / EO70 / EO08: share of plants below parity and below 0.5x
  - median crown per EO and year (is a "bad year" visible as small plants?)
  - figure: per-EO fold-of-expectation, 2025 vs 2026, for EOs with n >= min-n in both years

Each year's expectation is relative to THAT year's species curve, so a year-wide drop in
yield is absorbed; a population that moves between years moved relative to the others.

Usage:  python3 Queries/size_seed_years.py [--db PATH] [--k 15] [--min-n 10] [--no-plot]
"""
import argparse, sqlite3
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent / "LEPA_SQL.db"
YEARS = ["2025", "2026"]
FOCUS = ["EO27", "EO70", "EO08"]


def load(db, year):
    con = sqlite3.connect(db)
    rows = con.execute(
        """SELECT v.occurrenceCrownSize c, v.seedQuantityTotal y, e.EOCode
           FROM vOccurrenceTraits v JOIN Occurrences o ON v.occurrenceID=o.occurrenceID
           LEFT JOIN EOs e ON o.EOID=e.EOID
           WHERE v.occurrenceCrownSize>0 AND v.seedQuantityTotal>0
             AND (substr(v.occurrenceDate, -4) = ? OR (? = '2026' AND length(v.occurrenceDate) = 5))""",
        (year, year)).fetchall()
    con.close()
    df = pd.DataFrame(rows, columns=["c", "y", "EO"])
    df["EO"] = df.EO.fillna("EOID?")
    return df


def matched_ratios(df, k):
    logc, yv, eo = np.log10(df.c.values), df.y.values, df.EO.values
    r = np.empty(len(df))
    for i in range(len(df)):
        m = eo != eo[i]
        r[i] = yv[i] / np.median(yv[m][np.argsort(np.abs(logc[m] - logc[i]))[:k]])
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--k", type=int, default=15)
    ap.add_argument("--min-n", type=int, default=10)
    ap.add_argument("--no-plot", action="store_true")
    a = ap.parse_args()

    per_eo = []
    for yr in YEARS:
        df = load(a.db, yr)
        df["ratio"] = matched_ratios(df, a.k)
        q1, q3 = np.percentile(df.ratio, [25, 75])
        print(f"{yr}: n={len(df)}  per-plant ratio IQR {q1:.2f}-{q3:.2f}x, "
              f"{100 * (df.ratio < 0.5).mean():.0f}% of plants below 0.5x; median crown {df.c.median():.0f} cm")
        for eo in FOCUS:
            g = df[df.EO == eo]
            if len(g):
                print(f"   {eo}: n={len(g)}  median crown {g.c.median():.0f} cm vs {df[df.EO != eo].c.median():.0f} cm elsewhere; "
                      f"{100 * (g.ratio < 1).mean():.0f}% below parity, {100 * (g.ratio < 0.5).mean():.0f}% below 0.5x")
        matched = pd.read_csv(HERE / f"size_matched_comparison_{yr}.tsv", sep="\t")
        for _, r in matched.iterrows():
            per_eo.append(dict(year=yr, EO=r.EO, BL=r.BL, n=int(r.n), matched=r.fold, q_matched=r.q,
                               crown=df[df.EO == r.EO].c.median()))
    t = pd.DataFrame(per_eo)
    both = t.pivot_table(index=["EO", "BL"], columns="year", values=["matched", "n", "crown"])
    both = both.dropna()
    both = both[(both[("n", "2025")] >= a.min_n) & (both[("n", "2026")] >= a.min_n)]
    print("\nEOs sampled (n >= %d) in both years — size-matched fold:" % a.min_n)
    print(f"{'EO':<6}{'BL':>4}{'n25':>5}{'n26':>5}{'fold25':>8}{'fold26':>8}{'crown25':>9}{'crown26':>9}")
    for (eo, bl), r in both.iterrows():
        print(f"{eo:<6}{bl:>4}{int(r[('n', '2025')]):>5}{int(r[('n', '2026')]):>5}{r[('matched', '2025')]:>8.2f}"
              f"{r[('matched', '2026')]:>8.2f}{r[('crown', '2025')]:>9.0f}{r[('crown', '2026')]:>9.0f}")
    t.to_csv(HERE / "size_seed_years.tsv", sep="\t", index=False)
    print("\ntable -> Queries/size_seed_years.tsv")

    if not a.no_plot:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        pal = {"BL1": "#E41A1C", "BL2": "#377EB8", "BL3": "#4DAF4A", "BL4": "#984EA3", "BL5": "#FF7F00"}
        fig, ax = plt.subplots(figsize=(6.5, 5.5))
        def spread(vals, gap=0.05):            # nudge labels apart (log10 units) so none overlap
            order = np.argsort(vals); out = np.log10(np.asarray(vals, float))
            for i in range(1, len(order)):
                a_, b_ = order[i - 1], order[i]
                out[b_] = max(out[b_], out[a_] + gap)
            return 10 ** out
        lab0 = spread([r[("matched", "2025")] for _, r in both.iterrows()])
        lab1 = spread([r[("matched", "2026")] for _, r in both.iterrows()])
        for j, ((eo, bl), r) in enumerate(both.iterrows()):
            y0, y1 = r[("matched", "2025")], r[("matched", "2026")]
            ax.plot([0, 1], [y0, y1], "-o", color=pal.get(bl, "grey"), lw=2, ms=6)
            ax.text(1.04, lab1[j], f"{eo} ({bl})", va="center", fontsize=9, color=pal.get(bl, "grey"))
            ax.text(-0.04, lab0[j], eo, va="center", ha="right", fontsize=9, color=pal.get(bl, "grey"))
        ax.axhline(1, color="k", ls="--", lw=1)
        ax.set_yscale("log"); ax.set_xlim(-0.35, 1.45); ax.set_xticks([0, 1]); ax.set_xticklabels(YEARS)
        ax.set_yticks([0.25, 0.5, 1, 2, 4]); ax.set_yticklabels(["0.25×", "0.5×", "1×", "2×", "4×"])
        ax.set_ylabel("seed yield ÷ same-size plants in other EOs (median)")
        ax.set_title(f"Lepidium papilliferum — size-matched seed yield by EO, 2025 vs 2026\n"
                     f"(EOs with n ≥ {a.min_n} in both years; <1 = fewer seeds than same-size plants)", fontsize=10)
        out = HERE / "size_seed_years.png"
        fig.savefig(out, dpi=130, bbox_inches="tight"); print(f"figure -> {out}")


if __name__ == "__main__":
    main()
