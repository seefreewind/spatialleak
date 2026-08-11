# Abstract Architecture

Date: 2026-08-10

## One-Sentence Argument

In spatial omics prediction benchmarks, SpatialLeak shows that apparent generalization under random spot splits can arise through two separable channels, within-section spatial-neighborhood leakage and patient/batch shortcuts, using frozen leakage metrics, spatial-buffer splits, patient-held-out splits, graph and baseline predictors, and independent spatial replication.

## Abstract Logic

### Background

Spatial omics prediction models are often evaluated on observations that are spatially and biologically dependent. This violates the independence assumptions behind many random spot-level benchmarks.

### Gap

Current benchmarks can conflate three signals: local neighborhood information, patient or sample identity, and transportable biological structure. A single random split or a single strict split cannot distinguish these mechanisms.

### Methods

SpatialLeak compares random spot splits with spatial-buffer, slide-held-out, patient-held-out, dataset-held-out, and cross-platform stress tests across public spatial transcriptomics datasets. It evaluates a strong non-spatial baseline, a spatial nearest-neighbor probe, and GraphSAGE using frozen LI, RLI, retention, and shared_panel_50 definitions.

### Results Number Budget

Use no more than 3-4 numbers:

1. Spatial-channel example: Visium breast Spatial kNN random 0.649 to matched_hop5 0.132, RLI 0.796.
2. Patient-channel example: GraphSAGE patient RLI 0.692 in Andersson or 0.718 in Thrane; PCA+Ridge patient RLI 0.662 in Andersson also works.
3. GSE278936 buffer finding: PCA+Ridge random 0.374, matched_hop0 0.375, matched_hop5 0.292, RLI 0.222.
4. Cross-platform stress test if space permits: Andersson-to-Visium PCA+Ridge mean Pearson 0.199.

Avoid loading the abstract with all dataset-specific RLI values.

### Conclusion

The abstract should end on the evaluation framework, not on alarmist language. The central message is that robust spatial-omics benchmarking requires matching the split to the generalization claim and reporting boundary conditions.

## Candidate A: Genome Biology Style

Spatial omics prediction models are commonly benchmarked with random spot-level train-test splits, yet nearby spots and samples from the same patient can share biological and technical information. This dependence can make apparent generalization difficult to interpret. We developed SpatialLeak, an evaluation framework that compares random splits with spatial-buffer, slide-held-out, patient-held-out, dataset-held-out, and cross-platform stress tests across public spatial transcriptomics datasets. SpatialLeak quantified leakage inflation, relative leakage inflation, and strict-split retention for PCA+Ridge, Spatial kNN, and GraphSAGE under frozen target-gene panels and split definitions. Random spot splits inflated performance through two separable channels. In dense Visium breast data, Spatial kNN decreased from 0.649 under random splits to 0.132 under a matched_hop5 spatial buffer, whereas patient-held-out tests in Andersson and Thrane revealed strong patient/batch shortcuts for PCA+Ridge and GraphSAGE. In GSE278936 prostate Visium, PCA+Ridge showed little loss at hop0 but declined after non-zero spatial buffers, indicating that non-overlapping partitions alone can be insufficient. Spatial kNN had little predictive signal in this dataset, defining a model- and dataset-specific boundary condition. SpatialLeak provides a practical hierarchy for leakage-resistant spatial-omics evaluation and separates local dependence from transportable biological signal.

## Candidate B: Nature Communications Style

Random spot-level splits are widely used to evaluate spatial omics prediction models, but they can mix local tissue continuity, patient-associated structure, and genuine transferable signal. Here we introduce SpatialLeak, a leakage-resistant evaluation framework for spatial transcriptomics prediction. Across public DLPFC, breast cancer, melanoma, Visium breast, and prostate Visium datasets, SpatialLeak compared random splits with spatial-buffer, patient-held-out, slide-held-out, dataset-held-out, and cross-platform tests using PCA+Ridge, Spatial kNN, and GraphSAGE. The results identify two distinct sources of apparent generalization. Dense Visium breast data showed strong within-section spatial-neighborhood inflation, with Spatial kNN decreasing from 0.649 under random splits to 0.132 under a matched_hop5 buffer. Andersson and Thrane instead showed strong patient/batch shortcuts, including patient RLI values of 0.692 and 0.718 for GraphSAGE. In the independent GSE278936 prostate Visium cohort, PCA+Ridge was unchanged at hop0 but decreased under hop2 and hop5 buffers, supporting the need for non-zero exclusion buffers. These findings suggest that model advantage and generalization claims depend materially on the evaluation regime. SpatialLeak is an evaluation framework for distinguishing local dependence, patient-associated shortcuts, and transportable biological structure.

## Candidate C: Bioinformatics / Benchmark Style

Motivation: Spatial transcriptomics benchmarks often use random spot-level splits, although spatial proximity and shared patient or section identity can violate train-test independence. Results: We present SpatialLeak, a leakage-resistant benchmark framework for spatial omics prediction. SpatialLeak evaluates random, spatial-buffer, slide-held-out, patient-held-out, dataset-held-out, and cross-platform tests using frozen leakage inflation metrics, shared target panels, and simple and graph-based predictors. Across public DLPFC, HER2+ breast cancer, melanoma, Visium breast, and GSE278936 prostate datasets, random splits produced evaluation-dependent performance inflation through two channels. Within-section spatial-neighborhood leakage was strongest in dense Visium breast, where Spatial kNN decreased from 0.649 under random splits to 0.132 under matched_hop5. Patient-held-out evaluation uncovered a separate shortcut channel in Andersson and Thrane, including GraphSAGE patient RLI values of 0.692 and 0.718. GSE278936 provided independent spatial-channel replication for PCA+Ridge, with loss emerging only after non-zero hop buffers. Availability: [Code and data availability placeholder]. Conclusion: SpatialLeak shows that spatial omics prediction benchmarks should report split hierarchy, spatial buffers, patient or section separation, strong baselines, and boundary conditions rather than relying on random spot-level performance alone.

## Preferred Use

- Genome Biology: Candidate A after tightening to journal word limit.
- Nature Communications: Candidate B; strongest broad-audience narrative.
- Bioinformatics / benchmark journal: Candidate C, especially if a structured abstract is required.

