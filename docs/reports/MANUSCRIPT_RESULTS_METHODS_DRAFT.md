# Manuscript Results and Methods Draft

> Updated: 2026-08-09 22:23  
> Scope: Results and Methods prose draft only. No Word/PDF formatting. No invented references.

## One-Sentence Argument

In spatial omics prediction benchmarks, SpatialLeak shows that random spot-level splits inflate apparent generalization through separable spatial-neighborhood and patient/batch shortcut channels, using frozen leakage-resistant splits, shared target panels, multiple model classes, and cross-platform stress testing across DLPFC, HER2+ breast, melanoma, and Visium breast datasets.

## Terminology Ledger

| Canonical term | First-use definition | Use |
|---|---|---|
| SpatialLeak | Leakage-resistant benchmark framework for spatial omics prediction | Framework name |
| random spot split | Random assignment of spots or cells to train/test partitions | Leakage-prone comparator |
| leakage-resistant split | Split that separates train and test samples by spatial buffer, patient, slide, or dataset | Umbrella term |
| spatial-buffer split | Matched split enforcing a kNN-hop or coordinate-distance train-test buffer | Within-section spatial leakage test |
| patient-held-out split | Split holding out all slides from one patient or donor | Patient/batch shortcut test |
| slide-held-out split | Split holding out one whole section or slide | Visium breast strict split |
| dataset-held-out transfer | Training on one dataset and testing on another | Cross-platform stress test |
| leakage inflation (LI) | `Perf_random - Perf_strict` | Absolute leakage metric |
| relative leakage inflation (RLI) | `(Perf_random - Perf_strict) / Perf_random` | Main normalized leakage metric |
| retention | `Perf_strict / Perf_random` | Strict-split performance retention |
| shared_panel_50 | Frozen 50-gene ENSG-anchored target panel shared across DLPFC, Andersson, and Thrane | Cross-dataset comparable target set |
| PCA+Ridge | PCA feature reduction followed by Ridge regression | Strong non-spatial baseline |
| Spatial kNN | Spatial nearest-neighbor expression baseline | Spatial-neighborhood leakage probe |
| GraphSAGE | Lightweight spatial graph neural network | Representative complex spatial model |

## Section Outline

1. Results 1: Random spot splits inflated apparent performance in dataset-specific target panels.
2. Results 2: The same conclusion held under a frozen shared target panel.
3. Results 3: Dense Visium data exposed strong within-section spatial-neighborhood leakage.
4. Results 4: Slide-held-out Visium performance remained high but did not establish patient-level generalization.
5. Results 5: GraphSAGE reproduced the two-channel leakage pattern.
6. Results 6: Cross-platform dataset-held-out transfer was feasible but weak.
7. Methods: Datasets, preprocessing, target panels, split definitions, models, metrics/statistics, and integrity controls.

## Draft: Results

### Random spot splits inflated apparent generalization across datasets

SpatialLeak first evaluated whether random spot-level train-test splits overestimated model performance relative to leakage-resistant partitions. In dataset-specific target panels, PCA+Ridge achieved higher mean Pearson under random splits than under patient-held-out evaluation in DLPFC, Andersson HER2+ breast cancer, and Thrane melanoma. The corresponding patient-level RLI values were 0.213 in DLPFC, 0.662 in Andersson, and 0.499 in Thrane (Fig. 1a). These losses showed that the performance gap was not restricted to a single tissue, disease setting, or platform.

The magnitude of the loss differed across datasets. DLPFC retained more patient-held-out performance, with PCA+Ridge decreasing from 0.292 under random splits to 0.230 under patient-held-out evaluation. Andersson and Thrane showed larger patient-held-out losses, decreasing from 0.604 to 0.204 and from 0.653 to 0.327, respectively. This pattern indicated that random splits can capture dataset-specific shortcuts that do not transfer across patients or donors.

Spatial kNN behaved differently across platforms. In DLPFC, Spatial kNN decreased from 0.297 under random splits to 0.177 under matched_hop0 and 0.261 under patient-held-out evaluation. In Andersson and Thrane, Spatial kNN performance was near zero under random splits, so RLI values for this model were not interpreted when the denominator was unstable. These results separated a meaningful spatial-neighborhood leakage probe from settings in which spatial nearest-neighbor prediction was not a useful baseline.

### Shared target panels preserved the main leakage conclusion

