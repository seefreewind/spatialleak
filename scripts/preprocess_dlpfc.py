#!/usr/bin/env python3
"""Preprocess DLPFC raw files into a cached h5ad (HVG subset + Moran's I targets).

Pipeline (per ANALYSIS_LOCK.md):
  1. per-slide: anndata.read_10x_h5 -> obs join (positions, layer, donor)
  2. normalize_total(target_sum=1e4) + log1p
  3. concat all slides; HVG-2000 (scanpy flavor="seurat", n_top_genes=2000)
  4. Moran's I per gene on the HVG set (Moran's I computed on pooled
     coordinates per slide with scipy; used for TARGET GENE selection)
  5. write data/processed/dlpfc_hvg2000.h5ad + VERSION.json + moran_top_genes.csv

Usage: python scripts/preprocess_dlpfc.py --config configs/datasets/dlpfc.yaml
"""
import argparse
import json
import time
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc
import yaml

SAMPLES = [
    "151507", "151508", "151509", "151510",
    "151669", "151670", "151671", "151672",
    "151673", "151674", "151675", "151676",
]
DONOR = {s: "Br5292" if i < 4 else ("Br5595" if i < 8 else "Br8100")
         for i, s in enumerate(SAMPLES)}
POS_HEADER = ["barcode", "in_tissue", "array_row", "array_col",
              "pxl_col_in_fullres", "pxl_row_in_fullres"]


def moran_weights(coords: np.ndarray, k: int = 7) -> np.ndarray:
    """Row-normalized inverse-distance weight matrix (precomputed once per slide)."""
    from scipy.spatial import cKDTree
    n = len(coords)
    tree = cKDTree(coords)
    d, idx = tree.query(coords, k=min(k, n))
    W = np.zeros((n, n))
    for i in range(n):
        for jj in range(1, len(d[i])):
            W[i, idx[i, jj]] = 1.0 / (d[i, jj] + 1e-6)
    W = (W + W.T) / 2
    S0 = W.sum()
    if S0 == 0:
        return np.zeros((n, n))
    return W / S0 * n


def moran_vectorized(Z: np.ndarray, W: np.ndarray) -> np.ndarray:
    """Moran's I per column of Z (n_spots x n_genes) with precomputed weights W.

    moran = (n / S0) * z' W z / (z' z); with W normalized s.t. sum(W)=n, factor=1.
    """
    n = Z.shape[0]
    Zc = Z - Z.mean(axis=0)
    denom = (Zc ** 2).sum(axis=0)
    num = Zc * (W @ Zc)
    with np.errstate(divide="ignore", invalid="ignore"):
        out = np.where(denom > 1e-12, num.sum(axis=0) / np.maximum(denom, 1e-12), np.nan)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/datasets/dlpfc.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    raw = Path(cfg["raw_dir"])
    out = Path(cfg["processed_dir"])
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    ads = []
    for s in SAMPLES:
        h5 = raw / "h5" / f"{s}_filtered_feature_bc_matrix.h5"
        if not h5.exists():
            raise FileNotFoundError(f"{h5} missing - run scripts/download_dlpfc.py first")
        a = sc.read_10x_h5(h5)
        a.var_names_make_unique()
        pos = pd.read_csv(raw / "spatial" / f"{s}_tissue_positions_list.txt",
                          header=None, names=POS_HEADER)
        pos = pos.set_index("barcode")
        a.obs = a.obs.join(pos, how="left")
        a.obs["slide"] = s
        a.obs["donor"] = DONOR[s]
        a.obs["in_tissue"] = a.obs["in_tissue"].astype("Int64")
        a.obs["total_counts"] = np.asarray(a.X.sum(axis=1)).ravel()
        sc.pp.normalize_total(a, target_sum=1e4)
        sc.pp.log1p(a)
        ads.append(a)
        print(f"  {s}: {a.n_obs} spots")

    layer_map = pd.read_csv(raw / "barcode_level_layer_map.tsv", sep="\t",
                            header=None, names=["barcode", "sample", "layer"])
    layer_map["barcode_short"] = layer_map["barcode"].map(lambda b: str(b).split("-")[0])
    layer_map["slide"] = layer_map["sample"].astype(str)
    full = ad.concat(ads, join="outer", index_unique="-")
    full.obs_names_make_unique()
    full.obs["barcode_short"] = [str(b).split("-")[0] for b in full.obs_names]
    full.obs = full.obs.reset_index().merge(
        layer_map[["barcode_short", "slide", "layer"]], on=["barcode_short", "slide"],
        how="left").set_index("index")
    if "layer" not in full.obs.columns:
        full.obs["layer"] = "NA"
    full.obs["layer"] = full.obs["layer"].fillna("NA").astype(str)
    adata = full
    sc.pp.highly_variable_genes(adata, flavor="seurat", n_top_genes=cfg["n_hvg"])
    hvg = adata.var["highly_variable"].values
    hv = np.asarray(adata[:, hvg].X.toarray() if hasattr(adata[:, hvg].X, "toarray")
                    else adata[:, hvg].X)
    # Per-gene Moran's I (inverse-distance weights, k=7 NN), averaged over slides.
    # Used ONLY for target-gene selection (data property, documented in ANALYSIS_LOCK).
    gene_scores = np.zeros(hv.shape[1])
    for s in SAMPLES:
        m = adata.obs["slide"].values == s
        coords = adata.obs.loc[m, ["array_row", "array_col"]].values.astype(float)
        W = moran_weights(coords)
        gene_scores += moran_vectorized(hv[m], W)
    gene_scores /= len(SAMPLES)
    moran = pd.DataFrame({"gene": adata.var_names[hvg], "moran_i": gene_scores})
    moran = moran.sort_values("moran_i", ascending=False)
    moran.to_csv(out / "moran_top_genes.csv", index=False)

    adata.write(out / "dlpfc_hvg2000.h5ad")
    version = {
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "n_obs": int(adata.n_obs), "n_vars": int(adata.n_vars),
        "n_hvg": int(cfg["n_hvg"]), "slides": SAMPLES,
        "donors": sorted(set(DONOR.values())),
        "normalization": "normalize_total(1e4)+log1p",
        "hvg_flavor": "seurat",
        "software": {"scanpy": sc.__version__, "anndata": ad.__version__,
                     "numpy": np.__version__, "pandas": pd.__version__},
    }
    (out / "VERSION.json").write_text(json.dumps(version, indent=2))
    print(f"\nDone in {time.time()-t0:.0f}s -> {out/'dlpfc_hvg2000.h5ad'}")


if __name__ == "__main__":
    main()
