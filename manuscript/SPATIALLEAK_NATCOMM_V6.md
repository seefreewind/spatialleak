# Evaluation design reshapes apparent generalization in spatial omics prediction

## Abstract

Spatial omics models are often evaluated using random spot-level splits, although spatial neighborhoods, section context and patient-associated structure complicate what such performance means. We developed SpatialLeak, a leakage-resistant framework that compares random spot splits with buffered spatial, section-held-out, patient-held-out and dataset-held-out regimes. In dense Visium breast data, Spatial kNN showed strong spatial-neighborhood inflation, with hop5 relative leakage inflation (RLI) of 0.796. Corrected train-only GraphSAGE reruns showed large patient-associated losses in Andersson and Thrane, with patient RLI values of 0.695 and 0.711. In GSE278936 prostate Visium, PCA+Ridge was unchanged at hop0 but declined under non-zero spatial buffers, reaching hop5 RLI 0.222. Random-size-matched controls indicated that reduced sample count alone did not explain the main spatial-buffer losses. SpatialLeak provides a hierarchy for matching benchmark design to the level of generalization being claimed.

## Introduction

Spatial transcriptomics and related spatial omics assays connect molecular measurements to tissue architecture, creating prediction tasks that are not available in dissociated profiling alone. These tasks include imputation of unmeasured genes, spatial molecular prediction, graph-based learning from tissue neighborhoods and representation learning over spatial context. As spatial datasets grow, such models increasingly support claims about whether molecular patterns can be recovered across locations, sections, patients or datasets.

The evaluation problem is that spatial observations are not independent in the ordinary IID sense. A random spot-level split can place neighboring tissue locations, similar local cell compositions, the same section background or the same patient-associated structure on both sides of the train-test boundary. Performance under this regime can therefore mix local interpolation with broader generalization.

Spatial dependence is not inherently invalid. A spatially aware model may use tissue architecture as a legitimate biological signal if that signal is retained under the separation required by the scientific claim. The central question is what claim the evaluation design can support: local interpolation, spatial transfer, section transfer, patient transfer, dataset transfer or cross-platform transfer.

Current spatial omics benchmarks do not consistently separate these levels. Existing split choices can conflate local spatial-neighborhood dependence, patient-associated structure and transportable biological signal. This makes it difficult to interpret whether an apparent model advantage reflects a robust predictive principle or the evaluation tier used to measure it.

Here we introduce SpatialLeak, a multi-tier evaluation framework for spatial omics prediction. SpatialLeak compares random spot splits with buffered spatial, section-held-out, patient-held-out and dataset-held-out regimes across public spatial transcriptomics datasets and diagnostic model classes. The framework shows that apparent generalization can arise through distinct spatial-neighborhood and patient-associated channels, and it organizes these findings into a generalization evidence hierarchy.


## Results

### Random spot-level evaluation inflates apparent predictive generalization

SpatialLeak first tested whether random spot-level performance was retained when the train-test boundary matched a stricter generalization claim (Fig. 1). Across DLPFC, Andersson, Thrane and Visium breast, random splits produced higher apparent performance than the relevant stricter split for the main interpretable model-dataset combinations. This established random spot evaluation as a permissive interpolation setting rather than evidence, by itself, for section-, patient- or dataset-level generalization.

The patient-channel datasets showed the clearest random-to-patient losses. In Andersson, PCA+Ridge patient RLI was 0.662, and corrected train-only GraphSAGE patient RLI was 0.695. In Thrane, PCA+Ridge patient RLI was 0.499, and corrected train-only GraphSAGE patient RLI was 0.711. These results show that a graph-based model did not remove the need for grouped evaluation.

### Non-zero spatial buffers reveal local neighborhood dependence

SpatialLeak next tested whether non-overlapping spatial partitions were sufficient to remove local neighborhood dependence. They were not always sufficient. In DLPFC and Visium breast, increasing hop distance reduced performance, especially for Spatial kNN. Visium breast showed the strongest spatial-channel example, with Spatial kNN hop5 RLI 0.796.

GSE278936 provided an independent high-density Visium spatial-channel replication. PCA+Ridge was essentially unchanged at hop0 but decreased under hop2 and hop5 buffers, reaching hop5 RLI 0.222. This pattern supports the specific claim that a non-zero exclusion buffer can be required to expose local neighborhood dependence. The random-size-matched control showed that the main spatial-buffer losses were larger than the losses caused by downsampling random splits to similar sample sizes.

### Patient-held-out evaluation identifies a distinct patient-associated channel

