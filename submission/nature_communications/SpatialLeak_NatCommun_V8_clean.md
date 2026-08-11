# Evaluation design reshapes apparent generalization in spatial omics prediction

Yu Zhang1, Ying Chen2, Yue Liu2, Da Lin1

1 Department of Ophthalmology, The Second Affiliated Hospital of Wenzhou Medical University, No. 109 Xueyuan West Road, Lucheng District, Wenzhou, Zhejiang Province, China

2 Wenzhou Medical University, Wenzhou, Zhejiang Province, China

Correspondence: Da Lin, 212574@wzhealth.com; ORCID 0009-0009-4410-0218

## Abstract

Spatial omics models are often evaluated using random spot-level splits, yet spatial neighborhoods, section context and patient-associated structure can make such performance difficult to interpret. We developed SpatialLeak, a leakage-resistant evaluation framework that compares random spot splits with buffered spatial, section-held-out, patient-held-out and dataset-held-out regimes. In dense Visium breast data, Spatial kNN showed strong spatial-neighborhood inflation, with hop5 relative leakage inflation (RLI) of 0.796. GraphSAGE evaluated with training-only preprocessing showed large patient-associated losses in Andersson and Thrane, with patient RLI values of 0.695 and 0.711. In GSE278936 prostate Visium, PCA+Ridge was unchanged at hop0 but decreased under non-zero spatial buffers, reaching hop5 RLI 0.222. Random-size-matched controls indicated that reduced sample count alone did not explain the main spatial-buffer losses. SpatialLeak provides a hierarchy for matching benchmark design to the level of generalization being claimed.

## Introduction

Spatial transcriptomics and related spatial omics assays connect molecular measurements to tissue architecture, creating prediction tasks that are not available in dissociated profiling alone [1]. These tasks include imputation of unmeasured genes, mapping between molecular and spatial modalities, graph-based learning from tissue neighborhoods and representation learning over spatial context [2,3,4]. Spatial graph and domain-learning methods further show how location, morphology and neighborhood structure can carry biologically meaningful information [5,6,7,8]. As these methods scale across tissues and cohorts, distinguishing these levels of generalization becomes increasingly important for interpreting model comparisons.

The evaluation problem is that spatial observations are not independent in the ordinary IID sense. A random spot-level split can place neighboring tissue locations, similar local cell compositions, the same section background or the same patient-associated structure on both sides of the train-test boundary. In machine-learning settings, such non-independent sampling and leakage between model development and evaluation can inflate apparent performance and reduce reproducibility [9,10,11,12]. Gene-expression analyses have long shown the related risk that feature selection and model evaluation must be separated to avoid biased estimates [13].

Spatial dependence is not inherently invalid. Spatial autocorrelation is a defining property of many tissue measurements and has a formal statistical history [14]. A spatially aware model may use tissue architecture as a legitimate biological signal if that signal is retained under the separation required by the scientific claim. The central question is what claim the evaluation design can support: local interpolation, spatial transfer, section transfer, patient transfer, dataset transfer or cross-platform transfer.

Current spatial omics benchmarks do not consistently separate these levels. Multiple spatial-learning studies use spot- or cell-level random splits or evaluation settings that can mix local interpolation with broader transfer claims [2,15,4]. Such choices can conflate local spatial-neighborhood dependence, patient-associated structure and transportable biological signal. This makes it difficult to interpret whether an apparent model advantage reflects a robust predictive principle or the evaluation tier used to measure it.

Here we introduce SpatialLeak, a multi-tier evaluation framework for spatial omics prediction. SpatialLeak compares random spot splits with buffered spatial, section-held-out, patient-held-out and dataset-held-out regimes across public spatial transcriptomics datasets and diagnostic model classes. The framework shows that apparent generalization can arise through distinct spatial-neighborhood and patient-associated channels, and it organizes these findings into a generalization evidence hierarchy.

## Results

### Random spot-level evaluation inflates apparent predictive generalization

SpatialLeak first tested whether random spot-level performance was retained when the train-test boundary matched a stricter generalization claim (Fig. 1, Fig. 2). Across DLPFC, Andersson, Thrane and Visium breast, random splits produced higher apparent performance than the relevant stricter split for the main interpretable model-dataset combinations. These comparisons position random spot evaluation as a permissive interpolation setting rather than, by itself, evidence of section-, patient- or dataset-level generalization.

