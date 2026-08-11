# Phase 18 Final Figure Architecture

## Final Main Figures

| Figure | Purpose | Main panels | Source data |
|---|---|---|---|
| Fig. 1 | SpatialLeak concept and evidence hierarchy | Random spot split, spatial buffer, slide, patient, dataset tiers; two inflation channels | schematic plus `docs/reports/EVIDENCE_HIERARCHY.md` |
| Fig. 2 | Random split inflation across datasets | Dataset/model RLI heatmap; random versus strict mean Pearson | `table_two_channel_leakage.csv` |
| Fig. 3 | Non-zero spatial buffers reveal neighborhood dependence | DLPFC and Visium breast hop curves; GSE278936 PCA hop curve as spatial-channel replication | `figure_distance_curve_data.csv`, `table_gse278936_spatial_pilot_RLI.csv` |
| Fig. 4 | Sample-size defense | Random full versus random-size-matched versus spatial buffer for hop2/hop5 | `table_random_size_matched_control.csv` |
| Fig. 5 | Patient/batch channel | Andersson and Thrane PCA+Ridge/GraphSAGE patient-held-out losses; DLPFC mixed case | `table_two_channel_leakage.csv`, `table_graphsage_shared_panel50_RLI.csv` |
| Fig. 6 | Model ranking and evaluation hierarchy | Model advantage changes by split regime; evaluation-tier decision tree | `table_two_channel_leakage.csv`, final manuscript methods |

## Supplementary Reallocation

- Move Andersson-to-Visium cross-platform mean Pearson 0.199 to Supplementary Information as a stress test.
- Keep GSE278936 in the spatial-channel supplementary/external replication logic, not the patient-held-out validation logic.
- Keep near-zero Spatial kNN rows in source tables but do not use them for positive RLI claims.

## Legend Rules

- Define LI, RLI, and retention in every figure legend that uses them.
- State when RLI is not interpreted because the random denominator is near zero.
- Use "apparent generalization inflation" for LI/RLI and reserve "patient-held-out" for true patient separation.
