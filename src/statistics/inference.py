"""Formal statistics (Phase 12 / Priority 4):
- slide/patient-level bootstrap (n=1000)
- paired Wilcoxon signed-rank + BH-FDR
- Spearman / Kendall model-rank correlation
- mixed-effects: Inflation ~ MoranI + Model + (1|Dataset)
No spot-level inferential statistics anywhere.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr, wilcoxon


def slide_bootstrap(slide_metrics: pd.DataFrame, n_boot: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Bootstrap over slides; resampling unit = slide, never spot."""
    rng = np.random.default_rng(seed)
    d = slide_metrics[["split", "model", "seed", "slide", "pearson"]].dropna(subset=["pearson"])
    stats = d.groupby(["split", "model", "seed", "slide"])["pearson"].mean().reset_index()
    rows = []
    for (split, model, seed), g in stats.groupby(["split", "model", "seed"]):
        if g["pearson"].isna().any() or len(g) == 0:
            continue
        means = np.empty(n_boot)
        for b in range(n_boot):
            ids = rng.choice(np.arange(len(g)), size=len(g), replace=True)
            means[b] = g.iloc[ids]["pearson"].mean()
        rows.append({
            "split": split, "model": model, "seed": seed,
            "n_slides": len(g), "mean": g["pearson"].mean(),
            "ci_low": np.percentile(means, 2.5), "ci_high": np.percentile(means, 97.5),
        })
    return pd.DataFrame(rows)


def paired_wilcoxon_bhfdr(df: pd.DataFrame, strict_split: str) -> pd.DataFrame:
    """Paired (per-seed) Wilcoxon random vs strict, per model; BH-FDR across models.

    df: formal_aggregate with columns split, model, seed, mean_pearson.
    """
    rand = df[df["split"] == "random"].set_index(["model", "seed"])["mean_pearson"]
    strict = df[df["split"] == strict_split].set_index(["model", "seed"])["mean_pearson"]
    rows = []
    for model in sorted(set(rand.index.get_level_values(0)) & set(strict.index.get_level_values(0))):
        a = rand.loc[model]
        b = strict.loc[model]
        common = a.index.intersection(b.index)
        if len(common) < 3:
            continue
        x, y = a.loc[common].values, b.loc[common].values
        if np.std(x - y) == 0:
            stat, p = 0.0, 1.0
        else:
            try:
                stat, p = wilcoxon(x, y, zero_method="wilcox")
            except ValueError:
                stat, p = 0.0, 1.0
        rows.append({"model": model, "n_pairs": len(common),
                     "median_diff": float(np.median(x - y)), "statistic": stat, "p": p})
    out = pd.DataFrame(rows)
    if len(out):
        p = out["p"].values
        m = len(p)
        order = np.argsort(p)
        q = p[order] * m / np.arange(1, m + 1)
        q = np.minimum.accumulate(q[::-1])[::-1]
        out["p_bh"] = q[np.argsort(order)]
        out["sig_bh_0.05"] = out["p_bh"] < 0.05
    return out


def model_rank_correlation(perf: pd.DataFrame, col: str = "mean_pearson") -> dict:
    """Spearman + Kendall between model ranks under different splits.

    perf: long-form with columns split, model, value.
    """
    piv = perf.pivot(index="model", columns="split", values=col)
    res = {}
    splits = list(piv.columns)
    for i in range(len(splits)):
        for j in range(i + 1, len(splits)):
            a, b = piv[splits[i]].dropna(), piv[splits[j]].dropna()
            common = a.index.intersection(b.index)
            if len(common) < 2:
                continue
            r = spearmanr(a.loc[common], b.loc[common])
            tau = kendalltau(a.loc[common], b.loc[common])
            res[f"{splits[i]}_vs_{splits[j]}"] = {
                "spearman": r.statistic, "p_spearman": r.pvalue,
                "kendall": tau.statistic, "p_kendall": tau.pvalue,
                "n_models": len(common),
            }
    return res


def mixed_effects_inflation(
    per_gene_inflation: pd.DataFrame,
    dataset_col: str = "dataset",
    interaction: bool = False,
) -> dict:
    """Inflation ~ MoranI + Model + (1|Dataset), optionally + MoranI:Model.

    per_gene_inflation columns: dataset, gene, model, moran_i, inflation.
    """
    from statsmodels.formula.api import mixedlm

    d = per_gene_inflation.dropna(subset=["inflation", "moran_i"]).copy()
    formula = f"inflation ~ moran_i + C(model)"
    if interaction:
        formula += " + moran_i:C(model)"
    m = mixedlm(formula, d, groups=d[dataset_col])
    try:
        fit = m.fit(reml=True, method="lbfgs", maxiter=2000)
        params = fit.params
        res = {
            "formula": formula,
            "n_obs": int(fit.nobs),
            "n_datasets": int(d[dataset_col].nunique()),
            "coef_moran_i": float(params.get("moran_i", np.nan)),
            "p_moran_i": float(fit.pvalues.get("moran_i", np.nan)),
            "coefs": {k: float(v) for k, v in params.items()},
            "pvalues": {k: float(v) for k, v in fit.pvalues.items()},
        }
        return res
    except Exception as e:  # noqa: BLE001 - report fit failure transparently
        return {"error": str(e), "formula": formula, "n_obs": int(d.shape[0])}
