# Manuscript Skeleton

> Updated: 2026-08-09 22:25  
> Working title: **SpatialLeak: leakage-resistant benchmarking reveals inflated generalization in spatial omics prediction**

## One-Sentence Argument

In spatial omics prediction benchmarks, we show that random spot-level splits inflate apparent generalization through distinct spatial-neighborhood and patient/batch shortcut channels, using leakage-resistant spatial-buffer, patient-held-out, slide-held-out, shared-panel, GraphSAGE, and cross-platform stress tests across DLPFC, HER2+ breast, melanoma, and Visium breast datasets.

## Terminology Ledger

| Canonical term | First-use definition | Use |
|---|---|---|
| SpatialLeak | SpatialLeak benchmark framework | Framework name |
| leakage-resistant split | Split that separates samples by spatial buffer, patient, slide, or dataset | General strict-split term |
| random spot split | Random assignment of spots to train/validation/test | Main leakage-prone comparator |
| spatial-buffer split | Matched spatial-block split with kNN-hop or coordinate buffer | Within-section spatial leakage test |
| patient-held-out split | Strict split holding out all slides from one patient/donor | Patient/batch shortcut test |
| slide-held-out split | Strict split holding out an entire section | Used for Visium breast only |
| dataset-held-out transfer | Cross-dataset train-test transfer | Stress test, not patient-level validation |
| leakage inflation (LI) | `Perf_random - Perf_strict` | Absolute inflation |
| relative leakage inflation (RLI) | `(Perf_random - Perf_strict) / Perf_random` | Main normalized leakage metric |
| retention | `Perf_strict / Perf_random` | Strict-split performance retention |
| shared_panel_50 | Frozen 50-gene ENSG-anchored target panel | Cross-dataset comparable target set |
| PCA+Ridge | PCA feature reduction followed by Ridge regression | Strong non-spatial baseline |
| Spatial kNN | Spatial nearest-neighbor expression baseline | Spatial-neighborhood leakage probe |
| GraphSAGE | Lightweight transductive spatial graph neural network | Representative complex spatial model |

## Title Options

1. **SpatialLeak reveals inflated generalization in spatial omics prediction benchmarks**
2. **Leakage-resistant benchmarking exposes spatial and patient shortcuts in spatial omics prediction**
3. **Random spot splits overestimate generalization in spatial omics prediction**
4. **Spatial and patient-level leakage inflate spatial omics prediction benchmarks**

Recommended title: option 2. It states the contribution, names the leakage channels, and avoids overclaiming clinical or mechanistic relevance.

## Abstract Draft

Spatial omics prediction studies commonly evaluate models by randomly splitting spots or cells into training and test sets. This practice can violate independence assumptions because neighboring spots share tissue architecture, molecular gradients, and technical context, while slides from the same patient can also share patient- or batch-specific signals. SpatialLeak evaluates this problem with leakage-resistant splits that separate test samples by spatial buffer, patient, slide, or dataset. Across DLPFC, HER2+ breast cancer, melanoma, and Visium breast datasets, random spot splits consistently produced higher apparent performance than stricter evaluation schemes. In dataset-specific target panels, PCA+Ridge patient RLI reached 0.21 in DLPFC, 0.66 in Andersson HER2+ breast, and 0.50 in Thrane melanoma. In a frozen shared 50-gene panel, PCA+Ridge patient RLI remained 0.25, 0.63, and 0.64 across the same datasets. Spatial-neighborhood leakage was strongest in dense Visium data: Spatial kNN achieved mean Pearson 0.65 under random splits but fell to 0.13 under matched_hop5. GraphSAGE reproduced the two-channel pattern, with substantial spatial-buffer loss in DLPFC and large patient-held-out loss in Andersson. These results show that random spot splits can substantially overestimate spatial omics model generalization and that leakage-resistant reporting should distinguish within-section spatial leakage from patient/batch shortcuts.

## Results-First Outline

### Result 1. Random spot splits inflate performance across spatial omics datasets

Claim: Random spot-level evaluation overestimates model generalization relative to patient-held-out or spatial-buffer splits.

Evidence:

