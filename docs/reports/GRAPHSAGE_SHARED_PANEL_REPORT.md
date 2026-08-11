# GraphSAGE Shared-Panel Integration

> Updated: 2026-08-09 21:55  
> Scope: DLPFC and Andersson GraphSAGE on the frozen `shared_panel_50` target panel.

## 1. Runs

| Dataset | Output | Seeds | Splits |
|---------|--------|-------|--------|
| DLPFC | `results/formal_dlpfc/formal_aggregate_graphsage_shared_panel50.csv` | 0-9 | random, matched_hop0 |
| Andersson | `results/anderson_graphsage_shared_panel50/shared_panel50_graphsage_aggregate.csv` | 0-4 | random, matched_hop0; patient folds once |

The DLPFC run used CPU-only GraphSAGE and took approximately 41 minutes after reusing the seed0 smoke result. The Andersson run took approximately 22 minutes.

## 2. Results

| Dataset | Split | Mean Pearson | Seeds/folds |
|---------|-------|--------------|-------------|
| DLPFC | random | 0.151 | 10 seeds |
| DLPFC | matched_hop0 | 0.094 | 10 seeds |
| Andersson | random | 0.251 | 5 seeds |
| Andersson | matched_hop0 | 0.233 | 5 seeds |
| Andersson | patient-held-out | 0.077 | 8 folds |

Derived leakage metrics:

| Dataset | Strict comparison | RLI | Retention |
|---------|-------------------|-----|-----------|
| DLPFC | matched_hop0 | 0.378 | 0.622 |
| Andersson | matched_hop0 | 0.072 | 0.928 |
| Andersson | patient-held-out | 0.692 | 0.308 |

## 3. Interpretation

The shared-panel GraphSAGE results support the two-channel leakage interpretation:

- DLPFC shows a substantial within-section spatial-buffer loss under `matched_hop0`, consistent with local spatial-neighborhood information sharing.
- Andersson shows only a small `matched_hop0` loss but a large patient-held-out loss, matching the patient/batch shortcut channel seen with PCA+Ridge.
- GraphSAGE does not rescue cross-patient generalization in Andersson; its patient RLI is 0.692, close to the PCA+Ridge shared-panel patient RLI of 0.632.

## 4. Boundary Conditions

- DLPFC shared-panel GraphSAGE patient folds were not run in this pass because the CPU-only cost is high and the current priority was random-vs-spatial loss. Existing dataset-specific DLPFC GraphSAGE patient results remain available in `formal_aggregate_graphsage.csv`.
- Thrane and Visium GraphSAGE were not run yet. Thrane spatial kNN denominators are near zero and high-hop curves are not resolvable; Visium would be useful for spatial-neighborhood leakage but is not patient-level validation.
- Patient folds are seed-invariant for Andersson and were run once, consistent with the external baseline convention.
