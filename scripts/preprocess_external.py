#!/usr/bin/env python3
"""Preprocess external datasets (Andersson HER2+, Thrane melanoma, 10x Visium
breast) into the shared analysis format:

  data/processed/{dataset}_hvg2000.h5ad   (HVG-2000 features, targets = top-50 Moran)
  data/processed/{dataset}_moran.csv

Same pipeline as DLPFC: per-section normalize_total(1e4)+log1p, pooled HVG-2000,
per-slide-averaged Moran's I. Spot IDs 'RxC' -> hex-grid coordinates.

Usage: python scripts/preprocess_external.py --dataset anderson|thrane|visium_breast
"""
import argparse
import json
import sys
import time
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.data.preprocess_utils import hex_coords_from_spot_ids, per_slide_moran

N_HVG = 2000
N_TARGET = 50


def strip_version(g):
    return g.split(".")[0] if g.count(".") == 1 else g


def anderson(raw: Path, out: Path):
    cm = raw / "extracted" / "count-matrices"
    files = sorted(cm.glob("*.tsv.gz"))
    sections = [f.name.replace(".tsv.gz", "") for f in files]
    ads = []
    for f, sec in zip(files, sections):
        df = pd.read_csv(f, sep="\t", index_col=0)  # spots x genes, index = RxC spot IDs
        df = df.fillna(0)
        df.columns = [strip_version(g) for g in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]
        a = ad.AnnData(df.astype(np.float32))
        a.obs["slide"] = sec
        a.obs["patient"] = sec[0]
        a.obs["total_counts"] = np.asarray(a.X.sum(axis=1)).ravel()
        a.obs["array_row"] = a.obs_names.map(lambda s: int(str(s).split("x")[0]))
        a.obs["array_col"] = a.obs_names.map(lambda s: int(str(s).split("x")[1]))
        sc.pp.normalize_total(a, target_sum=1e4)
        sc.pp.log1p(a)
        ads.append(a)
        print(f"  {sec}: {a.n_obs} spots x {a.n_vars} genes")
    a = ad.concat(ads, join="outer", index_unique="-")
    a.obs_names_make_unique()
    a.X = np.nan_to_num(np.asarray(a.X.toarray() if hasattr(a.X, "toarray") else a.X))
    sc.pp.filter_genes(a, min_cells=20)  # drop degenerate genes (NaN dispersion guard)
    sc.pp.highly_variable_genes(a, flavor="seurat", n_top_genes=N_HVG)
    hvg = a.var["highly_variable"].values
    hv = np.asarray(a[:, hvg].X.toarray())
    coords = hex_coords_from_spot_ids([str(n).split('-')[0] for n in a.obs_names])
    moran = per_slide_moran(hv, a.obs["slide"].values, coords)
    moran_df = pd.DataFrame({"gene": a.var_names[hvg], "moran_i": moran}).sort_values(
        "moran_i", ascending=False)
    a.obsm["spatial"] = coords
    a.write(out / "anderson_hvg2000.h5ad")
    moran_df.to_csv(out / "anderson_moran.csv", index=False)
    print(f"  -> {out/'anderson_hvg2000.h5ad'} ({a.n_obs} x {a.n_vars}, {moran_df['moran_i'].notna().sum()} Moran-valid genes)")


def thrane(raw: Path, out: Path):
    files = sorted((raw / "extracted").glob("ST_*_counts.tsv"))
    ads = []
    for f in files:
        df = pd.read_csv(f, sep="\t")
        df = df.fillna(0)
        df["ensg"] = df["gene"].map(lambda s: str(s).split()[-1] if " " in str(s) else str(s).split(".")[0])
        df["symbol"] = df["gene"].map(lambda s: str(s).split()[0] if " " in str(s) else str(s))
        df = df.set_index("ensg").drop(columns=["gene", "symbol"], errors="ignore")
        df = df.T  # spots x genes
        a = ad.AnnData(df.astype(np.float32))
        sec = f.name.replace("_counts.tsv", "").replace("ST_", "")
        a.obs["slide"] = sec
        a.obs["patient"] = sec.replace("rep1", "").replace("rep2", "")
        a.obs["total_counts"] = np.asarray(a.X.sum(axis=1)).ravel()
        a.obs["array_row"] = a.obs_names.map(lambda s: int(str(s).split("x")[0]))
        a.obs["array_col"] = a.obs_names.map(lambda s: int(str(s).split("x")[1]))
        sc.pp.normalize_total(a, target_sum=1e4)
        sc.pp.log1p(a)
        ads.append(a)
        print(f"  {sec}: {a.n_obs} spots x {a.n_vars} genes")
    a = ad.concat(ads, join="outer", index_unique="-")
    a.obs_names_make_unique()
    a.X = np.nan_to_num(np.asarray(a.X.toarray() if hasattr(a.X, "toarray") else a.X))
    sc.pp.filter_genes(a, min_cells=20)
    sc.pp.highly_variable_genes(a, flavor="seurat", n_top_genes=N_HVG)
    hvg = a.var["highly_variable"].values
    hv = np.asarray(a[:, hvg].X.toarray())
    coords = hex_coords_from_spot_ids([str(n).split('-')[0] for n in a.obs_names])
    moran = per_slide_moran(hv, a.obs["slide"].values, coords)
    moran_df = pd.DataFrame({"gene": a.var_names[hvg], "moran_i": moran}).sort_values(
        "moran_i", ascending=False)
    a.obsm["spatial"] = coords
    a.write(out / "thrane_hvg2000.h5ad")
    moran_df.to_csv(out / "thrane_moran.csv", index=False)
    print(f"  -> {out/'thrane_hvg2000.h5ad'} ({a.n_obs} x {a.n_vars})")


