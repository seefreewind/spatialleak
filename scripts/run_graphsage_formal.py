#!/usr/bin/env python3
"""GraphSAGE formal run (Phase 7A): 10 seeds x {random, matched_hop0,
patient_Br5292, patient_Br5595, patient_Br8100}.

Usage: python scripts/run_graphsage_formal.py --config configs/experiments/formal_dlpfc.yaml
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
from src.splits.matched_block_split import matched_block_split
from src.splits.random_split import random_spot_split


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/experiments/formal_dlpfc.yaml")
    ap.add_argument("--seeds", default="0,1,2,3,4,5,6,7,8,9")
    ap.add_argument("--patient-only", action="store_true")
    ap.add_argument("--gene-csv", default=None, help="explicit target gene list CSV (gene column)")
    ap.add_argument("--splits", default=None, help="comma list: random,matched_hop0,patient")
    ap.add_argument("--out-suffix", default="")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    out_dir = Path(cfg["out_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    torch.set_num_threads(2)

    # resume-safe: load existing partial results
    suffix = f"_{args.out_suffix}" if args.out_suffix else ""
    agg_path = out_dir / f"formal_aggregate_graphsage{suffix}.csv"
    gene_path = out_dir / f"formal_per_gene_graphsage{suffix}.csv"
    rows_prev = pd.read_csv(agg_path).to_dict("records") if agg_path.exists() else []
    gene_prev = pd.read_csv(gene_path) if gene_path.exists() else None
    done = {(r["split"], r["seed"]) for r in rows_prev}
    split_filters = set(args.splits.split(",")) if args.splits else set()

    adata = ad.read_h5ad(cfg["h5ad"])
    obs = adata.obs.reset_index(drop=True)
    layer_cols = [c for c in obs.columns if c.startswith("layer_")]
    if args.gene_csv:
        target_genes = pd.read_csv(args.gene_csv)["gene"].tolist()
    else:
        target_genes = pd.read_csv(Path(cfg["moran_csv"]), index_col=0).index[:cfg["n_target_genes"]].tolist()
    target_genes = [g for g in target_genes if g in adata.var_names]
    feature_genes = [g for g in adata.var_names if g not in target_genes][:cfg["n_features"]]
    X_all = np.asarray(adata[:, feature_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, feature_genes].X)
    Y_all = np.asarray(adata[:, target_genes].X.toarray() if hasattr(adata.X, "toarray") else adata[:, target_genes].X)
    obs["layer"] = obs["layer"].astype(str)
    dm = pd.get_dummies(obs["layer"], prefix="layer")
    for c in dm.columns:
        obs[c] = dm[c].values
    obs["moran_signal"] = Y_all.mean(axis=1)
    coords = obs[["array_row", "array_col"]].values.astype(float)
    for slide in obs["slide"].unique():
        m = (obs["slide"] == slide).values
        coords[m] = (coords[m] - coords[m].mean(axis=0)) / coords[m].std(axis=0)
    slide_of = obs["slide"].values
    del adata

    rows, gene_rows = [], []
    for seed in [int(s) for s in args.seeds.split(",")]:
        splits = {"random": random_spot_split(obs, seed=seed)}
        splits["matched_hop0"] = matched_block_split(
            obs, seed=seed, buffer_kind="hop", buffer_value=0,
            n_candidates=cfg["n_candidates"], knn_k=cfg["knn_k"], layer_cols=layer_cols,
            name="matched_hop0")
        if args.patient_only:
            splits = {}
        for donor in sorted(obs["donor"].unique()):
            if (f"patient_{donor}", seed) in done:
                continue  # seed-invariant folds already computed
            if args.patient_only or seed == int(args.seeds.split(",")[0]):
                test_slides = sorted(obs.loc[obs["donor"] == donor, "slide"].unique())
                train_donors = [d for d in sorted(obs["donor"].unique()) if d != donor]
                val_slides = [sorted(obs.loc[obs["donor"] == train_donors[0], "slide"].unique())[0]]
                splits[f"patient_{donor}"] = group_held_out_split(
                    obs, "slide", seed=seed, test_groups=test_slides, val_groups=val_slides,
                    name=f"patient_holdout_{donor}")

        for sname, sp in splits.items():
            if split_filters and not any(sname.startswith(f) or sname == f for f in split_filters):
                continue
            if (sname, seed) in done:
                print(f"  skip {sname} seed{seed} (already done)", flush=True)
                continue
            if (sname, seed) in set((r["split"], r["seed"]) for r in rows):
                print(f"  skip {sname} seed{seed} (this session)", flush=True)
                continue
            tr, va = np.asarray(sp.train_idx, dtype=int), np.asarray(sp.val_idx, dtype=int)
            t = time.time()
            _, _, pred = fit_graphsage(
                X_train=X_all[tr], Y_train=Y_all[tr], X_all=X_all, Y_all=Y_all,
                coords_all=coords, slide_of=slide_of, train_idx=tr, val_idx=va,
                n_components=cfg["model_params"]["pca_components"],
                hidden=128, lr=1e-3, epochs=500, patience=60,
                seed=seed, device="cpu")
            te = np.asarray(sp.test_idx, dtype=int)
            gm = per_gene_metrics(Y_all[te], pred[te], target_genes)
            gm.insert(0, "split", sname); gm.insert(1, "model", "graphsage"); gm.insert(2, "seed", seed)
            gene_rows.append(gm)
            rows.append({"split": sname, "model": "graphsage", "seed": seed,
                         **aggregate_metrics(gm)})
            print(f"  {sname} seed{seed}: {rows[-1]['mean_pearson']:.4f} ({time.time()-t:.0f}s)", flush=True)
            # incremental checkpoint: survive aborts
            _flush(rows_prev, rows, gene_rows, gene_prev, agg_path, gene_path)

    gene_df = pd.concat([gene_prev] + gene_rows, ignore_index=True) if gene_rows else gene_prev
    agg_df = pd.DataFrame(rows_prev + rows)
    if gene_df is not None:
        gene_df = gene_df.drop_duplicates(subset=["split", "model", "seed", "gene"])
        gene_df.to_csv(gene_path, index=False)
    agg_df = agg_df.drop_duplicates(subset=["split", "model", "seed"])
    agg_df.to_csv(agg_path, index=False)
    print(f"\nDone in {time.time()-t0:.0f}s -> {out_dir}")


def _flush(rows_prev, rows, gene_rows, gene_prev, agg_path, gene_path):
    """Incremental CSV checkpoint (survives aborts)."""
    try:
        parts = ([gene_prev] if gene_prev is not None else []) + gene_rows
        gene_df = pd.concat(parts, ignore_index=True)
        gene_df = gene_df.drop_duplicates(subset=["split", "model", "seed", "gene"])
        gene_df.to_csv(gene_path, index=False)
        agg_df = pd.DataFrame(rows_prev + rows)
        agg_df = agg_df.drop_duplicates(subset=["split", "model", "seed"])
        agg_df.to_csv(agg_path, index=False)
    except Exception as e:  # noqa: BLE001 - checkpoint must never kill the run
        print(f"  checkpoint failed: {e}", flush=True)


if __name__ == "__main__":
    main()
