"""Spatial kNN baseline: predict test spot from its k nearest TRAIN spots.

This baseline is the key leakage probe: under random splits it can exploit
spatial autocorrelation; under spatial-block / patient-held-out splits it must
collapse if the reported gains were driven by neighbor information sharing.
"""
from __future__ import annotations

import numpy as np
from scipy.spatial import cKDTree


def predict_spatial_knn(
    train_coords: np.ndarray,
    train_Y: np.ndarray,
    test_coords: np.ndarray,
    k: int = 15,
    inverse_distance: bool = True,
    eps: float = 1e-6,
) -> np.ndarray:
    """train_coords/test_coords: (n, 2) coordinates (per-slide scaled).

    Prediction = (inverse-)distance weighted mean of neighbors' target genes.
    """
    tree = cKDTree(train_coords)
    dist, idx = tree.query(test_coords, k=min(k, len(train_coords)))
    if k == 1 or len(train_coords) == 1:
        dist = dist.reshape(-1, 1)
        idx = idx.reshape(-1, 1)
    w = 1.0 / (dist + eps) if inverse_distance else np.ones_like(dist)
    w = w / w.sum(axis=1, keepdims=True)
    pred = np.zeros((len(test_coords), train_Y.shape[1]))
    for i in range(len(test_coords)):
        pred[i] = w[i] @ train_Y[idx[i]]
    return pred
