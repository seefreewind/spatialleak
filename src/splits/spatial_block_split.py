"""Split 2: spatial block split (grid-based or clustering-based) with optional buffer.

Blocks are defined per slide; folds assigned over blocks; a buffer zone removes
test spots too close to train spots (in array units; 1 array step ~= 100 um on
10x Visium). Dropped spots are recorded, not silently discarded.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from sklearn.cluster import KMeans

from .base import Split


def _assign_blocks(obs: pd.DataFrame, method: str, n_blocks_per_slide: int, seed: int) -> pd.Series:
    """Per-slide block id (string 'SLIDE:block') for each spot."""
    ids = {}
    for slide, g in obs.groupby("slide", sort=False):
        if method == "grid":
            n = n_blocks_per_slide
            row_edges = np.quantile(g["array_row"].values, np.linspace(0, 1, n + 1))
            col_edges = np.quantile(g["array_col"].values, np.linspace(0, 1, n + 1))
            row_bin = np.clip(np.digitize(g["array_row"].values, row_edges[1:-1]), 0, n - 1)
            col_bin = np.clip(np.digitize(g["array_col"].values, col_edges[1:-1]), 0, n - 1)
            block = row_bin * n + col_bin
        elif method == "kmeans":
            km = KMeans(n_clusters=n_blocks_per_slide, n_init=10, random_state=seed)
            coords = g[["array_row", "array_col"]].values.astype(float)
            block = km.fit_predict(coords)
        else:
            raise ValueError(f"unknown block method: {method}")
        ids[slide] = block
    return pd.concat({s: pd.Series(v) for s, v in ids.items()}).sort_index()


def spatial_block_split(
    obs: pd.DataFrame,
    seed: int = 0,
    method: str = "grid",
    n_blocks_per_slide: int = 4,
    test_block_frac: float = 0.2,
    val_block_frac: float = 0.1,
    buffer: float = 0.0,
    name: str = "spatial_block",
) -> Split:
    """Block-based split with train/test separation >= `buffer` (array units).

    Blocks are randomly (seeded) assigned to train/val/test with target
    fractions; test spots within `buffer` of the nearest train spot are moved
    to `dropped_idx`.
    """
    rng = np.random.default_rng(seed)
    obs = obs.reset_index(drop=True)
    n = len(obs)
    block = _assign_blocks(obs, method, n_blocks_per_slide, seed)
    block_ids = np.unique(block.values)
    rng.shuffle(block_ids)

    n_test_blocks = max(1, int(round(len(block_ids) * test_block_frac)))
    n_val_blocks = max(1, int(round(len(block_ids) * val_block_frac)))
    test_blocks = set(block_ids[:n_test_blocks])
    val_blocks = set(block_ids[n_test_blocks : n_test_blocks + n_val_blocks])

    train_idx = np.where(~block.isin(test_blocks | val_blocks))[0].tolist()
    val_idx = np.where(block.isin(val_blocks))[0].tolist()
    test_idx = np.where(block.isin(test_blocks))[0].tolist()

    dropped = []
    if buffer > 0 and len(train_idx) > 0:
        keep = []
        for slide in obs["slide"].unique():
            s = obs["slide"].values == slide
            tr_local = np.where(s)[0][np.isin(np.where(s)[0], train_idx)]
            te_local = np.where(s)[0][np.isin(np.where(s)[0], test_idx)]
            if len(tr_local) == 0 or len(te_local) == 0:
                keep.extend(te_local)
                continue
            tr_coords = obs.loc[tr_local, ["array_row", "array_col"]].values.astype(float)
            te_coords = obs.loc[te_local, ["array_row", "array_col"]].values.astype(float)
            tree = cKDTree(tr_coords)
            dist, _ = tree.query(te_coords, k=1)
            keep_local = te_local[dist >= buffer]
            dropped_local = te_local[dist < buffer]
            keep.extend(keep_local)
            dropped.extend(dropped_local)
        test_idx = sorted(keep)

    split = Split(
        name=name,
        method=f"spatial_block_{method}",
        params={
            "n_blocks_per_slide": n_blocks_per_slide,
            "test_block_frac": test_block_frac,
            "val_block_frac": val_block_frac,
            "buffer_array_steps": buffer,
        },
        seed=seed,
        train_idx=train_idx,
        val_idx=val_idx,
        test_idx=test_idx,
        dropped_idx=dropped,
    )
    split.check_valid(n)
    return split
