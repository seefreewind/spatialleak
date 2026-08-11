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