def visium_breast(raw: Path, out: Path):
    import tarfile

    ads = []
    mtx_files = sorted(raw.glob("*_filtered_feature_bc_matrix.tar.gz"))
    sp_files = sorted(raw.glob("*_spatial.tar.gz"))
    assert len(mtx_files) == len(sp_files) >= 1, (len(mtx_files), len(sp_files))
    for mtx, sp in zip(mtx_files, sp_files):
        import re
        m = re.search(r"Section_(\d+)", mtx.name)
        sec = f"Section_{m.group(1)}" if m else mtx.stem[:20]
        tmp = Path("/tmp") / sec
        tmp.mkdir(parents=True, exist_ok=True)
        for tar, sub in [(mtx, "mtx"), (sp, "sp")]:
            d = tmp / sub
            if not any(d.rglob("matrix.mtx.gz")) and not any(d.rglob("*.h5")):
                with tarfile.open(tar) as t:
                    t.extractall(d)
        h5s = list((tmp / "mtx").rglob("*.h5"))
        if h5s:
            a = sc.read_10x_h5(h5s[0])
        else:
            a = sc.read_10x_mtx(next((tmp / "mtx").rglob("filtered_feature_bc_matrix")))
        a.var_names_make_unique()
        pos_file = next((tmp / "sp").rglob("tissue_positions_list.*"))
        if pos_file.suffix == ".json":
            pos = pd.read_json(pos_file)
            pos = pos[pos["in_tissue"] == 1]
            pos = pos.set_index("barcode")
        else:
            pos = pd.read_csv(pos_file, header=None, names=[
                "barcode", "in_tissue", "array_row", "array_col",
                "pxl_col_in_fullres", "pxl_row_in_fullres"])
            pos = pos[pos["in_tissue"] == 1].set_index("barcode")
        a.obs = a.obs.join(pos[["array_row", "array_col", "pxl_col_in_fullres", "pxl_row_in_fullres"]])
        a = a[a.obs["array_row"].notna()]
        a.obs["slide"] = sec
        a.obs["patient"] = "P1"  # single block/donor (10x metadata)
        a.obs["total_counts"] = np.asarray(a.X.sum(axis=1)).ravel()
        sc.pp.normalize_total(a, target_sum=1e4)
        sc.pp.log1p(a)
        ads.append(a)
        print(f"  {sec}: {a.n_obs} spots")
    a = ad.concat(ads, join="outer", index_unique="-")
    a.obs_names_make_unique()
    sc.pp.highly_variable_genes(a, flavor="seurat", n_top_genes=N_HVG)
    hvg = a.var["highly_variable"].values
    hv = np.asarray(a[:, hvg].X.toarray())
    coords = a.obs[["array_row", "array_col"]].values.astype(float)
    moran = per_slide_moran(hv, a.obs["slide"].values, coords)
    moran_df = pd.DataFrame({"gene": a.var_names[hvg], "moran_i": moran}).sort_values(
        "moran_i", ascending=False)
    a.obsm["spatial"] = coords
    a.write(out / "visium_breast_hvg2000.h5ad")
    moran_df.to_csv(out / "visium_breast_moran.csv", index=False)
    print(f"  -> {out/'visium_breast_hvg2000.h5ad'} ({a.n_obs} x {a.n_vars})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["anderson", "thrane", "visium_breast"])
    ap.add_argument("--config", default="configs/datasets/dlpfc.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    out = Path(cfg["processed_dir"])
    out.mkdir(parents=True, exist_ok=True)
    raw = Path(cfg["raw_dir"]).parent
    t0 = time.time()
    fn = {"anderson": anderson, "thrane": thrane, "visium_breast": visium_breast}[args.dataset]
    dirname = {"anderson": "anderson_her2", "thrane": "thrane_melanoma",
               "visium_breast": "visium_breast"}[args.dataset]
    fn(raw / dirname, out)
    print(f"Done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
