# Leakage-resistant evaluation reveals distinct spatial and patient-associated generalization inflation in spatial omics prediction

## Abstract

Spatial omics prediction models are commonly evaluated with random spot-level splits, although spatial neighborhoods and patient-associated structure can make test performance optimistic. We developed SpatialLeak, a leakage-resistant evaluation framework that compares random splits with buffered spatial, section-held-out, patient-held-out, and dataset-held-out regimes. Across public DLPFC, breast cancer, melanoma, and prostate spatial transcriptomics datasets, random-split performance was not explained by a single source of dependence. Dense Visium breast data showed strong spatial-neighborhood inflation for Spatial kNN (hop5 RLI 0.796), while corrected train-only GraphSAGE reruns showed large patient-associated losses in Andersson and Thrane (patient RLI 0.695 and 0.711). In GSE278936 prostate Visium, PCA+Ridge was unchanged at hop0 but declined under non-zero buffers (hop5 RLI 0.222). Random-size-matched controls showed that sample-count reduction alone did not explain the main spatial-buffer losses. SpatialLeak provides an evaluation hierarchy for matching benchmark design to the intended generalization claim.

## Introduction

Spatial transcriptomics links gene expression to tissue architecture, enabling prediction tasks that infer missing genes, spatial molecular states, or tissue-associated expression patterns. These tasks increasingly use spatial coordinates, graph neighborhoods, single-cell references, or histology-derived features to improve prediction and representation learning [1,8-17].

The validity of these benchmarks depends on how train and test observations are separated. Random spot-level splits can place neighboring tissue locations, adjacent sections, or same-patient samples on both sides of the evaluation boundary. Similar forms of leakage and validation bias are well recognized in machine learning and biomedical prediction, especially when grouped or correlated observations are split as if they were independent [20-28].

Spatial omics adds a second challenge: spatial dependence is not inherently invalid. A model may exploit local neighborhood overlap in a permissive split, but it may also learn tissue organization that transfers across sections or patients. Existing evaluation practice does not systematically separate local spatial dependence from patient-associated structure or broader dataset transfer.

SpatialLeak addresses this gap with a multi-tier benchmark for spatial omics prediction. It compares permissive random splits with buffered spatial evaluation, section-held-out evaluation, patient-held-out evaluation, and dataset-held-out stress tests. The framework reports leakage inflation, relative leakage inflation, and strict-split retention while keeping target panels and model parameters frozen across evaluation regimes.

## Results

### Random spot-level splitting inflates apparent predictive generalization

We first asked whether random spot-level performance was retained under stricter evaluation regimes. Across DLPFC, Andersson, Thrane, and Visium breast, random splits produced higher apparent performance than the relevant stricter split for the main interpretable model-dataset combinations. This established random evaluation as a permissive interpolation regime rather than evidence of patient- or dataset-level generalization.

The strongest patient-associated losses appeared in Andersson and Thrane. PCA+Ridge dropped under patient-held-out evaluation in both datasets, and corrected train-only GraphSAGE reruns reproduced the pattern. These results support the conclusion that patient-associated performance inflation is not removed simply by using a graph model.

### Non-zero spatial buffers reveal local neighborhood dependence

We next asked whether non-overlapping spatial blocks were sufficient to remove local neighborhood dependence. They were not always sufficient. In DLPFC and Visium breast, increasing hop distance reduced performance, especially for Spatial kNN. In GSE278936 prostate Visium, PCA+Ridge was essentially unchanged at hop0 but decreased under hop2 and hop5 buffers.

The sample-size control addressed a competing explanation. For DLPFC and Visium breast, downsampling the random split to similar sizes changed performance much less than imposing spatial separation. GSE278936 PCA+Ridge showed the same direction with smaller magnitude. Thus the main buffered-split losses were not explained by sample count alone.

### Patient-held-out evaluation identifies a distinct patient-associated channel

We then asked whether patient-held-out evaluation measured the same phenomenon as spatial buffering. Andersson and Thrane showed that it did not. Patient-held-out losses were large even when spatial kNN was near zero or high-hop spatial curves were not resolvable in low-density ST v1.0 geometry.

This patient-associated channel should be interpreted carefully. It may include patient identity, section background, processing batch, cohort structure, and biological heterogeneity. SpatialLeak does not claim to decompose these causes. It shows that a random spot split can benefit from structure that is not retained when patient-associated groups are separated.

### Dominant inflation channels vary across datasets and model classes

We asked whether one leakage-sensitive model or one strict split could diagnose all settings. The answer was no. DLPFC showed both spatial and donor-associated effects. Andersson and Thrane were patient-channel dominant. Visium breast was spatial-channel dominant but single-patient. GSE278936 supported a PCA+Ridge spatial-channel replication and a kNN boundary condition.

These differences are central to the framework. Spatial kNN is a useful local-neighborhood probe when it has signal. PCA+Ridge provides a strong non-graph baseline. Corrected train-only GraphSAGE tests whether spatial graph learning follows the same split-dependent behavior as simpler baselines.

### Model advantage depends on evaluation regime

We asked whether apparent model behavior remained stable after the split changed. It did not. Spatial kNN was strong in dense random or local settings but weak when spatial signal was absent or isolated. GraphSAGE retained random-split performance in some settings but showed strong patient-held-out losses in tumor datasets. PCA+Ridge often retained broader transfer signal better than purely local kNN.

These results argue against treating random-split leaderboards as evidence of patient- or dataset-level model superiority. Model comparisons should be reported at the evaluation tier that matches the intended use.

### SpatialLeak defines an evaluation hierarchy

