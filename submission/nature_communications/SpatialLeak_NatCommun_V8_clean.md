# Evaluation design reshapes apparent generalization in spatial omics prediction

Yu Zhang1, Ying Chen2, Yue Liu2, Da Lin1

1 Department of Ophthalmology, The Second Affiliated Hospital of Wenzhou Medical University, No. 109 Xueyuan West Road, Lucheng District, Wenzhou, Zhejiang Province, China

2 Wenzhou Medical University, Wenzhou, Zhejiang Province, China

Correspondence: Da Lin, 212574@wzhealth.com; ORCID 0009-0009-4410-0218

## Abstract

Spatial omics models are often evaluated using random spot-level splits, yet spatial neighborhoods, section context and patient-associated structure can make such performance difficult to interpret. We developed SpatialLeak, a leakage-resistant evaluation framework that compares random spot splits with buffered spatial, section-held-out, patient-held-out and dataset-held-out regimes. In dense Visium breast data, Spatial kNN showed strong spatial-neighborhood inflation, with hop5 relative leakage inflation (RLI) of 0.796. GraphSAGE showed large patient-associated losses in Andersson and Thrane, with patient RLI values of 0.695 and 0.711. In GSE278936 prostate Visium, PCA+Ridge was unchanged at hop0 but decreased under non-zero spatial buffers, reaching hop5 RLI 0.222. Random-size-matched controls indicated that reduced sample count alone did not explain the main spatial-buffer losses. SpatialLeak provides a hierarchy for matching benchmark design to the level of generalization being claimed.

## Introduction

Spatial transcriptomics and related spatial omics assays connect molecular measurements to tissue architecture, enabling prediction tasks that are not available in dissociated profiling alone [1]. These tasks include imputation of unmeasured genes and mapping between molecular and spatial modalities [2,3]. They also include graph-based learning from tissue neighborhoods and representation learning over spatial context [4]. Spatial graph and domain-learning methods further show how location, morphology and neighborhood structure can carry biologically meaningful information [5,6]. Histology-aware graph models and deep spatial representations extend this trend by combining molecular profiles with tissue context at increasing scale [7,8]. As spatial models are increasingly compared across tissues and cohorts, the validity of these comparisons depends not only on model architecture but also on whether the evaluation design matches the level of generalization being claimed.

Spatial observations are not independent in the conventional IID sense. Random spot-level splits can place neighboring tissue locations, similar local cell compositions, the same section background or the same patient-associated structure on both sides of the train-test boundary. Under such settings, apparent test performance can combine local interpolation with broader transfer. Related forms of non-independent sampling and information leakage are known to inflate machine-learning performance estimates [9,10]. Leakage between model development and evaluation can also reduce reproducibility in biomedical prediction studies [11,12]. Gene-expression analyses have long shown the related risk that feature selection and model evaluation must be separated to avoid biased estimates [13]. Spatial omics adds a further challenge because biological proximity itself may carry genuine predictive information.

Spatial dependence is therefore not inherently invalid. Spatial autocorrelation is a defining property of many tissue measurements and has a formal statistical history [14]. A spatially aware model may legitimately exploit tissue architecture when the intended task is local interpolation or when the learned signal remains predictive across the separation required by the scientific claim. The relevant question is not whether a model uses spatial information, but whether the information it exploits remains predictive under the level of separation implied by that claim. Local interpolation, spatial transfer, section transfer, patient transfer, dataset transfer and cross-platform transfer are distinct evaluation targets and should not be treated as interchangeable.

Existing spatial omics benchmarks do not consistently distinguish these levels of evidence. Spatial prediction and enhancement studies illustrate how benchmark tasks are often framed around held-out measurements within related spatial or molecular contexts [2,15]. Graph-based spatial prediction further highlights the need to distinguish useful neighborhood signal from evaluation settings that permit local interpolation [4]. It remains unclear whether apparent performance inflation is driven primarily by local spatial-neighborhood dependence, patient-associated structure or broader distributional differences, and whether non-overlapping spatial partitions alone are sufficient to remove local dependence. Here we introduce SpatialLeak, a multi-tier evaluation framework that compares random spot splits with buffered spatial, section-held-out, patient-held-out and dataset-held-out regimes across public spatial transcriptomics datasets and diagnostic model classes. We show that apparent generalization can be attenuated through distinct spatial-neighborhood and patient-associated channels, that non-zero spatial buffers can be necessary to expose local dependence, and that model comparisons change with the evaluation tier. SpatialLeak therefore organizes spatial omics benchmarking into a generalization evidence hierarchy that links evaluation design to the level of claim it can support.

