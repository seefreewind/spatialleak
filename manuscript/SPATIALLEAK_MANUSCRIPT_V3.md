# Leakage-resistant benchmarking reveals two channels of inflated generalization in spatial omics prediction

## Abstract

Spatial transcriptomics benchmarks commonly use random spot-level splits, although spatial neighborhoods and patient-specific structure can make test performance optimistic. SpatialLeak evaluates this risk by pairing permissive random splits with spatially buffered, section-held-out, patient-held-out, and dataset-held-out tests. Across DLPFC, breast cancer, melanoma, and prostate datasets, random-split advantages were not explained by one mechanism. Spatial kNN in dense Visium breast data dropped sharply under spatial buffering, whereas PCA+Ridge and GraphSAGE showed large patient-held-out losses in Andersson and Thrane. In GSE278936 prostate Visium, PCA+Ridge was unchanged at hop0 but declined under non-zero buffers, supporting a spatial-channel replication without providing patient-level validation. Random-size-matched controls showed that reduced sample count alone did not explain the main spatial-buffer losses. These results argue for split-aware reporting in spatial omics prediction and separate local neighborhood dependence from patient/batch-associated shortcuts.

## Introduction

Spatial transcriptomics measures molecular state while preserving tissue location, making it possible to connect gene expression with tissue architecture. This has motivated prediction tasks in which measured genes, spatial expression profiles, or molecular states are inferred from other genes, neighboring spots, graph structure, or matched tissue morphology [1,8,9]. These tasks are now used to compare model classes and to decide whether spatial context improves prediction.

The interpretation of these benchmarks depends on the split design. A random spot-level split can place neighboring tissue locations, spots from the same section, and samples from the same patient on both sides of the train-test boundary. In that setting, high test performance can reflect local neighborhood dependence or patient-associated structure as much as transportable prediction. This problem is familiar in machine learning and genomics, where leakage and validation bias can produce optimistic performance estimates [12-14].

Spatial omics adds a specific difficulty: spatial dependence is not automatically an error. A model that uses laminar brain architecture or conserved tumor organization may be learning meaningful biology if the signal transfers across the intended evaluation tier. The practical problem is therefore not to remove all spatial information. It is to match the evaluation design to the claim being made: local interpolation, transfer across sections, patient-level generalization, dataset transfer, or cross-platform transportability.

Here we present SpatialLeak, a leakage-resistant benchmark framework for spatial omics prediction. SpatialLeak compares random spot splits with spatial-buffer, slide-held-out, patient-held-out, and dataset-held-out tests across public spatial transcriptomics datasets [2-7]. It reports leakage inflation (LI), relative leakage inflation (RLI), and strict-split retention for PCA+Ridge, Spatial kNN, and GraphSAGE. The framework separates two channels of apparent generalization inflation: local spatial-neighborhood dependence and patient/batch-associated shortcuts.

## Results

### Random spot-level splitting inflates apparent predictive generalization

How much random-split performance is retained when the train-test boundary matches a stricter generalization claim? Across the frozen paper tables, random spot-level splits produced higher apparent performance than stricter patient, section, or spatial-buffer evaluations in multiple datasets and model classes. The pattern was not limited to a single platform or tissue.

In the patient-channel datasets, PCA+Ridge showed clear random-to-patient losses in DLPFC, Andersson HER2-positive breast cancer, and Thrane melanoma. The same channel was reproduced by GraphSAGE in the tumor datasets, with patient RLI values of 0.692 in Andersson and 0.718 in Thrane. These results show that graph-based spatial models can remain sensitive to patient- or sample-associated structure.

The spatial-channel datasets showed a different pattern. DLPFC and Visium breast retained some strict-split signal but lost performance under spatial separation, especially for Spatial kNN. Visium breast was the clearest dense-platform example, with Spatial kNN hop5 RLI of 0.796. These findings support the central premise of SpatialLeak: random spot-level performance is not a sufficient estimate of the generalization claimed by a model.

### Non-zero spatial buffers reveal neighborhood dependence