SpatialLeak next tested whether the leakage effect depended on dataset-specific target-gene selection. A frozen shared_panel_50 target set was constructed before performance computation and then evaluated across DLPFC, Andersson, and Thrane. PCA+Ridge again showed lower performance under patient-held-out evaluation than under random spot splits, with patient RLI values of 0.251, 0.632, and 0.644, respectively (Fig. 1b).

The shared-panel analysis clarified the balance between transferable biological signal and patient/batch shortcut signal. DLPFC retained 74.9% of PCA+Ridge random-split performance under patient-held-out evaluation, consistent with a signal that partly transfers across donors. Andersson and Thrane retained 36.8% and 35.6%, respectively, which showed that the random-split advantage in these datasets was dominated by non-transferable patient or batch structure. The common target panel therefore supported the main conclusion without relying on dataset-specific gene choices.

### Spatial-neighborhood leakage was strongest in dense Visium data

Spatial-buffer splits tested whether local spatial proximity between training and test samples inflated apparent performance. In DLPFC, Spatial kNN performance decreased as the train-test buffer expanded, from 0.177 at matched_hop0 to 0.089 at matched_hop5. PCA+Ridge also decreased across the matched-hop curve, from 0.196 at matched_hop0 to 0.157 at matched_hop5 (Fig. 2a).

The same analysis produced a stronger spatial-neighborhood signal in the Visium breast dataset. Spatial kNN achieved a mean Pearson of 0.649 under random splits but decreased to 0.285 at matched_hop0, 0.229 at matched_hop2, and 0.132 at matched_hop5. The matched_hop5 RLI for Spatial kNN was 0.796 (Fig. 1a and Fig. 2c). PCA+Ridge showed a smaller but consistent decline, from 0.597 under random splits to 0.442 at matched_hop5.

The low-density ST v1.0 datasets provided an important boundary condition. Andersson retained high PCA+Ridge performance at matched_hop0 and matched_hop2 but decreased at matched_hop5, whereas Spatial kNN remained weak under all matched buffers (Fig. 2b). Thrane high-hop and region-buffer splits were not plotted because the corresponding strict test sets became empty or non-resolvable at larger hop thresholds. Spatial-buffer evaluation therefore depends on platform density, and empty high-hop tests should be reported rather than silently replaced by easier splits.

### Slide-held-out Visium performance did not establish patient-level generalization

The Visium breast dataset contained two sections from a single patient, so SpatialLeak treated slide-held-out evaluation as a strict section-level test rather than patient-held-out validation. PCA+Ridge achieved 0.597 under random splits and 0.580 under slide-held-out evaluation. Spatial kNN achieved 0.649 under random splits and 0.552 under slide-held-out evaluation. These values corresponded to high slide-level retention, especially compared with the spatial-buffer loss observed for Spatial kNN.

This contrast separated two claims that are often conflated. Slide-held-out performance showed that adjacent Visium sections shared transportable tissue structure, but it did not test whether a model generalized to a different patient. The same dataset showed strong spatial-neighborhood leakage under hop buffers. Visium breast therefore served as a dense-platform contrast for within-section leakage, not as external patient-level validation.

### GraphSAGE reproduced the two-channel leakage pattern

SpatialLeak included GraphSAGE to test whether a representative spatial graph model followed the same leakage structure as simpler baselines. In the shared_panel_50 setting, DLPFC GraphSAGE decreased from 0.151 under random splits to 0.094 under matched_hop0, giving an RLI of 0.378 (Fig. 3a). This result aligned with the DLPFC spatial-neighborhood channel observed with Spatial kNN and PCA+Ridge.

Andersson showed a different pattern. GraphSAGE decreased only modestly from 0.251 under random splits to 0.233 under matched_hop0, but it decreased to 0.077 under patient-held-out evaluation. The corresponding patient RLI was 0.692 (Fig. 3a). This showed that a graph neural network could still rely on patient- or batch-associated structure under random spot splits. Model complexity therefore did not remove the need for leakage-resistant evaluation.

### Cross-platform dataset-held-out transfer was feasible but weak

As a final stress test, SpatialLeak trained PCA+Ridge on Andersson HER2+ breast cancer and evaluated it on Visium breast using the shared target panel. Forty-nine of the 50 shared targets were usable because `SEPT4` was absent from the Visium breast data. Spatial kNN was excluded from this analysis because spatial coordinates are not comparable across platforms and tissues.