Patient-held-out evaluation measured a different axis of dependence from within-section spatial buffering (Fig. 3). Andersson and Thrane had large patient-held-out losses even when spatial kNN was near zero or when high-hop spatial curves were not resolvable in low-density ST v1.0 geometry. DLPFC showed a mixed pattern, with both spatial and donor-associated effects.

The patient-associated channel should not be interpreted as a causal batch-effect estimate. It can include patient identity, section background, tissue processing, sample handling, cohort structure and biological heterogeneity. The result is that random spot splits can use structure that is not retained when patient-associated groups are separated.

### Dominant generalization-inflation channels vary across datasets and model classes

Figure 3 summarizes the central heterogeneity result. DLPFC showed both spatial and donor-associated effects. Andersson and Thrane were patient-channel dominant. Visium breast was spatial-channel dominant but single-patient. GSE278936 replicated the spatial-channel PCA+Ridge buffer response and provided a kNN boundary condition because random kNN performance was below zero.

This two-channel landscape explains why one split or one model cannot diagnose all settings. Spatial kNN is useful as a local-neighborhood probe when it has signal. PCA+Ridge provides a strong non-graph baseline. Corrected train-only GraphSAGE tests whether graph learning follows the same split-dependent behavior as simpler baselines.

### Apparent model advantage depends on evaluation regime

Model comparisons changed when the evaluation claim changed. Spatial kNN was strong in dense random or local settings but weak when spatial signal was absent or isolated. Corrected GraphSAGE retained random-split performance in some settings but showed strong patient-held-out losses in tumor datasets. PCA+Ridge often retained broader transfer signal better than a purely local spatial-neighbor baseline.

These observations argue against using a single random-split leaderboard as evidence of model superiority. A method can be useful for local interpolation while being less informative for patient transfer, and a model that appears robust under a spatial split may still lose performance under patient-held-out evaluation.

### SpatialLeak defines a hierarchy for spatial-omics generalization claims

SpatialLeak formalizes six evaluation tiers (Fig. 1 and Fig. 6). Level 0, random spot interpolation, supports local interpolation but does not establish spatial, section or patient transfer. Level 1, buffered spatial transfer, tests local neighborhood separation but does not establish patient transfer. Level 2, section-held-out transfer, tests transfer across sections but not necessarily across patients. Level 3, patient-held-out transfer, tests retention across patient-associated groups but does not establish dataset or platform transfer. Level 4, dataset-held-out transfer, tests broader dataset transportability. Level 5, cross-platform transfer, tests robustness when measurement platforms also change.

This hierarchy fixes the language of the manuscript. Visium breast supports dense Visium spatial and section-level evidence, not patient-level validation. GSE278936 supports spatial-channel replication, not clean patient-level validation. Andersson-to-Visium transfer remains a supplementary cross-platform stress test rather than a central validation claim.

## Discussion

SpatialLeak shows that apparent performance in spatial omics prediction can be inflated through separable spatial-neighborhood and patient-associated channels. Random spot-level evaluation overstated apparent predictive generalization in multiple settings, non-zero spatial buffers exposed local neighborhood dependence, patient-held-out tests revealed a distinct patient-associated channel, and the resulting evidence hierarchy clarified what each evaluation tier can claim.

The non-zero buffer result is important because non-overlapping spatial blocks do not necessarily create local independence. A test spot can remain close to a training neighborhood even when it is assigned to a different block. GSE278936 illustrates this point: hop0 was essentially unchanged, whereas hop2 and hop5 exposed a stable PCA+Ridge loss. This does not mean that every study requires hop5, but it does mean that spatial split definitions should report the exclusion distance they actually impose.

Spatial information itself is not leakage. Tissue architecture is often the object of spatial omics analysis, and a model should be allowed to use it when the intended claim is local interpolation or when the signal survives stricter separation. SpatialLeak is designed to determine whether spatial signal survives the evaluation tier implied by the biological claim, not to remove spatial context from spatial models.

Patient-associated performance loss is also not a single causal mechanism. A patient-held-out drop can reflect patient identity, section context, processing batch, sample handling, cohort structure, tissue biology or their combination. Public datasets do not always allow these components to be separated. The appropriate claim is therefore patient-associated performance inflation, not proof of a specific batch shortcut.

These findings suggest practical minimum expectations for future spatial omics benchmarks. Studies should report grouped splits, explicit spatial buffers, patient separation where the claim requires it, strong non-spatial baselines, spatial diagnostic baselines, uncertainty at the biological unit, transparent split metadata and code that reproduces the evaluation tier. Model rankings should be tied to the claim being tested rather than presented as universal.

