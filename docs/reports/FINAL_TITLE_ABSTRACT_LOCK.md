# Final Title And Abstract Lock

## Title Candidates

| Candidate | Novelty clarity | Overclaim risk | Journal fit | Length | Memorability |
|---|---:|---:|---:|---:|---:|
| Leakage-resistant benchmarking reveals two channels of inflated generalization in spatial omics prediction | 5 | 2 | 5 | 4 | 4 |
| SpatialLeak separates spatial-neighborhood and patient-associated inflation in spatial omics prediction | 5 | 2 | 4 | 4 | 5 |
| Random spot splits overestimate spatial omics prediction through local and patient-associated dependence | 5 | 2 | 4 | 4 | 4 |
| Evaluation design reshapes apparent model performance in spatial omics prediction | 4 | 1 | 5 | 5 | 3 |
| SpatialLeak: an evidence hierarchy for leakage-resistant spatial omics prediction | 4 | 1 | 5 | 4 | 4 |
| Stricter split designs expose hidden dependence in spatial omics prediction benchmarks | 4 | 2 | 4 | 4 | 4 |
| Spatial and patient-associated dependence inflate random-split performance in spatial omics prediction | 5 | 2 | 4 | 5 | 4 |
| A benchmark framework for split-aware evaluation of spatial omics prediction | 3 | 1 | 5 | 5 | 3 |
| SpatialLeak identifies evaluation-dependent inflation in spatial transcriptomics prediction | 4 | 2 | 5 | 5 | 4 |
| From random spots to patient-held-out tests: a hierarchy for spatial omics model evaluation | 4 | 1 | 4 | 4 | 3 |

## Top 3

1. **Leakage-resistant benchmarking reveals two channels of inflated generalization in spatial omics prediction**
2. **SpatialLeak separates spatial-neighborhood and patient-associated inflation in spatial omics prediction**
3. **Random spot splits overestimate spatial omics prediction through local and patient-associated dependence**

## Recommended Top 1

**Leakage-resistant benchmarking reveals two channels of inflated generalization in spatial omics prediction**

This title is explicit, searchable, and defensible. It names the evaluation problem, the core conceptual result, and the application domain without claiming universal causality.

## Abstract A: Genome Biology Leaning

Spatial omics prediction models are often evaluated with random spot-level splits, a practice that can place neighboring tissue locations or same-patient samples on both sides of the train-test boundary. We developed SpatialLeak, a split-aware benchmark that compares random splits with spatial-buffer, slide-held-out, patient-held-out, and dataset-held-out evaluation across public spatial transcriptomics datasets. Random splits inflated apparent performance through two separable channels. Dense Visium breast data showed strong spatial-neighborhood sensitivity, with Spatial kNN hop5 RLI of 0.796, while Andersson and Thrane showed large patient/batch-associated losses for GraphSAGE, with patient RLI values of 0.692 and 0.718. A GSE278936 prostate Visium pilot replicated the spatial-channel pattern for PCA+Ridge but not for near-zero kNN. Size-matched random controls showed that spatial-buffer loss exceeded sample-count loss in the main spatial settings. SpatialLeak provides an evidence hierarchy for matching spatial omics evaluation to the intended generalization claim.

## Abstract B: Nature Communications Leaning

Spatial transcriptomics benchmarks commonly use random spot-level splits, although spatial neighborhoods and patient-specific structure can make test performance optimistic. SpatialLeak evaluates this risk by pairing permissive random splits with spatially buffered, section-held-out, patient-held-out, and dataset-held-out tests. Across DLPFC, breast cancer, melanoma, and prostate datasets, random-split advantages were not explained by one mechanism. Spatial kNN in dense Visium breast data dropped sharply under spatial buffering, whereas PCA+Ridge and GraphSAGE showed large patient-held-out losses in Andersson and Thrane. In GSE278936 prostate Visium, PCA+Ridge was unchanged at hop0 but declined under non-zero buffers, supporting a spatial-channel replication without providing patient-level validation. Random-size-matched controls showed that reduced sample count alone did not explain the main spatial-buffer losses. These results argue for split-aware reporting in spatial omics prediction and separate local neighborhood dependence from patient/batch-associated shortcuts.

## Abstract C: Bioinformatics / Briefings Leaning

Random train-test splits can overstate performance in spatial omics prediction when nearby or same-patient observations are shared across splits. We introduce SpatialLeak, an evaluation framework that compares random spot splits with spatial-buffer, slide-held-out, patient-held-out, and dataset-held-out protocols. Across public spatial transcriptomics datasets, the random-split advantage separated into spatial-neighborhood and patient/batch-associated channels. Spatial kNN was highly sensitive to spatial buffering in dense Visium breast data, while GraphSAGE showed strong patient-held-out loss in Andersson and Thrane. GSE278936 prostate Visium provided an additional spatial-channel replication for PCA+Ridge, with the important boundary that kNN performance was near zero and RLI was not interpreted. A random-size-matched control confirmed that the main spatial-buffer losses were larger than the loss expected from sample-count reduction. SpatialLeak turns spatial omics model evaluation from a single leaderboard into a hierarchy of generalization claims.

## Master Abstract Recommendation

Use Abstract B as the master abstract. It is concise, avoids citation needs, includes the Phase 18 sample-size defense, and keeps GSE278936 in the correct spatial-channel replication role.
