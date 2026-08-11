"""Shared preprocessing helpers: Moran's I, hex-grid coordinates from ST spot IDs."""
from __future__ import annotations

import numpy as np
from scipy.spatial import cKDTree


def moran_weights(coords: np.ndarray, k: int = 7) -> np.ndarray:
    """Row-normalized inverse-distance weight matrix (precomputed once per slide)."""
    n = len(coords)
    if n < 3:
        return np.zeros((n, n))
    tree = cKDTree(coords)
    d, idx = tree.query(coords, k=min(k, n))
    W = np.zeros((n, n))
    for i in range(n):
        for jj in range(1, len(d[i])):
            W[i, idx[i, jj]] = 1.0 / (d[i, jj] + 1e-6)
    W = (W + W.T) / 2
    S0 = W.sum()
    if S0 == 0:
        return np.zeros((n, n))
    return W / S0 * n


def moran_vectorized(Z: np.ndarray, W: np.ndarray) -> np.ndarray:
    """Moran's I per column of Z (n_spots x n_genes) with precomputed W."""
    n = Z.shape[0]
    if n < 3:
        return np.full(Z.shape[1], np.nan)
    Zc = Z - Z.mean(axis=0)
    denom = (Zc ** 2).sum(axis=0)
    num = Zc * (W @ Zc)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(denom > 1e-12, num.sum(axis=0) / np.maximum(denom, 1e-12), np.nan)


def per_slide_moran(hv_matrix: np.ndarray, slides: np.ndarray, coords: np.ndarray) -> np.ndarray:
    """Per-gene Moran's I averaged over slides (inverse-distance, k=7 NN)."""
    gene_scores = np.zeros(hv_matrix.shape[1])
    counts = np.zeros(hv_matrix.shape[1])
    for slide in np.unique(slides):
        m = slides == slide
        if m.sum() < 3:
            continue
        W = moran_weights(coords[m])
        mi = moran_vectorized(hv_matrix[m], W)
        ok = ~np.isnan(mi)
        gene_scores[ok] += mi[ok]
        counts[ok] += 1
    return np.where(counts > 0, gene_scores / np.maximum(counts, 1), np.nan)


def hex_coords_from_spot_ids(spot_ids) -> np.ndarray:
    """ST v1.0 'RxC' spot IDs -> hex-grid 2D coordinates (row y-axis, col x-axis).

    x = col + 0.5*(row mod 2); y = row * sqrt(3)/2. Consistent metric space.
    """
    out = np.zeros((len(spot_ids), 2))
    for i, sid in enumerate(spot_ids):
        parts = str(sid).split("x")
        if len(parts) == 2:
            r, c = int(parts[0]), int(parts[1])
            out[i] = [c + 0.5 * (r % 2), r * np.sqrt(3) / 2]
        else:
            out[i] = [np.nan, np.nan]
    return out
