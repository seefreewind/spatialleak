# Evaluation design reshapes apparent generalization in spatial omics prediction

## Abstract

Spatial omics models are often evaluated using random spot-level splits. Spatial neighborhoods, section context and patient-associated structure can complicate the interpretation of performance estimated from such splits. We developed SpatialLeak, a leakage-resistant evaluation framework that compares random spot splits with buffered spatial, section-held-out, patient-held-out and dataset-held-out regimes. In dense Visium breast data, Spatial kNN showed strong spatial-neighborhood inflation, with hop5 relative leakage inflation (RLI) of 0.796. Corrected train-only GraphSAGE reruns showed large patient-associated losses in Andersson and Thrane, with patient RLI values of 0.695 and 0.711. In the independent GSE278936 prostate Visium cohort, PCA+Ridge was unchanged at hop0 but decreased under non-zero spatial buffers, reaching hop5 RLI 0.222. Random-size-matched controls indicated that reduced sample count alone did not explain the main spatial-buffer losses. SpatialLeak provides a hierarchy for matching benchmark design to the level of generalization being claimed.

## Introduction

Spatial transcriptomics and related spatial omics assays connect molecular measurements to tissue architecture, creating prediction tasks that are not available in dissociated profiling alone. These tasks include imputation of unmeasured genes, spatial molecular prediction, graph-based learning from tissue neighborhoods and representation learning over spatial context. As spatial datasets grow, such models increasingly support claims about whether molecular patterns can be recovered across locations, sections, patients or datasets.

The evaluation problem is that spatial observations are not independent in the ordinary IID sense. A random spot-level split can place neighboring tissue locations, similar local cell compositions, the same section background or the same patient-associated structure on both sides of the train-test boundary. Performance under this regime can therefore mix local interpolation with broader generalization.

Spatial dependence is not inherently invalid. A spatially aware model may use tissue architecture as a legitimate biological signal if that signal is retained under the separation required by the scientific claim. The central question is what claim the evaluation design can support: local interpolation, spatial transfer, section transfer, patient transfer, dataset transfer or cross-platform transfer.

Current spatial omics benchmarks do not consistently separate these levels. Existing split choices can conflate local spatial-neighborhood dependence, patient-associated structure and transportable biological signal. This makes it difficult to interpret whether an apparent model advantage reflects a robust predictive principle or the evaluation tier used to measure it.

Here we introduce SpatialLeak, a multi-tier evaluation framework for spatial omics prediction. SpatialLeak compares random spot splits with buffered spatial, section-held-out, patient-held-out and dataset-held-out regimes across public spatial transcriptomics datasets and diagnostic model classes. The framework shows that apparent generalization can arise through distinct spatial-neighborhood and patient-associated channels, and it organizes these findings into a generalization evidence hierarchy.

## Results

### Random spot-level evaluation inflates apparent predictive generalization

SpatialLeak first tested whether random spot-level performance was retained when the train-test boundary matched a stricter generalization claim. Across DLPFC, Andersson, Thrane and Visium breast, random splits produced higher apparent performance than the relevant stricter split for the main interpretable model-dataset combinations. This established random spot evaluation as a permissive interpolation setting rather than evidence, by itself, for section-, patient- or dataset-level generalization.

The patient-channel datasets showed the clearest random-to-patient losses. In Andersson, PCA+Ridge patient RLI was 0.662, and corrected train-only GraphSAGE patient RLI was 0.695. In Thrane, PCA+Ridge patient RLI was 0.499, and corrected train-only GraphSAGE patient RLI was 0.711. These results show that a graph-based model did not remove the need for grouped evaluation.

### Non-zero spatial buffers reveal local neighborhood dependence

SpatialLeak next tested whether non-overlapping spatial partitions were sufficient to remove local neighborhood dependence. They were not always sufficient. In DLPFC and Visium breast, increasing hop distance reduced performance, especially for Spatial kNN. Visium breast showed the strongest spatial-channel example, with Spatial kNN hop5 RLI 0.796.

GSE278936 provided an independent high-density Visium spatial-channel replication. PCA+Ridge was essentially unchanged at hop0 (RLI -0.000) but decreased under hop2 and hop5 buffers, reaching hop5 RLI 0.222. This pattern supports the specific claim that a non-zero exclusion buffer can be required to expose local neighborhood dependence. The random-size-matched control showed that the main spatial-buffer losses were larger than the losses caused by downsampling random splits to similar sample sizes.

