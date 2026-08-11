# GSE278936 Spatial-Channel Pilot Current Status

Date: 2026-08-10

## Decision

GSE278936 should be kept as a spatial-channel external replication dataset only. It should not be described as clean patient-level validation or batch/site validation.

The usable public GEO release contains 52 public Visium sections from 52 patients, so patient-held-out and section-held-out splits are nearly the same design object. This prevents a clean separation of patient effect, section effect, and site/cohort effect. The restricted validation cohort is not used.

Recommended manuscript language:

> GSE278936 was used as an independent high-density human Visium cohort to test whether within-section spatial-neighborhood inflation is reproducible under spatially isolated splits.

Avoid manuscript language:

> GSE278936 validates patient-level generalization.

Primary sources used for dataset positioning:

- GEO record: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278936
- GEO processed supplement directory: https://ftp.ncbi.nlm.nih.gov/geo/series/GSE278nnn/GSE278936/suppl/
- Article: https://www.nature.com/articles/s41467-024-54364-1
- Reporting summary PDF: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-54364-1/MediaObjects/41467_2024_54364_MOESM14_ESM.pdf

## What Was Run

Scope was intentionally limited to the approved pilot:

- Dataset: public GSE278936 prostate Visium processed data
- Role: spatial-channel external replication
- Panel: `shared_panel_50`
- Seeds: `0,1,2,3,4`
- Models: Mean, PCA+Ridge, Spatial kNN
- Splits: random, matched_hop0, matched_hop2, matched_hop5
- Not run: GraphSAGE, patient-held-out, slide-held-out, EGA restricted data, expanded SOTA models

Commands and code paths:

- Download script: `scripts/download_gse278936_processed_minimal.py`
- Preprocessing script: `scripts/preprocess_gse278936_prostate.py`
- Benchmark script: `scripts/benchmark_external.py`
- Processed AnnData: `data/processed/gse278936_prostate_hvg2000.h5ad`
- Target panel: `data/processed/gene_panels/shared_panel_50_gse278936_prostate_targets.csv`
- Result directory: `results/gse278936_prostate_spatial_pilot`
- Paper asset table: `results/paper_assets/table_gse278936_spatial_pilot_RLI.csv`

## Data Status

Download integrity is complete for the minimal public processed set:

- Expected files: 208 gzipped files
- Observed files: 208 gzipped files
- Missing files: 0
- `gzip -t`: passed

Preprocessing completed successfully:

- Total spots: 134,509
- Variables retained: 2,028
- Public patients: 52
- Public sections: 52
- shared_panel_50 targets available: 50/50

The benchmark completed successfully in 1,567 seconds.

## Aggregate Results

Mean Pearson across 50 target genes and 5 seeds:

| Model | random | matched_hop0 | matched_hop2 | matched_hop5 |
|---|---:|---:|---:|---:|
| Mean | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| PCA+Ridge | 0.374473 | 0.374584 | 0.294437 | 0.291516 |
| Spatial kNN | -0.007289 | -0.007824 | -0.001770 | -0.004150 |

PCA+Ridge loss relative to random:

| Comparison | LI | RLI | Retention |
|---|---:|---:|---:|
| random vs matched_hop0 | -0.000111 | -0.000296 | 1.000296 |
| random vs matched_hop2 | 0.080036 | 0.213731 | 0.786269 |
| random vs matched_hop5 | 0.082958 | 0.221532 | 0.778468 |

Spatial kNN should not be used for RLI interpretation in this pilot because random-split performance is below zero. Its behavior is a boundary condition, not a positive replication of the Visium breast kNN pattern.

## Interpretation

This pilot meets a weak GO criterion for spatial-channel replication. PCA+Ridge shows a stable drop from random/hop0 to hop2/hop5 across all five seeds, with approximately 21-22% relative leakage/inflation removed by spatial isolation. The pattern is not strictly monotonic across all hop levels because hop0 is essentially identical to random and hop5 is only slightly lower than hop2 on average.

The clean interpretation is:

> In GSE278936, random spot splitting inflates PCA+Ridge target-gene prediction compared with spatially isolated matched splits, and the inflation becomes visible when a nonzero neighborhood buffer is imposed.

The result should not be framed as:

> Spatial kNN strongly reproduces the breast Visium leakage pattern in GSE278936.

or:

> GSE278936 validates patient-level leakage.

## Stop/Go Call

Decision: weak GO, suitable as supplementary spatial-channel external replication with explicit boundary-condition wording.

This dataset adds value because it extends the spatial channel to a larger independent human Visium cohort. It does not justify expanding into patient validation, GraphSAGE, or restricted-data work.

Recommended next project decision:

Stop adding datasets after incorporating this pilot. The current two-channel story is sufficient:

- Spatial channel: DLPFC, Visium breast, GSE278936 prostate
- Patient/batch channel: Andersson, Thrane
- Core claim: SpatialLeak identifies two distinct sources of apparent generalization: local neighborhood leakage and patient/batch shortcuts.

Next work should move to manuscript drafting, figure/table consolidation, and careful wording of dataset roles.

