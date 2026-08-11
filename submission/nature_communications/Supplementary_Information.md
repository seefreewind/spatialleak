# Supplementary Information

## Supplementary Methods

### Dataset construction and QC

The analysis used public spatial transcriptomics datasets from DLPFC, HER2-positive breast cancer, melanoma, 10x Visium breast cancer and GSE278936 prostate Visium. Dataset-level metadata, patient/section structure and public accessions are reported in Supplementary Table 1. Restricted EGA validation data associated with the prostate study were not used.

### Split implementation

Random spot splits, matched spatial block splits, hop-buffer filtering, slide-held-out splits, patient-held-out splits and dataset-held-out stress tests are documented with split units, retained sample counts and non-resolvable cases. NA values indicate that a tier was unavailable or not interpretable; NA is never treated as zero.

### Target-panel definition and robustness

Dataset-specific panels used Moran-ranked genes to define the prediction task. The `shared_panel_50` target set was frozen independently of downstream prediction performance. Shared-panel analyses support the patient-associated findings but do not remove all target-definition limitations.

### Model specifications

Mean, PCA+Ridge, Spatial kNN and GraphSAGE settings are listed in Supplementary Table 3. PCA+Ridge fits PCA only on training predictors. GraphSAGE uses train-only PCA and train-only feature scaling after the Phase 19 audit.

### Statistical analysis

Supplementary methods report LI, RLI, retention, the near-zero denominator rule, slide-level bootstrap, paired Wilcoxon tests with BH-FDR correction and mixed-effects models.

## Supplementary Notes

1. Dataset QC and sample structure.
2. Split implementation and retained sample counts.
3. Robustness to target-panel definition.
4. Random-size-matched controls.
5. Corrected train-only GraphSAGE details.
6. Mixed-effects model details.
7. Boundary conditions and non-resolvable splits.
8. Cross-platform stress test.
9. Full numerical results.

## Supplementary Figures

1. Dataset QC and sample structure.
2. Full buffer curves.
3. Random-size-matched controls.
4. Corrected train-only GraphSAGE results.
5. Moran analyses.
6. Boundary conditions and non-resolvable splits.
7. Cross-platform stress test.

## Supplementary Tables

1. Dataset accessions and sample counts.
2. Target panels.
3. Model hyperparameters.
4. Split sample counts.
5. Full metric summaries.
6. Full seed and fold summaries.
7. Statistical outputs.
8. Software versions.
