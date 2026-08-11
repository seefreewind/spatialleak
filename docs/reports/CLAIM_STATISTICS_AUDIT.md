# Claim Statistics Audit

Date: 2026-08-10

## Audit Rule

No main claim should treat spots as independent biological replicates. Main evidence should be reported at the dataset, patient, section, seed, or fold level. RLI is not interpreted when random-split performance is near zero.

## Main Claim Audit

| Claim | Dataset(s) | Model(s) | Metric / effect size | Statistical support | Independent unit | Evidence level | Main / Supp | Wording strength |
|---|---|---|---|---|---|---:|---|---|
| Random spot-level splits inflate apparent predictive generalization | DLPFC, Andersson, Thrane, Visium breast | PCA+Ridge, Spatial kNN where interpretable | Dataset-specific PCA patient RLI: DLPFC 0.213, Andersson 0.662, Thrane 0.499; Visium breast Spatial kNN hop5 RLI 0.796 | Wilcoxon+BH-FDR significant for DLPFC/Andersson patient and Visium hop5; Thrane PCA patient significant | seed/fold, patient/donor, section | 1-3 | Main | "show" / "support" |
| Spatial-buffer splits reveal within-section spatial-neighborhood leakage | DLPFC, Visium breast, GSE278936 prostate | Spatial kNN, PCA+Ridge, GraphSAGE | DLPFC Spatial kNN spatial RLI 0.402; Visium breast Spatial kNN RLI 0.796; GSE278936 PCA+Ridge hop5 RLI 0.222 | Spatial-channel mixed model Moran coefficient positive but borderline; Spatial kNN model effect p=0.0058; GSE pilot 5 seeds descriptive | seed, section, dataset | 1 | Main | "reveal" / "are consistent with" |
| Non-zero spatial exclusion buffers can be necessary | GSE278936 prostate; supported by DLPFC/Visium curves | PCA+Ridge primarily; Spatial kNN not interpretable in GSE278936 | GSE278936 PCA+Ridge random 0.374473, hop0 0.374584, hop2 0.294437, hop5 0.291516 | 5-seed pilot; no p-value required for headline because effect is descriptive and stable | seed | 1 | Main or prominent Supplement | "indicate" / "can be necessary" |
| Patient-held-out evaluation uncovers a distinct shortcut channel | Andersson, Thrane, DLPFC | PCA+Ridge, GraphSAGE | Andersson PCA patient RLI 0.662; Thrane PCA patient RLI 0.499; Andersson GraphSAGE patient RLI 0.692; Thrane GraphSAGE patient RLI 0.718 | Patient-channel mixed model Moran p=0.932; patient losses significant where tested | patient/fold, seed bookkeeping | 3 | Main | "uncovers" / "identifies" |
| Dominant leakage channel varies across datasets and model classes | DLPFC, Andersson, Thrane, Visium breast, GSE278936 | PCA+Ridge, Spatial kNN, GraphSAGE | Two-channel matrix: DLPFC both channels; Andersson/Thrane patient-dominant; Visium breast spatial-dominant; GSE278936 moderate PCA spatial, kNN boundary | Descriptive synthesis from frozen two-channel table | dataset-model combination | 1-3 | Main | "varies" / "is heterogeneous" |
| Leakage-resistant evaluation reshapes apparent model advantage | DLPFC, Andersson, Thrane, Visium breast | PCA+Ridge, GraphSAGE | DLPFC GraphSAGE spatial RLI 0.378; Andersson GraphSAGE patient RLI 0.692; Thrane GraphSAGE patient RLI 0.718; Visium breast GraphSAGE spatial RLI 0.262 | Descriptive comparison; DLPFC original formal GraphSAGE advantage shrinkage Wilcoxon p=0.002 from prior status | seed/fold | 1-3 | Main | "depends on evaluation regime" |
| Spatial dependence is not intrinsically leakage | DLPFC, Visium breast, dataset-held-out stress test | PCA+Ridge, Spatial kNN | DLPFC patient retention for Spatial kNN 0.880; Visium slide-held-out kNN retention 0.852; Andersson-to-Visium PCA mean Pearson 0.199 | Conceptual interpretation; not a single formal test | patient/section/dataset | 2-5 | Discussion | "may represent transportable biological structure" |

## Pseudoreplication Check

- Do not calculate confidence intervals from individual spots as if they were independent biological replicates.
- Results should report seeds, folds, patients, sections, or datasets as the relevant unit.
- Patient folds that are seed-invariant can be replicated for paired bookkeeping but should be described transparently.

## Confidence Intervals

Current status:

- Formal DLPFC includes slide-level bootstrap procedures.
- Main paper assets mostly report mean Pearson and RLI point estimates.
- For final submission, uncertainty should be shown with seed/fold-level variation or bootstrap at section/patient level where available.

Recommendation:

- Main figures can show points and linked random-strict effects.
- Supplementary figures should show all seed/fold values.
- Avoid spot-level error bars.

## Multiple Testing

Current status:

- Wilcoxon signed-rank tests with Benjamini-Hochberg FDR correction are documented in `FINAL_STATS_REFRESH.md`.
- Per-gene analyses should use BH-FDR if promoted beyond exploratory supplement.

Recommendation:

- Do not make per-gene discovery claims in the main manuscript.
- Use per-gene results as supporting evidence for heterogeneity and robustness.

## Mixed-Effects Interpretation

Locked interpretation:

- The earlier pooled Moran analysis supported a directional relationship between Moran signal and pooled inflation.
- The refreshed stratified models showed patient-channel inflation was not explained by Moran (`p=0.932`), while the spatial-channel Moran trend was positive but borderline (`p=0.079`).

Manuscript wording:

- Correct: "Moran signal was most relevant to the spatial-buffer channel and did not explain patient-held-out loss in the stratified analysis."
- Incorrect: "Moran autocorrelation explains all leakage."

## Optional Pre-Submission Analyses

Only these are worth considering, and none is required before a complete draft:

1. Add seed/fold-level uncertainty panels to the supplement from existing outputs.
2. Generate a final two-channel scatter plot with NA values explicitly shown as missing.
3. Recompute final source-data tables after manuscript wording freezes, as a provenance check.

No new datasets, SOTA model zoo, GSE278936 GraphSAGE, or restricted-data analysis is recommended.

