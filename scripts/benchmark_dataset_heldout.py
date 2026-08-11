#!/usr/bin/env python3
"""Dataset-held-out prototype for cross-platform transfer.

This is intentionally conservative: train on one dataset and test on another
using intersected gene symbols. Spatial kNN is excluded because coordinates are
not comparable across datasets/platforms.
"""
import argparse
import sys
import time
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.metrics.metrics import aggregate_metrics, per_gene_metrics
from src.models.mean_model import predict_mean
from src.models.pca_ridge import fit_pca_ridge, predict_pca_ridge


def dense(a):
    return np.asarray(a.X.toarray() if hasattr(a.X, "toarray") else a.X)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-dataset", default="anderson")
    ap.add_argument("--test-dataset", default="visium_breast")
    ap.add_argument("--target-csv", default="data/processed/gene_panels/shared_panel_50_anderson_targets.csv")
    ap.add_argument("--processed-dir", default="data/processed")
    ap.add_argument("--out-dir", default="results/dataset_heldout")
    ap.add_argument("--out-prefix", default="anderson_to_visium")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--n-features", type=int, default=2000)
    ap.add_argument("--pca-components", type=int, default=64)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    train = ad.read_h5ad(Path(args.processed_dir) / f"{args.train_dataset}_hvg2000.h5ad")
    test = ad.read_h5ad(Path(args.processed_dir) / f"{args.test_dataset}_hvg2000.h5ad")
    targets_requested = pd.read_csv(args.target_csv)["gene"].tolist()
    target_genes = [g for g in targets_requested if g in train.var_names and g in test.var_names]
    missing = [g for g in targets_requested if g not in target_genes]
    common_features = sorted((set(train.var_names) & set(test.var_names)) - set(target_genes))[: args.n_features]
    if len(target_genes) < 10:
        raise ValueError(f"Too few target genes: {len(target_genes)}")
    if len(common_features) < args.pca_components:
        raise ValueError(f"Too few common features: {len(common_features)}")

    X_train = dense(train[:, common_features])
    Y_train = dense(train[:, target_genes])
    X_test = dense(test[:, common_features])
    Y_test = dense(test[:, target_genes])
    rows, gene_rows, slide_rows = [], [], []
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]

    for seed in seeds:
        pred = predict_mean(X_train, Y_train, X_test)
        gm = per_gene_metrics(Y_test, pred, target_genes)
        agg = aggregate_metrics(gm)
        gm.insert(0, "split", "dataset_heldout")
        gm.insert(1, "model", "mean")
        gm.insert(2, "seed", seed)
        gene_rows.append(gm)
        rows.append({"split": "dataset_heldout", "model": "mean", "seed": seed, **agg})
        for slide, idx in test.obs.reset_index(drop=True).groupby("slide").indices.items():
            sm = per_gene_metrics(Y_test[idx], pred[idx], target_genes)
            sm.insert(0, "slide", slide)
            sm.insert(1, "split", "dataset_heldout")
            sm.insert(2, "model", "mean")
            sm.insert(3, "seed", seed)
            slide_rows.append(sm)

        fit = fit_pca_ridge(
            X_train, Y_train, n_components=args.pca_components,
            alpha=1.0, random_state=seed)
        pred = predict_pca_ridge(X_test, fit)
        gm = per_gene_metrics(Y_test, pred, target_genes)
        agg = aggregate_metrics(gm)
        gm.insert(0, "split", "dataset_heldout")
        gm.insert(1, "model", "pca_ridge")
        gm.insert(2, "seed", seed)
        gene_rows.append(gm)
        rows.append({"split": "dataset_heldout", "model": "pca_ridge", "seed": seed, **agg})
        for slide, idx in test.obs.reset_index(drop=True).groupby("slide").indices.items():
            sm = per_gene_metrics(Y_test[idx], pred[idx], target_genes)
            sm.insert(0, "slide", slide)
            sm.insert(1, "split", "dataset_heldout")
            sm.insert(2, "model", "pca_ridge")
            sm.insert(3, "seed", seed)
            slide_rows.append(sm)
        print(f"seed{seed}: pca_ridge {agg['mean_pearson']:.4f}", flush=True)

    pd.DataFrame(rows).to_csv(out_dir / f"{args.out_prefix}_aggregate.csv", index=False)
    pd.concat(gene_rows, ignore_index=True).to_csv(out_dir / f"{args.out_prefix}_per_gene.csv", index=False)
    pd.concat(slide_rows, ignore_index=True).to_csv(out_dir / f"{args.out_prefix}_per_gene_per_slide.csv", index=False)
    meta = {
        "train_dataset": args.train_dataset,
        "test_dataset": args.test_dataset,
        "n_targets": len(target_genes),
        "missing_targets": missing,
        "n_common_features": len(common_features),
        "models": ["mean", "pca_ridge"],
        "note": "Cross-platform prototype; spatial coordinates are not comparable and spatial kNN is excluded.",
    }
    (out_dir / f"{args.out_prefix}_meta.json").write_text(__import__("json").dumps(meta, indent=2))
    print(f"Done in {time.time()-t0:.0f}s -> {out_dir}")


if __name__ == "__main__":
    main()
