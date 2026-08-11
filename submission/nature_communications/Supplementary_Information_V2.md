# Supplementary Information

# SpatialLeak: evaluation design reshapes apparent generalization in spatial omics prediction

## Supplementary Methods

### Dataset Details

The study used public DLPFC, Andersson HER2-positive breast cancer, Thrane melanoma, 10x Visium breast cancer and GSE278936 prostate Visium data. GSE278936 was used only as a spatial-channel external replication dataset. Restricted EGA data from the prostate study were not used.

### Preprocessing and Target Panels

All datasets were normalized with library-size scaling to 10,000 counts per spot followed by log1p transformation. Up to 2000 highly variable predictor genes were used after excluding target genes. Dataset-specific targets were the top 50 Moran-ranked genes. The `shared_panel_50` analyses used a frozen target set independent of downstream performance.

### Model Settings

PCA+Ridge used 64 PCs and Ridge alpha 1.0, with PCA fitted on training observations only. Spatial kNN used k = 15 training neighbors and inverse-distance weighting in normalized per-slide coordinates. GraphSAGE used train-only PCA and scaling, two layers, hidden dimension 128, within-slide kNN graph k = 10 with self-loops, Adam learning rate 1e-3, weight decay 1e-4, 500 maximum epochs and validation-loss early stopping with patience 60.

### Split Definitions

Random splits used 80/10/10 train/validation/test proportions. Matched spatial splits used 3 x 3 within-slide grid blocks and 300 candidate assignments per seed. Hop buffers were defined on a within-slide spatial kNN graph with k = 15. Patient-held-out splits separated all sections from the held-out patient or donor, with validation sections chosen from training patients.

### Statistical Analyses

Main baseline analyses used seeds 0-9; GSE278936 used seeds 0-4. RLI was defined as `(Perf_random - Perf_strict) / Perf_random` and was not interpreted when absolute random mean Pearson was below 0.05. Paired Wilcoxon tests used seed-level summaries with BH-FDR correction. Mixed-effects analyses used `inflation ~ moran_i + C(model)` with dataset random intercepts. Slide-level bootstrap used 1000 replicates where available.

## Supplementary Tables

- Supplementary Table 1. Dataset roles and sample structures.
- Supplementary Table 2. Split definitions and sample-size retention.
- Supplementary Table 3. Model and hyperparameter settings.
- Supplementary Table 4. Full seed/fold result summaries.
- Supplementary Table 5. Sample-size matched control.
- Supplementary Table 6. Shared-panel robustness results.
- Supplementary Table 7. Mixed-effects output.
- Supplementary Table 8. Cross-platform stress test.

## Robustness to Target-Panel Definition

Shared-panel analyses supported the patient-associated channel in Andersson and Thrane and provided a non-performance-selected comparison across datasets. These analyses do not replace dataset-specific panels, but they show that the central patient-channel result is not driven solely by dataset-specific Moran target selection.

## Boundary Conditions

Spatial kNN RLI was not interpreted when random performance was near zero. Thrane high-hop spatial buffers were limited by ST v1.0 density. Visium breast was single-patient and therefore supports spatial and section-level evidence, not patient-level validation. GSE278936 public data contain one section per patient and were used only for spatial-channel replication.

## Supplementary Numerical Anchors

- Visium breast Spatial kNN hop5 RLI: 0.796.
- Andersson GraphSAGE patient RLI with training-only preprocessing: 0.695.
- Thrane GraphSAGE patient RLI with training-only preprocessing: 0.711.
- GSE278936 PCA+Ridge hop5 RLI: 0.222.
- Andersson-to-Visium PCA dataset-held-out mean Pearson: 0.199.
