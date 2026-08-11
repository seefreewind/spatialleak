# Dataset-Held-Out Prototype

> Updated: 2026-08-09 22:05  
> Prototype: Andersson HER2+ breast ST v1.0 → 10x Visium breast.

## 1. Design

This prototype trains on all Andersson spots and evaluates on all Visium breast spots using intersected gene symbols.

Models:

- Mean baseline
- PCA+Ridge

Spatial kNN was excluded because spatial coordinates are not comparable across datasets or platforms.

Gene set:

- Target panel: frozen `shared_panel_50`, mapped to gene symbols.
- Usable targets: 49/50. `SEPT4` was absent from Visium breast and was dropped.
- Common feature genes: 2,000 selected from the Andersson/Visium intersection after excluding targets.

## 2. Results

| Model | Mean Pearson | SD across seeds | n target genes |
|-------|--------------|-----------------|----------------|
| Mean | 0.000 | 0.000 | 49 |
| PCA+Ridge | 0.199 | 0.001 | 49 |

For context, Visium breast within-dataset top-target PCA+Ridge performance was much higher:

| Visium split | PCA+Ridge mean Pearson |
|--------------|------------------------|
| random | 0.597 |
| matched_hop0 | 0.468 |
| matched_hop5 | 0.442 |
| slide-held-out | 0.580 |

## 3. Interpretation

Andersson→Visium transfer is feasible but difficult. Performance above the mean baseline indicates some transferable expression structure, but the large gap from Visium within-dataset performance reflects platform, preprocessing, tissue-section, gene-panel, and cohort/domain differences.

This result should be reported as a cross-platform stress test or supplementary analysis. It should not be framed as patient-level external validation and should not replace patient-held-out evidence from DLPFC, Andersson, and Thrane.

## 4. Outputs

- `results/dataset_heldout/anderson_to_visium_shared_panel50_aggregate.csv`
- `results/dataset_heldout/anderson_to_visium_shared_panel50_per_gene.csv`
- `results/dataset_heldout/anderson_to_visium_shared_panel50_per_gene_per_slide.csv`
- `results/dataset_heldout/anderson_to_visium_shared_panel50_meta.json`
