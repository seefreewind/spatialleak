# Target-Panel Leakage Audit

## Decision

**CASE A: no material target-panel leakage. No new target-panel analysis is required.**

Dataset-specific target panels were used to define the prediction task. They were not selected by prediction performance, not reselected after model evaluation, and not varied between random and strict splits within a dataset. The shared_panel_50 analyses independently support the main patient-channel conclusion.

## Dataset-Specific Moran Panels

| Question | Audit answer |
|---|---|
| Where was Moran's I computed? | On processed expression matrices after normalization, log transformation, HVG selection, and per-slide spatial weighting. |
| Was it computed before splitting? | Yes. Moran files under `data/processed/*moran*.csv` are preprocessing artifacts. |
| Did it include eventual test spots? | Yes. Dataset-wide Moran ranking used all spots to define a benchmark target set. |
| Did target selection use model performance? | No. It used spatial autocorrelation only. |
| Were targets reselected after results? | No evidence of reselection. Scripts read frozen Moran CSVs or explicit gene CSVs. |
| Were targets identical across splits? | Yes within each dataset/run. |

## shared_panel_50

The shared panel was frozen before shared-panel model comparison. It was built from cross-dataset HVG overlap and average Moran rank, then materialized under `data/processed/gene_panels/`. It was not selected by prediction performance. It supports the central patient-channel conclusion in DLPFC, Andersson, and Thrane and was extended to GSE278936 as a spatial-channel pilot panel.

## Manuscript Wording Lock

Methods should state: **Target selection defined the prediction task independently of downstream model performance and was frozen across evaluation regimes.**

Because Moran ranking used the whole dataset, Methods should also state: **Moran-based target ranking was used to define the benchmark task rather than to tune or select predictive models.**

Limitations should state: **Dataset-wide target definition may use descriptive information from the full dataset, although target selection was independent of model performance.**
