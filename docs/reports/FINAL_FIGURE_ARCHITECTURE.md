# Final Figure Architecture

Date: 2026-08-10

## Current Figure Assets

Existing files:

- `results/paper_assets/figures/fig1_leakage_overview.svg/.png`
- `results/paper_assets/figures/fig2_spatial_distance_curves.svg/.png`
- `results/paper_assets/figures/fig3_model_and_transfer.svg/.png`
- `results/paper_assets/figures/FIGURE_PACKAGE_NOTES.md`

Current assets are useful but should be reorganized for a six-figure high-impact manuscript. Do not redraw yet; this file defines the final contract.

## Main Figures

### Figure 1. SpatialLeak Conceptual Framework

Purpose: make the whole manuscript legible before the reader sees results.

Panels:

- Channel A: within-section spatial-neighborhood leakage.
- Channel B: patient/batch shortcut.
- Distinction between leakage-like local dependence and transportable biology.
- Evidence hierarchy from random split to cross-platform held-out stress testing.

Source: conceptual figure, not quantitative.

Legend rule: state that SpatialLeak measures evaluation-dependent apparent generalization inflation, not proven causal leakage for every performance difference.

### Figure 2. Cross-Dataset Performance Inflation

Purpose: establish the general problem.

Panels:

- Paired random versus strict performance for PCA+Ridge across DLPFC, Andersson, Thrane, and Visium breast.
- RLI forest or compact dot plot for dataset-specific primary strict comparisons.

Source:

- `results/paper_assets/table_dataset_specific_RLI.csv`
- `results/paper_assets/table_two_channel_leakage.csv`

Design note: avoid a large heatmap. Use paired effect visualization so the reader sees that RLI is derived from performance loss.

### Figure 3. Two-Channel Leakage Landscape

Purpose: visual core of the paper.

Recommended design:

- x-axis: spatial RLI.
- y-axis: patient RLI.
- point: dataset-model combination.
- shape: model.
- color: dataset or platform.
- NA values shown outside the plot or as explicit missing markers; NA must not be plotted as zero.

Source:

- `results/paper_assets/table_two_channel_leakage.csv`

Required annotations:

- DLPFC: both channels.
- Andersson and Thrane: patient-dominant.
- Visium breast: spatial-only because one patient.
- Spatial kNN near-zero denominators excluded.

### Figure 4. Spatial Exclusion and Distance Curves

Purpose: show that non-zero buffers matter.

Panels:

- DLPFC matched-hop curve.
- Visium breast matched-hop curve.
- GSE278936 prostate random/hop0/hop2/hop5 PCA+Ridge pilot.

Source:

- `results/paper_assets/figure_distance_curve_data.csv`
- `results/paper_assets/table_gse278936_spatial_pilot_RLI.csv`
- `results/gse278936_prostate_spatial_pilot/spatial_pilot_aggregate.csv`

Headline: spatial partitioning without an exclusion buffer may leave local dependence intact. In GSE278936, random and hop0 are nearly identical, while hop2 and hop5 decline.

### Figure 5. Model Sensitivity and Leaderboard Instability

Purpose: show that model advantage depends on the evaluation regime.

Panels:

- PCA+Ridge versus GraphSAGE under random and strict evaluation in DLPFC, Andersson, Thrane, and Visium breast where available.
- Small panel for strong simple baseline versus graph model strict retention.

Source:

- `results/paper_assets/table_graphsage_shared_panel50_RLI.csv`
- `results/paper_assets/table_shared_panel50_RLI.csv`
- `results/paper_assets/table_two_channel_leakage.csv`

Wording rule: do not say complex models fail. Say apparent model advantage is evaluation-regime dependent.

### Figure 6. Evidence Hierarchy and External Stress Tests

Purpose: convert results into a methodological recommendation.

Panels:

- Evidence hierarchy schematic.
- Dataset-held-out / cross-platform stress test: Andersson to Visium PCA+Ridge mean Pearson 0.199.
- Minimum reporting set for future spatial-omics prediction papers.

Source:

- `results/paper_assets/table_dataset_heldout_anderson_to_visium.csv`
- `docs/reports/EVIDENCE_HIERARCHY.md`

If space is limited, move the cross-platform stress test to Supplementary Figure 7 and keep Figure 6 as the evaluation hierarchy.

## Existing Figure Mapping

| Existing asset | Keep / revise | Final destination |
|---|---|---|
| `fig1_leakage_overview` | Revise | Split into final Fig. 2 and Fig. 3 |
| `fig2_spatial_distance_curves` | Revise | Final Fig. 4, adding GSE278936 |
| `fig3_model_and_transfer` | Revise | Final Fig. 5 and Fig. 6 |

## Immediate No-Redraw Decision

No figure should be redrawn until the manuscript Results order is accepted. The next figure task should be a source-data audit and layout sketch, not a new plot run.