The Andersson-to-Visium transfer achieved a mean Pearson of 0.199 across five seeds, while the mean baseline was 0 (Fig. 3b). This result showed that cross-platform transfer was possible but substantially weaker than within-dataset random or slide-held-out performance in Visium breast. Dataset-held-out transfer should therefore be interpreted as a stress test of transportable molecular signal rather than as a replacement for patient-held-out validation.

### Statistical models separated spatial and patient leakage channels

The statistical analysis distinguished the pooled leakage signal from channel-specific explanations. In the early pooled analysis, per-gene Moran autocorrelation tracked performance inflation across leakage-resistant comparisons and supported the GO-D criterion. The final analysis separated patient/batch leakage from within-section spatial-neighborhood leakage because these mechanisms have different biological and technical interpretations.

In the patient-channel mixed-effects model, the Moran coefficient was 0.007 with p = 0.932, after excluding Visium breast because it lacked patient-held-out folds. This result showed that patient-held-out loss was not explained by per-gene spatial autocorrelation alone. In the spatial-channel model, the Moran coefficient was positive but not conventionally significant (0.167, p = 0.079), while the Spatial kNN model effect was significant (p = 0.0058). The final interpretation is therefore not that Moran autocorrelation explains all leakage. Spatial autocorrelation remains relevant to within-section spatial leakage, whereas patient-held-out loss reflects a separate patient or batch shortcut channel.

## Draft: Methods

### Study design

SpatialLeak was designed as an evaluation framework for spatial omics prediction rather than a new prediction model. The benchmark compared random spot splits with leakage-resistant splits that separated training and test samples by spatial buffer, patient, slide, or dataset. The primary question was whether performance estimated under random spot-level evaluation was retained under stricter evaluation designs.

The benchmark used mean Pearson correlation as the main performance metric. For each strict split, leakage inflation was defined as `Perf_random - Perf_strict`, and relative leakage inflation was defined as `(Perf_random - Perf_strict) / Perf_random`. Retention was defined as `Perf_strict / Perf_random`. RLI was not interpreted for model-dataset combinations in which random-split performance was near zero, because the denominator made the ratio unstable.

### Datasets and preprocessing

The benchmark used four public spatial omics datasets: DLPFC, Andersson HER2+ breast cancer, Thrane melanoma, and 10x Visium breast. The processed analysis objects contained 47,681 spots for DLPFC, 13,620 spots for Andersson, 2,345 spots for Thrane, and 7,785 spots for Visium breast. Andersson included eight patients, Thrane included four patients, and Visium breast contained two sections from a single patient.

Each dataset was converted to an analysis-ready AnnData object. Expression matrices were normalized with total-count normalization to 10,000 counts per spot followed by log transformation. Spatial coordinates, slide or section identifiers, patient or donor identifiers where available, and target-gene metadata were stored with the processed objects. Dataset-specific preprocessing checks included missing-gene handling after concatenation, coordinate recovery for ST spot identifiers, and DLPFC layer-label merging by barcode keys.

### Target-gene panels

SpatialLeak evaluated both dataset-specific and shared target panels. Dataset-specific panels used the top Moran-ranked target genes available in each dataset. The shared_panel_50 target set was constructed before model evaluation from the intersection of highly variable genes shared across DLPFC, Andersson, and Thrane. The final shared panel contained 50 ENSG-anchored genes selected by average Moran rank across datasets.

The shared-panel analysis was used to test whether leakage estimates persisted when the prediction target set was held constant across datasets. In the Andersson-to-Visium dataset-held-out stress test, 49 of the 50 shared targets were usable because `SEPT4` was absent from the Visium breast data.

### Split definitions

The random spot split assigned spots to train and test partitions without enforcing spatial, patient, slide, or dataset separation. This split represented the leakage-prone comparator used to estimate apparent performance under standard random spot-level evaluation.

Spatial-buffer splits enforced spatial separation between training and test samples. Matched-hop splits used kNN graph distance to require a minimum train-test hop buffer. Coordinate-buffer and region-buffer splits provided complementary spatial separation checks. When a high-hop or region-buffer split produced no usable test spots, the split was recorded as non-resolvable instead of being replaced by a weaker test.

Patient-held-out splits held out all slides or sections from one patient or donor during testing. These splits tested whether model performance transferred across patient or donor identity. Slide-held-out splits held out one complete section and were used for Visium breast, where patient-held-out evaluation was impossible because only one patient was present.