- DLPFC dataset-specific PCA+Ridge: random 0.292, patient 0.230, RLI 0.213.
- Andersson dataset-specific PCA+Ridge: random 0.604, patient 0.204, RLI 0.662.
- Thrane dataset-specific PCA+Ridge: random 0.653, patient 0.327, RLI 0.499.
- Wilcoxon tests show significant random-vs-patient loss for PCA+Ridge in DLPFC, Andersson, and Thrane.

Figure/table callout: `table_dataset_specific_RLI.csv`.

Paragraph job:

1. Define the main comparison and metric.
2. Report the dataset-specific evidence.
3. State the conclusion without attributing all loss to one mechanism.

### Result 2. Shared-panel benchmarking preserves the main conclusion under a common target set

Claim: The leakage effect is not an artifact of dataset-specific target-gene selection.

Evidence:

- shared_panel_50 PCA+Ridge patient RLI: DLPFC 0.251, Andersson 0.632, Thrane 0.644.
- DLPFC retains more strict-split performance than Andersson/Thrane, consistent with transportable cortical layer structure.
- Andersson and Thrane retain less patient-held-out signal, consistent with patient/batch shortcut dominance.

Figure/table callout: `table_shared_panel50_RLI.csv`.

Paragraph job:

1. Explain why shared-panel analysis was needed.
2. Report shared-panel RLI.
3. Interpret DLPFC versus ST v1.0 datasets as distinct leakage-channel balance.

### Result 3. Spatial-neighborhood leakage is strongest in dense Visium settings

Claim: Spatial-neighborhood information sharing can drive high random-split performance, especially when spot density is high.

Evidence:

- Visium breast Spatial kNN: random 0.649, matched_hop5 0.132, RLI 0.796.
- Visium region_hop10 kNN remains low at 0.120.
- DLPFC kNN also declines under matched_hop0 and distance buffers.
- Thrane high-hop curves are not resolvable because ST v1.0 density leaves no test spots at high hop thresholds.

Figure/table callout: `figure_distance_curve_data.csv`.

Paragraph job:

1. Introduce the spatial-buffer mechanism.
2. Lead with Visium because it is the clearest platform contrast.
3. Use Thrane as a boundary condition, not a failed replication.

### Result 4. Slide-held-out performance can remain high without proving patient-level generalization

Claim: Visium breast slide-held-out evaluation shows cross-section retention but cannot substitute for patient-held-out validation.

Evidence:

- Visium PCA+Ridge slide-held-out mean 0.580 versus random 0.597.
- Visium Spatial kNN slide-held-out mean 0.552 versus random 0.649.
- The dataset has one patient, so patient-held-out validation is impossible.

Figure/table callout: Visium rows in `table_dataset_specific_RLI.csv`.

Paragraph job:

1. State the single-patient limitation plainly.
2. Report high slide-held-out retention.
3. Frame this as transportable tissue-section signal plus a caution against over-interpreting slide splits.

### Result 5. GraphSAGE reproduces the two-channel leakage pattern

Claim: A representative complex spatial graph model follows the same leakage structure as simpler baselines.

Evidence:

- DLPFC GraphSAGE shared-panel: random 0.151, matched_hop0 0.094, RLI 0.378.
- Andersson GraphSAGE shared-panel: random 0.251, matched_hop0 0.233, RLI 0.072.
- Andersson GraphSAGE patient-held-out: 0.077, RLI 0.692.

Figure/table callout: `table_graphsage_shared_panel50_RLI.csv`.

Paragraph job:

1. Explain why GraphSAGE was included.
2. Report DLPFC spatial-buffer loss.
3. Report Andersson patient loss.
4. State that model complexity does not remove evaluation leakage.

### Result 6. Cross-platform dataset-held-out transfer is feasible but weak

Claim: Andersson-to-Visium transfer provides a stress test, not a replacement for patient-held-out validation.

Evidence:

- Andersson→Visium PCA+Ridge shared-panel mean Pearson 0.199 across 5 seeds.
- Mean baseline is 0.
- 49/50 shared targets were usable; `SEPT4` was absent from Visium.
- Spatial kNN was excluded because coordinates are not comparable across platforms.

Figure/table callout: `table_dataset_heldout_anderson_to_visium.csv`.

Paragraph job:

1. Present the transfer setup.
2. Report the modest signal.
3. State why this belongs in supplement or stress-test framing.

## Methods Skeleton

### Datasets and preprocessing