### Patient-held-out evaluation identifies a distinct patient-associated channel

Patient-held-out evaluation measured a different axis of dependence from within-section spatial buffering. Andersson and Thrane had large patient-held-out losses even when spatial kNN was near zero or when high-hop spatial curves were not resolvable in low-density ST v1.0 geometry. DLPFC showed a mixed pattern, with both spatial and donor-associated effects.

The patient-associated channel should not be interpreted as a causal batch-effect estimate. It can include patient identity, section background, tissue processing, sample handling, cohort structure and biological heterogeneity. The result is that random spot splits can use structure that is not retained when patient-associated groups are separated.

### Dominant generalization-inflation channels vary across datasets and model classes

The strongest evidence came from treating heterogeneity as a result rather than a nuisance. DLPFC showed both spatial and donor-associated effects. Andersson and Thrane were patient-channel dominant. Visium breast was spatial-channel dominant but single-patient. GSE278936 replicated the spatial-channel PCA+Ridge buffer response and provided a kNN boundary condition because random kNN performance was below zero.

This two-channel landscape explains why one split or one model cannot diagnose all settings. Spatial kNN is useful as a local-neighborhood probe when it has signal. PCA+Ridge provides a strong non-graph baseline. Corrected train-only GraphSAGE tests whether graph learning follows the same split-dependent behavior as simpler baselines.

### Apparent model advantage depends on evaluation regime

Model comparisons changed when the evaluation claim changed. Spatial kNN was strong in dense random or local settings but weak when spatial signal was absent or isolated. Corrected GraphSAGE retained random-split performance in some settings but showed strong patient-held-out losses in tumor datasets. PCA+Ridge often retained broader transfer signal better than a purely local spatial-neighbor baseline.

These observations argue against using a single random-split leaderboard as evidence of model superiority. A method can be useful for local interpolation while being less informative for patient transfer, and a model that appears robust under a spatial split may still lose performance under patient-held-out evaluation.

### SpatialLeak defines a hierarchy for spatial-omics generalization claims

SpatialLeak formalizes six evaluation tiers. Level 0, random spot interpolation, supports local interpolation but does not establish spatial, section or patient transfer. Level 1, buffered spatial transfer, tests local neighborhood separation but does not establish patient transfer. Level 2, section-held-out transfer, tests transfer across sections but not necessarily across patients. Level 3, patient-held-out transfer, tests retention across patient-associated groups but does not establish dataset or platform transfer. Level 4, dataset-held-out transfer, tests broader dataset transportability. Level 5, cross-platform transfer, tests robustness when measurement platforms also change.

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