Dataset-held-out transfer trained on one dataset and tested on another. The Andersson-to-Visium analysis used PCA+Ridge on the shared target panel and excluded Spatial kNN because spatial coordinate systems are not comparable across datasets.

### Models

The Mean baseline predicted target expression using training-set means. PCA+Ridge used principal component feature reduction followed by Ridge regression and served as the main non-spatial predictive baseline. Spatial kNN predicted expression from spatially neighboring training spots and served as a direct probe for spatial-neighborhood leakage.

GraphSAGE was included as a representative spatial graph neural network. The model was evaluated on DLPFC and Andersson in the shared_panel_50 setting. These runs tested whether a more complex graph model followed the same leakage patterns observed for simpler baselines.

### Reproducibility parameter table

| Component | Locked setting |
|---|---|
| Target genes | 50 target genes per dataset-specific panel; shared_panel_50 frozen before model evaluation |
| Feature genes | Top 2,000 available HVG features after excluding target genes |
| Normalization | Per-slide total-count normalization to 10,000 followed by `log1p` |
| Random split | 80% train, 10% validation, 10% test |
| Formal DLPFC seeds | 0-9 for random and matched spatial splits |
| External formal seeds | 0-9 for Andersson/Thrane formal baselines; GraphSAGE shared-panel external run used seeds 0-4 plus patient folds |
| Patient folds | Leave-one-patient/donor-out where patient/donor labels were available |
| Slide folds | Leave-one-section-out for Visium breast because only one patient was available |
| Matched block construction | 3 x 3 per-slide grid blocks; 300 candidate assignments per seed; selected by train-test composition distance |
| Hop buffers | matched_hop0, matched_hop1, matched_hop2, matched_hop5; region_hop5 and region_hop10 where resolvable |
| kNN graph for hop buffers | Within-slide kNN graph with k = 15 |
| Coordinate buffers | z-scaled coordinate buffers 0.25, 0.5, and 1.0 where used |
| PCA+Ridge | 64 PCA components; Ridge alpha = 1.0 |
| Spatial kNN | k = 15; inverse-distance weighting; per-slide coordinate scaling |
| GraphSAGE | Two SAGE layers; PCA-64 input features; within-slide kNN graph k = 10 with self-loops; hidden dimension 128 in formal/shared-panel runs; Adam lr = 1e-3; epochs up to 500; early stopping patience = 60; CPU execution |
| Metrics | Per-gene Pearson, aggregated as mean Pearson for main performance |
| Multiple testing | Wilcoxon signed-rank tests with Benjamini-Hochberg FDR correction |
| Bootstrap | Slide-level bootstrap for formal DLPFC analyses; spot-level confidence intervals not used |

### Statistical analysis

Formal DLPFC analyses used 10 seeds for random and matched spatial splits. External formal analyses used multiple seeds for random and matched spatial-buffer splits and patient folds where patient labels were available. Paired random-versus-strict comparisons were tested with Wilcoxon signed-rank tests and Benjamini-Hochberg false-discovery-rate correction. Slide-level bootstrap procedures were used where appropriate; spot-level confidence intervals were not used.

Mixed-effects models were used to separate patient/batch and spatial-neighborhood leakage channels. The patient-channel model excluded Visium breast because it did not support patient-held-out evaluation. The spatial-channel model used each dataset's configured spatial split. The final channel-separated model showed that patient/batch leakage was not explained by per-gene Moran autocorrelation alone, while the spatial channel retained a positive Moran trend and a significant Spatial kNN model effect.

### Integrity controls

Analysis decisions were frozen before the final paper assets were generated. These included the definitions of LI, RLI, and retention; the shared_panel_50 construction; seed handling; the constant-prediction Pearson convention; and the rule that empty strict splits must be reported as non-resolvable. Split metadata and output suffixes were retained to avoid overwriting formal benchmark results.

All plotted values in the first figure package were generated from frozen CSV files in `results/paper_assets/`. The figure script produced editable SVG files and high-resolution PNG previews. No PDF outputs were generated by default.

### Software environment

The current analysis environment used system Python 3.9.6 on macOS arm64. The key package versions recorded from the active environment were: NumPy 1.26.4, pandas 2.3.3, SciPy 1.13.1, scikit-learn 1.6.1, Scanpy 1.10.3, AnnData 0.10.9, h5py 3.14.0, statsmodels 0.14.6, Matplotlib 3.9.4, seaborn 0.13.2, Pillow 11.3.0, PyTorch 2.8.0, and pytest 8.4.2. The GraphSAGE implementation used the lightweight PyTorch module in `src/models/graphsage.py`; `torch-geometric` was not installed in the active environment.

