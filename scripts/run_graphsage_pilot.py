#!/usr/bin/env python3
"""Pilot criterion C: representative complex spatial model (GraphSAGE, CPU).

Splits: random (seed 0), spatial_block buffer=2 (seed 0), patient_holdout
(Br5595 fold). 2 seeds x 3 splits. Output: results/sensitivity/graphsage_pilot.csv.

Usage: python scripts/run_graphsage_pilot.py --config configs/experiments/pilot_dlpfc.yaml
"""
import argparse
import sys
import time
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import torch
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.metrics.metrics import aggregate_metrics, per_gene_metrics
from src.models.graphsage import fit_graphsage
from src.splits.group_split import group_held_out_split
from src.splits.random_split import random_spot_split
from src.splits.spatial_block_split import spatial_block_split


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/experiments/pilot_dlpfc.yaml")
    ap.add_argument("--seeds", default="0,1")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    out_dir = Path(cfg["out_dir"]).parent / "sensitivity"
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    torch.set_num_threads(4)  # be polite to concurrent jobs

    adata = ad.read_h5ad(cfg["h5ad"])
    obs = adata.obs.reset_index(drop=True)
    target_genes = pd.read_csv(Path(cfg["moran_csv"]), index_col=0).index[:cfg["n_target_genes"]].tolist()
    target_genes = [g for g in target_genes if g in adata.var_names]
    feature_genes = [g for g in adata.var_names if g not in target_genes][:cfg["n_features"]]
    X_all = np.asarray(adata[:, feature_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, feature_genes].X)
    Y_all = np.asarray(adata[:, target_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, target_genes].X)
    coords = obs[["array_row", "array_col"]].values.astype(float)
    for slide in obs["slide"].unique():
        m = (obs["slide"] == slide).values
        coords[m] = (coords[m] - coords[m].mean(axis=0)) / coords[m].std(axis=0)
    slide_of = obs["slide"].values
    del adata

    rows = []
    for seed in [int(s) for s in args.seeds.split(",")]:
        splits = {"random": random_spot_split(obs, seed=seed)}
        splits["block_buf2"] = spatial_block_split(obs, seed=seed, method=cfg["block_method"],
                                                   n_blocks_per_slide=cfg["n_blocks_per_slide"],
                                                   buffer=2, name="spatial_block_buf2")
        test_slides = sorted(obs.loc[obs["donor"] == "Br5595", "slide"].unique())
        val_slides = [sorted(obs.loc[obs["donor"] == "Br5292", "slide"].unique())[0]]
        splits["patient_Br5595"] = group_held_out_split(
            obs, "slide", seed=seed, test_groups=test_slides, val_groups=val_slides,
            name="patient_holdout_Br5595")

        for sname, sp in splits.items():
            tr, va = np.asarray(sp.train_idx), np.asarray(sp.val_idx)
            t = time.time()
            _, _, pred = fit_graphsage(
                X_train=X_all[tr], Y_train=Y_all[tr], X_all=X_all, Y_all=Y_all,
                coords_all=coords, slide_of=slide_of, train_idx=tr, val_idx=va,
                n_components=cfg["model_params"]["pca_components"],
                hidden=128, lr=1e-3, epochs=500, patience=60,
                seed=seed, device="cpu")
            te = np.asarray(sp.test_idx)
            gm = per_gene_metrics(Y_all[te], pred[te], target_genes)
            rows.append({"split": sname, "seed": seed, **aggregate_metrics(gm)})
            print(f"  {sname} seed{seed}: mean_pearson={rows[-1]['mean_pearson']:.4f} "
                  f"({time.time()-t:.0f}s)", flush=True)

    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "graphsage_pilot.csv", index=False)
    print(f"\nDone in {time.time()-t0:.0f}s -> {out_dir / 'graphsage_pilot.csv'}")


if __name__ == "__main__":
    main()