## Results

### Random spot-level evaluation inflates apparent predictive generalization

SpatialLeak first tested whether random spot-level performance was retained when the train-test boundary matched a stricter generalization claim (Fig. 1, Fig. 2). Across DLPFC, Andersson, Thrane and Visium breast, random splits produced higher apparent performance than the relevant stricter split for the main interpretable model-dataset combinations. These comparisons position random spot evaluation as a permissive interpolation setting rather than, by itself, evidence of section-, patient- or dataset-level generalization.

The patient-channel datasets showed the clearest random-to-patient losses (Fig. 3). In Andersson, PCA+Ridge patient RLI was 0.662, and GraphSAGE patient RLI was 0.695. In Thrane, PCA+Ridge patient RLI was 0.499, and GraphSAGE patient RLI was 0.711. These results show that a graph-based model did not remove the need for grouped evaluation.

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

### SpatialLeak defines a hierarchy for spatial omics generalization claims

SpatialLeak formalizes six evaluation tiers (Fig. 1). Level 0, random spot interpolation, supports local interpolation but does not establish spatial, section or patient transfer. Level 1, buffered spatial transfer, tests local neighborhood separation but does not establish patient transfer. Level 2, section-held-out transfer, tests transfer across sections but not necessarily across patients. Level 3, patient-held-out transfer, tests retention across patient-associated groups but does not establish dataset or platform transfer. Level 4, dataset-held-out transfer, tests broader dataset transportability. Level 5, cross-platform transfer, tests robustness when measurement platforms also change.

This hierarchy fixes the language of the manuscript. Visium breast supports dense Visium spatial and section-level evidence, not patient-level validation. GSE278936 supports spatial-channel replication, not clean patient-level validation. Andersson-to-Visium transfer remains a supplementary cross-platform stress test rather than a central validation claim.

## Discussion

SpatialLeak shows that apparent performance in spatial omics prediction depends materially on the evaluation design used to define generalization. Across tissues and platforms, replacing random spot-level evaluation with stricter designs attenuated performance through two separable channels: local spatial-neighborhood dependence and patient-associated structure. This extends recent benchmarking work showing that spatial omics methods rarely have a single evaluation-independent ranking. Large comparative studies of spatial clustering and histology-based spatial gene-expression prediction have found that apparent method superiority varies across accuracy, robustness, generalizability and downstream utility [23,24]. Benchmarking across sequencing-based spatial transcriptomics technologies has also emphasized that evaluation criteria must reflect the biological and technical question being asked [26]. SpatialLeak adds a complementary point: the split itself is part of the estimand, because different train-test boundaries test different forms of generalization.

The requirement for a non-zero spatial exclusion buffer highlights a distinction between nominal partitioning and effective independence. Assigning neighboring spots to different spatial blocks prevents literal overlap, but it does not eliminate correlation generated by continuous tissue architecture, spatially structured cell composition or molecular gradients. Spatial autocorrelation is therefore not merely a property of the response variable; it can determine the effective information distance between nominally separate training and test observations [14]. Contemporary benchmarks increasingly recognize spatial continuity and technology-dependent variation as distinct dimensions of performance rather than treating observations as exchangeable [23,26]. GSE278936 illustrates this point clearly: hop0 was nearly indistinguishable from random evaluation, whereas positive exclusion distances exposed a stable loss despite random-size-matched controls. A spatial split should therefore be defined by the dependence it removes, not only by whether train and test labels occupy different geometric partitions.

Patient-held-out evaluation exposed a second dependence structure that was largely orthogonal to local spatial autocorrelation. In Andersson and Thrane, substantial patient-associated losses persisted for both PCA+Ridge and GraphSAGE even when local spatial-neighbor baselines were weak, indicating that within-section proximity was insufficient to explain the observed attenuation. This channel should not be interpreted as a single batch effect. Patient identity can be entangled with tissue composition, disease heterogeneity, section preparation, sequencing characteristics and other technical factors. Multi-site spatial transcriptomics studies have independently shown that platform and processing context can account for major variation, motivating standardized reproducibility metrics across sites and technologies [27]. This interpretation is consistent with the broader machine-learning literature showing that non-independent grouping between development and evaluation data can produce optimistic estimates when the intended deployment unit is a new biological subject [9,10]. Patient-held-out evaluation therefore measures the portability of a predictive relationship across patient-associated contexts rather than identifying which individual source of heterogeneity caused the loss.