The patient-channel datasets showed the clearest random-to-patient losses (Fig. 3). In Andersson, PCA+Ridge patient RLI was 0.662, and GraphSAGE evaluated with training-only preprocessing had patient RLI 0.695. In Thrane, PCA+Ridge patient RLI was 0.499, and GraphSAGE patient RLI was 0.711. These results show that a graph-based model did not remove the need for grouped evaluation.

### Non-zero spatial buffers reveal local neighborhood dependence

SpatialLeak next tested whether non-overlapping spatial partitions were sufficient to remove local neighborhood dependence (Fig. 4). They were not always sufficient. In DLPFC and Visium breast, increasing hop distance reduced performance, especially for Spatial kNN. Visium breast showed the strongest spatial-channel example, with Spatial kNN hop5 RLI 0.796.

GSE278936 provided an independent high-density Visium spatial-channel replication. PCA+Ridge was essentially unchanged at hop0 (RLI -0.000) but decreased under hop2 and hop5 buffers, reaching hop5 RLI 0.222. This pattern supports the specific claim that a non-zero exclusion buffer can be required to expose local neighborhood dependence. The random-size-matched control showed that the main spatial-buffer losses were larger than the losses caused by downsampling random splits to similar sample sizes.

### Patient-held-out evaluation identifies a distinct patient-associated channel

Patient-held-out evaluation measured a different axis of dependence from within-section spatial buffering (Fig. 3). Andersson and Thrane had large patient-held-out losses even when spatial kNN was near zero or when high-hop spatial curves were not resolvable in low-density ST v1.0 geometry. DLPFC showed a mixed pattern, with both spatial and donor-associated effects.

The patient-associated channel should not be interpreted as a causal batch-effect estimate. It can include patient identity, section background, tissue processing, sample handling, cohort structure and biological heterogeneity. The result is that random spot splits can use structure that is not retained when patient-associated groups are separated.

### Dominant generalization-inflation channels vary across datasets and model classes

Figure 3 summarizes the central heterogeneity result. DLPFC showed both spatial and donor-associated effects. Andersson and Thrane were patient-channel dominant. Visium breast was spatial-channel dominant but single-patient. GSE278936 replicated the spatial-channel PCA+Ridge buffer response and provided a kNN boundary condition because random kNN performance was below zero.

This two-channel landscape explains why one split or one model cannot diagnose all settings. Spatial kNN is useful as a local-neighborhood probe when it has signal. PCA+Ridge provides a strong non-graph baseline. GraphSAGE tests whether graph learning follows the same split-dependent behavior as simpler baselines.

### Apparent model advantage depends on evaluation regime

Model comparisons changed when the evaluation claim changed (Supplementary Fig. 1). Spatial kNN was strong in dense random or local settings but weak when spatial signal was absent or isolated. GraphSAGE retained random-split performance in some settings but showed strong patient-held-out losses in tumor datasets. PCA+Ridge often retained broader transfer signal better than a purely local spatial-neighbor baseline.

These observations argue against using a single random-split leaderboard as evidence of model superiority. A method can be useful for local interpolation while being less informative for patient transfer, and a model that appears robust under a spatial split may still lose performance under patient-held-out evaluation.

### SpatialLeak defines a hierarchy for spatial-omics generalization claims

SpatialLeak formalizes six evaluation tiers (Fig. 1). Level 0, random spot interpolation, supports local interpolation but does not establish spatial, section or patient transfer. Level 1, buffered spatial transfer, tests local neighborhood separation but does not establish patient transfer. Level 2, section-held-out transfer, tests transfer across sections but not necessarily across patients. Level 3, patient-held-out transfer, tests retention across patient-associated groups but does not establish dataset or platform transfer. Level 4, dataset-held-out transfer, tests broader dataset transportability. Level 5, cross-platform transfer, tests robustness when measurement platforms also change.

This hierarchy fixes the language of the manuscript. Visium breast supports dense Visium spatial and section-level evidence, not patient-level validation. GSE278936 supports spatial-channel replication, not clean patient-level validation. Andersson-to-Visium transfer remains a supplementary cross-platform stress test rather than a central validation claim.

## Discussion

