# Supplement Architecture

Date: 2026-08-10

## Principle

The Supplement should not be a storage area for inconvenient results. It should preserve reproducibility, boundary conditions, and full result breadth while keeping the main manuscript focused on the two-channel claim.

## Supplementary Figures

| Item | Purpose | Source files | Notes |
|---|---|---|---|
| Supplementary Fig. 1 | Dataset QC and sample structure | processed h5ad metadata; `data/processed/*moran*`; audit files | Show spot counts, patient counts, section counts, platform density |
| Supplementary Fig. 2 | All seed/fold aggregate results | formal aggregate CSV files; `results/gse278936_prostate_spatial_pilot/spatial_pilot_aggregate.csv` | Use seed/fold as the visual unit, not spots |
| Supplementary Fig. 3 | Per-gene results | per-gene CSV outputs | Include unstable denominator labels where needed |
| Supplementary Fig. 4 | Moran analyses | `results/final_stats/per_gene_inflation_patient.csv`; `results/final_stats/per_gene_inflation_spatial.csv`; `results/final_stats/mixed_effects.json` | Separate spatial and patient channels; do not claim Moran explains all leakage |
| Supplementary Fig. 5 | Negative controls and mean baselines | aggregate CSVs | Mean baseline is sanity check, not evidence for leakage |
| Supplementary Fig. 6 | Additional distance curves | `figure_distance_curve_data.csv`; formal per-split outputs | Include non-resolvable Thrane high-hop annotation |
| Supplementary Fig. 7 | Dataset-held-out stress test | `table_dataset_heldout_anderson_to_visium.csv` | Keep supplementary unless main text needs Figure 6 panel |
| Supplementary Fig. 8 | Additional GraphSAGE results | `table_graphsage_shared_panel50_RLI.csv`; GraphSAGE output dirs | Include DLPFC/Andersson/Thrane/Visium breast scope limitations |

## Supplementary Tables

| Item | Content | Source files |
|---|---|---|
| Supplementary Table 1 | Dataset summary: accession/source, tissue, platform, patients, sections, spots, evidence level | status reports, h5ad metadata |
| Supplementary Table 2 | Models: Mean, PCA+Ridge, Spatial kNN, GraphSAGE | `MANUSCRIPT_RESULTS_METHODS_DRAFT.md`; scripts |
| Supplementary Table 3 | Split definitions and evidence levels | `EVIDENCE_HIERARCHY.md`; `ANALYSIS_LOCK.md` |
| Supplementary Table 4 | Full metrics: random, spatial strict, patient strict, LI, RLI, retention | `results/paper_assets/*.csv` |
| Supplementary Table 5 | Software and hyperparameters | `MANUSCRIPT_RESULTS_METHODS_DRAFT.md`; configs |
| Supplementary Table 6 | Claim-evidence map | `FINAL_CLAIM_EVIDENCE_MAP.md` |

## Boundary Conditions To Preserve

- GSE278936 Spatial kNN random performance is below zero; RLI is not interpreted.
- Thrane high-hop spatial tests are non-resolvable at larger buffers.
- Andersson/Thrane Spatial kNN random performance is near zero; do not use these rows as positive RLI evidence.
- Visium breast is a single-patient two-section dataset; slide-held-out is section-level evidence.
- Dataset-held-out transfer is a stress test, not a replacement for patient-held-out validation.

## Main-Supplement Boundary

Main text should carry:

- The two-channel claim.
- One strong spatial example.
- One strong patient/batch example.
- The GSE278936 non-zero-buffer finding.
- The evidence hierarchy.

Supplement should carry:

- All seed/fold/per-gene details.
- Non-resolvable split metadata.
- Full model/dataset table.
- Optional stress-test details.

