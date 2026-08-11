# Code Availability

Code used for data preprocessing, split generation, benchmark models, statistical analyses, figure generation and source-data generation is publicly available at https://github.com/seefreewind/spatialleak and archived at https://doi.org/10.5281/zenodo.21881438.

The release will include `src/`, `scripts/`, `configs/`, `tests/`, frozen target-panel metadata and paper assets needed to reproduce the submitted figures from processed results. The paper-asset smoke test is:

```bash
python3 scripts/reproduce_paper_assets.py
```

The unit-test smoke test is:

```bash
python3 -m pytest
```

This statement follows Springer Nature code policy for original research that uses custom code needed to interpret and replicate the reported conclusions.
