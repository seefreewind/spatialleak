#!/usr/bin/env python3
"""Pilot benchmark: 1 dataset (DLPFC) x 1 task (multi-gene prediction) x
splits (random / spatial-block / patient-held-out) x models (Mean / PCA+Ridge /
Spatial kNN / GraphSAGE-optional) x seeds.

All outputs land in results/pilot/ as CSV (per-gene, per-seed) + aggregate +
config snapshot + run log. Never edit result CSVs by hand.

Usage: python scripts/pilot_benchmark.py --config configs/experiments/pilot_dlpfc.yaml
"""
import argparse
import json
import logging
import sys
import time
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.metrics.metrics import aggregate_metrics, per_gene_metrics
from src.models.mean_model import predict_mean
from src.models.pca_ridge import fit_pca_ridge, predict_pca_ridge
from src.models.spatial_knn import predict_spatial_knn
from src.splits.group_split import group_held_out_split
from src.splits.random_split import random_spot_split
from src.splits.spatial_block_split import spatial_block_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("pilot")


def make_splits(obs: pd.DataFrame, cfg: dict, seed: int) -> dict:
    """Build all splits for one seed; patient split is deterministic by donor fold."""
    splits = {}
    splits["random"] = random_spot_split(
        obs, seed=seed, train_frac=cfg["train_frac"], val_frac=cfg["val_frac"])
    for buffer in [0, 1, 2, 5]:
        splits[f"block_buf{buffer}"] = spatial_block_split(
            obs, seed=seed, method=cfg["block_method"],
            n_blocks_per_slide=cfg["n_blocks_per_slide"], buffer=buffer,
            name=f"spatial_block_buf{buffer}")
    if seed == cfg["seeds"][0]:  # patient folds are seed-invariant: build once
        for donor in sorted(obs["donor"].unique()):
            test_slides = sorted(obs.loc[obs["donor"] == donor, "slide"].unique())
            train_donors = [d for d in sorted(obs["donor"].unique()) if d != donor]
            # validation slide must come from TRAIN donors (never the test donor)
            val_slides = [sorted(obs.loc[obs["donor"] == train_donors[0], "slide"].unique())[0]]
            splits[f"patient_holdout_{donor}"] = group_held_out_split(
                obs, "slide", seed=seed, test_groups=test_slides, val_groups=val_slides,
                name=f"patient_holdout_{donor}")
    return splits


def run_model(model: str, X, Y, coords, split, params) -> np.ndarray:
    tr, te = np.asarray(split.train_idx), np.asarray(split.test_idx)
    if model == "mean":
        return predict_mean(X[tr], Y[tr], X[te])
    if model == "pca_ridge":
        fit = fit_pca_ridge(X[tr], Y[tr], n_components=params["pca_components"],
                            alpha=params["ridge_alpha"], random_state=params["seed"])
        return predict_pca_ridge(X[te], fit)
    if model == "spatial_knn":
        return predict_spatial_knn(coords[tr], Y[tr], coords[te], k=params["knn_k"])
    raise ValueError(f"unknown model: {model}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/experiments/pilot_dlpfc.yaml")
    ap.add_argument("--splits", default=None,
                    help="comma list: random,block_buf0,block_buf1,block_buf2,block_buf5,patient_holdout")
    ap.add_argument("--models", default=None, help="comma list: mean,pca_ridge,spatial_knn")
    ap.add_argument("--gene-csv", default=None, help="explicit target gene list CSV (gene column)")
    ap.add_argument("--out-suffix", default="", help="suffix for output filenames")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    if args.splits:
        cfg["splits"] = args.splits.split(",")
    if args.models:
        cfg["models"] = args.models.split(",")
    out_dir = Path(cfg["out_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    adata = ad.read_h5ad(cfg["h5ad"])
    obs = adata.obs.reset_index(drop=True)
    log.info(f"Loaded {adata.n_obs} spots x {adata.n_vars} genes")

    if args.gene_csv:
        target_genes = pd.read_csv(args.gene_csv)["gene"].tolist()
        log.info(f"Target genes from {args.gene_csv}: {len(target_genes)}")
    else:
        target_genes = pd.read_csv(Path(cfg["moran_csv"]), index_col=0).index[:cfg["n_target_genes"]].tolist()
    feature_genes = [g for g in adata.var_names if g not in target_genes][:cfg["n_features"]]
    target_genes = [g for g in target_genes if g in adata.var_names]
    log.info(f"Target genes: {len(target_genes)} | Feature genes: {len(feature_genes)}")

    X = np.asarray(adata[:, feature_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, feature_genes].X)
    Y = np.asarray(adata[:, target_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, target_genes].X)
    coords = obs[["array_row", "array_col"]].values.astype(float)
    # per-slide coordinate scaling (positions comparable within slide only)
    for slide in obs["slide"].unique():
        m = (obs["slide"] == slide).values
        coords[m] = (coords[m] - coords[m].mean(axis=0)) / coords[m].std(axis=0)
    del adata

    rows, gene_rows, slide_rows = [], [], []
    requested = set(cfg["splits"])
    for seed in cfg["seeds"]:
        splits = make_splits(obs, cfg, seed)
        for split_name, split in splits.items():
            if requested and not any(split_name.startswith(r) or split_name == r
                                     for r in requested):
                continue
            for model in cfg["models"]:
                tag = f"{split_name}__{model}__seed{seed}"
                t = time.time()
                test_pos = np.asarray(split.test_idx)
                pred = run_model(model, X, Y, coords, split, {**cfg["model_params"], "seed": seed})
                gm = per_gene_metrics(Y[test_pos], pred, target_genes)
                agg = aggregate_metrics(gm)
                gm.insert(0, "split", split_name)
                gm.insert(1, "model", model)
                gm.insert(2, "seed", seed)
                gene_rows.append(gm)
                rows.append({"split": split_name, "model": model, "seed": seed, **agg})
                # per-slide metrics (slide = resampling unit for bootstrap CIs)
                for slide, idx in obs.iloc[test_pos].groupby("slide").indices.items():
                    sm = per_gene_metrics(Y[test_pos[idx]], pred[idx], target_genes)
                    sm.insert(0, "slide", slide)
                    sm.insert(1, "split", split_name)
                    sm.insert(2, "model", model)
                    sm.insert(3, "seed", seed)
                    slide_rows.append(sm)
                log.info(f"  {tag}: mean_pearson={agg['mean_pearson']:.4f} ({time.time()-t:.1f}s)")

    gene_df = pd.concat(gene_rows, ignore_index=True)
    agg_df = pd.DataFrame(rows)
    slide_df = pd.concat(slide_rows, ignore_index=True)
    suffix = f"_{args.out_suffix}" if args.out_suffix else ""
    gene_df.to_csv(out_dir / f"pilot_per_gene{suffix}.csv", index=False)
    slide_df.to_csv(out_dir / f"pilot_per_gene_per_slide{suffix}.csv", index=False)
    agg_df.to_csv(out_dir / f"pilot_aggregate{suffix}.csv", index=False)
    (out_dir / "pilot_config.yaml").write_text(yaml.safe_dump(cfg))
    log.info(f"\nDone in {time.time()-t0:.0f}s -> {out_dir}")


if __name__ == "__main__":
    main()