Does a non-overlapping spatial partition remove local train-test neighborhood overlap? The matched-hop experiments show that hop0 partitions can still be too permissive. A non-zero spatial buffer was needed to reveal the full loss associated with local neighborhood separation.

In Visium breast, Spatial kNN performance dropped sharply as the hop buffer increased, while the slide-held-out result retained substantial signal. This contrast indicates that a local-neighborhood channel and section-level transportable structure can coexist. DLPFC showed a related but milder pattern, with Spatial kNN spatial RLI of 0.402.

GSE278936 prostate was used only as a spatial-channel Visium replication. In the public GEO portion, 52 patients correspond to 52 sections, so patient and section effects cannot be separated. Within that boundary, PCA+Ridge showed the expected distance response: random and hop0 performance were nearly identical, while hop5 decreased to 0.292 (RLI 0.222). Spatial kNN was near zero in this dataset, so its RLI was not interpreted.

The Phase 18 random-size-matched control addressed whether these decreases were artifacts of smaller test sets. In DLPFC and Visium breast, the loss from imposing the spatial buffer exceeded the loss from reducing the random split to comparable sample size. GSE278936 PCA+Ridge showed the same direction with smaller magnitude. This control supports the interpretation that the main spatial-buffer losses were not explained by sample count alone.

### Patient-held-out evaluation identifies a distinct patient-associated channel

Does patient separation reveal a channel that spatial buffers miss? Andersson and Thrane answer yes. In these ST v1.0 tumor datasets, patient-held-out performance losses were large for PCA+Ridge and GraphSAGE even when some spatial-buffer comparisons were weak or near zero.

Andersson showed the clearest contrast. GraphSAGE had a small matched_hop0 loss but a large patient-held-out loss, indicating that a model can appear robust to within-section block separation while still depending on patient-associated structure. Thrane showed the same patient-channel pattern for GraphSAGE, despite low-density geometry that made high-hop kNN curves difficult to interpret.

DLPFC was a mixed case. Patient-held-out losses were present but smaller than the strongest tumor-dataset patient losses, and Spatial kNN retained substantial patient-held-out signal. This is consistent with a setting where some spatial structure is transportable across donors. The result also shows why the manuscript should not equate every strict-split loss with leakage.

### Dominant inflation channels vary across datasets and model classes

Which channel dominates depends on the dataset and model. DLPFC contains both spatial and patient-associated components. Andersson and Thrane are patient-channel dominant for PCA+Ridge and GraphSAGE. Visium breast is spatial-channel dominant but cannot support patient-level claims. GSE278936 supports a PCA+Ridge spatial-channel replication and a kNN boundary condition.

This heterogeneity is a result, not a nuisance. It shows that a single benchmark split cannot diagnose all forms of apparent generalization. It also explains why simple diagnostic baselines are useful: Spatial kNN can directly reveal local neighborhood dependence when it has signal, while PCA+Ridge provides a strong non-graph baseline and GraphSAGE tests whether graph learning follows the same split-dependent patterns.

### Model advantage depends on evaluation regime

Does a model remain advantaged after the split changes? The answer was evaluation-dependent. GraphSAGE reproduced patient-channel sensitivity in Andersson and Thrane, rather than eliminating it. Spatial kNN was strong under random or dense local conditions but collapsed in several low-signal or spatially isolated settings. PCA+Ridge often retained more performance under broader transfer than purely spatial kNN.

These observations argue against interpreting random-split leaderboards as model rankings for patient- or dataset-level generalization. A model can be useful for local interpolation while being weak for patient-held-out transfer. Conversely, a method with lower random-split performance may retain more signal under the evaluation tier that matches the intended use.

### SpatialLeak defines a hierarchy for robust evaluation

SpatialLeak organizes evaluation evidence into a hierarchy. Random spot splits test local interpolation and should be reported as permissive. Spatial-buffer splits test within-section neighborhood separation. Slide-held-out tests section transfer. Patient-held-out tests patient-, sample-, and batch-associated structure. Dataset-held-out and cross-platform tests evaluate broader transportability.