```bibtex
@article{Stahl2016Science,
  title = {Visualization and analysis of gene expression in tissue sections by spatial transcriptomics},
  author = {St{\aa}hl, Patrik L. and Salm{\'e}n, Fredrik and Vickovic, Sanja and Lundmark, Anna and Navarro, Jos{\'e} Fern{\'a}ndez and Magnusson, Jens and Giacomello, Stefania and Asp, Michaela and Westholm, Jakub O. and Huss, Mikael and Mollbrink, Annelie and Linnarsson, Sten and Codeluppi, Simone and Borg, {\AA}ke and Pont{\'e}n, Fredrik and Costea, Paul Igor and Sahl{\'e}n, Pelin and Mulder, Jan and Bergmann, Olaf and Lundeberg, Joakim and Fris{\'e}n, Jonas},
  journal = {Science},
  year = {2016},
  volume = {353},
  number = {6294},
  pages = {78--82},
  doi = {10.1126/science.aaf2403}
}

@article{Maynard2021NatNeurosci,
  title = {Transcriptome-scale spatial gene expression in the human dorsolateral prefrontal cortex},
  author = {Maynard, Kristen R. and Collado-Torres, Leonardo and Weber, Lukas M. and Uytingco, Cedric and Barry, Brianna K. and Williams, Stephen R. and Catallini, Joseph L. and Tran, Matthew N. and Besich, Zachary and Tippani, Madhavi and Chew, Jennifer and Yin, Ye and Kleinman, Joel E. and Hyde, Thomas M. and Rao, N. A. and Hicks, Stephanie C. and Martinowich, Keri and Jaffe, Andrew E.},
  journal = {Nature Neuroscience},
  year = {2021},
  volume = {24},
  pages = {425--436},
  doi = {10.1038/s41593-020-00787-0}
}

@article{Andersson2021NatCommun,
  title = {Spatial deconvolution of {HER2}-positive breast cancer delineates tumor-associated cell type interactions},
  author = {Andersson, Alma and Larsson, Ludvig and Stenbeck, Linnea and Salm{\'e}n, Fredrik and Ehinger, Anna and Wu, Sunny Z. and Al-Eryani, Ghamdan and Roden, Daniel and Swarbrick, Alexander and Borg, {\AA}ke and Fris{\'e}n, Jonas and Lundeberg, Joakim},
  journal = {Nature Communications},
  year = {2021},
  volume = {12},
  pages = {6012},
  doi = {10.1038/s41467-021-26271-2}
}

@misc{Andersson2021Zenodo,
  title = {Spatial deconvolution of {HER2}-positive breast cancer delineates tumor-associated cell type interactions},
  author = {Andersson, Alma and Larsson, Ludvig and Stenbeck, Linnea and Salm{\'e}n, Fredrik and others},
  year = {2021},
  doi = {10.5281/zenodo.4751624},
  publisher = {Zenodo}
}

@article{Thrane2018CancerRes,
  title = {Spatially resolved transcriptomics enables dissection of genetic heterogeneity in stage {III} cutaneous malignant melanoma},
  author = {Thrane, Kim and Eriksson, Hanna and Maaskola, Jonas and Hansson, Johan and Lundeberg, Joakim},
  journal = {Cancer Research},
  year = {2018},
  volume = {78},
  number = {20},
  pages = {5970--5979},
  doi = {10.1158/0008-5472.CAN-18-0747}
}

@article{Kiviaho2024NatCommun,
  title = {Single cell and spatial transcriptomics highlight the interaction of club-like cells with immunosuppressive myeloid cells in prostate cancer},
  author = {Kiviaho, Antti and Eerola, Sini K. and Kallio, Heini M. L. and others},
  journal = {Nature Communications},
  year = {2024},
  volume = {15},
  pages = {9949},
  doi = {10.1038/s41467-024-54364-1}
}

@misc{TenXBreastSection1,
  title = {Human Breast Cancer (Block A Section 1): Spatial Gene Expression dataset},
  author = {{10x Genomics}},
  year = {2020},
  url = {https://www.10xgenomics.com/datasets/human-breast-cancer-block-a-section-1-1-standard-1-0-0},
  note = {Accessed 2026-08-10}
}

@article{Abdelaal2020NAR,
  title = {{SpaGE}: Spatial Gene Enhancement using sc{RNA}-seq},
  author = {Abdelaal, Tamim and Mourragui, Soufiane and Mahfouz, Ahmed and Reinders, Marcel J. T.},
  journal = {Nucleic Acids Research},
  year = {2020},
  volume = {48},
  number = {18},
  pages = {e107},
  doi = {10.1093/nar/gkaa740}
}

@article{He2020NatBiomedEng,
  title = {Integrating spatial gene expression and breast tumour morphology via deep learning},
  author = {He, Bryan and Bergenstr{\aa}hle, Ludvig and Stenbeck, Linnea and Abid, Abubakar and Andersson, Alma and Borg, {\AA}ke and Maaskola, Jonas and Lundeberg, Joakim and Zou, James},
  journal = {Nature Biomedical Engineering},
  year = {2020},
  volume = {4},
  pages = {827--834},
  doi = {10.1038/s41551-020-0578-x}
}

@inproceedings{Hamilton2017GraphSAGE,
  title = {Inductive representation learning on large graphs},
  author = {Hamilton, William L. and Ying, Rex and Leskovec, Jure},
  booktitle = {Advances in Neural Information Processing Systems},
  year = {2017},
  eprint = {1706.02216},
  archivePrefix = {arXiv}
}

@article{Moran1950Biometrika,
  title = {Notes on continuous stochastic phenomena},
  author = {Moran, P. A. P.},
  journal = {Biometrika},
  year = {1950},
  volume = {37},
  number = {1/2},
  pages = {17--23},
  doi = {10.1093/biomet/37.1-2.17}
}

@article{Ambroise2002PNAS,
  title = {Selection bias in gene extraction on the basis of microarray gene-expression data},
  author = {Ambroise, Christophe and McLachlan, Geoffrey J.},
  journal = {Proceedings of the National Academy of Sciences},
  year = {2002},
  volume = {99},
  number = {10},
  pages = {6562--6566},
  doi = {10.1073/pnas.102102699}
}

@article{Vabalas2019PLOSOne,
  title = {Machine learning algorithm validation with a limited sample size},
  author = {Vabalas, Andrius and Gowen, Emma and Poliakoff, Ellen and Casson, Alexander J.},
  journal = {PLOS ONE},
  year = {2019},
  volume = {14},
  number = {11},
  pages = {e0224365},
  doi = {10.1371/journal.pone.0224365}
}

@article{Kapoor2023Patterns,
  title = {Leakage and the reproducibility crisis in machine-learning-based science},
  author = {Kapoor, Sayash and Narayanan, Arvind},
  journal = {Patterns},
  year = {2023},
  volume = {4},
  number = {9},
  pages = {100804},
  doi = {10.1016/j.patter.2023.100804}
}


@article{Biancalani2021NatMethods,
  title={Deep learning and alignment of spatially resolved single-cell transcriptomes with Tangram},
  author={Biancalani, Tommaso and others},
  journal={Nature Methods},
  year={2021},
  volume={18},
  pages={1352--1362},
  doi={10.1038/s41592-021-01264-7}
}

@article{Chen2021Bioinformatics,
  title={stPlus: a reference-based method for the accurate enhancement of spatial transcriptomics},
  author={Chen, Shengquan and Zhang, Boheng and Chen, Xiaoyang and Zhang, Xuegong and Jiang, Rui},
  journal={Bioinformatics},
  year={2021},
  volume={37},
  pages={i299--i307},
  doi={10.1093/bioinformatics/btab298}
}

@article{Long2023NatCommun,
  title={Spatially informed clustering, integration, and deconvolution of spatial transcriptomics with GraphST},
  author={Long, Yuchen and others},
  journal={Nature Communications},
  year={2023},
  volume={14},
  pages={1155},
  doi={10.1038/s41467-023-36796-3}
}

@article{Dong2022NatCommun,
  title={Deciphering spatial domains from spatially resolved transcriptomics with an adaptive graph attention auto-encoder},
  author={Dong, Kangning and Zhang, Shihua},
  journal={Nature Communications},
  year={2022},
  volume={13},
  pages={1739},
  doi={10.1038/s41467-022-29439-6}
}

@article{Hu2021NatMethods,
  title={SpaGCN: Integrating gene expression, spatial location and histology to identify spatial domains and spatially variable genes by graph convolutional network},
  author={Hu, Jian and Li, Xiangjie and Coleman, Kyle and Schroeder, Andrew and Ma, Nan and Irwin, David J. and Lee, Edward B. and Shinohara, Russell T. and Li, Mingyao},
  journal={Nature Methods},
  year={2021},
  volume={18},
  pages={1342--1351},
  doi={10.1038/s41592-021-01255-8}
}

@article{Fu2024GenomeMed,
  title={Unsupervised spatially embedded deep representation of spatial transcriptomics},
  author={Fu, Huazhu and others},
  journal={Genome Medicine},
  year={2024},
  volume={16},
  pages={12},
  doi={10.1186/s13073-024-01283-x}
}

@article{Kaufman2012ACM,
  title={Leakage in data mining: formulation, detection, and avoidance},
  author={Kaufman, Shachar and Rosset, Saharon and Perlich, Claudia},
  journal={ACM Transactions on Knowledge Discovery from Data},
  year={2012},
  volume={6},
  number={4},
  doi={10.1145/2382577.2382579}
}

@article{Varma2006BMCBioinformatics,
  title={Bias in error estimation when using cross-validation for model selection},
  author={Varma, Sudhir and Simon, Richard},
  journal={BMC Bioinformatics},
  year={2006},
  volume={7},
  pages={91},
  doi={10.1186/1471-2105-7-91}
}

```