SpatialLeak shows that apparent performance in spatial omics prediction can be inflated through separable spatial-neighborhood and patient-associated channels. Random spot-level evaluation overstated apparent predictive generalization in multiple settings, non-zero spatial buffers exposed local neighborhood dependence, patient-held-out tests revealed a distinct patient-associated channel, and the resulting evidence hierarchy clarified what each evaluation tier can claim.

The non-zero buffer result is important because non-overlapping spatial blocks do not necessarily create local independence. A test spot can remain close to a training neighborhood even when it is assigned to a different block. GSE278936 illustrates this point: hop0 was essentially unchanged, whereas hop2 and hop5 exposed a stable PCA+Ridge loss. This does not mean that every study requires hop5, but it does mean that spatial split definitions should report the exclusion distance they actually impose.

Spatial information itself is not leakage. Tissue architecture is often the object of spatial omics analysis, and a model should be allowed to use it when the intended claim is local interpolation or when the signal survives stricter separation. SpatialLeak is designed to determine whether spatial signal survives the evaluation tier implied by the biological claim, not to remove spatial context from spatial models.

Patient-associated performance loss is also not a single causal mechanism. A patient-held-out drop can reflect patient identity, section context, processing batch, sample handling, cohort structure, tissue biology or their combination. Public datasets do not always allow these components to be separated. The appropriate claim is therefore patient-associated performance inflation, not proof of a specific batch shortcut.

These findings suggest practical minimum expectations for future spatial omics benchmarks. Studies should report grouped splits, explicit spatial buffers, patient separation where the claim requires it, strong non-spatial baselines, spatial diagnostic baselines, uncertainty at the biological unit, transparent split metadata and code that reproduces the evaluation tier. Model rankings should be tied to the claim being tested rather than presented as universal.

The study has clear boundaries. The model set is diagnostic rather than exhaustive. Public datasets are heterogeneous in platform, tissue, density and sample structure. Visium breast is single-patient, GSE278936 public data contain one section per patient, DLPFC GraphSAGE was not used as main evidence, and cross-platform transfer remains supplementary. Strict-split loss can include legitimate distribution shift as well as leakage-sensitive dependence. These limitations define the scope of inference but do not alter the central need to align evaluation design with the generalization claim.

## Methods

### Datasets

SpatialLeak used public spatial transcriptomics datasets covering human dorsolateral prefrontal cortex (DLPFC), HER2-positive breast cancer, cutaneous malignant melanoma, 10x Visium breast cancer and GSE278936 prostate Visium data [16,17,18,19,20,21]. Restricted EGA validation data from the prostate study were not used. Dataset roles were defined by public sample structure: GSE278936 was used only as a spatial-channel replication dataset because the public release contains one section per patient.

### Preprocessing

Each section or sample was library-size normalized with `normalize_total(target_sum=1e4)` and transformed with `log1p`. Highly variable genes were selected with the Scanpy Seurat-flavor highly variable gene procedure using up to 2000 predictor genes. Slide or section identifiers and patient or donor metadata were retained where available. Spatial coordinates were standardized within slide for model input while preserving within-slide geometry for split construction.

### Target panels

Dataset-specific panels used the top 50 Moran-ranked genes after preprocessing. Moran ranking was computed on the processed dataset to define the prediction task, not to tune models or select results. Shared-panel analyses used the frozen `shared_panel_50` target set. Target selection was independent of downstream model performance and fixed across evaluation regimes.

### Split construction

Random spot splits used an 80/10/10 train/validation/test partition. Matched spatial block splits assigned 3 x 3 grid blocks within each section to train, validation or test folds and selected balanced assignments from 300 random candidates per seed using spot count, library size, Moran signal and layer composition where available. `matched_hop0` denotes non-overlapping block assignment without a positive exclusion buffer. Hop2 and hop5 splits removed test spots whose nearest training neighborhood was within fewer than two or five edges on a within-slide spatial kNN graph with k = 15. Patient-held-out splits held out all sections from a patient or donor where available. Validation sections were selected from training patients rather than the held-out test patient. Slide-held-out splits held out sections but were not treated as patient-held-out unless patient identity was also separated.

### Spatial graph construction

Spatial graphs were built within slides only. kNN edges were calculated from spatial coordinates, preventing cross-slide graph connections. GraphSAGE used within-slide graph neighborhoods as input features but never aggregated test labels [22].

