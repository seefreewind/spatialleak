# Supplementary Information

# SpatialLeak: evaluation design reshapes apparent generalization in spatial omics prediction

## Supplementary Methods

SpatialLeak used public DLPFC, Andersson HER2-positive breast cancer, Thrane melanoma, 10x Visium breast cancer and GSE278936 prostate Visium data. Restricted EGA data from the prostate study were not used. All datasets were normalized with library-size scaling to 10,000 counts per spot followed by log1p transformation. Up to 2000 highly variable predictor genes were used after excluding target genes.

Random splits used 80/10/10 train/validation/test proportions. Matched spatial splits used 3 x 3 within-slide grid blocks and 300 candidate assignments per seed. Hop buffers were defined on a within-slide spatial kNN graph with k = 15. Patient-held-out splits separated all sections from the held-out patient or donor, with validation sections chosen from training patients.

PCA+Ridge used 64 PCs and Ridge alpha 1.0, with PCA fitted on training observations only. Spatial kNN used k = 15 training neighbors and inverse-distance weighting in normalized per-slide coordinates. GraphSAGE used train-only PCA and scaling, two layers, hidden dimension 128, graph k = 10 with self-loops, Adam learning rate 1e-3, weight decay 1e-4, 500 maximum epochs and validation-loss early stopping with patience 60.

## Robustness to Target-Panel Definition

Shared-panel analyses used `shared_panel_50`, a frozen target set independent of downstream performance. These analyses support the patient-associated channel in Andersson and Thrane and provide a non-performance-selected comparison across datasets.

## Sample-Size-Matched Controls

Random-size-matched controls downsampled random splits to comparable sample sizes without using strict-split performance. These controls showed that the main spatial-buffer losses were larger than losses caused by sample-count reduction alone.

## Full Statistical Outputs

Main baseline analyses used seeds 0-9; GSE278936 used seeds 0-4. RLI was not interpreted when absolute random mean Pearson was below 0.05. Paired Wilcoxon tests used seed-level summaries with BH-FDR correction. Mixed-effects analyses used `inflation ~ moran_i + C(model)` with dataset random intercepts.

## Cross-Platform Stress Test

The Andersson-to-Visium PCA+Ridge dataset-held-out stress test had mean Pearson 0.199. This is reported as a supplementary stress test rather than central validation.

## Supplementary Fig. 1. Evaluation-regime-dependent model behavior

Model performance changed with the evaluation tier. The source data are provided in `source_data/Supplementary_Figure1_SourceData.csv`.

## Boundary Conditions

Spatial kNN RLI was not interpreted when random performance was near zero. Thrane high-hop spatial buffers were limited by ST v1.0 density. Visium breast was single-patient and therefore supports spatial and section-level evidence, not patient-level validation. GSE278936 public data contain one section per patient and were used only for spatial-channel replication.
