# Phase 18 Sample-Size Matching Audit

## Decision

Existing matched-hop splits do not fully control sample size. The matched-block assignment keeps the training set fixed across hop buffers within a seed, but the hop buffer removes only test spots. Random spot splits also use a different train/validation/test geometry from the matched-block splits. The project should therefore include the limited random-size-matched control requested in Phase 18.

## Split-Size Summary

| dataset_label      | split        |   n_train |     n_val |    n_test |   n_dropped |   test_retained |   train_vs_random |
|:-------------------|:-------------|----------:|----------:|----------:|------------:|----------------:|------------------:|
| DLPFC              | matched_hop0 | 31735.100 |  5361.600 | 10584.300 |       0.000 |           1.000 |             0.832 |
| DLPFC              | matched_hop2 | 31735.100 |  5361.600 |  8291.700 |    2292.600 |           0.783 |             0.832 |
| DLPFC              | matched_hop5 | 31735.100 |  5361.600 |  2087.400 |    8496.900 |           0.194 |             0.832 |
| GSE278936 prostate | matched_hop0 | 87322.000 | 15560.000 | 31627.000 |       0.000 |           1.000 |             0.811 |
| GSE278936 prostate | matched_hop2 | 87322.000 | 15560.000 |  2256.800 |   29370.200 |           0.071 |             0.811 |
| GSE278936 prostate | matched_hop5 | 87322.000 | 15560.000 |  1386.600 |   30240.400 |           0.044 |             0.811 |
| Visium breast      | matched_hop0 |  5218.600 |   886.900 |  1679.500 |       0.000 |           1.000 |             0.838 |
| Visium breast      | matched_hop2 |  5218.600 |   886.900 |  1453.100 |     226.400 |           0.864 |             0.838 |
| Visium breast      | matched_hop5 |  5218.600 |   886.900 |   777.400 |     902.100 |           0.459 |             0.838 |

## Random-Size-Matched Feasibility

Exact matching means the random partition had enough train, validation, or test spots to downsample to the strict matched-hop count. Values below 1.0 identify capped comparisons where the random partition was already smaller than the strict target.

| dataset            |   hop |   train_exact |   val_exact |   test_exact |
|:-------------------|------:|--------------:|------------:|-------------:|
| dlpfc              |     2 |         1.000 |       0.000 |        0.000 |
| dlpfc              |     5 |         1.000 |       0.000 |        0.700 |
| gse278936_prostate |     2 |         1.000 |       0.000 |        1.000 |
| gse278936_prostate |     5 |         1.000 |       0.000 |        1.000 |
| visium_breast      |     2 |         1.000 |       0.000 |        0.000 |
| visium_breast      |     5 |         1.000 |       0.000 |        0.800 |

## Defensive Control Summary

| dataset_label      | model       |   hop |   random_full |   random_size_matched |   spatial_buffer |   delta_size |   delta_spatial |
|:-------------------|:------------|------:|--------------:|----------------------:|-----------------:|-------------:|----------------:|
| DLPFC              | pca_ridge   |     2 |        0.2916 |                0.2908 |           0.1844 |       0.0008 |          0.1063 |
| DLPFC              | pca_ridge   |     5 |        0.2916 |                0.2769 |           0.1566 |       0.0147 |          0.1203 |
| DLPFC              | spatial_knn |     2 |        0.2969 |                0.2957 |           0.1556 |       0.0012 |          0.1401 |
| DLPFC              | spatial_knn |     5 |        0.2969 |                0.2904 |           0.0890 |       0.0065 |          0.2014 |
| GSE278936 prostate | pca_ridge   |     2 |        0.3745 |                0.3678 |           0.2944 |       0.0067 |          0.0733 |
| GSE278936 prostate | pca_ridge   |     5 |        0.3745 |                0.3457 |           0.2915 |       0.0288 |          0.0542 |
| GSE278936 prostate | spatial_knn |     2 |       -0.0073 |               -0.0095 |          -0.0018 |       0.0022 |         -0.0077 |
| GSE278936 prostate | spatial_knn |     5 |       -0.0073 |               -0.0066 |          -0.0042 |      -0.0007 |         -0.0024 |
| Visium breast      | pca_ridge   |     2 |        0.5973 |                0.5956 |           0.4601 |       0.0017 |          0.1355 |
| Visium breast      | pca_ridge   |     5 |        0.5973 |                0.5962 |           0.4424 |       0.0011 |          0.1538 |
| Visium breast      | spatial_knn |     2 |        0.6485 |                0.6520 |           0.2292 |      -0.0034 |          0.4228 |
| Visium breast      | spatial_knn |     5 |        0.6485 |                0.6518 |           0.1322 |      -0.0032 |          0.5196 |

## Interpretation

The defensive comparison separates two effects: performance lost by reducing the random split to a similar sample size, and performance lost after imposing spatial separation. The manuscript should emphasize the latter only when delta_spatial exceeds delta_size in the relevant dataset/model/hop comparison. GSE278936 remains a spatial-channel external replication only, because its public GEO design has one section per patient and cannot separate patient and section effects.

## Provenance Notes

- DLPFC formal aggregate results contain hop2/hop5 performance, but the current split JSON manifests were later overwritten by a restricted split-filter run. Split sizes in this audit were reconstructed from `configs/experiments/formal_dlpfc.yaml` and the frozen split implementation rather than read from those overwritten JSON files.
- The control reuses the original random split for each seed, then downsamples train/validation/test indices without using strict-split performance.
- The split-size table is written to `results/paper_assets/table_split_sample_sizes.csv`.
- The control comparison table is written to `results/paper_assets/table_random_size_matched_control.csv`.