| Component | Version / status |
|---|---|
| Python | 3.9.6 |
| Platform | macOS-26.4-arm64-arm-64bit |
| NumPy | 1.26.4 |
| pandas | 2.3.3 |
| SciPy | 1.13.1 |
| scikit-learn | 1.6.1 |
| Scanpy | 1.10.3 |
| AnnData | 0.10.9 |
| h5py | 3.14.0 |
| statsmodels | 0.14.6 |
| Matplotlib | 3.9.4 |
| seaborn | 0.13.2 |
| Pillow | 11.3.0 |
| PyTorch | 2.8.0 |
| torch-geometric | not installed; not used |
| pytest | 8.4.2 |

## Citation-Ready Scaffold: Introduction

Selected structure: general-to-specific-setting. The Introduction should be compact, about four paragraphs, and should use verified references only after the reference audit is completed.

| Paragraph | Job | Draft content target | Citation need |
|---|---|---|---|
| 1 | Field stake | Spatial omics assays measure molecular profiles in tissue context, making prediction tasks attractive for imputing genes, transferring labels, and evaluating spatial structure. | Foundational spatial transcriptomics / Visium / spatial omics prediction references |
| 2 | Bottleneck | Many prediction studies use random spot or cell splits, but nearby tissue locations and same-patient slides can violate independence assumptions. | Prior ML evaluation / spatial data leakage / random split examples from split audit |
| 3 | Prior attempts and unresolved gap | Some studies use section-, slide-, cluster-, or patient-aware splits, but protocols differ and often do not separate spatial-neighborhood leakage from patient/batch shortcuts. | Audited papers with strict split examples; benchmark/evaluation references |
| 4 | Present study | SpatialLeak defines leakage-resistant splits and metrics, compares simple and graph models, evaluates dataset-specific and shared panels, and separates spatial-neighborhood from patient/batch channels across four datasets. | No citation needed beyond methods/results; cite code/data availability later |

### Introduction paragraph skeleton

Spatial omics technologies measure molecular variation while preserving tissue location, creating opportunities to predict missing expression, transfer annotations, and evaluate how tissue architecture shapes molecular state. These prediction tasks are increasingly used to compare models, but their conclusions depend on whether the test samples are independent of the training samples.

Random spot-level evaluation can violate this independence requirement. Neighboring spots often share morphology, molecular gradients, and technical context, while slides from the same patient can share patient- or batch-specific structure. A model can therefore achieve high random-split performance by exploiting signals that are unavailable when prediction is required across spatially separated regions, patients, slides, or datasets.

Existing evaluation protocols do not consistently separate these leakage channels. Some studies adopt section-, cluster-, or patient-aware tests, but random spot splits remain common, and strict splits are often reported without a shared metric for the resulting performance loss. This makes it difficult to decide whether a model has learned transportable biological structure or has benefited from spatial-neighborhood or patient-associated shortcuts.

Here we present SpatialLeak, a leakage-resistant benchmark framework for spatial omics prediction. SpatialLeak compares random spot splits with spatial-buffer, patient-held-out, slide-held-out, and dataset-held-out tests; reports leakage inflation, relative leakage inflation, and retention; and evaluates PCA+Ridge, Spatial kNN, and GraphSAGE across DLPFC, HER2+ breast cancer, melanoma, and Visium breast datasets. This design tests whether apparent generalization under random splits is retained under stricter evaluation, and whether the loss arises from within-section spatial leakage, patient/batch shortcuts, or both.

## Citation-Ready Scaffold: Discussion

Selected structure: central advance -> mechanisms -> practice -> limits -> future use. The Discussion should compare directly with verified prior work after the reference list is built.

