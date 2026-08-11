"""Slide-level bootstrap for CIs (spots are NOT independent units).

Input: per-gene-per-slide metrics (each row: gene x slide x split x model x seed).
Resampling unit = slide. Output: per (split, model, seed): mean across slides
of per-slide mean Pearson, with 95% CI.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def slide_bootstrap(slide_metrics: pd.DataFrame, n_boot: int = 200, seed: int = 42) -> pd.DataFrame:
    """Bootstrap over slides, aggregating per-gene Pearson within slide first.

    slide_metrics must have columns: split, model, seed, slide, gene, pearson.
    Returns per (split, model, seed): mean, CI_low, CI_high of the mean-Pearson.
    """
    rng = np.random.default_rng(seed)
    d = slide_metrics[["split", "model", "seed", "slide", "pearson"]].dropna(subset=["pearson"])
    stats = (
        d.groupby(["split", "model", "seed", "slide"])["pearson"]
        .mean()
        .reset_index()
    )
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
            "n_slides": len(g),
            "mean": g["pearson"].mean(),
            "ci_low": np.percentile(means, 2.5),
            "ci_high": np.percentile(means, 97.5),
        })
    return pd.DataFrame(rows)
