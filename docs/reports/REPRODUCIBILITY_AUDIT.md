# Reproducibility Audit

## Runtime

- Operating system: `macOS-26.4-arm64-arm-64bit`
- Python: `Python 3.9.6`
- Key dependency versions:

```text
anndata==0.10.9
numpy==1.26.4
pandas==2.3.3
scipy==1.13.1
scikit-learn==1.6.1
PyYAML==6.0.3
torch==2.8.0
scanpy==1.10.3
```

## Seeds And Configs

- DLPFC formal benchmark: seeds 0-9.
- Andersson and Thrane shared-panel patient-channel analyses: seeds 0-4 for shared-panel tables, 0-9 where formal external V0.1 files are used.
- Visium breast: seeds 0-9.
- GSE278936 prostate spatial pilot: seeds 0-4.
- Phase 18 random-size-matched control: DLPFC and Visium breast seeds 0-9; GSE278936 seeds 0-4.

## Full Reproduction

Full reproduction requires raw public data downloads, preprocessing, split construction, baseline training, GraphSAGE runs, paper table generation, and figure generation. Start from:

- `scripts/download_dlpfc.py`
- `scripts/download_external.py`
- `scripts/download_gse278936_processed_minimal.py`
- `scripts/preprocess_dlpfc.py`
- `scripts/preprocess_external.py`
- `scripts/preprocess_gse278936_prostate.py`
- `scripts/formal_benchmark.py`
- `scripts/benchmark_external.py`
- `scripts/run_graphsage_formal.py`
- `scripts/run_graphsage_external.py`
- `scripts/build_paper_tables.py`
- `scripts/run_sample_size_defense.py`

## Paper-Assets Reproduction

Paper-assets reproduction starts from existing processed `.h5ad` files and result aggregates under `data/processed/` and `results/`. Use:

```bash
python3 scripts/build_two_channel_leakage_table.py
python3 scripts/build_paper_tables.py
python3 scripts/run_sample_size_defense.py
python3 scripts/make_paper_figures.py
python3 scripts/finalize_phase18_package.py
```

## Resource Notes

- DLPFC and Visium breast controls run on CPU in the current environment.
- GSE278936 has 134,509 public spots in the processed object and is the main RAM/time driver.
- GPU is optional for baseline controls; GraphSAGE runtime depends on PyTorch availability.

## Data Locations

- Raw public data: `data/raw/`
- External admission audit files: `data/external_audit/`
- Processed AnnData objects and target panels: `data/processed/`
- Benchmark results: `results/`
- Paper assets: `results/paper_assets/`
- Reports and manuscript drafts: `docs/reports/`, `manuscript/`