SpatialLeak organizes spatial omics prediction into a hierarchy of claims. Random spot splits test permissive interpolation. Buffered spatial splits test local neighborhood separation. Slide-held-out splits test section transfer. Patient-held-out splits test patient-, sample-, and batch-associated structure. Dataset-held-out and cross-platform tests evaluate broader transportability.

The hierarchy also fixes dataset interpretation. Visium breast supports dense Visium spatial and section-level evidence, not patient-level validation. GSE278936 supports spatial-channel replication, not clean patient/batch validation. Andersson-to-Visium transfer is retained as a supplementary stress test.

## Discussion

SpatialLeak shows that apparent performance in spatial omics prediction can be inflated through separable spatial-neighborhood and patient-associated channels. This is a benchmark-design result rather than a claim that every strict-split loss is leakage. The main recommendation is to match the split design to the generalization claim.

Non-zero buffers matter because non-overlapping blocks can still leave test spots close to training neighborhoods. The GSE278936 result illustrates this point: hop0 alone was not informative, while hop2 and hop5 revealed a performance decrease. The Phase 18 random-size-matched control further showed that the main spatial-buffer losses were not a simple consequence of fewer test observations.

Spatial dependence is not inherently leakage. Tissue architecture can be a transportable biological signal when it survives the intended strict evaluation. DLPFC and Visium breast both show retained strict-split signal in some regimes, so the manuscript avoids equating all spatial information with invalid evaluation.

Patient-associated performance loss is distinct from local spatial dependence. Andersson and Thrane showed large patient-held-out losses for PCA+Ridge and corrected GraphSAGE. These losses may reflect patient, section, sample, batch, and biological structure together; public datasets do not always allow those components to be separated.

The findings have practical implications for model benchmarking. Complex spatial models should be compared with strong non-spatial baselines, spatial nearest-neighbor probes, and grouped evaluation designs. Random-split performance should be labelled as local interpolation unless stronger split tiers support broader claims.

This study has limitations. It uses public datasets with heterogeneous platforms and sample structures. Visium breast is single-patient. GSE278936 public data have one section per patient. The model set is diagnostic rather than exhaustive, and the DLPFC train-only GraphSAGE rerun was not completed in Phase 19. These limits bound the scope but do not alter the central conclusion that evaluation regime materially changes apparent generalization.

## Methods

### Benchmark design

SpatialLeak evaluated spatial omics prediction under fixed target panels, fixed model settings, and multiple train-test separation regimes. The primary outcome was mean Pearson correlation across target genes. All model comparisons were made within the same dataset and target panel unless explicitly labelled as a dataset-held-out stress test.

### Data preprocessing

Each section or sample was library-size normalized with `normalize_total(target_sum=1e4)` and transformed with `log1p`. Processed datasets retained slide or section identifiers and patient or donor metadata where available. Highly variable genes were selected using Scanpy's Seurat-flavor HVG procedure, and target genes were excluded from predictor matrices.

### Target panels

Dataset-specific target panels used the top 50 Moran-ranked genes after preprocessing. Moran ranking was computed on the full processed dataset to define the prediction task, not to tune models or select results. Shared-panel analyses used the frozen `shared_panel_50` target set. Target selection was independent of downstream model performance and fixed across evaluation regimes.

### Split definitions

Random spot splits used an 80/10/10 train/validation/test partition. Matched spatial block splits assigned grid blocks within each section to train, validation, or test folds and selected balanced assignments based on spot count, library size, Moran signal, and layer composition where available. `matched_hop0` denotes non-overlapping block assignment without a positive exclusion buffer. Hop2 and hop5 splits removed test spots whose nearest training neighborhood was within fewer than two or five kNN graph hops. Patient-held-out splits held out all sections from a patient or donor where available. Slide-held-out splits held out sections but were not treated as patient-held-out unless patient identity was separated.

### Models

PCA+Ridge fit PCA only on training predictor genes and fit one Ridge model per target gene. The PCA component number and Ridge alpha were fixed. Spatial kNN predicted target expression from spatially nearest training spots only, using inverse-distance weighting in normalized per-slide coordinates. GraphSAGE used within-slide spatial graphs, train-only PCA and train-only feature scaling after the Phase 19 audit, two GraphSAGE layers, hidden dimension 128, Adam optimization, validation-loss early stopping, and no test metric for checkpoint selection.

### Statistical analysis

For each strict split, LI was defined as `Perf_random - Perf_strict`. RLI was defined as `(Perf_random - Perf_strict) / Perf_random`, and retention as `Perf_strict / Perf_random`. RLI is an operational measure of evaluation-dependent performance inflation and should not be interpreted as the proportion of performance causally attributable to information leakage. RLI was not interpreted when absolute random mean Pearson was below 0.05. Bootstrap summaries used slide-level resampling, not spot-level resampling. Wilcoxon signed-rank tests used paired seed or fold summaries and BH-FDR correction within comparison families. Mixed-effects analyses were run separately for patient and spatial channels with `inflation ~ moran_i + C(model)` and dataset random intercepts.

## Data Availability

DLPFC, Andersson, Thrane, 10x Visium breast, and GSE278936 public data were used from their cited public resources. Restricted EGA validation data from the prostate study were not used. Project-derived processed objects and split manifests will be deposited before submission or publication; repository decision pending.

## Code Availability

Code used for split generation, benchmarking, statistical analysis and figure generation is prepared for public release; repository URL and archival DOI will be inserted upon release.

## Author Contributions

`[Author contribution statement to be added.]`

## Funding

`[Funding statement to be added.]`

## Competing Interests

`[Competing interests statement to be added.]`

## Acknowledgements

`[Acknowledgements to be added.]`

## References

See `manuscript/references_master.bib` and `docs/reports/CITATION_PLACEMENT_MAP_FINAL.md` for the expanded verified reference set.
