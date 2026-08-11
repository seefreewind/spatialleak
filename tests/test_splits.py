import numpy as np
import pandas as pd
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.splits.random_split import random_spot_split
from src.splits.spatial_block_split import spatial_block_split
from src.splits.group_split import group_held_out_split


def make_obs(n_slides=3, spots_per_slide=200, n_blocks=2):
    """Synthetic 10x-like grid: array_row/array_col in [0, 4*n_blocks)."""
    rows = []
    for s in range(n_slides):
        for i in range(spots_per_slide):
            rows.append({
                "barcode": f"s{s}_{i}", "slide": f"slide{s}",
                "patient": f"p{s % 2}", "array_row": i % (4 * n_blocks),
                "array_col": (i // 10) % (4 * n_blocks),
            })
    return pd.DataFrame(rows)


def test_random_split_consistency():
    obs = make_obs()
    sp = random_spot_split(obs, seed=0)
    assert len(sp.train_idx) + len(sp.val_idx) + len(sp.test_idx) == len(obs)
    assert len(sp.train_idx) / len(obs) == pytest.approx(0.8, abs=0.01)
    assert len(sp.test_idx) / len(obs) == pytest.approx(0.1, abs=0.01)
    sp.check_valid(len(obs))


def test_random_split_deterministic():
    obs = make_obs()
    a = random_spot_split(obs, seed=7)
    b = random_spot_split(obs, seed=7)
    assert a.train_idx == b.train_idx and a.test_idx == b.test_idx


def test_block_split_separation_and_buffer():
    obs = make_obs(n_slides=2, spots_per_slide=800)
    sp = spatial_block_split(obs, seed=0, method="grid", n_blocks_per_slide=4,
                             buffer=0.0)
    sp.check_valid(len(obs))
    assert len(sp.dropped_idx) == 0
    assert len(sp.test_idx) > 0 and len(sp.train_idx) > 0

    spb = spatial_block_split(obs, seed=0, method="grid", n_blocks_per_slide=4,
                              buffer=2.0)
    spb.check_valid(len(obs))
    # buffer property: every kept test spot is >= 2 array steps from train spots
    tr = set(spb.train_idx)
    for i in spb.test_idx:
        d = min(np.sqrt((obs.loc[i, "array_row"] - obs.loc[list(tr), "array_row"]) ** 2
                        + (obs.loc[i, "array_col"] - obs.loc[list(tr), "array_col"]) ** 2))
        assert d >= 2.0 - 1e-9
    assert len(spb.dropped_idx) > 0  # some boundary spots dropped


def test_group_split_no_group_crossover():
    obs = make_obs(n_slides=4)
    sp = group_held_out_split(obs, "slide", seed=0, test_groups=["slide0"],
                              val_groups=["slide1"])
    tr_slides = set(obs.loc[sp.train_idx, "slide"])
    te_slides = set(obs.loc[sp.test_idx, "slide"])
    assert tr_slides.isdisjoint(te_slides)
    assert "slide0" in te_slides
    assert len(sp.train_idx) + len(sp.val_idx) + len(sp.test_idx) == len(obs)
