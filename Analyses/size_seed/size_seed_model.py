#!/usr/bin/env python3
"""
Seed production from plant size: predictor selection + populations below expectation
====================================================================================

Goal (Sven): treat plant size as a predictor of seed production, choose the best
size metric *honestly* (out-of-sample), build the species-wide "expectation", then
**detect the populations whose seed production falls below what their plants' sizes
predict** — the candidate reproductive-shortfall populations.

Pipeline
  STAGE 1  Predictor selection — 10-fold cross-validated RMSE (log10 seed yield) among
           candidate allometric models:
             height      :  log(yield) ~ log(height)
             crown       :  log(yield) ~ log(crown)
             area        :  log(yield) ~ log( (pi/4)*crown*height )      (ellipse, equal exponents)
             crown+height:  log(yield) ~ log(crown) + log(height)        (free exponents)
           Best = lowest mean CV-RMSE (out-of-sample), with in-sample R2 and AIC reported.
  STAGE 2  Expectation model — refit the winner on all plants. Fitted value = expected
           log10(yield) for a plant of that size. Residual = observed - expected.
  STAGE 3  Below-expectation detection, per BL / EO / location:
             - mean residual (= log10 fold-deviation from expectation) + 95% CI
             - one-sample t-test vs 0, Benjamini-Hochberg FDR across populations
             - mixed-model (random intercept by EO) shrinkage estimate of each offset
             - slope heterogeneity test: does the size->yield slope differ by BL? (ANCOVA F)
           A population is FLAGGED "below expectation" if its FDR-significant mean
           residual is < 0 (yields less than its plant sizes predict).
  STAGE 4  Outputs — console report, Queries/size_seed_model_strata.tsv, and figures
           (calibration scatter + per-EO and per-BL forest plots of fold-of-expectation).

Conventions (shared with the SRK / spatial-clustering projects): Bottleneck Lineage
(BL) is the inferential unit and is shown first; BL order = BL4,BL5,BL3,BL1,BL2
(habitat area then connectivity); RColorBrewer Set1 BL palette. EO = management unit.
Seed viability runs >98% in the field, so seedQuantityEstimate ~ viable seed; this
script measures the *quantity* axis (mate/SI-limitation signal), not viability.

Caveats: size = 2025 vision estimates (+/-2-8 cm); yield = weight-derived estimate;
observational (controlled crosses are the confirmatory arm); n per population is small
(BL-level inference is strongest). Not a proof of SI status by itself.

Usage:  python3 Queries/size_seed_model.py [--db PATH] [--bl-key PATH] [--folds 10] [--seed 1] [--no-plot]
"""
import argparse
import csv
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy import stats
from sklearn.model_selection import KFold
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
BL_COLORS = {"BL1": "#E41A1C", "BL2": "#377EB8", "BL3": "#4DAF4A",
             "BL4": "#984EA3", "BL5": "#FF7F00", "Unassigned": "#999999"}
CANDIDATES = {
    "height": "logy ~ logh",
    "crown": "logy ~ logc",
    "area": "logy ~ logarea",
    "crown+height": "logy ~ logc + logh",
}


def load_bl_key(path):
    loc = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            for lid in str(r["Population_IDs"]).replace('"', "").split(","):
                lid = lid.strip()
                if lid.isdigit():
                    loc[int(lid)] = {"BL": r["BL"], "Group": int(r["Group"]), "EO": r["EO"]}
    return loc


def load_df(db, blkey, year="all"):
    con = sqlite3.connect(db)
    rows = con.execute(
        """SELECT v.occurrenceID, v.occurrenceHeight h, v.occurrenceCrownSize c, v.seedQuantityTotal y,
                  o.EOID, e.EOCode, o.locationID, l.locationCode
           FROM vOccurrenceTraits v
           JOIN Occurrences o ON v.occurrenceID=o.occurrenceID
           LEFT JOIN EOs e ON o.EOID=e.EOID
           LEFT JOIN Locations l ON o.locationID=l.locationID
           WHERE v.occurrenceHeight>0 AND v.occurrenceCrownSize>0 AND v.seedQuantityTotal>0""" + year_sql(year)[0], year_sql(year)[1]
    ).fetchall()
    con.close()
    df = pd.DataFrame(rows, columns=["occ", "h", "c", "y", "EOID", "EO", "locID", "locCode"])
    df["area"] = np.pi / 4.0 * df.c * df.h
    df["logh"], df["logc"], df["logarea"], df["logy"] = np.log10(df.h), np.log10(df.c), np.log10(df.area), np.log10(df.y)
    df["BL"] = df.locID.map(lambda L: blkey.get(L, {}).get("BL", "Unassigned"))
    df["Group"] = df.locID.map(lambda L: blkey.get(L, {}).get("Group", -1))
    df["EO"] = df.EO.fillna("EOID?" )
    df["locCode"] = df.locCode.fillna(df.locID.astype(str))
    return df