### Models

PCA+Ridge used 2000 predictor genes excluding the 50 target genes. PCA used 64 components and was fit only on training observations. Ridge regression used alpha = 1.0 and was fit separately for each target gene. Spatial kNN used k = 15 nearest training spots in normalized per-slide coordinates and inverse-distance weights `1/(d + 1e-6)` normalized to sum to one for each test spot. Neighbors were drawn only from the training split; when fewer than 15 training spots were available, all available training spots were used. GraphSAGE used train-only PCA and train-only feature scaling, two GraphSAGE layers, hidden dimension 128 for formal external runs, within-slide graph k = 10 with self-loops, ReLU activation, Adam optimization with learning rate 1e-3, weight decay 1e-4, up to 500 epochs, validation-loss early stopping with patience 60, and validation-loss checkpoint selection. Test performance was not used for checkpoint selection.

### Metrics and inference

The primary metric was mean Pearson correlation across target genes. Leakage inflation was defined as `Perf_random - Perf_strict`. Relative leakage inflation (RLI) was defined as `(Perf_random - Perf_strict) / Perf_random`, and retention was defined as `Perf_strict / Perf_random`. RLI is an operational measure of evaluation-dependent performance inflation and is not interpreted as the fraction of performance causally attributable to leakage. RLI was not interpreted when absolute random mean Pearson was below 0.05. Main DLPFC, Andersson, Thrane and Visium breast baseline analyses used seeds 0-9; GSE278936 spatial-channel replication used seeds 0-4. Random-size-matched controls downsampled the random split to comparable sample sizes without using strict-split performance. Bootstrap summaries used slide-level resampling with 1000 bootstrap replicates where available. Wilcoxon signed-rank tests used paired seed summaries with Benjamini-Hochberg false-discovery-rate correction within comparison families. Mixed-effects analyses were run separately for patient and spatial channels with `inflation ~ moran_i + C(model)` and dataset random intercepts.

### Reproducibility

Seeds were frozen before final analyses. Test performance was not used for hyperparameter selection, checkpoint selection, target-panel selection or seed selection. Scripts for regenerating frozen paper assets and unit tests for core split and evaluation functions are provided with the accompanying code repository.

## Data Availability

DLPFC, Andersson, Thrane, 10x Visium breast and GSE278936 public data were used from the public resources cited above. Restricted EGA validation data from the prostate study were not used. Project-derived processed objects, split manifests and source data are prepared for deposition. Code and derived paper assets are available at https://github.com/seefreewind/spatialleak. The archival DOI is https://doi.org/10.5281/zenodo.21881438.

## Code Availability

Code used for preprocessing, target-panel definition, split generation, benchmark models, statistical analyses, figure generation and source-data generation is prepared for public release. Code is available at https://github.com/seefreewind/spatialleak (version v1.0.0). The archival DOI is https://doi.org/10.5281/zenodo.21881438.

## Author Contributions

Yu Zhang: Conceptualization, methodology, software, formal analysis, visualization, data curation and writing of the original draft. Ying Chen: Data curation, preprocessing review, result checking and manuscript review. Yue Liu: Source-data preparation, reproducibility checks and manuscript review. Da Lin: Supervision, conceptualization, interpretation, correspondence and manuscript review.

## Funding

No specific funding was received for this work.

## Competing Interests

The authors declare no competing interests.



## References

