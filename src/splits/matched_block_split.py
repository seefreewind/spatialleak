"""Matched spatial block split with kNN-hop / normalized-coordinate buffers.

Design (Phase 7A, ANALYSIS_LOCK appendix):
1. Per-slide grid blocks (3x3 quantile-based by default).
2. Per seed: draw `n_candidates` random block->fold assignments; score each by
   train/test composition distance (n spots, layer fractions, library size,
   top-Moran-gene signal); keep the BEST assignment (deterministic per seed).
   This removes assignment luck as a variance source while retaining
   per-seed variation.
3. Buffer: drop TEST spots whose separation to the nearest TRAIN spot is below
   threshold, in one of two metrics:
   - kNN graph hop distance (within-slide kNN graph, k=knn_k)
   - normalized coordinate distance (per-slide z-scored array coords)
   Dropped spots are recorded (never silently discarded).
"""
from __future__ import annotations

from collections import deque

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from .base import Split


def _grid_blocks(obs: pd.DataFrame, n_per_slide: int) -> pd.Series:
    ids = {}
    for slide, g in obs.groupby("slide", sort=False):
        n = int(round(n_per_slide ** 0.5))
        row_edges = np.quantile(g["array_row"].values, np.linspace(0, 1, n + 1))
        col_edges = np.quantile(g["array_col"].values, np.linspace(0, 1, n + 1))
        rb = np.clip(np.digitize(g["array_row"].values, row_edges[1:-1]), 0, n - 1)
        cb = np.clip(np.digitize(g["array_col"].values, col_edges[1:-1]), 0, n - 1)
        ids[slide] = rb * n + cb
    return pd.concat({s: pd.Series(v) for s, v in ids.items()}).sort_index()


def _match_score(obs: pd.DataFrame, train_idx, test_idx, layer_cols) -> float:
    """L1 distance between test and train composition, each feature
    standardized by its global SD across spots."""
    feats = []
    for idx_set in (train_idx, test_idx):
        sub = obs.iloc[idx_set]
        f = []
        f.append(np.log(max(len(sub), 1)))                                  # n spots
        f.append(sub["total_counts"].mean())                                # library size
        f.append(sub["moran_signal"].mean())                                # Moran structure proxy
        for c in layer_cols:
            f.append(sub[c].mean())                                         # layer fractions
        feats.append(np.array(f, dtype=float))
    diff = feats[0] - feats[1]
    scale = np.zeros_like(diff)
    for j, name in enumerate(["n_spots", "total_counts", "moran_signal"] + layer_cols):
        scale[j] = obs[name].std() if name != "n_spots" else np.log(max(len(obs), 2)) * 0.5
    scale = np.maximum(scale, 1e-9)
    return float(np.abs(diff / scale).sum())


def _hop_distances_to_train(obs: pd.DataFrame, train_idx, k: int) -> np.ndarray:
    """Per-spot shortest-path hop distance to the train set (within slide)."""
    n = len(obs)
    dist = np.full(n, np.inf)
    adj = [[] for _ in range(n)]
    for slide in obs["slide"].unique():
        m = np.where(obs["slide"].values == slide)[0]
        tree = cKDTree(obs.iloc[m][["array_row", "array_col"]].values.astype(float))
        d, idx = tree.query(obs.iloc[m][["array_row", "array_col"]].values.astype(float),
                            k=min(k + 1, len(m)))
        for i in range(len(m)):
            for j in idx[i][1:]:
                adj[m[i]].append(m[j])
    dq = deque(train_idx)
    for i in train_idx:
        dist[i] = 0
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist


def _coord_distances_to_train(obs: pd.DataFrame, train_idx, coords_z) -> np.ndarray:
    """Per-spot nearest-train distance in normalized (z-scored) coordinates."""
    n = len(obs)
    dist = np.full(n, np.inf)
    for slide in obs["slide"].unique():
        m = np.where(obs["slide"].values == slide)[0]
        tr = np.intersect1d(m, train_idx, assume_unique=True)
        if len(tr) == 0:
            continue
        tree = cKDTree(coords_z[tr])
        d, _ = tree.query(coords_z[m], k=1)
        dist[m] = d
    return dist


def matched_block_split(
    obs: pd.DataFrame,
    seed: int = 0,
    n_blocks_per_slide: int = 9,
    test_block_frac: float = 0.2,
    val_block_frac: float = 0.1,
    n_candidates: int = 300,
    buffer_kind: str = "hop",        # "hop" | "coord" | "none"
    buffer_value: float = 0.0,
    knn_k: int = 15,
    layer_cols: list | None = None,
    name: str = "matched_block",
) -> Split:
    obs = obs.reset_index(drop=True)
    n = len(obs)
    if layer_cols is None:
        layer_cols = [c for c in obs.columns if c.startswith("layer_")]

    block = _grid_blocks(obs, n_blocks_per_slide)
    block_ids = np.unique(block.values)
    n_test_blocks = max(1, int(round(len(block_ids) * test_block_frac)))
    n_val_blocks = max(1, int(round(len(block_ids) * val_block_frac)))

    rng = np.random.default_rng(seed)
    best = None
    for _ in range(n_candidates):
        perm = rng.permutation(block_ids)
        test_blocks = set(perm[:n_test_blocks])
        val_blocks = set(perm[n_test_blocks : n_test_blocks + n_val_blocks])
        tr = np.where(~block.isin(test_blocks | val_blocks))[0]
        te = np.where(block.isin(test_blocks))[0]
        score = _match_score(obs, tr, te, layer_cols)
        if best is None or score < best[0]:
            best = (score, test_blocks, val_blocks)

    score, test_blocks, val_blocks = best
    train_idx = np.where(~block.isin(test_blocks | val_blocks))[0].tolist()
    val_idx = np.where(block.isin(val_blocks))[0].tolist()
    test_idx = np.where(block.isin(test_blocks))[0].tolist()

    dropped = []
    if buffer_kind != "none" and buffer_value > 0:
        if buffer_kind == "hop":
            dist = _hop_distances_to_train(obs, train_idx, k=knn_k)
        elif buffer_kind == "coord":
            coords = obs[["array_row", "array_col"]].values.astype(float)
            coords_z = np.zeros_like(coords)
            for slide in obs["slide"].unique():
                m = (obs["slide"].values == slide)
                coords_z[m] = (coords[m] - coords[m].mean(0)) / (coords[m].std(0) + 1e-6)
            dist = _coord_distances_to_train(obs, train_idx, coords_z)
        else:
            raise ValueError(buffer_kind)
        keep, dropped = [], []
        for i in test_idx:
            (keep if dist[i] >= buffer_value else dropped).append(i)
        test_idx = sorted(keep)

    split = Split(
        name=name,
        method=f"matched_block_{buffer_kind}{buffer_value}",
        params={
            "n_blocks_per_slide": n_blocks_per_slide,
            "test_block_frac": test_block_frac,
            "val_block_frac": val_block_frac,
            "n_candidates": n_candidates,
            "buffer_kind": buffer_kind,
            "buffer_value": buffer_value,
            "knn_k": knn_k,
            "match_score": round(score, 4),
        },
        seed=seed,
        train_idx=train_idx,
        val_idx=val_idx,
        test_idx=test_idx,
        dropped_idx=dropped,
    )
    split.check_valid(n)
    return split
