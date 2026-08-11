#!/usr/bin/env python3
"""Preprocess public GSE278936 processed Visium data for spatial-channel pilot."""
from __future__ import annotations

import argparse
import gzip
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc
from scipy.io import mmread
from scipy import sparse

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.data.preprocess_utils import per_slide_moran


N_FEATURES = 2000


def read_gzip_lines(path: Path) -> list[str]:
    with gzip.open(path, "rt") as handle:
        return [line.rstrip("\n") for line in handle]


def read_positions(path: Path) -> pd.DataFrame:
    with gzip.open(path, "rt") as handle:
        first = handle.readline().rstrip("\n").split(",")
    has_header = first[0] == "barcode"
    pos = pd.read_csv(path, header=0 if has_header else None)
    if not has_header:
        pos.columns = [
            "barcode",
            "in_tissue",
            "array_row",
            "array_col",
            "pxl_col_in_fullres",
            "pxl_row_in_fullres",
        ]
    return pos[pos["in_tissue"].astype(int).eq(1)].set_index("barcode")


def sample_paths(sample_dir: Path) -> dict[str, Path]:
    return {
        "matrix": next(sample_dir.glob("*_matrix.mtx.gz")),
        "features": next(sample_dir.glob("*_features.tsv.gz")),
        "barcodes": next(sample_dir.glob("*_barcodes.tsv.gz")),
        "positions": next(sample_dir.glob("*_tissue_positions_list.csv.gz")),
    }


def read_sample(sample_dir: Path, audit: pd.DataFrame) -> ad.AnnData:
    paths = sample_paths(sample_dir)
    features = pd.read_csv(paths["features"], sep="\t", header=None,
                           names=["gene_id", "gene_symbol", "feature_type"])
    barcodes = read_gzip_lines(paths["barcodes"])
    mat = mmread(paths["matrix"]).tocsr().T.astype(np.float32)
    a = ad.AnnData(mat)
    a.obs_names = barcodes
    a.var_names = features["gene_symbol"].astype(str).values
    a.var["gene_id"] = features["gene_id"].astype(str).values
    a.var["feature_type"] = features["feature_type"].astype(str).values
    a.var_names_make_unique()

    pos = read_positions(paths["positions"])
    a.obs = a.obs.join(pos[["array_row", "array_col", "pxl_col_in_fullres", "pxl_row_in_fullres"]])
    a = a[a.obs["array_row"].notna()].copy()

    gsm = sample_dir.name.split("_", 1)[0]
    meta = audit[audit["gsm"].eq(gsm)].iloc[0]
    a.obs["slide"] = str(meta["geo_sample_label"])
    a.obs["patient"] = str(meta["patient_id"])
    a.obs["section_id"] = str(meta["section_id"])
    a.obs["treatment_group"] = str(meta["treatment_group"])
    a.obs["slide_serial"] = str(meta["slide_serial"])
    a.obs["total_counts"] = np.asarray(a.X.sum(axis=1)).ravel()
    sc.pp.normalize_total(a, target_sum=1e4)
    sc.pp.log1p(a)
    print(f"  {gsm} {meta['geo_sample_label']}: {a.n_obs} spots x {a.n_vars} genes")
    return a


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", default="data/raw/gse278936_prostate/processed_minimal")
    ap.add_argument("--audit-csv", default="data/external_audit/gse278936/public_sample_audit.csv")
    ap.add_argument("--target-csv", default="data/external_audit/gse278936/shared_panel_50_gse278936_usable_symbols.csv")
    ap.add_argument("--out-dir", default="data/processed")
    ap.add_argument("--dataset-name", default="gse278936_prostate")
    args = ap.parse_args()

    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    audit = pd.read_csv(args.audit_csv)
    target_genes = pd.read_csv(args.target_csv)["gene"].astype(str).tolist()
    sample_dirs = sorted([p for p in raw_dir.iterdir() if p.is_dir() and p.name.startswith("GSM")])
    if not sample_dirs:
        raise FileNotFoundError(f"No sample directories found in {raw_dir}")

    ads = [read_sample(d, audit) for d in sample_dirs]
    a = ad.concat(ads, join="outer", index_unique="-")
    a.obs_names_make_unique()
    if sparse.issparse(a.X):
        a.X.data = np.nan_to_num(a.X.data)
    else:
        a.X = np.nan_to_num(np.asarray(a.X))
    sc.pp.filter_genes(a, min_cells=20)

    sc.pp.highly_variable_genes(a, flavor="seurat", n_top_genes=N_FEATURES)
    hvg_genes = a.var_names[a.var["highly_variable"].values].astype(str).tolist()
    target_genes = [g for g in target_genes if g in a.var_names]
    selected = []
    for gene in hvg_genes + target_genes:
        if gene not in selected:
            selected.append(gene)
    a = a[:, selected].copy()
    a.obs["array_row"] = a.obs["array_row"].astype(float)
    a.obs["array_col"] = a.obs["array_col"].astype(float)
    coords = a.obs[["array_row", "array_col"]].values.astype(float)
    a.obsm["spatial"] = coords

    dense = np.asarray(a.X.toarray() if sparse.issparse(a.X) else a.X)
    moran = per_slide_moran(dense, a.obs["slide"].values, coords)
    moran_df = pd.DataFrame({"gene": a.var_names.astype(str), "moran_i": moran}).sort_values(
        "moran_i", ascending=False)

    a.write(out_dir / f"{args.dataset_name}_hvg2000.h5ad")
    moran_df.to_csv(out_dir / f"{args.dataset_name}_moran.csv", index=False)
    pd.DataFrame({"gene": target_genes}).to_csv(
        out_dir / "gene_panels" / "shared_panel_50_gse278936_prostate_targets.csv",
        index=False,
    )
    print(f"wrote {out_dir / f'{args.dataset_name}_hvg2000.h5ad'}")
    print(f"wrote {out_dir / f'{args.dataset_name}_moran.csv'}")
    print(f"shared targets usable: {len(target_genes)}/50")


if __name__ == "__main__":
    main()