This hierarchy clarifies the role of each dataset in the manuscript. DLPFC contributes both spatial and donor separation. Andersson and Thrane contribute patient/batch-channel evidence. Visium breast contributes dense Visium spatial-buffer and section-level evidence. GSE278936 contributes high-density Visium spatial-channel replication only. Andersson-to-Visium transfer is retained as a supplementary stress test, not as a main patient-level validation result.

## Discussion

SpatialLeak shows that random spot-level evaluation can overstate apparent performance in spatial omics prediction. The effect separates into at least two channels: local spatial-neighborhood dependence and patient/batch-associated structure. These channels require different split designs and should not be collapsed into a single random-split leakage claim.

The sample-size control strengthens the spatial-channel interpretation. Buffering can reduce the number of evaluable test spots, so a performance decrease could in principle arise from smaller samples. The random-size-matched control showed that reducing the random split to similar sizes had little effect in DLPFC and Visium breast compared with imposing spatial separation. This does not prove a single causal mechanism, but it rules out a simple sample-count explanation for the main spatial-buffer losses.

The patient-channel findings have a different interpretation. Andersson and Thrane showed large patient-held-out losses for PCA+Ridge and GraphSAGE. These losses may combine patient identity, section background, processing batch, cohort structure, and biological heterogeneity. The public data do not allow every component to be decomposed. The correct conclusion is that random spot splits can benefit from patient-associated structure that is not retained under patient-held-out evaluation.

Spatial dependence should not be treated as intrinsically invalid. If tissue architecture transfers across patients or sections, using that information can be biologically meaningful. DLPFC and Visium breast both illustrate this boundary: strict-split performance was reduced but not eliminated in all settings, and slide-held-out or patient-held-out retention can reflect transportable organization. SpatialLeak therefore measures whether performance is retained under the intended claim, not whether spatial information is forbidden.

The study has limitations. It uses public datasets with heterogeneous platforms, tissues, densities, and sample structures. Visium breast contains one patient and supports section-level, not patient-level, evidence. GSE278936 public data contain one section per patient, preventing clean patient-versus-section decomposition. The model set is intentionally diagnostic rather than exhaustive. The dataset-held-out stress test remains supplementary because cross-platform transfer changes more than leakage risk.

These boundaries do not weaken the main recommendation. Spatial omics prediction papers should report split designs that match their stated generalization claims, include simple diagnostic baselines, avoid interpreting near-zero RLI denominators, and separate local spatial interpolation from patient-level or dataset-level generalization. SpatialLeak provides a practical framework for doing so.

## Methods

### Benchmark overview

SpatialLeak evaluated spatial omics prediction under progressively stricter train-test separation. The benchmark compared random spot-level splits with matched spatial block splits, non-zero spatial exclusion buffers, slide-held-out splits, patient-held-out splits, and dataset-held-out stress tests. The main unit of prediction was a spatial spot or capture location, and the output was expression of a frozen target-gene panel.

### Datasets

DLPFC Visium data were derived from the human dorsolateral prefrontal cortex dataset. Andersson HER2-positive breast cancer and Thrane melanoma represented ST v1.0 tumor datasets with patient-held-out evaluation. Visium breast used public 10x Genomics breast cancer demonstration sections and was treated as section-level and spatial-buffer evidence. GSE278936 prostate Visium was used as a public spatial-channel replication only.

### Target genes and features

Dataset-specific target panels used the top 50 Moran-ranked genes available after preprocessing. Shared-panel analyses used `shared_panel_50` where required. Predictor features were selected from highly variable genes after excluding target genes. All panels were frozen before model comparison.

### Split definitions

Random spot splits used an 80/10/10 train/validation/test partition. Matched spatial block splits assigned grid blocks within each section to train, validation, or test folds and selected the candidate assignment with balanced spot count, library size, Moran signal, and layer composition where available. Hop-buffered splits removed test spots within the specified kNN graph distance from the training set. Patient-held-out splits held out all sections from a patient or donor where the dataset design allowed it.

### Models

The Mean baseline predicted target expression from training-set means. PCA+Ridge applied principal component reduction to predictor genes followed by Ridge regression for each target gene. Spatial kNN predicted each test spot from spatially nearest training spots within normalized section coordinates. GraphSAGE was included as a representative inductive graph neural network.

