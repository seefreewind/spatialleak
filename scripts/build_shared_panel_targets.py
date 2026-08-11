#!/usr/bin/env python3
"""Build dataset-specific target-gene CSVs for the frozen shared ENSG panel.

The frozen panel is stored as ENSG IDs. DLPFC and Andersson processed matrices
use gene symbols, while Thrane uses ENSG IDs. This script reconstructs local
symbol mappings from raw files and writes one target CSV per dataset.
"""
import argparse
from pathlib import Path

import anndata as ad
import pandas as pd
import scanpy as sc


def read_panel(path: Path) -> list:
    genes = [g.strip() for g in path.read_text().splitlines() if g.strip()]
    return [g for g in genes if g.lower() != "gene"]


def dlpfc_ensg_to_symbol(raw_h5: Path) -> dict:
    adata = sc.read_10x_h5(raw_h5)
    return dict(zip(adata.var["gene_ids"].astype(str), adata.var.index.astype(str)))


def thrane_ensg_to_symbol(raw_dir: Path) -> dict:
    rows = []
    for path in sorted(raw_dir.glob("ST_*_counts.tsv")):
        genes = pd.read_csv(path, sep="\t", usecols=["gene"])["gene"].astype(str)
        parsed = genes.str.extract(r"^(\S+)\s+(ENSG\d+)")
        parsed.columns = ["symbol", "ensg"]
        rows.append(parsed.dropna())
    table = pd.concat(rows, ignore_index=True).drop_duplicates("ensg")
    return dict(zip(table["ensg"], table["symbol"]))


def assert_present(dataset: str, genes: list, processed_dir: Path) -> None:
    adata = ad.read_h5ad(processed_dir / f"{dataset}_hvg2000.h5ad")
    missing = [g for g in genes if g not in adata.var_names]
    if missing:
        preview = ", ".join(missing[:10])
        raise ValueError(f"{dataset}: {len(missing)} target genes missing: {preview}")


def write_csv(path: Path, genes: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"gene": genes}).to_csv(path, index=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", default="data/processed/gene_panels/shared_panel_50.txt")
    ap.add_argument("--processed-dir", default="data/processed")
    ap.add_argument("--dlpfc-h5", default="data/raw/dlpfc/h5/151507_filtered_feature_bc_matrix.h5")
    ap.add_argument("--thrane-raw-dir", default="data/raw/thrane_melanoma/extracted")
    ap.add_argument("--out-dir", default="data/processed/gene_panels")
    args = ap.parse_args()

    panel = read_panel(Path(args.panel))
    processed_dir = Path(args.processed_dir)
    out_dir = Path(args.out_dir)
    dlpfc_map = dlpfc_ensg_to_symbol(Path(args.dlpfc_h5))
    thrane_map = thrane_ensg_to_symbol(Path(args.thrane_raw_dir))

    targets = {
        "dlpfc": [dlpfc_map[g] for g in panel],
        "anderson": [thrane_map[g] for g in panel],
        "thrane": panel,
    }
    for dataset, genes in targets.items():
        assert_present(dataset, genes, processed_dir)
        out = out_dir / f"shared_panel_50_{dataset}_targets.csv"
        write_csv(out, genes)
        print(f"{dataset}: {len(genes)} genes -> {out}")


if __name__ == "__main__":
    main()
