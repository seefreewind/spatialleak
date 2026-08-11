"""Region holdout split: per slide, 5 contiguous bands along the dominant axis;
test = middle band, val = bands adjacent to test, train = outer bands.

Purpose: resolvable kNN-hop distance curve (hops 0-10). Unlike matched_block,
this is a fixed geometric split WITHOUT composition matching - it exists only
for the distance-curve analysis (documented in ANALYSIS_LOCK).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Split
from .matched_block_split import _hop_distances_to_train


def region_holdout_split(
    obs: pd.DataFrame,
    seed: int = 0,
    n_bands: int = 5,
    buffer_value: float = 0.0,
    knn_k: int = 15,
    adjacent_train: bool = True,
    name: str = "region_holdout",
) -> Split:
    """Per-slide contiguous bands; test = middle band.

    adjacent_train=True : train = bands adjacent to test (hop range ~1-5)
    adjacent_train=False: train = outer bands (hop range ~6-14) -> high-hop curve
    """
    obs = obs.reset_index(drop=True)
    n = len(obs)
    train_idx, val_idx, test_idx = [], [], []
    for _, g in obs.groupby("slide", sort=False):
        coords = g[["array_row", "array_col"]].values.astype(float)
        c = coords - coords.mean(0)
        _, _, vh = np.linalg.svd(c, full_matrices=False)
        proj = c @ vh[0]
        edges = np.quantile(proj, np.linspace(0, 1, n_bands + 1))
        band = np.clip(np.digitize(proj, edges[1:-1]), 0, n_bands - 1)
        gpos = g.index.to_numpy()
        mid = n_bands // 2
        test_idx.extend(gpos[band == mid].tolist())                        # middle band
        if adjacent_train:
            train_idx.extend(gpos[band == mid - 1].tolist())
            train_idx.extend(gpos[band == mid + 1].tolist())
            for b in range(n_bands):
                if b not in (mid - 1, mid, mid + 1):
                    val_idx.extend(gpos[band == b].tolist())
        else:
            for b in range(n_bands):
                if b in (0, n_bands - 1):
                    train_idx.extend(gpos[band == b].tolist())
                elif b != mid:
                    val_idx.extend(gpos[band == b].tolist())

    dropped = []
    if buffer_value > 0:
        dist = _hop_distances_to_train(obs, train_idx, k=knn_k)
        keep, dropped = [], []
        for i in test_idx:
            (keep if dist[i] >= buffer_value else dropped).append(i)
        test_idx = sorted(keep)

    split = Split(
        name=name,
        method=f"region_holdout_hop{buffer_value}",
        params={"n_bands": n_bands, "buffer_kind": "hop", "buffer_value": buffer_value,
                "knn_k": knn_k},
        seed=seed,
        train_idx=train_idx,
        val_idx=val_idx,
        test_idx=test_idx,
        dropped_idx=dropped,
    )
    split.check_valid(n)
    return split
