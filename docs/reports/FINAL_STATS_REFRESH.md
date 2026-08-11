# Final Statistics Refresh

> Updated: 2026-08-09 20:25  
> Scope: DLPFC formal, Andersson/Thrane external formal, Visium breast V0.1, and shared downstream statistical files under `results/final_stats/`.

## 1. Inputs

| Dataset | Result source | Strict split used in final statistics | Note |
|---------|---------------|----------------------------------------|------|
| DLPFC | `results/formal_dlpfc/formal_aggregate.csv` | patient-held-out; matched_hop0 | 10 seeds; donor folds replicated across seeds only for paired tests |
| Andersson | `results/anderson_formal_external/formal_external_aggregate.csv` | patient-held-out; matched_hop5 | 10 seeds; ST v1.0; patient/batch channel dominates |
| Thrane | `results/thrane_formal_external/formal_external_aggregate.csv` | patient-held-out; matched_hop2 | 10 seeds; matched_hop5 and region high-hop are not resolvable |
| Visium breast | `results/visium_breast_v01/v01_aggregate.csv` | slide-held-out; matched_hop5 | Single patient; slide-held-out is not patient-level external validation |

## 2. Main RLI Results

| Dataset | Model | Strict type | Random | Strict | RLI | Retention |
|---------|-------|-------------|--------|--------|-----|-----------|
| DLPFC | PCA+Ridge | patient | 0.292 | 0.230 | 0.213 | 0.787 |
| DLPFC | Spatial kNN | patient | 0.297 | 0.261 | 0.120 | 0.880 |
| Andersson | PCA+Ridge | patient | 0.604 | 0.204 | 0.662 | 0.338 |
| Andersson | Spatial kNN | patient | 0.035 | -0.009 | 1.273 | -0.273 |
| Thrane | PCA+Ridge | patient | 0.653 | 0.327 | 0.499 | 0.501 |
| Thrane | Spatial kNN | patient | 0.003 | 0.015 | not interpretable | not interpretable |
| Visium breast | PCA+Ridge | spatial hop5 | 0.597 | 0.442 | 0.259 | 0.741 |
| Visium breast | Spatial kNN | spatial hop5 | 0.649 | 0.132 | 0.796 | 0.204 |
| Visium breast | PCA+Ridge | slide-held-out | 0.597 | 0.580 | 0.029 | 0.971 |
| Visium breast | Spatial kNN | slide-held-out | 0.649 | 0.552 | 0.148 | 0.852 |

## 3. Paired Tests

Wilcoxon signed-rank tests used seed as the pairing unit. Seed-invariant patient/slide folds were replicated across seed only for paired comparison bookkeeping.

Significant BH-FDR results:

- DLPFC: random > patient and random > matched_hop0 for PCA+Ridge and Spatial kNN.
- Andersson: random > patient for PCA+Ridge and Spatial kNN; random > matched_hop5 for PCA+Ridge.
- Thrane: random > patient for PCA+Ridge; spatial-buffer tests are not significant.
- Visium breast: random > matched_hop5 for PCA+Ridge and Spatial kNN; random > slide-held-out is statistically detectable but biologically small compared with spatial-buffer loss.

## 4. Mixed Effects

Two mixed-effects models were fit to avoid conflating patient/batch shortcuts with spatial-neighborhood leakage.

| Model | Datasets | Formula | Moran coefficient | P value | Interpretation |
|-------|----------|---------|-------------------|---------|----------------|
| Patient-channel inflation | DLPFC, Andersson, Thrane | `inflation ~ moran_i + C(model) + (1|dataset)` | 0.007 | 0.932 | Patient/batch leakage is not explained by per-gene spatial autocorrelation in this stratified model. |
| Spatial-buffer inflation | DLPFC, Andersson, Thrane, Visium breast | `inflation ~ moran_i + C(model) + (1|dataset)` | 0.167 | 0.079 | Direction is positive, but the four-dataset model is borderline; Spatial kNN has significantly larger spatial inflation than PCA+Ridge. |

This refresh should not be read as a contradiction of the earlier GO-D result. The earlier model pooled leakage modes and found a strong Moran-associated direction. The refreshed analysis separates patient/batch leakage from within-section spatial leakage; after separation, Moran signal primarily tracks the spatial-buffer channel, while patient-held-out loss is dominated by dataset identity and batch/patient structure.

## 5. Boundary Conditions

- Spatial kNN RLI is not interpretable when the random denominator is near zero, especially in Thrane and parts of Andersson.
- Thrane high-hop curves are not resolvable on ST v1.0 density: matched_hop5 and region_hop5/10 have empty test sets.
- Visium breast has one patient. Slide-held-out performance should be reported as a cross-section/platform contrast, not as patient-level validation.
- Mixed-effects random intercept estimates remain weak with 3-4 datasets and should be presented as supportive, not definitive.

## 6. Outputs

- `results/final_stats/summary_all_datasets.csv`
- `results/final_stats/LI_RLI_all_datasets.csv`
- `results/final_stats/wilcoxon_all_datasets.csv`
- `results/final_stats/per_gene_inflation_patient.csv`
- `results/final_stats/per_gene_inflation_spatial.csv`
- `results/final_stats/mixed_effects.json`
