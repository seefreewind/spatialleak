#!/usr/bin/env python3
"""DLPFC formal analysis (Phase 7A): summary, LI/RLI/LSS, ranks, bootstrap-1000,
paired Wilcoxon + BH-FDR, retention, GraphSAGE block-anomaly investigation.

Usage: python scripts/analyze_formal.py
Outputs: results/formal_dlpfc/analysis/*.csv + summary.json
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.statistics.inference import (
    model_rank_correlation,
    paired_wilcoxon_bhfdr,
    slide_bootstrap,
)

RES = Path("results/formal_dlpfc")
OUT = RES / "analysis"
OUT.mkdir(exist_ok=True)
RANDOM = "random"
STRICT = ["matched_hop0", "patient"]


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(["split", "model"])["mean_pearson"]
    out = g.agg(["mean", "std", "min", "max", "count"]).reset_index()
    out.columns = ["split", "model", "mean", "sd", "min", "max", "n_seeds"]
    return out


def li_rli(summary: pd.DataFrame, strict_prefixes) -> pd.DataFrame:
    base = summary[summary["split"] == RANDOM][["model", "mean"]].rename(columns={"mean": "random"})
    rows = []
    for p in strict_prefixes:
        strict = summary[summary["split"].str.startswith(p)]
        if strict.empty:
            continue
        m = strict.groupby("model")["mean"].mean().rename("strict").reset_index()
        j = base.merge(m, on="model")
        j["split"] = p
        j["LI"] = j["random"] - j["strict"]
        j["RLI"] = j["LI"] / j["random"].replace(0, np.nan)
        rows.append(j)
    return pd.concat(rows, ignore_index=True)


def main():
    t0 = time.time()
    agg = pd.read_csv(RES / "formal_aggregate.csv")
    # seed-invariant splits (patient_*, region_*) were computed once (seed == seeds[0]);
    # replicate their rows across all seeds for paired analyses (folds are identical).
    seeds_all = sorted(agg["seed"].unique())
    inv_rows = agg[agg["split"].str.startswith(("patient_", "region_"))].copy()
    if set(inv_rows["seed"]) == {seeds_all[0]} and len(seeds_all) > 1:
        inv_rows = pd.concat([inv_rows.assign(seed=s) for s in seeds_all])
        agg = pd.concat([agg[~agg["split"].str.startswith(("patient_", "region_"))], inv_rows],
                        ignore_index=True)
    slide_m = pd.read_csv(RES / "formal_per_gene_per_slide.csv")
    gene = pd.read_csv(RES / "formal_per_gene.csv")
    moran = pd.read_csv("data/processed/moran_top_genes.csv")

    # ---- 1. summary ----
    summary = summarize(agg)
    summary.to_csv(OUT / "summary.csv", index=False)
    print("== Summary (mean Pearson, 10 seeds) ==")
    print(summary.pivot(index="split", columns="model", values="mean").round(3))

    # ---- 2. LI / RLI / LSS ----
    lirli = li_rli(summary, STRICT)
    lirli.to_csv(OUT / "LI_RLI.csv", index=False)
    print("\n== LI / RLI (strict = matched_hop0, patient) ==")
    print(lirli.pivot_table(index="split", columns="model", values="RLI").round(3))
    lss = lirli.groupby("model")["RLI"].mean().rename("LSS_A").reset_index()
    tmp = lirli.copy()
    tmp["retention"] = tmp["strict"] / tmp["random"].replace(0, np.nan)
    lss["LSS_B"] = 1 - tmp.groupby("model")["retention"].min().values
    lss.to_csv(OUT / "LSS.csv", index=False)
    print("\n== LSS (A=mean RLI, B=min retention loss) ==")
    print(lss.round(3))

    # ---- 3. ranks ----
    rank = summary.copy()
    rank["grp"] = np.where(rank["split"].str.startswith("patient"), "patient",
                           rank["split"])
    rank = rank.groupby(["grp", "model"])["mean"].mean().reset_index()
    rank["rank"] = rank.groupby("grp")["mean"].rank(ascending=False)
    piv = rank.pivot(index="model", columns="grp", values="rank").round(2)
    piv.to_csv(OUT / "model_ranks.csv")
    print("\n== Model ranks (1=best) ==")
    print(piv)
    rc = model_rank_correlation(rank.rename(columns={"grp": "split", "mean": "mean_pearson"}))
    print("\n== Rank correlation ==")
    for k, v in rc.items():
        print(f"  {k}: Spearman={v['spearman']:.2f} Kendall={v['kendall']:.2f}")

    # ---- 4. bootstrap 1000 ----
    boot = slide_bootstrap(slide_m, n_boot=1000, seed=42)
    boot.to_csv(OUT / "bootstrap_1000.csv", index=False)
    print("\n== Bootstrap-1000 (slide-level, aggregated per split/model/seed) ==")
    print(boot[boot["seed"] == 0].round(3).head(10))

    # ---- 5. paired Wilcoxon + BH-FDR ----
    agg2 = agg.copy()
    agg2["grp"] = np.where(agg2["split"].str.startswith("patient_"), "patient", agg2["split"])
    agg2 = agg2.groupby(["grp", "model", "seed"], as_index=False)["mean_pearson"].mean()
    agg2 = agg2.rename(columns={"grp": "split"})
    w = paired_wilcoxon_bhfdr(agg2, "matched_hop0")
    w2 = paired_wilcoxon_bhfdr(agg2, "patient")
    w.to_csv(OUT / "wilcoxon_vs_matched_hop0.csv", index=False)
    w2.to_csv(OUT / "wilcoxon_vs_patient.csv", index=False)
    print("\n== Wilcoxon random vs matched_hop0 (per-seed paired) ==")
    print(w.round(4).to_string(index=False))
    print("\n== Wilcoxon random vs patient (per-seed paired) ==")
    print(w2.round(4).to_string(index=False))

    # ---- 6. retention (Priority 5) ----
    pat_mean = summary[summary["split"].str.startswith("patient")].groupby("model")["mean"].mean()
    rand_mean = summary[summary["split"] == RANDOM].set_index("model")["mean"]
    ret = pd.DataFrame({
        "model": pat_mean.index,
        "retention": (pat_mean / rand_mean.reindex(pat_mean.index).replace(0, np.nan)).values,
    })
    ret = ret.merge(lss, on="model")
    ret.to_csv(OUT / "retention_LSS.csv", index=False)
    print("\n== Retention (patient/random) vs LSS ==")
    print(ret.round(3))

    # ---- 7. Moran vs per-gene inflation (hybrid needs rerun; here top-50) ----
    pg = gene.merge(moran, on="gene")
    rand = pg[pg["split"] == RANDOM].groupby(["gene", "model"])["pearson"].mean().rename("rand").reset_index()
    pat = pg[pg["split"].str.startswith("patient_")].groupby(["gene", "model"])["pearson"].mean().rename("pat").reset_index()
    inf = rand.merge(pat, on=["gene", "model"])
    inf["inflation"] = inf["rand"] - inf["pat"]
    inf = inf.merge(moran[["gene", "moran_i"]], on="gene").dropna(subset=["inflation"])
    inf.to_csv(OUT / "per_gene_inflation.csv", index=False)
    from scipy.stats import pearsonr
    print("\n== Moran vs inflation (top-50 targets) ==")
    for model, g in inf.groupby("model"):
        if len(g) > 5 and np.std(g["inflation"]) > 0:
            r = pearsonr(g["moran_i"], g["inflation"])
            print(f"  {model}: r={r.statistic:.3f} p={r.pvalue:.2e}")

    # ---- 8. GraphSAGE anomaly investigation ----
    sage = pd.read_csv(RES / "formal_aggregate_graphsage.csv")
    ssum = summarize(sage)
    ssum.to_csv(OUT / "summary_graphsage.csv", index=False)
    print("\n== GraphSAGE summary ==")
    print(ssum.round(3))
    # match score vs performance (per seed, matched_hop0)
    scores = []
    for f in sorted((RES / "splits").glob("seed*.json")):
        meta = json.loads(f.read_text())
        seed = int(f.stem.split("seed")[1])
        if "matched_hop0" in meta:
            scores.append({"seed": seed,
                           "match_score": meta["matched_hop0"]["params"]["match_score"],
                           "n_dropped": meta["matched_hop0"]["n_dropped"]})
    scores_df = pd.DataFrame(scores)
    perf = sage[sage["split"] == "matched_hop0"][["seed", "mean_pearson"]]
    inv = scores_df.merge(perf, on="seed")
    inv.to_csv(OUT / "graphsage_anomaly_investigation.csv", index=False)
    print("\n== GraphSAGE matched_hop0: match_score vs performance ==")
    print(inv.round(4))
    if len(inv) > 2 and np.std(inv["match_score"]) > 0 and np.std(inv["mean_pearson"]) > 0:
        from scipy.stats import pearsonr
        r = pearsonr(inv["match_score"], inv["mean_pearson"])
        print(f"  correlation(match_score, perf): r={r.statistic:.3f} p={r.pvalue:.3f}")

    (OUT / "analysis_meta.json").write_text(json.dumps({
        "date": time.strftime("%Y-%m-%d %H:%M"), "bootstrap_n": 1000,
        "seeds": sorted(agg["seed"].unique().tolist()),
    }, indent=2))
    print(f"\nDone in {time.time()-t0:.0f}s -> {OUT}")


if __name__ == "__main__":
    main()
