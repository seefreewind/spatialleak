import numpy as np
import pytest
from scipy.stats import pearsonr

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.metrics.metrics import aggregate_metrics, per_gene_metrics
from src.models.spatial_knn import predict_spatial_knn


def test_per_gene_metrics_matches_scipy():
    rng = np.random.default_rng(0)
    t = rng.normal(size=100)
    p = 0.8 * t + 0.2 * rng.normal(size=100)
    df = per_gene_metrics(t[:, None], p[:, None], ["g1"])
    ref = pearsonr(t, p).statistic
    assert df.loc[0, "pearson"] == pytest.approx(ref, abs=1e-9)
    assert df.loc[0, "rmse"] > 0


def test_aggregate_metrics():
    rng = np.random.default_rng(1)
    t = rng.normal(size=50)
    df = per_gene_metrics(np.c_[t, 2 * t], np.c_[t + 0.01, 2 * t - 0.01], ["a", "b"])
    agg = aggregate_metrics(df)
    assert agg["mean_pearson"] == pytest.approx(1.0, abs=1e-3)
    assert agg["n_genes"] == 2


def test_spatial_knn_recovers_local_mean():
    # points in two spatial clusters with different expression
    coords = np.vstack([np.random.default_rng(0).normal(0, 0.1, (50, 2)),
                        np.random.default_rng(1).normal(5, 0.1, (50, 2))])
    Y = np.concatenate([np.ones(50), np.zeros(50)])[:, None]
    test_coords = np.array([[0.05, 0.0], [4.95, 5.0]])
    pred = predict_spatial_knn(coords, Y, test_coords, k=10)
    assert pred[0, 0] == pytest.approx(1.0, abs=0.05)
    assert pred[1, 0] == pytest.approx(0.0, abs=0.05)
