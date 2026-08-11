# SpatialLeak reveals distinct spatial-neighborhood and patient-level shortcuts in spatial omics prediction

## Abstract

Spatial omics prediction models are commonly evaluated with random spot-level train-test splits, although nearby tissue locations and samples from the same patient can share biological and technical information. This dependence can make apparent generalization difficult to interpret. We developed SpatialLeak, a leakage-resistant evaluation framework that compares random splits with spatial-buffer, slide-held-out, patient-held-out, dataset-held-out, and cross-platform stress tests across public spatial transcriptomics datasets. SpatialLeak quantified leakage inflation, relative leakage inflation, and strict-split retention for PCA+Ridge, Spatial kNN, and GraphSAGE under frozen target-gene panels and split definitions. Random spot splits inflated performance through two separable channels. In dense Visium breast data, Spatial kNN decreased from 0.649 under random splits to 0.132 under a matched_hop5 spatial buffer, whereas patient-held-out tests in Andersson and Thrane revealed strong patient/batch shortcuts for PCA+Ridge and GraphSAGE. In GSE278936 prostate Visium, PCA+Ridge showed little loss at hop0 but declined after non-zero spatial buffers, indicating that non-overlapping partitions alone can be insufficient. Spatial kNN had little predictive signal in this dataset, defining a model- and dataset-specific boundary condition. SpatialLeak provides a practical hierarchy for leakage-resistant spatial-omics evaluation and separates local dependence from transportable biological signal.

## Introduction

Spatial omics technologies measure molecular variation while preserving tissue location, creating opportunities to predict missing expression, transfer annotations, integrate modalities, and evaluate how tissue architecture shapes molecular state. These prediction tasks are increasingly used to compare computational models, including graph-based and representation-learning approaches. Their conclusions depend on whether the test observations are independent of the training observations in the way claimed by the study.

Random spot-level evaluation can violate this requirement. Neighboring spots often share morphology, molecular gradients, local cell-type composition, and technical context. Slides, sections, or regions from the same patient can also share patient-specific and batch-associated structure. A model can therefore achieve high random-split performance by exploiting information that would not be available when prediction is required across spatially separated regions, patients, sections, datasets, or platforms.

Existing evaluation protocols do not consistently separate these sources of apparent generalization. Some studies use section-, cluster-, patient-, or dataset-aware tests, but random spot or cell splits remain common, and strict splits are often reported without a shared metric for the resulting performance loss. This makes it difficult to decide whether a model has learned transportable biological structure or has benefited from local spatial-neighborhood dependence or patient-associated shortcuts.

Here we present SpatialLeak, a leakage-resistant benchmark framework for spatial omics prediction. SpatialLeak compares random spot splits with spatial-buffer, patient-held-out, slide-held-out, dataset-held-out, and cross-platform evaluation tiers; reports leakage inflation, relative leakage inflation, and retention; and evaluates PCA+Ridge, Spatial kNN, and GraphSAGE across public spatial transcriptomics datasets. The framework is designed to test whether apparent generalization under permissive random splits is retained under evaluation designs that better match the intended generalization claim.

The results support four conclusions. First, random spot-level splits can inflate apparent predictive generalization. Second, within-section spatial-neighborhood inflation and patient/batch shortcuts are separable channels that require different split designs. Third, non-zero spatial exclusion buffers can be necessary because non-overlapping spatial partitions may still preserve local train-test dependence. Fourth, apparent model advantage depends materially on the evaluation regime. SpatialLeak therefore reframes spatial omics benchmarking as a question of evidence hierarchy rather than a single leaderboard.

## Results

### Random spot-level splitting inflates apparent predictive generalization

SpatialLeak first evaluated whether random spot-level splits overestimated model performance relative to stricter evaluation designs. In dataset-specific target panels, PCA+Ridge achieved higher mean Pearson under random splits than under patient-held-out evaluation in DLPFC, Andersson HER2+ breast cancer, and Thrane melanoma. The corresponding patient-level relative leakage inflation (RLI) values were 0.213 in DLPFC, 0.662 in Andersson, and 0.499 in Thrane. These losses showed that the random-split advantage was not restricted to a single tissue, disease setting, or platform.

