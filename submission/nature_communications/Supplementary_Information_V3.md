# Supplementary Information

# SpatialLeak: evaluation design reshapes apparent generalization in spatial omics prediction

## Supplementary Methods

SpatialLeak used public DLPFC, Andersson HER2-positive breast cancer, Thrane melanoma, two public 10x Visium breast cancer sections and GSE278936 prostate Visium data. Restricted EGA data from the prostate study were not used. All datasets were normalized with library-size scaling to 10,000 counts per spot followed by log1p transformation. After target panels had been fixed, up to 2,000 highly variable predictor genes were selected once during dataset preprocessing after excluding target genes and then frozen before split-specific model fitting, with 2,000 predictors used whenever available. HVG selection was treated as a fixed, unsupervised dataset-level feature-definition step and did not use downstream model performance, labels or evaluation-tier outcomes.

Random splits used 80/10/10 train/validation/test proportions. Matched spatial splits used 3 x 3 within-slide grid blocks and 300 candidate assignments per seed. Block-only splits correspond to hop0; +2-hop and +5-hop buffers correspond to hop2 and hop5 exclusion on a within-slide spatial kNN graph with k = 15. Patient/donor-held-out splits separated all sections from the held-out patient or donor, with validation sections chosen from training subjects. Section-held-out splits held out sections but were not treated as patient/donor-held-out unless subject identity was also separated.

The Andersson-to-Visium dataset-held-out/cross-platform stress test trained PCA+Ridge on Andersson and evaluated on 10x Visium breast using 49 of the 50 shared-panel targets because SEPT4 was absent from the cross-dataset target-gene intersection, together with 2,000 common predictor features. PCA and Ridge parameters were fitted on the training dataset only and applied to the held-out Visium dataset without refitting; spatial kNN was excluded because spatial coordinates are not comparable across platforms.

PCA+Ridge used up to 2,000 predictor genes, with 2,000 used whenever available, 64 PCs and Ridge alpha 1.0, with PCA fitted on training observations only. Spatial kNN used k = 15 training neighbors and inverse-distance weighting in normalized per-slide coordinates. GraphSAGE used train-only PCA and scaling, two layers, hidden dimension 128 in all reported analyses, graph k = 10 with self-loops, ReLU activation, no dropout, mean-squared-error loss on training nodes, Adam learning rate 1e-3, weight decay 1e-4, 500 maximum epochs and validation-loss early stopping with patience 60. The split-construction kNN graph (k = 15) was distinct from the GraphSAGE message-passing graph (k = 10).

## Dataset and Sample Structure

Dataset provenance, sample counts and split eligibility are documented in `DATA_MANIFEST.md`, `results/paper_assets/table_split_sample_sizes.csv` and `data/external_audit/gse278936/public_sample_audit.csv`. The public GSE278936 GEO release contains one section per patient and was used only as a spatial-channel Visium replication, not as patient-level validation.

## Split Sample Counts and Non-Resolvable Cases

Split-level train, validation and test counts are reported in `results/paper_assets/table_split_sample_sizes.csv`. Non-resolvable comparisons were retained as unavailable rather than converted to zero. RLI was not interpreted when the absolute random-split mean Pearson correlation was below 0.05; affected rows are listed in `results/final_stats/LI_RLI_all_datasets.csv` and the figure source data.

## Software Versions

The reproducibility environment used Python 3.10/3.12-compatible code. The locked environment files specify NumPy 1.26.4, pandas 2.3.3, SciPy 1.13.1, scikit-learn 1.6.1, Scanpy 1.10.3, AnnData 0.10.9, statsmodels 0.14.6 and PyTorch 2.8.0. PyTorch Geometric was not required for the in-repository GraphSAGE implementation, which uses native PyTorch tensor operations.

## Robustness to Target-Panel Definition

Shared-panel analyses used `shared_panel_50`, a frozen target set independent of downstream performance. These analyses support the patient-associated channel in Andersson and Thrane and provide a non-performance-selected comparison across datasets.

The shared-panel robustness source files are `results/paper_assets/table_shared_panel50_RLI.csv`, `results/paper_assets/table_graphsage_shared_panel50_RLI_trainonly.csv`, `results/anderson_shared_panel50/` and `results/thrane_shared_panel50/`.

## Sample-Size-Matched Controls

Random-size-matched controls downsampled random splits to comparable sample sizes without using strict-split performance. These controls showed that the main spatial-buffer losses were larger than losses caused by sample-count reduction alone.

The source files are `results/sample_size_control/random_size_matched_per_seed.csv` and `results/paper_assets/table_random_size_matched_control.csv`.

## Full Per-Seed and Per-Fold Outputs

Per-seed and per-fold model outputs are retained in the frozen `results/` subdirectories used by the manuscript scripts. Figure-level aggregates are mirrored in `submission/nature_communications/source_data/`, with Figure 2 and Figure 4 explicitly recording the error-bar unit and n for each value.

## Full Statistical Outputs

Main baseline analyses used seeds 0-9; GSE278936 used seeds 0-4. RLI was not interpreted when absolute random mean Pearson was below 0.05. Paired Wilcoxon tests used seed-level summaries with BH-FDR correction. Mixed-effects analyses used `inflation ~ moran_i + C(model)` with dataset random intercepts.

The principal statistical source files are `results/final_stats/LI_RLI_all_datasets.csv`, `results/final_stats/mixed_effects.json`, `results/final_stats/per_gene_inflation_spatial.csv` and `results/final_stats/per_gene_inflation_patient.csv`.

## Moran Analysis

Moran-ranked target genes were used to define frozen target panels and to assess the relationship between spatial autocorrelation and inflation. The Moran analysis source files include `data/processed/*moran*.csv`, `results/final_stats/per_gene_inflation_spatial.csv`, `results/final_stats/per_gene_inflation_patient.csv` and `results/paper_assets/moran_top_genes.csv` where available.

## Cross-Platform Stress Test

The Andersson-to-Visium PCA+Ridge dataset-held-out stress test had mean Pearson 0.199. This is reported as a supplementary stress test rather than central validation.

The source file is `results/paper_assets/table_dataset_heldout_anderson_to_visium.csv`.

## Supplementary Fig. 1. Evaluation-regime-dependent model behavior

Model performance changed with the evaluation tier. The source data are provided in `source_data/SupplementaryFigure1_SourceData.csv`.

## Boundary Conditions

Spatial kNN RLI was not interpreted when random performance was near zero. Thrane high-hop spatial buffers were limited by ST v1.0 density. Visium breast was single-patient and contained two sections in the frozen split manifest; it therefore supports dense Visium spatial and section-level evidence, not patient-level validation. GSE278936 public data contain one section per patient and were used only for spatial-channel replication.
