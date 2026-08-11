#!/usr/bin/env python3
"""Pilot analysis: summary tables, LI/RLI, ranking stability, slide-level
bootstrap CIs, and Moran's-I vs leakage-inflation (per-gene) correlation.

Reads results/pilot/*.csv, writes results/pilot/analysis/*.
Usage: python scripts/analyze_pilot.py --config configs/experiments/pilot_dlpfc.yaml
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.statistics.bootstrap import slide_bootstrap

RANDOM_SPLIT = "random"
STRICT_SPLITS = ["block_buf0", "block_buf2", "patient_holdout"]


def mean_by_split_model(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(["split", "model"])[["mean_pearson", "mean_spearman", "mean_rmse"]].mean()
    g["se"] = df.groupby(["split", "model"])["mean_pearson"].std() / np.sqrt(
        df.groupby(["split", "model"]).size())
    return g.reset_index()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/experiments/pilot_dlpfc.yaml")
    ap.add_argument("--n_boot", type=int, default=200)
    ap.add_argument("--suffix", default="", help="filename suffix (e.g. _distance)")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    res = Path(cfg["out_dir"])
    out = res / "analysis"
    out.mkdir(exist_ok=True)
    t0 = time.time()
    suf = f"_{args.suffix}" if args.suffix else ""

    agg = pd.read_csv(res / f"pilot_aggregate{suf}.csv")
    slide_metrics = pd.read_csv(res / f"pilot_per_gene_per_slide{suf}.csv")
    moran = pd.read_csv(Path(cfg["moran_csv"]))
    per_gene = pd.read_csv(res / f"pilot_per_gene{suf}.csv")

    # ---- 1. summary: mean across seeds ----
    summary = mean_by_split_model(agg)
    summary.to_csv(out / f"summary_mean_pearson{suf}.csv", index=False)
    print("== Mean Pearson (across seeds) by split x model ==")
    print(summary.pivot(index="split", columns="model", values="mean_pearson").round(3))

    # ---- 2. LI / RLI ----
    base = summary[summary["split"] == RANDOM_SPLIT][["model", "mean_pearson"]]
    base = base.rename(columns={"mean_pearson": "random"})
    li_rows = []
    for s in STRICT_SPLITS:
        strict = summary[summary["split"].str.startswith(s)]
        if strict.empty:
            continue
        m = strict.groupby("model")["mean_pearson"].mean().rename("strict").reset_index()
        joined = base.merge(m, on="model")
        joined["split"] = s
        joined["LI"] = joined["random"] - joined["strict"]
        joined["RLI"] = joined["LI"] / joined["random"]
        li_rows.append(joined)
    li_df = pd.concat(li_rows, ignore_index=True)
    li_df.to_csv(out / f"LI_RLI{suf}.csv", index=False)
    print("\n== Leakage Inflation (LI) and Relative LI (RLI) ==")
    print(li_df.pivot_table(index="split", columns="model", values="RLI").round(3))

    # ---- 3. ranking stability (model rank by split) ----
    # collapse patient folds: mean Pearson across the 3 donor folds, then rank
    rank = summary.copy()
    rank["split_grp"] = np.where(rank["split"].str.startswith("patient_holdout"),
                                 "patient_holdout", rank["split"])
    rank = rank.groupby(["split_grp", "model"])["mean_pearson"].mean().reset_index()
    rank["rank"] = rank.groupby("split_grp")["mean_pearson"].rank(ascending=False)
    rank_piv = rank.pivot(index="model", columns="split_grp", values="rank").round(2)
    rank_piv.to_csv(out / f"model_ranks{suf}.csv")
    print("\n== Model ranks (1=best) by split ==")
    print(rank_piv)
    from scipy.stats import spearmanr
    r_rand, r_pat = rank_piv["random"], rank_piv["patient_holdout"]
    if len(r_rand.dropna()) > 1 and len(r_pat.dropna()) > 1:
        print("Spearman(random, patient):", round(spearmanr(r_rand, r_pat).statistic, 3))

    # ---- 4. slide-level bootstrap CI on mean Pearson (per split x model) ----
    boot = slide_bootstrap(slide_metrics, n_boot=args.n_boot, seed=42)
    boot.to_csv(out / f"bootstrap_CI{suf}.csv", index=False)
    print("\n== Slide-level bootstrap 95% CI (mean Pearson over genes/slides) ==")
    print(boot.round(3))

    # ---- 5. Moran's I vs per-gene inflation (random - patient, mean over seeds) ----
    pg = per_gene.merge(moran, on="gene")
    pg["is_patient"] = pg["split"].str.startswith("patient_holdout")
    pt = pg[pg["split"] == RANDOM_SPLIT].groupby(["gene", "model"])["pearson"].mean().rename("rand").reset_index()
    pp = pg[pg["is_patient"]].groupby(["gene", "model"])["pearson"].mean().rename("pat").reset_index()
    infl = pt.merge(pp, on=["gene", "model"])
    infl["inflation"] = infl["rand"] - infl["pat"]
    infl = infl.merge(moran[["gene", "moran_i"]], on="gene")
    infl.to_csv(out / f"per_gene_inflation{suf}.csv", index=False)
    from scipy.stats import pearsonr as pr
    print("\n== Moran's I vs per-gene inflation (random - patient) ==")
    for model, g in infl.groupby("model"):
        g = g.dropna(subset=["inflation", "moran_i"])
        if len(g) < 5 or np.std(g["inflation"]) == 0:
            continue
        r = pr(g["moran_i"], g["inflation"])
        print(f"  {model}: n={len(g)}, r={r.statistic:.3f}, p={r.pvalue:.2e}")

    (out / f"analysis_meta{suf}.json").write_text(json.dumps({
        "n_boot": args.n_boot, "seed": 42, "date": time.strftime("%Y-%m-%d %H:%M"),
        "inputs": [p.name for p in (res / "pilot_aggregate.csv", res / "pilot_per_gene_per_slide.csv", res / "pilot_per_gene.csv")],
    }, indent=2))
    print(f"\nDone in {time.time()-t0:.0f}s -> {out}")


if __name__ == "__main__":
    main()