The magnitude of the loss differed across datasets. DLPFC retained more patient-held-out performance, with PCA+Ridge decreasing from 0.292 under random splits to 0.230 under patient-held-out evaluation. Andersson and Thrane showed larger patient-held-out losses, decreasing from 0.604 to 0.204 and from 0.653 to 0.327, respectively. This pattern indicated that random splits can capture dataset-specific structure that does not transfer across patients or donors.

The same conclusion held under a frozen shared target panel. In shared_panel_50, PCA+Ridge patient RLI values were 0.251 for DLPFC, 0.632 for Andersson, and 0.644 for Thrane. The shared-panel analysis reduced the possibility that the main result was driven by dataset-specific target-gene choices. It also showed that the patient/batch channel remained visible when the prediction task was held more constant across datasets.

Spatial kNN provided a boundary condition in low-density ST v1.0 datasets. In Andersson and Thrane, Spatial kNN random performance was near zero, making RLI unstable and unsuitable for interpretation. These rows were retained in the source tables but excluded from positive RLI claims. This rule became important throughout the manuscript: a low or negative random denominator is not evidence for or against leakage, but a setting in which relative inflation cannot be interpreted.

### Spatial exclusion buffers reveal within-section neighborhood leakage

Spatial-buffer splits tested whether local spatial proximity between training and test samples inflated apparent performance. In DLPFC, Spatial kNN decreased from 0.297 under random splits to 0.177 at matched_hop0, giving a spatial RLI of 0.402. PCA+Ridge also showed a spatial-buffer loss in DLPFC, with matched_hop0 RLI of 0.328. These results supported a within-section spatial-neighborhood channel in which nearby spots share information not removed by random spot assignment.

Dense Visium breast data showed the strongest spatial-neighborhood signal. Spatial kNN achieved a mean Pearson of 0.649 under random splits but decreased to 0.285 at matched_hop0, 0.229 at matched_hop2, and 0.132 at matched_hop5. The matched_hop5 RLI for Spatial kNN was 0.796. PCA+Ridge showed a smaller but consistent decline, from 0.597 under random splits to 0.442 at matched_hop5. These results indicate that local spatial neighborhoods can be a major source of apparent random-split performance in high-density Visium data.

The GSE278936 prostate Visium pilot added an independent spatial-channel replication with a different pattern. PCA+Ridge random performance was 0.374473, and matched_hop0 was essentially unchanged at 0.374584. Performance then decreased to 0.294437 at matched_hop2 and 0.291516 at matched_hop5, corresponding to RLI values of 0.214 and 0.222. This result indicates that non-overlapping spatial partitions alone can be insufficient; inflation became apparent only after imposing a non-zero spatial exclusion buffer.

GSE278936 also defined an important boundary. Spatial kNN random performance was below zero and RLI was not interpreted. This does not make the dataset a failed replication. It shows that the strength and mechanism of apparent spatial generalization are model- and dataset-dependent. In the manuscript, GSE278936 should be used as an independent high-density Visium spatial-channel replication for PCA+Ridge, not as evidence for patient-level validation or a universal kNN pattern.

### Patient-held-out evaluation uncovers a distinct shortcut channel

Patient-held-out evaluation tested a different source of apparent generalization. In Andersson, PCA+Ridge decreased from 0.604 under random splits to 0.204 under patient-held-out evaluation. GraphSAGE showed a similar patient-channel pattern, decreasing from 0.251 under random splits to 0.077 under patient-held-out evaluation, with patient RLI of 0.692. The matched_hop0 loss for GraphSAGE in the same dataset was only 0.072. This contrast shows that a model can appear spatially robust while still depending strongly on patient-associated structure.