| Paragraph | Job | Draft content target | Citation need |
|---|---|---|---|
| 1 | Central advance | Random spot splits inflate spatial omics prediction performance across datasets, target panels, and model classes. | None beyond Results |
| 2 | Mechanism separation | Patient/batch shortcuts and spatial-neighborhood leakage are different mechanisms and should not be collapsed into one explanation. | Prior spatial autocorrelation / batch effect / evaluation leakage references |
| 3 | Relation to model complexity | GraphSAGE reproduced leakage sensitivity, so strict evaluation is needed even for spatial graph models. | Graph neural network / spatial prediction references |
| 4 | Practical reporting recommendations | Papers should report strong non-spatial baselines, spatial-neighborhood probes, patient/slide separation, split metadata, and unstable denominator rules. | Benchmark/reporting guideline references if available |
| 5 | Limitations | Public datasets, limited patient-rich Visium validation, CPU-feasible model set, no SOTA main analysis, non-resolvable high-hop splits in low-density ST v1.0. | None unless discussing dataset sources |
| 6 | Future directions | Add more patient-rich datasets, audited SOTA models, multi-omics tasks, and external validation under frozen splits. | Optional |

### Discussion paragraph skeleton

SpatialLeak shows that random spot-level splits can substantially overestimate spatial omics prediction performance. The effect persisted across dataset-specific target panels, a frozen shared target panel, and both simple and graph-based models. The benchmark therefore supports a practical conclusion: random spot splits should not be treated as sufficient evidence of generalization in spatial omics prediction.

The results also show that leakage is not a single mechanism. DLPFC and dense Visium analyses exposed within-section spatial-neighborhood leakage, especially for Spatial kNN and GraphSAGE-like spatial models. Andersson and Thrane showed stronger patient-held-out losses, consistent with patient or batch shortcuts that were not explained by per-gene Moran autocorrelation alone. Separating these channels is important because the appropriate strict split depends on the scientific claim being tested.

Model complexity did not remove the need for leakage-resistant evaluation. GraphSAGE showed substantial spatial-buffer loss in DLPFC and large patient-held-out loss in Andersson. This does not imply that graph models are inappropriate for spatial omics. It shows that their reported performance should be interpreted through split designs that match the intended deployment setting.

The benchmark suggests several reporting practices for future spatial omics prediction studies. A random split can remain useful as an upper-bound or internal interpolation check, but it should be paired with a strong non-spatial baseline, a spatial-neighborhood leakage probe, and patient-, slide-, or dataset-separated tests where the data support them. Studies should also report split metadata, buffer definitions, empty strict splits, and RLI only when the random-split denominator is large enough to interpret.

This study has boundaries. The analysis used public datasets and CPU-feasible models, and the Visium breast dataset contained one patient, so it could not support patient-held-out validation. High-hop spatial buffers were not resolvable in Thrane because the low-density ST v1.0 geometry left too few test spots. The current main analysis does not include additional SOTA models because those runs require split-protocol, license, compatibility, and compute audits before they can be interpreted fairly.

Future extensions should add patient-rich Visium datasets, audited SOTA models under the same frozen splits, and multi-omics prediction tasks where modality and spatial leakage can interact. These extensions should preserve the core principle of the framework: evaluation should test the form of generalization claimed by the study, rather than only the easiest random partition available.

## Reference Audit Candidates

> Status: candidate placement map only. These entries were verified from local audit notes and online primary or index pages on 2026-08-09. Do not convert to a final reference list until the target journal style is chosen.

| Candidate | Verified locator | Manuscript use | Placement |
|---|---|---|---|
| Maynard et al., transcriptome-scale spatial gene expression in human DLPFC | Nature Neuroscience 2021; DOI `10.1038/s41593-020-00787-0`; PubMed / spatialLIBD pages verified | DLPFC source dataset and spatial layer context | Methods, Datasets |
| Andersson HER2+ breast cancer spatial transcriptomics data | Zenodo record `10.5281/zenodo.4751624`; associated article/data pages verified | HER2+ breast ST v1.0 source dataset | Methods, Datasets |
| Thrane et al., spatially resolved transcriptomics in melanoma | Cancer Research 2018; DOI `10.1158/0008-5472.CAN-18-0747`; PubMed / AACR dataset page verified | Thrane melanoma ST v1.0 source dataset | Methods, Datasets |
| 10x Genomics Human Breast Cancer Block A Section 1/2 | 10x Genomics dataset page, Space Ranger 1.1.0 | Visium breast source dataset | Methods, Datasets |
| MultiVI | Nature Methods 2023; DOI `10.1038/s41592-023-01909-9` | High-impact random cell split example from split audit | Introduction paragraph 2 or Discussion relation to prior practice |
| ST-Net | Nature Biomedical Engineering 2020; DOI `10.1038/s41551-020-0578-x` | Strict patient leave-one-out positive control from split audit | Introduction paragraph 3 or Discussion reporting recommendations |
| BABEL | PNAS 2021; DOI `10.1073/pnas.2023070118` | Cluster-based anti-memorization split example | Introduction paragraph 3 or Discussion reporting recommendations |
| SpaGE | Nucleic Acids Research 2020; DOI `10.1093/nar/gkaa740` | Spatial gene prediction/imputation background; coordinate use mainly for evaluation | Introduction paragraph 1 or prior-work paragraph |
| GraphSAGE | NeurIPS 2017 proceedings / arXiv `1706.02216` | Conceptual source for the representative graph model family | Methods, Models |
| NicheTrans | Nature Methods 2026; DOI `10.1038/s41592-026-03153-3`; PubMed verified | Recent SOTA candidate and split-audit discussion, not main benchmark | Discussion future SOTA audit / limitations |
| HisToGene | bioRxiv 2021; DOI `10.1101/2021.11.28.470212` | Section-level but not necessarily patient-separated split example from local code audit | Discussion relation to prior practice, with UNVERIFIED method-text caveat |
| SpatialGlue | Nature Methods 2024; DOI `10.1038/s41592-024-02316-4` | Future SOTA audit candidate for spatial multi-omics integration | Discussion future directions only |