Conversely, performance that persists after stricter separation should not be dismissed as residual leakage. Spatial organization is an intrinsic component of tissue biology, and conserved anatomical or pathological structures may legitimately support prediction across sections or patients. The important distinction is between local interpolation and transportable structure, not between models that do and do not use spatial information. Recent work on spatial prediction similarly indicates that prediction accuracy and generalizability are separate properties: methods that perform strongly within a study may show weaker cross-study or cross-platform transfer [24]. Uncertainty-aware spatial prediction frameworks further show that nominally accurate predictions can differ in reliability for downstream inference [25]. We therefore view the SpatialLeak hierarchy as an extrapolation ladder: retention under increasingly independent evaluation tiers provides progressively stronger evidence that a learned relationship reflects transportable structure. At the same time, strict-split loss can include legitimate distribution shift, so RLI should be interpreted as evaluation-dependent inflation rather than as the causal fraction of performance attributable to leakage [9].

The dependence of apparent model advantage on evaluation regime has implications for how spatial omics leaderboards are interpreted. In our analyses, models that benefited strongly from local neighborhoods under random evaluation did not necessarily retain the same advantage under patient- or spatially isolated testing. This is consistent with independent spatial omics benchmarks in which no method dominates all evaluation criteria: spatial clustering algorithms show complementary performance across accuracy, continuity and robustness [23], and histology-to-expression prediction methods can rank differently for within-study accuracy, cross-study generalizability and translational utility [24]. A recent benchmark of spatial alignment methods likewise found that performance is scenario-dependent and that challenging cross-platform or multi-slice settings expose limitations that are not apparent under conventional evaluations [28]. A leaderboard without an explicit generalization regime is therefore underspecified. Spatial omics studies should specify whether model superiority refers to local interpolation, patient transfer, dataset transfer or platform transportability.

These findings support a shift from single-split benchmarking toward tiered reporting standards for spatial omics. Recent spatial transcriptomics benchmark initiatives have called for standardized performance metrics, reference tissues and reproducible workflows because platform resolution, molecular capture, sequencing depth and other technical characteristics can materially alter analytical conclusions [26]. Multi-site imaging-based spatial studies further demonstrate the importance of harmonized procedures and standardized reproducibility metrics when results are compared across laboratories or platforms [27]. Contemporary method benchmarks increasingly include robustness, usability and challenging cross-platform scenarios rather than relying on a single internal accuracy measure [28]. For predictive modeling, authors should report at minimum the biological grouping unit, exact spatial exclusion rule, patient or donor separation where relevant, uncertainty at the biological-unit level, strong non-spatial and spatial diagnostic baselines, and machine-readable split manifests. This would not mandate a universal split; it would make explicit which claim each reported performance estimate can support.

Several limitations define the scope of this framework and motivate the next generation of spatial omics benchmarks. First, our model set was deliberately diagnostic rather than exhaustive; the study was designed to identify evaluation-sensitive behavior rather than establish a new state-of-the-art leaderboard. Second, public datasets differ in tissue composition, platform density and sample structure: Visium breast contains a single patient, whereas the public GSE278936 cohort contains one section per patient, preventing clean decomposition of patient and section effects. Future evaluations would benefit from multi-patient, multi-section and multi-site reference resources of the kind now emerging for spatial omics reproducibility studies [27]. Third, our main task focused on gene-expression prediction; evaluation dependence should also be tested in multimodal translation, spatial domain inference, alignment and representation learning, where recent benchmarks already show strong scenario-specific behavior [28]. Finally, point performance alone does not capture the reliability of predicted spatial quantities, suggesting that future leakage-resistant benchmarks should integrate uncertainty calibration and downstream inference alongside discrimination metrics [25]. These limitations constrain the breadth of our conclusions, but they also define a path toward benchmark designs that distinguish interpolation, biological transportability and out-of-domain transfer.

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

PCA+Ridge used 2000 predictor genes excluding the 50 target genes. PCA used 64 components and was fit only on training observations. Ridge regression used alpha = 1.0 and was fit separately for each target gene. Spatial kNN used k = 15 nearest training spots in normalized per-slide coordinates and inverse-distance weights `1/(d + 1e-6)` normalized to sum to one for each test spot. Neighbors were drawn only from the training split; when fewer than 15 training spots were available, all available training spots were used. GraphSAGE used train-only PCA and train-only feature scaling, two GraphSAGE layers, hidden dimension 128 for formal external runs, within-slide graph k = 10 with self-loops, ReLU activation, no dropout, mean-squared-error loss on training nodes, Adam optimization with learning rate 1e-3, weight decay 1e-4, up to 500 epochs, validation-loss early stopping with patience 60, and validation-loss checkpoint selection. Test performance was not used for checkpoint selection.