Thrane showed the same patient-channel pattern. PCA+Ridge decreased from 0.653 under random splits to 0.327 under patient-held-out evaluation, and GraphSAGE decreased from 0.302 to 0.085, with patient RLI of 0.718. Spatial-buffer evidence in Thrane was weak or non-resolvable at larger hop distances, but the patient-held-out loss was substantial. This supports the conclusion that patient/batch shortcuts cannot be reduced to within-section spatial autocorrelation.

DLPFC provided a mixed case. PCA+Ridge patient RLI was 0.213 and Spatial kNN patient RLI was 0.120, while spatial-buffer RLI values were larger for both models. This suggests that DLPFC contains both local spatial dependence and patient-independent tissue structure. High retention under patient-held-out evaluation should not be treated as absence of spatial signal. It may indicate transportable biological organization that survives patient separation.

The final statistics refresh supported this channel separation. In the patient-channel mixed-effects model, the Moran coefficient was 0.007 with p = 0.932, indicating that patient-held-out loss was not explained by per-gene spatial autocorrelation alone. In the spatial-channel model, the Moran coefficient was positive but borderline, and the Spatial kNN model effect was significant. The manuscript should therefore avoid saying that Moran autocorrelation explains all leakage. Moran signal is most relevant to the within-section spatial channel, whereas patient-held-out loss reflects patient-, sample-, or batch-associated structure.

### The dominant leakage channel varies across datasets and model classes

The two-channel matrix summarizes the main manuscript logic. DLPFC showed both spatial-neighborhood and patient/donor separation effects, with the spatial channel more pronounced for Spatial kNN and GraphSAGE. Andersson showed a strong patient/batch channel for PCA+Ridge and GraphSAGE, while GraphSAGE spatial loss at matched_hop0 was small. Thrane also showed a patient-dominant pattern for PCA+Ridge and GraphSAGE. Visium breast showed a spatial-dominant pattern, especially for Spatial kNN, but could not support patient-level evaluation because it contained one patient.

GSE278936 should sit beside this matrix as a spatial-channel external replication rather than as a full two-channel row. Public GSE278936 contains 52 public patients and 52 public sections, so patient-held-out and section-held-out are nearly the same public design object. The restricted validation cohort was not used. The clean contribution of GSE278936 is therefore to test whether within-section spatial-buffer loss is reproducible in another high-density human Visium cohort.

This heterogeneity is a feature of the framework. SpatialLeak is not merely a test for one specific leakage mechanism. It distinguishes whether apparent generalization is attenuated by spatial isolation, patient separation, section separation, dataset transfer, or platform transfer. Different datasets can express different dominant channels, and different models can be sensitive to different channels.

The boundary conditions are part of the evidence. Thrane high-hop curves were not resolvable at larger buffers in the low-density ST v1.0 geometry. Spatial kNN was near zero in several ST v1.0 settings and below zero in GSE278936. Visium breast retained high slide-held-out performance despite strong spatial-buffer loss. These observations prevent overgeneralization and help define when a strict split tests local leakage, transportable biology, or a harder distribution shift.

### Leakage-resistant evaluation reshapes apparent model advantage

SpatialLeak next asked whether model advantage depended on the evaluation regime. GraphSAGE was included as a representative spatial graph neural network, not as a full SOTA model zoo. In DLPFC shared_panel_50, GraphSAGE decreased from 0.151 under random splits to 0.094 under matched_hop0, giving an RLI of 0.378. This aligned with the DLPFC spatial-neighborhood channel observed with simpler models.

In Andersson, GraphSAGE showed little matched_hop0 loss but large patient-held-out loss. It decreased from 0.251 under random splits to 0.233 under matched_hop0, then to 0.077 under patient-held-out evaluation. In Thrane, GraphSAGE patient RLI was 0.718. These results show that a graph model can still rely on patient- or batch-associated structure under permissive evaluation. Model complexity does not remove the need for split designs that match the intended claim.

