# Final Experiment Lock

**Status:** EXPERIMENTAL PHASE CLOSED  
**Lock date:** 2026-08-10 19:56:04  
**Git commit:** UNAVAILABLE: Command '['git', 'rev-parse', '--short', 'HEAD']' returned non-zero exit status 128.  

## Scope Locked

No additional datasets, model classes, GraphSAGE expansions, SOTA model zoo runs, patient-held-out reinterpretations of GSE278936, restricted EGA downloads, or cross-platform expansions should be added before manuscript submission.

The only Phase 18 experiment added after the Phase 17 stop decision was the defensive random-size-matched control:

| Dataset | Seeds | Models | Strict references |
|---|---:|---|---|
| DLPFC | 10 | PCA+Ridge, Spatial kNN | matched_hop2, matched_hop5 |
| Visium breast | 10 | PCA+Ridge, Spatial kNN | matched_hop2, matched_hop5 |
| GSE278936 prostate | 5 | PCA+Ridge, Spatial kNN | matched_hop2, matched_hop5 |

## Frozen Result Manifests

- `results/paper_assets/table_two_channel_leakage.csv`
- `results/paper_assets/table_gse278936_spatial_pilot_RLI.csv`
- `results/paper_assets/table_split_sample_sizes.csv`
- `results/paper_assets/table_random_size_matched_control.csv`
- `results/sample_size_control/random_size_matched_per_seed.csv`
- `results/sample_size_control/random_size_matched_split_meta.csv`
- `results/sample_size_control/manifest.json`
- `results/final_stats/summary_all_datasets.csv`
- `results/final_stats/LI_RLI_all_datasets.csv`

## Locked Configs And Scripts

- `configs/experiments/formal_dlpfc.yaml`
- `scripts/formal_benchmark.py`
- `scripts/benchmark_external.py`
- `scripts/run_graphsage_external.py`
- `scripts/run_graphsage_formal.py`
- `scripts/build_two_channel_leakage_table.py`
- `scripts/build_paper_tables.py`
- `scripts/run_sample_size_defense.py`
- `scripts/finalize_phase18_package.py`

## Analysis Lock Version

The project-level analysis lock is `ANALYSIS_LOCK.md`. Phase 18 adds the sample-size defense and closes experiments. Any later analysis should be labelled post-lock sensitivity analysis and excluded from the main manuscript unless the lock is explicitly reopened.

## Git Status At Lock

```text
UNAVAILABLE: Command '['git', 'status', '--short']' returned non-zero exit status 128.
```

Note: if the git fields show unavailable, the active workspace is not initialized as a git repository. The manuscript lock still applies to the local file state listed above.
