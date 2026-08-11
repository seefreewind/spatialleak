# Methods Completeness Audit

## Preprocessing

| Item | Status | Evidence / manuscript need |
|---|---|---|
| raw/processed input source | Present | Scripts and Data Availability identify DLPFC, Andersson, Thrane, 10x Visium breast, and GSE278936. |
| normalization | Present | `normalize_total(target_sum=1e4)` per section/sample followed by `log1p`. |
| HVG selection | Present | `scanpy.pp.highly_variable_genes(..., flavor='seurat', n_top_genes=2000)`. |
| predictor genes | Present | Up to 2000 HVGs after target exclusion. |
| target exclusion | Present | `feature_genes = [g for g in adata.var_names if g not in target_genes][:n_features]`. |
| missing genes | Present | Outer joins followed by `nan_to_num`; GSE target usability recorded. |
| coordinate normalization | Present | Per-slide z-scoring for model coordinates; raw array coordinates for Moran and split geometry. |
| multiple sections | Present | Section/slide columns are retained; kNN graph and coordinate scaling are within-slide. |
| patient metadata | Present with boundary | Public metadata resolved; GSE278936 has one section per patient in public data. |

## PCA+Ridge Pipeline Leakage Audit

**PASS.** PCA is fit only on `X_train` in `src/models/pca_ridge.py`, and Ridge models are fit on train PCA scores and train labels. No full-data scaler is used in PCA+Ridge.

## Spatial kNN Audit

**PASS.** Spatial kNN uses only training coordinates and training target values to predict test spots. It uses inverse-distance weighting with `k=15` by default and does not use test labels or test-test targets.

## GraphSAGE Audit

**Issue found and resolved.** Phase 19 found that the previous GraphSAGE implementation performed PCA on train data but standardized PCA features using all nodes. This was a potential test-feature-informed transformer. `src/models/graphsage.py` was patched so PCA feature mean and standard deviation are estimated from train nodes only. Corrected train-only GraphSAGE reruns were completed for Andersson, Thrane, and Visium breast. DLPFC corrected GraphSAGE was partially attempted but not promoted to V4 evidence because the full 10-seed rerun was not completed.

## Split-Method Audit

| Split | Unit | Validation | Isolation meaning |
|---|---|---|---|
| random | spot | random 10% | permissive interpolation; no spatial, section, or patient isolation |
| matched_hop0 | spatial block | matched validation blocks | non-overlapping block assignment without positive exclusion buffer |
| matched_hop2 | spatial block plus hop buffer | matched validation blocks | test spots within fewer than 2 graph hops from train are dropped |
| matched_hop5 | spatial block plus hop buffer | matched validation blocks | test spots within fewer than 5 graph hops from train are dropped |
| slide-held-out | slide/section | separate validation slide where available | section transfer, not patient-level unless patient is also separated |
| patient-held-out | patient/donor via all slides | validation slide from remaining patients | patient-associated structure; may include batch/sample effects |
| dataset-held-out | dataset | no within-test tuning | cross-dataset/platform stress test |

Empty test splits were skipped and documented. Seed-invariant folds were replicated for paired summaries only when required by downstream statistics.

## Statistical Methods Audit

Mean Pearson correlation across target genes is the primary metric. Per-gene Pearson is calculated from test observed and predicted expression values; constant predictions return Pearson 0 by convention. LI is `Perf_random - Perf_strict`, RLI is `(Perf_random - Perf_strict) / Perf_random`, and retention is `Perf_strict / Perf_random`. RLI is operational and not a causal fraction of leakage. The reporting denominator floor is `abs(random mean Pearson) >= 0.05`; otherwise RLI is not interpreted. Bootstrap resampling is at slide level, not spot level. Paired Wilcoxon tests use seed-level or replicated seed/fold summaries with BH-FDR within comparison families. Mixed-effects models used `inflation ~ moran_i + C(model)` with dataset random intercepts, separately for patient and spatial channels.