Visium breast showed that GraphSAGE can also be sensitive to dense-platform spatial buffering. GraphSAGE decreased from 0.289 under random splits to 0.214 under matched_hop5, with spatial RLI of 0.262. This effect was smaller than the Spatial kNN loss but consistent with the idea that graph-connected local neighborhoods can preserve train-test dependence.

The interpretation is not that complex models fail. The point is that apparent model advantage is evaluation-regime dependent. A leaderboard based on random spot splits may reward signals that are unavailable under patient-held-out, spatially isolated, dataset-held-out, or cross-platform evaluation. Strong simple baselines and spatial-neighborhood probes are therefore necessary companions to graph or deep learning models in spatial omics prediction benchmarks.

### SpatialLeak defines a hierarchy for robust spatial-omics evaluation

The results support an evidence hierarchy for spatial omics prediction. Random spot splits are Level 0 and should be treated as permissive interpolation tests. Spatial-buffer splits with non-zero exclusion buffers are Level 1 and test within-section local dependence. Slide- or section-held-out tests are Level 2 and test cross-section transfer. Patient-held-out tests are Level 3 and test patient/donor separation. Dataset-held-out and cross-platform tests are Levels 4 and 5 and provide stronger stress tests of transportable signal.

This hierarchy clarifies why different datasets support different claims. Visium breast supports section-level and spatial-buffer conclusions, not patient-level validation. GSE278936 supports independent spatial-channel Visium replication in the public data, not clean patient/batch validation. Andersson and Thrane support patient-held-out claims but provide weak or non-resolvable spatial kNN/high-hop evidence. DLPFC supports both spatial and patient/donor separation, but with modest patient-channel loss compared with tumor datasets.

As a cross-platform stress test, SpatialLeak trained PCA+Ridge on Andersson and evaluated it on Visium breast using 49 usable shared targets. The model achieved mean Pearson 0.199 across five seeds, while the mean baseline was 0. This indicates feasible but weak cross-platform transfer. It should be interpreted as a stress test of transportable molecular signal, not as a replacement for patient-held-out validation.

SpatialLeak therefore proposes a minimum evaluation set for future spatial omics prediction studies: patient separation when labels permit it, section separation when patient separation is impossible, non-zero spatial buffers for within-section tests, exact split metadata, strong non-spatial baselines, spatial nearest-neighbor probes, patient/section-level uncertainty, dataset-held-out testing when feasible, an explicit distinction between transportable biology and local dependence, and reporting of boundary conditions and non-resolvable splits.

## Discussion

SpatialLeak shows that random spot-level splits can substantially inflate apparent spatial omics prediction performance. The effect persisted across dataset-specific target panels, a frozen shared target panel, and both simple and graph-based models. The benchmark supports a practical conclusion: random spot splits should not be treated as sufficient evidence of generalization in spatial omics prediction.

Spatial data violate conventional benchmark assumptions because observations are not exchangeable points. Spots near one another can share morphology, local cell composition, molecular gradients, and technical background. Graph models can also connect nearby observations explicitly. This spatial structure is biologically meaningful, but it becomes a benchmarking problem when train and test partitions are nominally separated while still sharing local information. Spatial-buffer tests make this dependence visible by asking whether performance is retained after local train-test neighborhoods are separated.

Spatial dependence is not intrinsically leakage. If a model uses tissue architecture that transfers across patients, datasets, or platforms, that signal may represent transportable biological structure. The DLPFC and Visium breast results illustrate this distinction. DLPFC retained substantial patient-held-out Spatial kNN performance, and Visium breast retained high slide-held-out performance even though spatial buffers strongly reduced within-section kNN performance. SpatialLeak is therefore not designed to remove all spatial information. It is designed to distinguish local dependence from the form of generalization being claimed.