Describe DLPFC, Andersson HER2+ breast, Thrane melanoma, and Visium breast. Report spot counts, patient/slide counts, preprocessing (`normalize_total(1e4)+log1p`), HVG selection, Moran target ranking, and shared_panel_50 construction.

### Split definitions

Define random spot split, matched spatial-block split, kNN-hop buffer, coordinate buffer, patient-held-out split, slide-held-out split, region holdout, and dataset-held-out transfer. Emphasize that patient/slide/dataset folds were never used for test tuning.

### Models

Define Mean, PCA+Ridge, Spatial kNN, and GraphSAGE. State that spatial kNN was excluded from dataset-held-out transfer because coordinates are not comparable across datasets.

### Metrics and statistics

Define Pearson aggregation, LI, RLI, retention, Wilcoxon signed-rank tests with BH-FDR, slide-level bootstrap, and mixed-effects models. State that spot-level confidence intervals were not used.

### Integrity controls

Mention frozen analysis decisions, split metadata, seed handling, shared-panel freezing before performance computation, and empty high-hop test-set reporting.

## Discussion Skeleton

### Central advance

SpatialLeak shows that random spot-level evaluation can inflate apparent spatial omics prediction performance and that this inflation has at least two separable channels: within-section spatial-neighborhood leakage and patient/batch shortcuts.

### Relation to prior evaluation practice

Position the result against random cell/spot splits, section-level splits that do not guarantee patient separation, and stricter patient/cluster split examples from prior literature. Use local split audit as the citation source list, then replace placeholders with verified references in the manuscript phase.

### Practical implications

Recommend that spatial omics prediction papers report at least one strong non-spatial baseline, one spatial-neighborhood baseline, patient/slide separation where available, split metadata, and buffer definitions when spatial splits are used.

### Boundaries

SpatialLeak is a benchmark and evaluation framework, not a new prediction model. The present results use public datasets and CPU-feasible models. Some SOTA models remain candidates for future inclusion after split, license, and resource audits. Visium breast provides platform contrast but not patient-held-out evidence.

### Future directions

Extend to additional patient-rich Visium datasets, add selected SOTA models after audit, and test multi-omics spatial prediction tasks where both modality and spatial leakage can occur.

## SOTA Inclusion Decision Note

Current recommendation: do not add SOTA model runs to the main analysis before manuscript skeleton and figures are stable. The benchmark already includes a strong non-spatial baseline, a spatial-neighborhood leakage probe, and a representative graph neural network. Adding SOTA now risks shifting the paper from an evaluation framework to an implementation contest.

If SOTA is added, limit to one or two models and require:

1. Original split protocol audited.
2. Official code license checked.
3. Data compatibility confirmed without changing the core task.
4. CPU/GPU budget estimated.
5. Results reported under the same frozen splits, not under method-specific custom splits.

Most defensible candidates for later audit:

- NicheTrans: recent spatial-aware supervised cross-omics method, but task and resources differ.
- SpatialGlue or GraphST: high-profile spatial graph methods, but primary tasks are integration/clustering rather than supervised gene prediction.

## Claim-Evidence Map

| Claim | Evidence | Status |
|---|---|---|
| Random spot splits inflate apparent generalization | DLPFC, Andersson, Thrane patient RLI; Visium spatial-buffer RLI | Supported |
| Patient/batch shortcuts dominate Andersson and Thrane | Shared-panel PCA and GraphSAGE patient RLI | Supported |
| Dense Visium data show strong spatial-neighborhood leakage | Visium kNN random 0.649 to hop5 0.132 | Supported |
| Slide-held-out is not patient-held-out | Visium single-patient design | Supported |
| GraphSAGE does not remove leakage sensitivity | DLPFC hop0 RLI and Andersson patient RLI | Supported |
| Dataset-held-out transfer is feasible but weak | Andersson→Visium PCA mean 0.199 | Supported as stress test |
| Spatial autocorrelation explains all leakage | Final mixed-effects split by channel does not support this | Rejected / reframed |

## Missing Inputs Before Full Manuscript

- Target journal and abstract format.
- Final reference list and citation style.
- Decision on whether SOTA model audit should remain discussion-only or become a supplementary analysis.
- Final figure backend and visual style.
- Author list, affiliations, funding, data availability, and code availability statements.