The study has clear boundaries. The model set is diagnostic rather than exhaustive. Public datasets are heterogeneous in platform, tissue, density and sample structure. Visium breast is single-patient, GSE278936 public data contain one section per patient, DLPFC corrected GraphSAGE was not used as main evidence, and cross-platform transfer remains supplementary. Strict-split loss can include legitimate distribution shift as well as leakage-sensitive dependence. These limitations define the scope of inference but do not alter the central need to align evaluation design with the generalization claim.


## Methods

### Datasets

SpatialLeak used public spatial transcriptomics datasets covering DLPFC, HER2-positive breast cancer, melanoma, 10x Visium breast cancer and GSE278936 prostate Visium data. Restricted EGA validation data from the prostate study were not used. Dataset roles were defined by public sample structure: GSE278936 was used only as a spatial-channel replication dataset because the public release contains one section per patient.

### Preprocessing

Each section or sample was library-size normalized with `normalize_total(target_sum=1e4)` and transformed with `log1p`. Highly variable genes were selected with Scanpy's Seurat-flavor HVG procedure using up to 2000 genes. Slide or section identifiers and patient or donor metadata were retained where available. Spatial coordinates were normalized within slide for model input while preserving within-slide geometry for split construction.

### Target panels

Dataset-specific panels used the top 50 Moran-ranked genes after preprocessing. Moran ranking was computed on the processed dataset to define the prediction task, not to tune models or select results. Shared-panel analyses used the frozen `shared_panel_50` target set. Target selection was independent of downstream model performance and fixed across evaluation regimes.

### Split construction

Random spot splits used an 80/10/10 train/validation/test partition. Matched spatial block splits assigned grid blocks within each section to train, validation or test folds and selected balanced assignments using spot count, library size, Moran signal and layer composition where available. `matched_hop0` denotes non-overlapping block assignment without a positive exclusion buffer. Hop2 and hop5 splits removed test spots whose nearest training neighborhood was within fewer than two or five kNN graph hops. Patient-held-out splits held out all sections from a patient or donor where available. Slide-held-out splits held out sections but were not treated as patient-held-out unless patient identity was also separated.

### Spatial graph construction

Spatial graphs were built within slides only. kNN edges were calculated from spatial coordinates, preventing cross-slide graph connections. GraphSAGE used within-slide graph neighborhoods as input features but never aggregated test labels.

### Models

PCA+Ridge fit PCA only on training predictor genes and fit one Ridge model per target gene. Spatial kNN predicted target expression from spatially nearest training spots only, using inverse-distance weighting in normalized per-slide coordinates. GraphSAGE used train-only PCA and train-only feature scaling after the Phase 19 audit, two GraphSAGE layers, hidden dimension 128 in formal reruns, Adam optimization, validation-loss early stopping and no test metric for checkpoint selection.

### Metrics and inference

The primary metric was mean Pearson correlation across target genes. Leakage inflation was defined as `Perf_random - Perf_strict`. Relative leakage inflation (RLI) was defined as `(Perf_random - Perf_strict) / Perf_random`, and retention was defined as `Perf_strict / Perf_random`. RLI is operational and was not interpreted when absolute random mean Pearson was below 0.05. Random-size-matched controls downsampled the random split to comparable sample sizes without using strict-split performance. Bootstrap summaries used slide-level resampling. Wilcoxon signed-rank tests used paired seed or fold summaries with BH-FDR correction within comparison families. Mixed-effects analyses were run separately for patient and spatial channels with `inflation ~ moran_i + C(model)` and dataset random intercepts.

### Reproducibility

Seeds were frozen before final analyses. Test performance was not used for hyperparameter selection, checkpoint selection, target-panel selection or seed selection. Paper assets can be regenerated from frozen processed results with `python3 scripts/reproduce_paper_assets.py`; the current smoke test passes. Unit tests can be run with `python3 -m pytest`; the current suite passes.


## Data Availability

DLPFC, Andersson, Thrane, 10x Visium breast and GSE278936 public data were used from their cited public resources. Restricted EGA validation data from the prostate study were not used. Project-derived processed objects, split manifests and source data will be deposited before submission or publication. Repository URL and archival DOI will be inserted after release: `[GitHub repository URL]`, `[Zenodo DOI]`.

## Code Availability

Code used for preprocessing, split generation, benchmarking, statistical analyses, figure generation and source-data generation is prepared for public release at `[GitHub repository URL]` and archival deposition at `[Zenodo DOI]`.

## Author Contributions

`[Author contribution statement to be added.]`

## Funding

`[Funding statement to be added.]`

## Competing Interests

`[Competing interests statement to be added.]`

## Acknowledgements

`[Acknowledgements to be added.]`

## References

References are maintained in `manuscript/references_master.bib` for final Nature-style formatting.