Patient/batch shortcuts are a separate problem. Andersson and Thrane showed large patient-held-out losses for PCA+Ridge and GraphSAGE, while their spatial-channel behavior differed from DLPFC and Visium breast. The stratified mixed-effects analysis also showed that patient-held-out loss was not explained by per-gene Moran autocorrelation alone. A single strict split is therefore insufficient. Spatial isolation tests local dependence; patient-held-out evaluation tests patient-, section-, batch-, and sample-associated structure; dataset-held-out tests transportability across a broader source shift.

These results have direct implications for model benchmarking. GraphSAGE reproduced both spatial-buffer and patient-held-out sensitivity, depending on the dataset. This does not mean that graph models are inappropriate for spatial omics. It means that their reported advantage cannot be interpreted independently of split design. Future model papers should pair complex spatial models with strong simple baselines, spatial nearest-neighbor probes, and evaluation tiers that match the intended deployment or biological claim.

The study has limitations. It used public datasets with heterogeneous platforms, tissues, and sample structures. Not every dataset supported every evidence level. Visium breast contained one patient, so slide-held-out evaluation was section-level evidence rather than patient-level validation. Public GSE278936 contained 52 patients and 52 sections, preventing clean patient-versus-section separation in the public cohort. The analysis did not include a broad SOTA model zoo or foundation models because the purpose was to test evaluation regimes under frozen splits rather than to run an implementation contest. Patient/batch mechanisms could not always be causally decomposed into patient identity, tissue processing, section background, or cohort effects. Dataset-held-out transfer remained challenging and was treated as a stress test. These limitations bound the claims but do not undermine the central finding that permissive random evaluation can overstate apparent generalization through separable channels.

SpatialLeak should therefore be read as an evaluation framework, not a causal generative model of leakage. It quantifies how much performance under a permissive split is not retained under stricter evaluation designs. This language also addresses the distinction between leakage and distribution shift: strict-split loss may include legitimate distribution shift, but that is precisely why the split hierarchy must match the generalization claim. The practical recommendation is to report multiple evaluation tiers and to state explicitly whether the intended claim is local interpolation, section transfer, patient-level generalization, dataset transfer, or cross-platform transportability.

## Methods

### Study design

SpatialLeak was designed as an evaluation framework for spatial omics prediction. The benchmark compared random spot-level splits with leakage-resistant evaluation designs that separated training and test samples by spatial buffer, section, patient, dataset, or platform. The primary question was whether performance estimated under random spot-level evaluation was retained under stricter evaluation designs.

The main performance metric was mean Pearson correlation across target genes. For a random split and a strict split, leakage inflation (LI) was defined as `Perf_random - Perf_strict`. Relative leakage inflation (RLI) was defined as `(Perf_random - Perf_strict) / Perf_random`. Retention was defined as `Perf_strict / Perf_random`. RLI was not interpreted for model-dataset combinations in which random-split performance was near zero, because the denominator made the ratio unstable.

### Datasets and preprocessing

The benchmark used public spatial transcriptomics datasets representing DLPFC, HER2+ breast cancer, melanoma, 10x Visium breast, and GSE278936 prostate Visium. Processed analysis objects contained 47,681 spots for DLPFC, 13,620 spots for Andersson, 2,345 spots for Thrane, 7,785 spots for Visium breast, and 134,509 spots for the public GSE278936 prostate pilot. Andersson included eight patients, Thrane included four patients, Visium breast contained two sections from one patient, and public GSE278936 resolved to 52 patients and 52 sections.

Each dataset was converted to an analysis-ready AnnData object. Expression matrices were normalized per slide or section using total-count normalization to 10,000 followed by log transformation. Spatial coordinates, slide or section identifiers, patient or donor identifiers where available, and target-gene metadata were stored with the processed objects. Dataset-specific preprocessing checks included missing-gene handling after concatenation, coordinate recovery for ST spot identifiers, DLPFC layer-label merging by barcode keys, and GSE278936 public processed-file integrity checks.

### Target-gene panels

