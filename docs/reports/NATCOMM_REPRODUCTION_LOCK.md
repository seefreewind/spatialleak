# Nature Communications Reproduction Lock

## Decision

**PASS.**

## Runtime

- System: `macOS-26.4-arm64-arm-64bit`
- Python: `3.9.6`
- Paper-asset smoke test expected runtime: seconds to a few minutes from existing processed result assets.
- Unit-test expected runtime: seconds.

## Paper-asset smoke test

Command:

```bash
python3 scripts/reproduce_paper_assets.py
```

Exit code: `0`

```text
+ /Library/Developer/CommandLineTools/usr/bin/python3 scripts/build_paper_tables.py
wrote paper assets -> results/paper_assets
+ /Library/Developer/CommandLineTools/usr/bin/python3 scripts/build_two_channel_leakage_table.py
wrote results/paper_assets/table_two_channel_leakage.csv (12 rows)
+ /Library/Developer/CommandLineTools/usr/bin/python3 scripts/build_phase19_corrected_tables.py
      dataset              preprocessing strict_label     model  random  strict     LI    RLI  retention  rli_denominator_floor
    Andersson train_only_pca_and_scaling matched_hop0 graphsage  0.2520  0.2332 0.0188 0.0746     0.9254                   0.05
    Andersson train_only_pca_and_scaling      patient graphsage  0.2520  0.0769 0.1752 0.6950     0.3050                   0.05
       Thrane train_only_pca_and_scaling      patient graphsage  0.3039  0.0877 0.2162 0.7115     0.2885                   0.05
Visium breast train_only_pca_and_scaling matched_hop5 graphsage  0.2915  0.2142 0.0773 0.2651     0.7349                   0.05
wrote results/paper_assets/table_graphsage_shared_panel50_RLI_trainonly.csv
wrote results/paper_assets/table_two_channel_leakage_phase19.csv (11 rows)
+ /Library/Developer/CommandLineTools/usr/bin/python3 scripts/make_paper_figures.py
Wrote figures to /Users/zy/Documents/SpatialLeak：空间组学模型的泄漏安全评测/spatialleak/results/paper_assets/figures
paper asset smoke test PASS
```

## Unit tests

Command:

```bash
python3 -m pytest
```

Exit code: `0`

Summary: `7 passed`

```text
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/zy/Documents/SpatialLeak：空间组学模型的泄漏安全评测/spatialleak
plugins: anyio-4.12.1
collected 7 items

tests/test_metrics_models.py ...                                         [ 42%]
tests/test_splits.py ....                                                [100%]

============================== 7 passed in 5.09s ===============================
```