### Metrics

The primary metric was mean Pearson correlation across target genes. Leakage inflation was defined as `Perf_random - Perf_strict`. Relative leakage inflation was defined as `(Perf_random - Perf_strict) / Perf_random`. Retention was defined as `Perf_strict / Perf_random`. RLI was not interpreted when random-split performance was near zero.

### Sample-size control

For Phase 18, random-size-matched controls were run for DLPFC, Visium breast, and GSE278936 prostate. For each seed and matched_hop2 or matched_hop5 reference, the original random split was downsampled toward the strict split's train, validation, and test sizes, with slide composition matched where feasible. The control did not use strict-split performance to select observations.

## Data Availability

All analyses used public or project-derived data. DLPFC data are available from the source study and associated public resources [2]. Andersson HER2-positive breast cancer data are available through the Nature Communications article and Zenodo record [3,4]. Thrane melanoma data are available through the Cancer Research article and linked public dataset resources [5]. Visium breast data are available from 10x Genomics public demonstration datasets [7]. GSE278936 prostate data are available through GEO accession GSE278936 and the associated Nature Communications article [6]. Restricted EGA data from the GSE278936 study were not used. Project-derived processed objects, split manifests, and paper tables should be deposited before submission; repository DOI or accession: `[to be added]`.

## Code Availability

Analysis code, split definitions, benchmark scripts, and manuscript asset generation scripts are contained in this project workspace. Public repository URL and archival DOI: `[to be added]`.

## Author Contributions

`[Author contribution statement to be added.]`

## Funding

`[Funding statement to be added.]`

## Competing Interests

`[Competing interests statement to be added.]`

## Acknowledgements

`[Acknowledgements to be added.]`

## References

1. Ståhl, P. L. et al. Visualization and analysis of gene expression in tissue sections by spatial transcriptomics. *Science* 353, 78-82 (2016).
2. Maynard, K. R. et al. Transcriptome-scale spatial gene expression in the human dorsolateral prefrontal cortex. *Nature Neuroscience* 24, 425-436 (2021).
3. Andersson, A. et al. Spatial deconvolution of HER2-positive breast cancer delineates tumor-associated cell type interactions. *Nature Communications* 12, 6012 (2021).
4. Andersson, A. et al. Spatial deconvolution of HER2-positive breast cancer delineates tumor-associated cell type interactions. Zenodo (2021).
5. Thrane, K. et al. Spatially resolved transcriptomics enables dissection of genetic heterogeneity in stage III cutaneous malignant melanoma. *Cancer Research* 78, 5970-5979 (2018).
6. Kiviaho, A. et al. Single cell and spatial transcriptomics highlight the interaction of club-like cells with immunosuppressive myeloid cells in prostate cancer. *Nature Communications* 15, 9949 (2024).
7. 10x Genomics. Human Breast Cancer (Block A Section 1): Spatial Gene Expression dataset (2020).
8. Abdelaal, T. et al. SpaGE: Spatial Gene Enhancement using scRNA-seq. *Nucleic Acids Research* 48, e107 (2020).
9. He, B. et al. Integrating spatial gene expression and breast tumour morphology via deep learning. *Nature Biomedical Engineering* 4, 827-834 (2020).
10. Hamilton, W. L., Ying, R. & Leskovec, J. Inductive representation learning on large graphs. *Advances in Neural Information Processing Systems* (2017).
11. Moran, P. A. P. Notes on continuous stochastic phenomena. *Biometrika* 37, 17-23 (1950).
12. Ambroise, C. & McLachlan, G. J. Selection bias in gene extraction on the basis of microarray gene-expression data. *Proceedings of the National Academy of Sciences* 99, 6562-6566 (2002).
13. Vabalas, A. et al. Machine learning algorithm validation with a limited sample size. *PLOS ONE* 14, e0224365 (2019).
14. Kapoor, S. & Narayanan, A. Leakage and the reproducibility crisis in machine-learning-based science. *Patterns* 4, 100804 (2023).