### Metrics and inference

The primary metric was mean Pearson correlation across target genes. Leakage inflation was defined as `Perf_random - Perf_strict`. Relative leakage inflation (RLI) was defined as `(Perf_random - Perf_strict) / Perf_random`, and retention was defined as `Perf_strict / Perf_random`. RLI is an operational measure of evaluation-dependent performance inflation and is not interpreted as the fraction of performance causally attributable to leakage. RLI was not interpreted when absolute random mean Pearson was below 0.05. Main DLPFC, Andersson, Thrane and Visium breast baseline analyses used seeds 0-9; GSE278936 spatial-channel replication used seeds 0-4. Random-size-matched controls downsampled the random split to comparable sample sizes without using strict-split performance. Bootstrap summaries used slide-level resampling with 1000 bootstrap replicates where available. Wilcoxon signed-rank tests used paired seed summaries with Benjamini-Hochberg false-discovery-rate correction within comparison families. Mixed-effects analyses were run separately for patient and spatial channels with `inflation ~ moran_i + C(model)` and dataset random intercepts.

### Reproducibility

Seeds were frozen before final analyses. Test performance was not used for hyperparameter selection, checkpoint selection, target-panel selection or seed selection. Scripts for regenerating frozen paper assets and unit tests for core split and evaluation functions are provided with the accompanying code repository.

## Data Availability

DLPFC, Andersson, Thrane, 10x Visium breast and GSE278936 public data were used from the public resources cited above. Restricted EGA validation data from the prostate study were not used. Project-derived split manifests, source-data files, analysis scripts and paper assets are available at https://github.com/seefreewind/spatialleak and archived at https://doi.org/10.5281/zenodo.21881438.

## Code Availability

Code for preprocessing, target-panel definition, split generation, benchmarking, statistical analysis, figure generation and source-data generation is available at https://github.com/seefreewind/spatialleak (v1.0.0) and archived at https://doi.org/10.5281/zenodo.21881438.

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
4. Chen, S., Zhang, B., Chen, X., Zhang, X. & Jiang, R. stPlus: a reference-based method for the accurate enhancement of spatial transcriptomics. Bioinformatics 37, i299–i307 (2021). https://doi.org/10.1093/bioinformatics/btab298
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
20. 10x Genomics Human Breast Cancer (Block A Section 1): Spatial Gene Expression dataset. 10x Genomics dataset, version 1.0.0, Block A Section 1; Accessed 2026-08-10. https://www.10xgenomics.com/datasets/human-breast-cancer-block-a-section-1-1-standard-1-0-0 (2020).
21. Kiviaho, A. et al. Single cell and spatial transcriptomics highlight the interaction of club-like cells with immunosuppressive myeloid cells in prostate cancer. Nat. Commun. 15, 9949 (2024). https://doi.org/10.1038/s41467-024-54364-1
22. Hamilton, W.L., Ying, R. & Leskovec, J. Inductive representation learning on large graphs. In Advances in Neural Information Processing Systems 30 (2017).
23. Yuan, Z. et al. Benchmarking spatial clustering methods with spatially resolved transcriptomics data. Nat. Methods 21, 712-722 (2024). https://doi.org/10.1038/s41592-024-02215-8
24. Wang, C. et al. Benchmarking the translational potential of spatial gene expression prediction from histology. Nat. Commun. 16, 1544 (2025). https://doi.org/10.1038/s41467-025-56618-y
25. Sun, E.D., Ma, R., Navarro Negredo, P., Brunet, A. & Zou, J. TISSUE: uncertainty-calibrated prediction of single-cell spatial transcriptomics improves downstream analyses. Nat. Methods 21, 444-454 (2024). https://doi.org/10.1038/s41592-024-02184-y
26. You, Y. et al. Systematic comparison of sequencing-based spatial transcriptomic methods. Nat. Methods 21, 1743-1754 (2024). https://doi.org/10.1038/s41592-024-02325-3
27. Plummer, J.T. et al. Standardized metrics for assessment and reproducibility of imaging-based spatial transcriptomics datasets. Nat. Biotechnol. 44, 1213-1225 (2026). https://doi.org/10.1038/s41587-025-02811-9
28. Yan, Y. et al. Benchmarking alignment methods for spatial transcriptomics data. Nat. Comput. Sci. 6, 524-541 (2026). https://doi.org/10.1038/s43588-026-00977-z