## Citation Placement Map

| Scaffold claim | Candidate citations | Notes |
|---|---|---|
| Spatial omics preserves tissue location and supports prediction/imputation tasks | Maynard et al.; SpaGE; ST-Net | Add one technology/dataset citation and one prediction/imputation citation. |
| Random cell/spot splits remain used in high-impact benchmarks | MultiVI; local split audit | Use exact split wording only after checking article Methods or code. |
| Section-level splits do not guarantee patient-level separation | HisToGene local code audit; ST-Net as contrast | Keep caveat that HisToGene method-text verification is incomplete. |
| Strict evaluation is feasible and publishable | ST-Net; BABEL | Use as positive controls, not as criticism of other studies. |
| Spatial graph / spatial multi-omics methods warrant split-aware evaluation | GraphSAGE; SpatialGlue; NicheTrans | Frame as motivation for auditing model classes, not as a claim that these methods are flawed. |
| Dataset sources and sample counts | Maynard et al.; Zenodo Andersson; Thrane; 10x Genomics | Cite in Methods and Data availability, not Results. |

## Claim-Evidence Map

| Claim | Evidence | Status |
|---|---|---|
| Random spot splits inflated apparent generalization | Dataset-specific PCA+Ridge patient RLI: DLPFC 0.213, Andersson 0.662, Thrane 0.499 | Supported |
| The result was not driven by dataset-specific target selection | shared_panel_50 PCA+Ridge patient RLI: DLPFC 0.251, Andersson 0.632, Thrane 0.644 | Supported |
| Dense Visium data showed strong spatial-neighborhood leakage | Visium Spatial kNN random 0.649 to matched_hop5 0.132; RLI 0.796 | Supported |
| Slide-held-out Visium performance was not patient-held-out validation | Visium breast has one patient; slide-held-out PCA+Ridge 0.580 and Spatial kNN 0.552 | Supported |
| GraphSAGE did not remove leakage sensitivity | DLPFC GraphSAGE matched_hop0 RLI 0.378; Andersson patient RLI 0.692 | Supported |
| Dataset-held-out transfer was feasible but weak | Andersson-to-Visium PCA+Ridge mean Pearson 0.199 across five seeds | Supported as stress test |
| Spatial autocorrelation explains all leakage | Final mixed-effects models split by channel did not support this | Rejected / reframed |

## Assumptions or Missing Inputs

- Target journal, abstract format, and word limits remain unspecified.
- Final reference list is not yet inserted; Results and Methods intentionally avoid fabricated citations.
- The software version table was captured from the active environment and should be rechecked on the final submission machine.
- Author, affiliation, funding, data availability, and code availability statements remain to be supplied.

## Why This Structure

- Results lead with the strongest benchmark finding before mechanism and stress-test sections.
- Patient/batch leakage and spatial-neighborhood leakage are separated throughout to avoid over-attributing all inflation to Moran autocorrelation.
- Methods define each split before each model, because the paper's contribution is primarily evaluation design.
- Boundary statements are kept close to the evidence: Visium is not patient-level validation, and dataset-held-out transfer is a stress test.
