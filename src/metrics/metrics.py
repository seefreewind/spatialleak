"""Regression metrics: per-gene Pearson/Spearman/RMSE with aggregation."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr


def per_gene_metrics(y_true: np.ndarray, y_pred: np.ndarray, gene_names) -> pd.DataFrame:
    """y_true/y_pred: (n_spots, n_genes) on normalized scale.

    Convention (ANALYSIS_LOCK.md): constant prediction => Pearson/Spearman = 0
    (linear predictability undefined; RMSE unaffected).
    """
    rows = []
    for j, g in enumerate(gene_names):
        t, p = y_true[:, j], y_pred[:, j]
        t_sd, p_sd = np.std(t), np.std(p)
        pearson = pearsonr(t, p).statistic if t_sd > 0 and p_sd > 0 else (0.0 if p_sd == 0 else np.nan)
        spearman = spearmanr(t, p).statistic if t_sd > 0 else (0.0 if p_sd == 0 else np.nan)
        rows.append(
            {
                "gene": g,
                "pearson": pearson,
                "spearman": spearman,
                "rmse": float(np.sqrt(np.mean((t - p) ** 2))),
            }
        )
    df = pd.DataFrame(rows)
    df["gene"] = gene_names
    return df


def aggregate_metrics(df: pd.DataFrame) -> dict:
    """Aggregate over genes (mean/median/sd of per-gene Pearson)."""
    p = df["pearson"].dropna()
    s = df["spearman"].dropna()
    return {
        "mean_pearson": float(p.mean()),
        "median_pearson": float(p.median()),
        "sd_pearson": float(p.std()),
        "mean_spearman": float(s.mean()),
        "median_spearman": float(s.median()),
        "mean_rmse": float(df["rmse"].mean()),
        "n_genes": int(len(df)),
    }