1. Ståhl, P.L. et al. Visualization and analysis of gene expression in tissue sections by spatial transcriptomics. Science 353, 78-82 (2016). https://doi.org/10.1126/science.aaf2403
2. Abdelaal, T., Mourragui, S., Mahfouz, A. & Reinders, M.J.T. SpaGE: Spatial Gene Enhancement using scRNA-seq. Nucleic Acids Res. 48, e107-e107 (2020). https://doi.org/10.1093/nar/gkaa740
3. Biancalani, T. et al. Deep learning and alignment of spatially resolved single-cell transcriptomes with Tangram. Nat. Methods 18, 1352-1362 (2021). https://doi.org/10.1038/s41592-021-01264-7
4. Shengquan, C., Boheng, Z., Xiaoyang, C., Xuegong, Z. & Rui, J. stPlus: a reference-based method for the accurate enhancement of spatial transcriptomics. Bioinformatics 37, i299-i307 (2021). https://doi.org/10.1093/bioinformatics/btab298
5. Long, Y. et al. Spatially informed clustering, integration, and deconvolution of spatial transcriptomics with GraphST. Nat. Commun. 14, 1155 (2023). https://doi.org/10.1038/s41467-023-36796-3
6. Dong, K. & Zhang, S. Deciphering spatial domains from spatially resolved transcriptomics with an adaptive graph attention auto-encoder. Nat. Commun. 13, 1739 (2022). https://doi.org/10.1038/s41467-022-29439-6
7. Hu, J. et al. SpaGCN: Integrating gene expression, spatial location and histology to identify spatial domains and spatially variable genes by graph convolutional network. Nat. Methods 18, 1342-1351 (2021). https://doi.org/10.1038/s41592-021-01255-8
8. Xu, H. et al. Unsupervised spatially embedded deep representation of spatial transcriptomics. Genome Med. 16, 12 (2024). https://doi.org/10.1186/s13073-024-01283-x
9. Kapoor, S. & Narayanan, A. Leakage and the reproducibility crisis in machine-learning-based science. Patterns 4, 100804 (2023). https://doi.org/10.1016/j.patter.2023.100804
10. Kaufman, S., Rosset, S., Perlich, C. & Stitelman, O. Leakage in data mining. ACM Trans. Knowl. Discov. Data 6, 1-21 (2012). https://doi.org/10.1145/2382577.2382579
11. Vabalas, A., Gowen, E., Poliakoff, E. & Casson, A.J. Machine learning algorithm validation with a limited sample size. PLOS ONE 14, e0224365 (2019). https://doi.org/10.1371/journal.pone.0224365
12. Varma, S. & Simon, R. Bias in error estimation when using cross-validation for model selection. BMC Bioinformatics 7, 91 (2006). https://doi.org/10.1186/1471-2105-7-91
13. Ambroise, C. & McLachlan, G.J. Selection bias in gene extraction on the basis of microarray gene-expression data. Proc. Natl Acad. Sci. USA 99, 6562-6566 (2002). https://doi.org/10.1073/pnas.102102699
14. Moran, P.A.P. Notes on continuous stochastic phenomena. Biometrika 37, 17–23 (1950). https://doi.org/10.1093/biomet/37.1-2.17
15. He, B. et al. Integrating spatial gene expression and breast tumour morphology via deep learning. Nat. Biomed. Eng. 4, 827-834 (2020). https://doi.org/10.1038/s41551-020-0578-x
16. Maynard, K.R. et al. Transcriptome-scale spatial gene expression in the human dorsolateral prefrontal cortex. Nat. Neurosci. 24, 425-436 (2021). https://doi.org/10.1038/s41593-020-00787-0
17. Andersson, A. et al. Spatial deconvolution of HER2-positive breast cancer delineates tumor-associated cell type interactions. Nat. Commun. 12, 6012 (2021). https://doi.org/10.1038/s41467-021-26271-2
18. Andersson, A. et al. Spatial deconvolution of HER2-positive breast cancer delineates tumor-associated cell type interactions. Zenodo (2021). https://doi.org/10.5281/zenodo.4751624
19. Thrane, K., Eriksson, H., Maaskola, J., Hansson, J. & Lundeberg, J. Spatially Resolved Transcriptomics Enables Dissection of Genetic Heterogeneity in Stage III Cutaneous Malignant Melanoma. Cancer Res. 78, 5970-5979 (2018). https://doi.org/10.1158/0008-5472.CAN-18-0747
20. 10x Genomics Human Breast Cancer (Block A Section 1): Spatial Gene Expression dataset. 10x Genomics https://www.10xgenomics.com/datasets/human-breast-cancer-block-a-section-1-1-standard-1-0-0 (2020).
21. Kiviaho, A. et al. Single cell and spatial transcriptomics highlight the interaction of club-like cells with immunosuppressive myeloid cells in prostate cancer. Nat. Commun. 15, 9949 (2024). https://doi.org/10.1038/s41467-024-54364-1
22. Hamilton, W.L., Ying, R. & Leskovec, J. Inductive representation learning on large graphs. Advances in Neural Information Processing Systems Preprint at https://arxiv.org/abs/1706.02216 (2017).
