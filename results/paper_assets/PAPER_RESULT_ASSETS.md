# Paper Result Assets

> Generated: 2026-08-09 22:15

## Primary Tables

- `table_dataset_specific_RLI.csv`: dataset-specific target results across strict splits.
- `table_shared_panel50_RLI.csv`: unified target-panel results for DLPFC, Andersson, and Thrane.
- `table_graphsage_shared_panel50_RLI.csv`: GraphSAGE shared-panel results.
- `table_two_channel_leakage.csv`: Phase 16 synthesis table separating spatial-neighborhood and patient/batch leakage channels.
- `table_dataset_heldout_anderson_to_visium.csv`: cross-platform dataset-held-out stress test.
- `figure_distance_curve_data.csv`: source data for hop/region distance curves.

## Suggested Figure Panels

1. Main leakage summary: PCA+Ridge RLI across DLPFC, Andersson, Thrane, and Visium breast.
2. Spatial-neighborhood channel: kNN/GraphSAGE random vs matched_hop buffers, emphasizing Visium and DLPFC.
3. Patient/batch shortcut channel: shared-panel patient retention for DLPFC vs Andersson/Thrane.
4. Platform contrast: Visium breast random/matched/slide-held-out; Thrane high-hop non-resolvability annotated.
5. Supplement: Andersson→Visium dataset-held-out stress test.

## High-Signal Numbers

- Dataset-specific PCA patient RLI: DLPFC 0.213, Andersson 0.662, Thrane 0.499.
- Visium kNN matched_hop5 RLI: 0.796.
- Shared-panel PCA patient RLI: DLPFC 0.251, Andersson 0.632, Thrane 0.644.
- GraphSAGE shared-panel RLI: DLPFC matched_hop0 0.378; Andersson patient 0.692.
- Andersson→Visium PCA dataset-held-out mean Pearson: 0.199.

## Cautions

- Spatial kNN RLI is not interpreted when random performance is near zero.
- Visium breast slide-held-out is a cross-section contrast, not patient-level external validation.
- Dataset-held-out transfer is a stress test; it should be supplementary unless strengthened with additional external datasets.
