"""Split 4b: layer-stratified random spot split (negative control).

Same 80/10/10 proportions as naive random split, but stratified by the
`layer` column (DLPFC laminar annotations). Tests whether part of the random-
split inflation is explainable by simple cell-type/layer imbalance between
train and test, independent of spatial autocorrelation.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Split


def stratified_spot_split(
    obs: pd.DataFrame,
    stratify_col: str,
    seed: int = 0,
    train_frac: float = 0.8,
    val_frac: float = 0.1,
    name: str = "stratified_spot",
) -> Split:
    rng = np.random.default_rng(seed)
    train, val, test = [], [], []
    for _, g in obs.groupby(stratify_col, sort=False):
        idx = g.index.to_numpy()
        rng.shuffle(idx)
        n_train = int(round(len(idx) * train_frac))
        n_val = int(round(len(idx) * val_frac))
        train.extend(idx[:n_train].tolist())
        val.extend(idx[n_train : n_train + n_val].tolist())
        test.extend(idx[n_train + n_val :].tolist())
    split = Split(
        name=name,
        method=f"stratified_{stratify_col}",
        params={"train_frac": train_frac, "val_frac": val_frac, "stratify_col": stratify_col},
        seed=seed,
        train_idx=train,
        val_idx=val,
        test_idx=test,
    )
    split.check_valid(len(obs))
    return split
