"""Splits 3-4: slide-held-out and patient-held-out via group assignment.

`group_held_out_split` assigns whole groups (slides or patients) to
train/val/test; used directly for slide-held-out, and per donor for
patient-held-out (see scripts/pilot_benchmark.py).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .base import Split


def group_held_out_split(
    obs: pd.DataFrame,
    group_col: str,
    seed: int = 0,
    test_groups: list | None = None,
    val_groups: list | None = None,
    n_test_groups: int = 1,
    name: str = "group_held_out",
) -> Split:
    """Hold out whole groups (e.g. 'slide' or 'patient').

    Either pass explicit test_groups/val_groups, or let the function draw
    `n_test_groups` random groups as test and one as validation.
    """
    obs = obs.reset_index(drop=True)
    n = len(obs)
    groups = sorted(obs[group_col].unique())
    rng = np.random.default_rng(seed)

    if test_groups is None:
        test_groups = rng.choice(groups, size=n_test_groups, replace=False).tolist()
    if val_groups is None:
        remaining = [g for g in groups if g not in set(test_groups)]
        val_groups = [rng.choice(remaining)] if remaining else []

    in_train = ~obs[group_col].isin(set(test_groups) | set(val_groups))
    in_val = obs[group_col].isin(val_groups)
    in_test = obs[group_col].isin(test_groups)

    split = Split(
        name=name,
        method=f"group_held_out_{group_col}",
        params={"test_groups": sorted(test_groups), "val_groups": sorted(val_groups)},
        seed=seed,
        train_idx=np.where(in_train.values)[0].tolist(),
        val_idx=np.where(in_val.values)[0].tolist(),
        test_idx=np.where(in_test.values)[0].tolist(),
    )
    split.check_valid(n)
    return split
