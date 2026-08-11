#!/usr/bin/env python3
"""Final multi-dataset statistics refresh.

Outputs compact CSV/JSON files under results/final_stats without overwriting
DLPFC-specific formal analysis artifacts.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.statistics.inference import mixed_effects_inflation, paired_wilcoxon_bhfdr


OUT = Path("results/final_stats")
OUT.mkdir(parents=True, exist_ok=True)


DATASETS = {
    "dlpfc": {
        "aggregate": "results/formal_dlpfc/formal_aggregate.csv",
        "per_gene": "results/formal_dlpfc/formal_per_gene.csv",
        "moran": "data/processed/moran_top_genes.csv",
        "patient_prefix": "patient_",
        "spatial_split": "matched_hop0",
        "platform": "Visium_DLPFC",
    },
    "anderson": {
        "aggregate": "results/anderson_formal_external/formal_external_aggregate.csv",
        "per_gene": "results/anderson_formal_external/formal_external_per_gene.csv",
        "moran": "data/processed/anderson_moran.csv",
        "patient_prefix": "patient_",
        "spatial_split": "matched_hop5",
        "platform": "ST_v1",
    },
    "thrane": {
        "aggregate": "results/thrane_formal_external/formal_external_aggregate.csv",
        "per_gene": "results/thrane_formal_external/formal_external_per_gene.csv",
        "moran": "data/processed/thrane_moran.csv",
        "patient_prefix": "patient_",
        "spatial_split": "matched_hop2",
        "platform": "ST_v1",
    },
    "visium_breast": {
        "aggregate": "results/visium_breast_v01/v01_aggregate.csv",
        "per_gene": "results/visium_breast_v01/v01_per_gene.csv",
        "moran": "data/processed/visium_breast_moran.csv",
        "patient_prefix": None,
        "spatial_split": "matched_hop5",
        "slide_prefix": "slide_",
        "platform": "Visium_breast",
    },
}


def replicate_seed_invariant(df: pd.DataFrame) -> pd.DataFrame:
    seeds = sorted(df["seed"].unique())
    if len(seeds) <= 1:
        return df
    inv_mask = df["split"].str.startswith(("patient_", "region_", "slide_"))
    inv = df[inv_mask].copy()
    if inv.empty:
        return df
    out = [df[~inv_mask]]
    for split, g in inv.groupby("split"):
        if set(g["seed"]) == {seeds[0]}:
            out.append(pd.concat([g.assign(seed=s) for s in seeds], ignore_index=True))
        else:
            out.append(g)
    return pd.concat(out, ignore_index=True)


def summary_rows() -> pd.DataFrame:
    rows = []
    for dataset, spec in DATASETS.items():
        agg = pd.read_csv(spec["aggregate"])
        for (split, model), g in agg.groupby(["split", "model"]):
            rows.append({
                "dataset": dataset,
                "platform": spec["platform"],
                "split": split,
                "model": model,
                "mean_pearson": g["mean_pearson"].mean(),
                "sd_seed": g["mean_pearson"].std(),
                "n_rows": len(g),
            })
    return pd.DataFrame(rows)


def rli_table(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for dataset, spec in DATASETS.items():
        d = summary[summary["dataset"] == dataset]
        base = d[d["split"] == "random"].set_index("model")["mean_pearson"]
        strict_specs = [("spatial", spec["spatial_split"])]
        if spec.get("patient_prefix"):
            strict_specs.append(("patient", spec["patient_prefix"]))
        if spec.get("slide_prefix"):
            strict_specs.append(("slide", spec["slide_prefix"]))
        for strict_type, split_key in strict_specs:
            if split_key.endswith("_"):
                strict = d[d["split"].str.startswith(split_key)].groupby("model")["mean_pearson"].mean()
            else:
                strict = d[d["split"] == split_key].set_index("model")["mean_pearson"]
            for model in sorted(base.index.intersection(strict.index)):
                random = base.loc[model]
                value = strict.loc[model]
                rows.append({
                    "dataset": dataset,
                    "platform": spec["platform"],
                    "strict_type": strict_type,
                    "strict_split": split_key,
                    "model": model,
                    "random": random,
                    "strict": value,
                    "LI": random - value,
                    "RLI": (random - value) / random if abs(random) > 1e-12 else np.nan,
                    "retention": value / random if abs(random) > 1e-12 else np.nan,
                })
    return pd.DataFrame(rows)


def wilcoxon_all() -> pd.DataFrame:
    rows = []
    for dataset, spec in DATASETS.items():
        agg = replicate_seed_invariant(pd.read_csv(spec["aggregate"]))
        tests = [("spatial", spec["spatial_split"])]
        if spec.get("patient_prefix"):
            tmp = agg.copy()
            tmp["split"] = np.where(tmp["split"].str.startswith(spec["patient_prefix"]),
                                    "patient", tmp["split"])
            test_df = tmp.groupby(["split", "model", "seed"], as_index=False)["mean_pearson"].mean()
            w = paired_wilcoxon_bhfdr(test_df, "patient")
            w.insert(0, "strict_type", "patient")
            w.insert(0, "dataset", dataset)
            rows.append(w)
        if spec.get("slide_prefix"):
            tmp = agg.copy()
            tmp["split"] = np.where(tmp["split"].str.startswith(spec["slide_prefix"]),
                                    "slide", tmp["split"])
            test_df = tmp.groupby(["split", "model", "seed"], as_index=False)["mean_pearson"].mean()
            w = paired_wilcoxon_bhfdr(test_df, "slide")
            w.insert(0, "strict_type", "slide")
            w.insert(0, "dataset", dataset)
            rows.append(w)
        for strict_type, split_name in tests:
            w = paired_wilcoxon_bhfdr(agg, split_name)
            w.insert(0, "strict_type", strict_type)
            w.insert(0, "dataset", dataset)
            rows.append(w)
    return pd.concat(rows, ignore_index=True)


def per_gene_inflation(dataset: str, spec: dict, strict_split: str, strict_label: str) -> pd.DataFrame:
    gene = pd.read_csv(spec["per_gene"])
    moran = pd.read_csv(spec["moran"])
    if "gene" not in moran.columns:
        moran = moran.reset_index().rename(columns={"index": "gene"})
    strict_mask = gene["split"].str.startswith(strict_split) if strict_split.endswith("_") else gene["split"].eq(strict_split)
    rand = gene[gene["split"].eq("random")].groupby(["gene", "model"])["pearson"].mean().rename("random").reset_index()
    strict = gene[strict_mask].groupby(["gene", "model"])["pearson"].mean().rename("strict").reset_index()
    out = rand.merge(strict, on=["gene", "model"])
    out = out.merge(moran[["gene", "moran_i"]], on="gene", how="left")
    out["inflation"] = out["random"] - out["strict"]
    out["dataset"] = dataset
    out["platform"] = spec["platform"]
    out["strict_type"] = strict_label
    out["strict_split"] = strict_split
    return out.dropna(subset=["inflation", "moran_i"])


def main():
    t0 = time.time()
    summary = summary_rows()
    summary.to_csv(OUT / "summary_all_datasets.csv", index=False)

    rli = rli_table(summary)
    rli.to_csv(OUT / "LI_RLI_all_datasets.csv", index=False)

    w = wilcoxon_all()
    w.to_csv(OUT / "wilcoxon_all_datasets.csv", index=False)

    patient_parts = []
    spatial_parts = []
    for dataset, spec in DATASETS.items():
        if spec.get("patient_prefix"):
            patient_parts.append(per_gene_inflation(dataset, spec, spec["patient_prefix"], "patient"))
        spatial_parts.append(per_gene_inflation(dataset, spec, spec["spatial_split"], "spatial"))

    patient_inf = pd.concat(patient_parts, ignore_index=True)
    spatial_inf = pd.concat(spatial_parts, ignore_index=True)
    patient_inf.to_csv(OUT / "per_gene_inflation_patient.csv", index=False)
    spatial_inf.to_csv(OUT / "per_gene_inflation_spatial.csv", index=False)

    mixed = {
        "patient": mixed_effects_inflation(patient_inf[patient_inf["model"].isin(["pca_ridge", "spatial_knn"])]),
        "spatial": mixed_effects_inflation(spatial_inf[spatial_inf["model"].isin(["pca_ridge", "spatial_knn"])]),
        "meta": {
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "datasets": list(DATASETS),
            "note": "patient model excludes Visium breast; spatial model uses each dataset's configured spatial split.",
        },
    }
    (OUT / "mixed_effects.json").write_text(json.dumps(mixed, indent=2))

    print("== RLI table ==")
    print(rli[rli["model"].isin(["pca_ridge", "spatial_knn"])].round(4).to_string(index=False))
    print("\n== Wilcoxon ==")
    print(w.round(4).to_string(index=False))
    print("\n== Mixed effects ==")
    print(json.dumps(mixed, indent=2))
    print(f"\nDone in {time.time()-t0:.1f}s -> {OUT}")


if __name__ == "__main__":
    main()
