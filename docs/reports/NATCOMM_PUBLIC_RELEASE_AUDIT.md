# Nature Communications Public Release Audit

## Git status

Exit code: `128`

```text
fatal: not a git repository (or any of the parent directories): .git
```

## P0 checks

| Check | Status | Notes |
|---|---|---|
| Local absolute paths in submission package | PASS | Source-data tables and submission files do not contain user-local paths. |
| Credentials / API keys / secrets | PASS | 0 suspicious filename hits. |
| Large h5ad files | PENDING EXCLUDE | 5 processed `.h5ad` files exist and should not be committed to the public code repo by default. |
| Temporary logs | PENDING EXCLUDE | 27 log files exist under `results/`; keep only selected provenance logs if needed. |
| Restricted/private data | PASS BY AUDIT | Restricted EGA data were not used. |
| Corrected GraphSAGE default path | PASS | Train-only PCA feature scaling is present in `src/models/graphsage.py`. |
| Obsolete old GraphSAGE result tables | PENDING CURATION | Old tables remain as historical artifacts but V6 and source data use corrected Phase 19 tables. |

## Release action

Create a clean public release branch or export that excludes raw data, large processed objects, caches and unnecessary logs while retaining source code, configs, tests, target-panel metadata, paper assets and Source Data.