SpatialLeak evaluated dataset-specific and shared target panels. Dataset-specific panels used top Moran-ranked target genes available in each dataset. The shared_panel_50 target set was frozen before model evaluation from the intersection of highly variable genes shared across DLPFC, Andersson, and Thrane, ranked by average Moran signal. The GSE278936 pilot used the same shared_panel_50 target set and confirmed that all 50 targets were available.

### Split definitions

The random spot split assigned spots to train, validation, and test partitions without enforcing spatial, patient, slide, or dataset separation. This split served as the permissive comparator for estimating apparent performance under standard random spot-level evaluation.

Spatial-buffer splits enforced spatial separation between training and test samples. Matched-hop splits used within-slide kNN graph distance to require a minimum train-test hop buffer. Coordinate-buffer and region-buffer splits provided complementary checks where resolvable. When a high-hop or region-buffer split produced no usable test spots, the split was recorded as non-resolvable rather than replaced by a weaker split.

Patient-held-out splits held out all slides or sections from one patient or donor during testing. These splits tested whether performance transferred across patient or donor identity and associated sample structure. Slide-held-out splits held out a complete section and were used for Visium breast, where patient-held-out evaluation was impossible. Dataset-held-out transfer trained on one dataset and tested on another; the Andersson-to-Visium analysis used PCA+Ridge on 49 usable shared targets and excluded Spatial kNN because spatial coordinate systems were not comparable across platforms.

### Models

The Mean baseline predicted target expression using training-set means. PCA+Ridge used principal component feature reduction followed by Ridge regression and served as the main non-spatial predictive baseline. Spatial kNN predicted expression from spatially neighboring training spots and served as a direct probe for spatial-neighborhood leakage. GraphSAGE was included as a representative spatial graph neural network to test whether a graph-based model followed the same evaluation-dependent patterns as simpler baselines.

### Reproducibility settings

Target panels, split definitions, LI, RLI, retention, seed handling, and the near-zero denominator rule were frozen before the Phase 17 manuscript rewrite. Formal DLPFC analyses used 10 seeds for random and matched spatial splits. Andersson and Thrane formal baselines used multiple seeds and deterministic patient folds where patient labels were available. The GSE278936 spatial pilot used seeds 0-4, shared_panel_50, Mean, PCA+Ridge, Spatial kNN, and random, matched_hop0, matched_hop2, and matched_hop5 splits. GraphSAGE runs used a lightweight PyTorch implementation with fixed settings described in the project reports.

### Statistical analysis

Paired random-versus-strict comparisons were tested with Wilcoxon signed-rank tests and Benjamini-Hochberg false-discovery-rate correction where formal statistical testing was performed. Slide-level bootstrap procedures were used where appropriate; spot-level confidence intervals were not used. Mixed-effects models were used to separate patient/batch and spatial-neighborhood channels. The patient-channel model excluded Visium breast because it did not support patient-held-out evaluation. The spatial-channel model used configured spatial splits and was interpreted as supportive rather than definitive because the number of datasets was small.

### Integrity controls

The analysis lock prohibited test-set tuning, seed cherry-picking, target-gene reselection based on model performance, spot-level pseudoreplication, and substituting slide-held-out results for patient-held-out validation. Split metadata and output suffixes were retained to avoid overwriting formal benchmark results. Boundary conditions, including non-resolvable high-hop splits and near-zero random denominators, were preserved in the reports and source tables.

## Data availability

[Placeholder: list public data accessions, processed data locations, and any repository links after final deposition decisions. Do not include restricted EGA data because it was not used.]

## Code availability

[Placeholder: provide repository URL, commit or release identifier, environment file, and instructions for reproducing paper assets after final repository preparation.]

## Author contributions

[Placeholder: author names and contribution taxonomy to be supplied by the user.]

## Funding

[Placeholder: funding sources to be supplied by the user.]

## Competing interests

[Placeholder: competing interest statement to be supplied by the user.]

## Acknowledgements

[Placeholder: acknowledgements to be supplied by the user.]

## References

[Placeholder: insert verified references after target journal and reference style are selected.]