def cv_rmse(df, formula, folds, seed):
    kf = KFold(n_splits=folds, shuffle=True, random_state=seed)
    err = []
    for tr, te in kf.split(df):
        m = smf.ols(formula, df.iloc[tr]).fit()
        pred = m.predict(df.iloc[te])
        err.append(np.sqrt(np.mean((df.iloc[te].logy.values - pred.values) ** 2)))
    return np.mean(err), np.std(err)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--bl-key", default=str(DEFAULT_BLKEY))
    ap.add_argument("--folds", type=int, default=10)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--no-plot", action="store_true")
    ap.add_argument("--year", default="all", help="2025, 2026 or all (default)")
    args = ap.parse_args()

    YEAR = args.year
    df = load_df(args.db, load_bl_key(args.bl_key), YEAR)
    print(f"n = {len(df)} plants (height, crown, seed yield); nAccessions==1 so yield = one accession/plant\n")

    # --- sampling overview (n per BL / EO) to gauge reliability per stratum ---
    print("SAMPLING (n plants with crown+yield) — BL is the inferential unit:")
    for bl in BL_ORDER:
        g = df[df.BL == bl]
        if len(g):
            eos = ", ".join(f"{e}({(g.EO == e).sum()})" for e in sorted(g.EO.unique()))
            print(f"  {bl}: {len(g):4d} plants / {g.EO.nunique()} EOs / {g.locID.nunique()} locations   {eos}")
    print()

    # ---------- STAGE 1: predictor selection ----------
    print("STAGE 1 — predictor selection (10-fold CV; lower RMSE = better out-of-sample)")
    rowsel = []
    for name, f in CANDIDATES.items():
        m = smf.ols(f, df).fit()
        rmse, sd = cv_rmse(df, f, args.folds, args.seed)
        rowsel.append((name, rmse, sd, m.rsquared, m.aic))
    rowsel.sort(key=lambda r: r[1])
    print(f"  {'predictor':<13}{'CV-RMSE':>9}{'±sd':>7}{'R2(in)':>8}{'AIC':>9}")
    for name, rmse, sd, r2, aic in rowsel:
        print(f"  {name:<13}{rmse:>9.3f}{sd:>7.3f}{r2:>8.3f}{aic:>9.1f}")
    best = rowsel[0][0]; best_f = CANDIDATES[best]
    print(f"  -> selected predictor: {best}")

    # ---------- STAGE 2: expectation model ----------
    gm = smf.ols(best_f, df).fit()
    df["expected"] = gm.fittedvalues          # expected log10(yield) from size
    df["resid"] = df.logy - df.expected        # >0 over-, <0 under-performing
    print(f"\nSTAGE 2 — global expectation model  ({best})")
    print(f"  {gm.params.to_dict()}")
    print(f"  R2={gm.rsquared:.3f}, residual SD={np.sqrt(gm.scale):.3f} log10-units (=> x/÷{10**np.sqrt(gm.scale):.1f})")

    # ---------- STAGE 3: below-expectation detection ----------
    def offsets(level):
        out = []
        for k, g in df.groupby(level):
            if len(g) < (1 if level == "BL" else (15 if level == "EO" else 10)):
                continue
            r = g.resid.values
            t, p = stats.ttest_1samp(r, 0.0)
            ci = stats.t.ppf(0.975, len(r) - 1) * r.std(ddof=1) / np.sqrt(len(r))
            # within-stratum slope of observed on expected (1=follows global scaling, 0=flat)
            sl = smf.ols("logy ~ expected", g).fit().params["expected"] if len(g) >= 5 else np.nan
            bl = g.BL.iloc[0]
            out.append(dict(level=level, stratum=str(k), BL=bl, n=len(r),
                            mean_resid=r.mean(), ci=ci, t=t, p=p, slope=sl))
        # FDR across strata within this level
        if out:
            q = fdrcorrection([o["p"] for o in out])[1]
            for o, qq in zip(out, q):
                o["q"] = qq
        return out

    all_off = {lvl: offsets(lvl) for lvl in ["BL", "EO", "locCode"]}

    def show(level, title):
        rows = all_off[level]
        if level == "BL":
            rows = sorted(rows, key=lambda o: BL_ORDER.index(o["BL"]) if o["BL"] in BL_ORDER else 9)
        else:
            rows = sorted(rows, key=lambda o: (BL_ORDER.index(o["BL"]) if o["BL"] in BL_ORDER else 9, o["mean_resid"]))
        print(f"\n  {title}")
        print(f"  {'stratum':<10}{'BL':>4}{'n':>5}{'fold-of-exp':>12}{'95% CI':>16}{'q(FDR)':>9}{'slope':>7}  flag")
        for o in rows:
            fold = 10 ** o["mean_resid"]; lo = 10 ** (o["mean_resid"] - o["ci"]); hi = 10 ** (o["mean_resid"] + o["ci"])
            flag = "BELOW expectation" if (o.get("q", 1) < 0.05 and o["mean_resid"] < 0) else \
                   ("above" if (o.get("q", 1) < 0.05 and o["mean_resid"] > 0) else "")
            print(f"  {o['stratum']:<10}{o['BL']:>4}{o['n']:>5}{fold:>12.2f}{f'{lo:.2f}-{hi:.2f}':>16}{o.get('q',1):>9.1e}{o['slope']:>7.2f}  {flag}")

    print("\nSTAGE 3 — populations vs expectation (fold-of-expectation: 1.0 = on the species curve, <1 = below)")
    show("BL", "BY BOTTLENECK LINEAGE (inferential unit)")
    show("EO", "BY ELEMENT OCCURRENCE (management unit)")
    show("locCode", "BY LOCATION (finest)")

    # mixed-model shrinkage offsets by EO + slope heterogeneity across BL
    try:
        mm = smf.mixedlm("logy ~ expected", df, groups=df.EO).fit(method="lbfgs")
        re = {k: v.values[0] for k, v in mm.random_effects.items()}
        print("\n  mixed-model (random intercept by EO) shrunken offsets, fold-of-expectation:")
        for eo in sorted(re, key=lambda e: re[e]):
            print(f"    {eo:<8} {10**re[eo]:.2f}")
    except Exception as e:
        print("  (mixed model skipped:", e, ")")
    inter = sm.stats.anova_lm(smf.ols("logy ~ expected + C(BL)", df).fit(),
                              smf.ols("logy ~ expected * C(BL)", df).fit())
    print(f"\n  slope heterogeneity across BL (ANCOVA interaction): F={inter['F'][1]:.2f}, p={inter['Pr(>F)'][1]:.2e}")

    # ---------- STAGE 4: outputs ----------
    flat = [o for lvl in all_off.values() for o in lvl]
    pd.DataFrame(flat).to_csv(Path(__file__).resolve().parent / f"size_seed_model_strata{suffix(YEAR)}.tsv", sep="\t", index=False)
    print(f"\nstrata table -> Queries/size_seed_model_strata{suffix(YEAR)}.tsv")
    flagged = [o for o in all_off["EO"] if o.get("q", 1) < 0.05 and o["mean_resid"] < 0]
    print("FLAGGED EOs below expectation:", [o["stratum"] for o in flagged] or "none at FDR<0.05")

    if not args.no_plot:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 3, figsize=(17, 5))
        # (a) calibration: expected vs observed, colored by BL, 1:1 = expectation
        for bl in BL_ORDER + ["Unassigned"]:
            g = df[df.BL == bl]
            if len(g): ax[0].scatter(10 ** g.expected, g.y, s=14, alpha=0.5, color=BL_COLORS[bl], label=f"{bl} (n={len(g)})")
        lim = [df.y.min(), df.y.max()]
        ax[0].plot(lim, lim, "k--", lw=1.5, label="expectation (1:1)")
        ax[0].set_xscale("log"); ax[0].set_yscale("log")
        ax[0].set(xlabel="expected seed yield (from size)", ylabel="observed seed yield",
                  title=f"Calibration — points below the line under-produce\nmodel: {best}, R²={gm.rsquared:.2f}")
        ax[0].legend(fontsize=8)
        # (b) per-EO forest (fold-of-expectation), ordered by BL then value
        def forest(axx, rows, title):
            rows = sorted(rows, key=lambda o: (BL_ORDER.index(o["BL"]) if o["BL"] in BL_ORDER else 9, o["mean_resid"]))
            yps = np.arange(len(rows))
            for i, o in enumerate(rows):
                lo, hi = 10 ** (o["mean_resid"] - o["ci"]), 10 ** (o["mean_resid"] + o["ci"])
                axx.plot([lo, hi], [i, i], color=BL_COLORS[o["BL"]], lw=2)
                axx.plot(10 ** o["mean_resid"], i, "o", color=BL_COLORS[o["BL"]], ms=5)
            axx.axvline(1.0, color="k", ls="--", lw=1)
            axx.set_yticks(yps); axx.set_yticklabels([f"{o['stratum']} ({o['BL']})" for o in rows], fontsize=7)
            axx.set_xscale("log"); axx.set(xlabel="seed yield ÷ expected (fold)", title=title)
        forest(ax[1], all_off["EO"], "Per-EO: fold of expectation (95% CI)\nCI entirely left of 1 = below expectation")
        forest(ax[2], all_off["BL"], "Per-BL: fold of expectation")
        fig.suptitle(f"Lepidium papilliferum — seed production vs size expectation, by lineage/population ({YEAR})", y=1.02)
        fig.tight_layout()
        out = Path(__file__).resolve().parent / f"size_seed_model{suffix(YEAR)}.png"
        fig.savefig(out, dpi=130, bbox_inches="tight")
        print(f"figure -> {out}")


if __name__ == "__main__":
    main()
