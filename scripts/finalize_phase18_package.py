#!/usr/bin/env python3
"""Generate Phase 18 manuscript-lock reports and V3 manuscript draft."""
from __future__ import annotations

import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path

import pandas as pd


ROOT = Path(".")
REPORTS = ROOT / "docs" / "reports"
PAPER = ROOT / "results" / "paper_assets"
MANUSCRIPT = ROOT / "manuscript"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n")


def cmd(args: list[str]) -> str:
    try:
        return subprocess.check_output(args, stderr=subprocess.STDOUT, text=True).strip()
    except Exception as exc:
        return f"UNAVAILABLE: {exc}"


def fmt(x: float) -> str:
    if pd.isna(x):
        return "NA"
    return f"{x:.3f}"


def load_tables():
    two = pd.read_csv(PAPER / "table_two_channel_leakage.csv")
    gse = pd.read_csv(PAPER / "table_gse278936_spatial_pilot_RLI.csv")
    size = pd.read_csv(PAPER / "table_random_size_matched_control.csv")
    split = pd.read_csv(PAPER / "table_split_sample_sizes.csv")
    return two, gse, size, split


def summary_strings():
    two, gse, size, split = load_tables()
    def row(dataset, model):
        r = two[(two.dataset == dataset) & (two.model == model)].iloc[0]
        return r
    vis_knn = row("Visium breast", "spatial_knn")
    dlpfc_knn = row("DLPFC", "spatial_knn")
    anders_gsage = row("Andersson", "graphsage")
    thrane_gsage = row("Thrane", "graphsage")
    gse_pca = gse[(gse.model == "pca_ridge") & (gse.comparison == "random_vs_matched_hop5")].iloc[0]
    size_summary = (
        size.groupby(["dataset_label", "model", "hop"])[
            ["random_full_mean_pearson", "random_size_matched_mean_pearson", "spatial_buffer_mean_pearson", "delta_size", "delta_spatial"]
        ]
        .mean()
        .reset_index()
    )
    return {
        "vis_knn_rli": fmt(vis_knn.RLI_spatial),
        "dlpfc_knn_rli": fmt(dlpfc_knn.RLI_spatial),
        "anders_gsage_patient": fmt(anders_gsage.RLI_patient),
        "thrane_gsage_patient": fmt(thrane_gsage.RLI_patient),
        "gse_pca_hop5": fmt(gse_pca.strict_mean_pearson),
        "gse_pca_rli5": fmt(gse_pca.rli),
        "size_summary": size_summary,
        "split_summary": split,
    }


def final_experiment_lock():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_head = cmd(["git", "rev-parse", "--short", "HEAD"])
    status = cmd(["git", "status", "--short"])
    text = f"""
# Final Experiment Lock

**Status:** EXPERIMENTAL PHASE CLOSED  
**Lock date:** {now}  
**Git commit:** {git_head}  

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
{status}
```

Note: if the git fields show unavailable, the active workspace is not initialized as a git repository. The manuscript lock still applies to the local file state listed above.
"""
    write(REPORTS / "FINAL_EXPERIMENT_LOCK.md", text)


def figure_architecture():
    text = """
# Phase 18 Final Figure Architecture

## Final Main Figures

| Figure | Purpose | Main panels | Source data |
|---|---|---|---|
| Fig. 1 | SpatialLeak concept and evidence hierarchy | Random spot split, spatial buffer, slide, patient, dataset tiers; two inflation channels | schematic plus `docs/reports/EVIDENCE_HIERARCHY.md` |
| Fig. 2 | Random split inflation across datasets | Dataset/model RLI heatmap; random versus strict mean Pearson | `table_two_channel_leakage.csv` |
| Fig. 3 | Non-zero spatial buffers reveal neighborhood dependence | DLPFC and Visium breast hop curves; GSE278936 PCA hop curve as spatial-channel replication | `figure_distance_curve_data.csv`, `table_gse278936_spatial_pilot_RLI.csv` |
| Fig. 4 | Sample-size defense | Random full versus random-size-matched versus spatial buffer for hop2/hop5 | `table_random_size_matched_control.csv` |
| Fig. 5 | Patient/batch channel | Andersson and Thrane PCA+Ridge/GraphSAGE patient-held-out losses; DLPFC mixed case | `table_two_channel_leakage.csv`, `table_graphsage_shared_panel50_RLI.csv` |
| Fig. 6 | Model ranking and evaluation hierarchy | Model advantage changes by split regime; evaluation-tier decision tree | `table_two_channel_leakage.csv`, final manuscript methods |

## Supplementary Reallocation

- Move Andersson-to-Visium cross-platform mean Pearson 0.199 to Supplementary Information as a stress test.
- Keep GSE278936 in the spatial-channel supplementary/external replication logic, not the patient-held-out validation logic.
- Keep near-zero Spatial kNN rows in source tables but do not use them for positive RLI claims.

## Legend Rules

- Define LI, RLI, and retention in every figure legend that uses them.
- State when RLI is not interpreted because the random denominator is near zero.
- Use "apparent generalization inflation" for LI/RLI and reserve "patient-held-out" for true patient separation.
"""
    write(REPORTS / "FINAL_FIGURE_ARCHITECTURE_PHASE18.md", text)


def terminology_audit():
    text = """
# Final Terminology Audit

## Locked Vocabulary

| Term | Use | Avoid |
|---|---|---|
| apparent generalization inflation | Primary interpretation of random-minus-strict performance loss | causal proof of leakage |
| leakage inflation (LI) | Numeric difference `Perf_random - Perf_strict` | leakage rate |
| relative leakage inflation (RLI) | Normalized LI when random performance is interpretable | RLI when random performance is near zero |
| spatial-neighborhood channel | Within-section train-test proximity and local tissue continuity | universal spatial leakage |
| patient/batch-associated channel | Patient, section, sample, batch, and cohort-associated shortcuts | clean causal patient mechanism |
| spatial-channel external replication | GSE278936 public Visium role | patient-level validation |
| section-level transfer | Visium breast slide-held-out role | independent patient validation |
| dataset-held-out stress test | Andersson-to-Visium cross-platform result | definitive external validation |

## High-Risk Terms

- `external validation`: use only for true external dataset stress tests and define the evidence level. Do not use for GSE278936 patient validation.
- `independent`: specify independent dataset, section, patient, or split tier.
- `bias`: use for evaluation bias or optimistic performance estimates, not for unmeasured biological bias.
- `causal`, `proof`, `proves`: avoid for LI/RLI. Replace with `supports`, `indicates`, or `is consistent with`.
- `shortcut`: acceptable for patient/batch-associated predictive structure, but pair with a boundary sentence that it may combine biological and technical components.

## Manuscript Rule

Every Results subsection should start with the question being tested, then report the evidence, then give one bounded interpretation. Avoid long sequences of table values in prose; move dense numbers to source tables or Supplementary Information.
"""
    write(REPORTS / "FINAL_TERMINOLOGY_AUDIT.md", text)


def title_abstract_lock():
    s = summary_strings()
    candidates = [
        ("Leakage-resistant benchmarking reveals two channels of inflated generalization in spatial omics prediction", 5, 2, 5, 4, 4),
        ("SpatialLeak separates spatial-neighborhood and patient-associated inflation in spatial omics prediction", 5, 2, 4, 4, 5),
        ("Random spot splits overestimate spatial omics prediction through local and patient-associated dependence", 5, 2, 4, 4, 4),
        ("Evaluation design reshapes apparent model performance in spatial omics prediction", 4, 1, 5, 5, 3),
        ("SpatialLeak: an evidence hierarchy for leakage-resistant spatial omics prediction", 4, 1, 5, 4, 4),
        ("Stricter split designs expose hidden dependence in spatial omics prediction benchmarks", 4, 2, 4, 4, 4),
        ("Spatial and patient-associated dependence inflate random-split performance in spatial omics prediction", 5, 2, 4, 5, 4),
        ("A benchmark framework for split-aware evaluation of spatial omics prediction", 3, 1, 5, 5, 3),
        ("SpatialLeak identifies evaluation-dependent inflation in spatial transcriptomics prediction", 4, 2, 5, 5, 4),
        ("From random spots to patient-held-out tests: a hierarchy for spatial omics model evaluation", 4, 1, 4, 4, 3),
    ]
    table = "\n".join(
        f"| {t} | {n} | {r} | {j} | {l} | {m} |" for t, n, r, j, l, m in candidates
    )
    abstract_a = f"""Spatial omics prediction models are often evaluated with random spot-level splits, a practice that can place neighboring tissue locations or same-patient samples on both sides of the train-test boundary. We developed SpatialLeak, a split-aware benchmark that compares random splits with spatial-buffer, slide-held-out, patient-held-out, and dataset-held-out evaluation across public spatial transcriptomics datasets. Random splits inflated apparent performance through two separable channels. Dense Visium breast data showed strong spatial-neighborhood sensitivity, with Spatial kNN hop5 RLI of {s['vis_knn_rli']}, while Andersson and Thrane showed large patient/batch-associated losses for GraphSAGE, with patient RLI values of {s['anders_gsage_patient']} and {s['thrane_gsage_patient']}. A GSE278936 prostate Visium pilot replicated the spatial-channel pattern for PCA+Ridge but not for near-zero kNN. Size-matched random controls showed that spatial-buffer loss exceeded sample-count loss in the main spatial settings. SpatialLeak provides an evidence hierarchy for matching spatial omics evaluation to the intended generalization claim."""
    abstract_b = f"""Spatial transcriptomics benchmarks commonly use random spot-level splits, although spatial neighborhoods and patient-specific structure can make test performance optimistic. SpatialLeak evaluates this risk by pairing permissive random splits with spatially buffered, section-held-out, patient-held-out, and dataset-held-out tests. Across DLPFC, breast cancer, melanoma, and prostate datasets, random-split advantages were not explained by one mechanism. Spatial kNN in dense Visium breast data dropped sharply under spatial buffering, whereas PCA+Ridge and GraphSAGE showed large patient-held-out losses in Andersson and Thrane. In GSE278936 prostate Visium, PCA+Ridge was unchanged at hop0 but declined under non-zero buffers, supporting a spatial-channel replication without providing patient-level validation. Random-size-matched controls showed that reduced sample count alone did not explain the main spatial-buffer losses. These results argue for split-aware reporting in spatial omics prediction and separate local neighborhood dependence from patient/batch-associated shortcuts."""
    abstract_c = f"""Random train-test splits can overstate performance in spatial omics prediction when nearby or same-patient observations are shared across splits. We introduce SpatialLeak, an evaluation framework that compares random spot splits with spatial-buffer, slide-held-out, patient-held-out, and dataset-held-out protocols. Across public spatial transcriptomics datasets, the random-split advantage separated into spatial-neighborhood and patient/batch-associated channels. Spatial kNN was highly sensitive to spatial buffering in dense Visium breast data, while GraphSAGE showed strong patient-held-out loss in Andersson and Thrane. GSE278936 prostate Visium provided an additional spatial-channel replication for PCA+Ridge, with the important boundary that kNN performance was near zero and RLI was not interpreted. A random-size-matched control confirmed that the main spatial-buffer losses were larger than the loss expected from sample-count reduction. SpatialLeak turns spatial omics model evaluation from a single leaderboard into a hierarchy of generalization claims."""
    text = f"""
# Final Title And Abstract Lock

## Title Candidates

| Candidate | Novelty clarity | Overclaim risk | Journal fit | Length | Memorability |
|---|---:|---:|---:|---:|---:|
{table}

## Top 3

1. **Leakage-resistant benchmarking reveals two channels of inflated generalization in spatial omics prediction**
2. **SpatialLeak separates spatial-neighborhood and patient-associated inflation in spatial omics prediction**
3. **Random spot splits overestimate spatial omics prediction through local and patient-associated dependence**

## Recommended Top 1

**Leakage-resistant benchmarking reveals two channels of inflated generalization in spatial omics prediction**

This title is explicit, searchable, and defensible. It names the evaluation problem, the core conceptual result, and the application domain without claiming universal causality.

## Abstract A: Genome Biology Leaning

{abstract_a}

## Abstract B: Nature Communications Leaning

{abstract_b}

## Abstract C: Bioinformatics / Briefings Leaning

{abstract_c}

## Master Abstract Recommendation

Use Abstract B as the master abstract. It is concise, avoids citation needs, includes the Phase 18 sample-size defense, and keeps GSE278936 in the correct spatial-channel replication role.
"""
    write(REPORTS / "FINAL_TITLE_ABSTRACT_LOCK.md", text)
    return abstract_b


def references():
    audit = """
# Reference Audit Final

Only verified references are placed in `manuscript/references_master.bib`. Items that still need author-side confirmation should be kept out of the formal manuscript until checked.

## Verified Reference Set

| Key | Category | Status | Verification source |
|---|---|---|---|
| Stahl2016Science | foundational spatial transcriptomics | VERIFIED | Science DOI `10.1126/science.aaf2403`; PubMed PMID 27365449 |
| Maynard2021NatNeurosci | source dataset, DLPFC Visium | VERIFIED | Nature Neuroscience DOI `10.1038/s41593-020-00787-0`; PubMed PMID 33558695 |
| Andersson2021NatCommun | source dataset, HER2+ breast ST | VERIFIED | Nature Communications DOI `10.1038/s41467-021-26271-2`; PubMed PMID 34650042 |
| Andersson2021Zenodo | dataset record | VERIFIED | Zenodo DOI `10.5281/zenodo.4751624` |
| Thrane2018CancerRes | source dataset, melanoma ST | VERIFIED | Cancer Research DOI `10.1158/0008-5472.CAN-18-0747`; PubMed PMID 30154148 |
| Kiviaho2024NatCommun | source dataset, GSE278936 prostate | VERIFIED | Nature Communications DOI `10.1038/s41467-024-54364-1`; PubMed PMID 39550375 |
| TenXBreastSection1 | source dataset, Visium breast demo | VERIFIED URL | 10x Genomics dataset page |
| Abdelaal2020NAR | prediction model | VERIFIED | Nucleic Acids Research DOI `10.1093/nar/gkaa740`; PubMed PMID 32955565 |
| He2020NatBiomedEng | prediction model | VERIFIED | Nature Biomedical Engineering DOI `10.1038/s41551-020-0578-x`; PubMed PMID 32572199 |
| Hamilton2017GraphSAGE | graph model | VERIFIED | arXiv `1706.02216`; SNAP project page |
| Moran1950Biometrika | spatial autocorrelation | VERIFIED | Biometrika DOI `10.1093/biomet/37.1-2.17`; PubMed PMID 15420245 |
| Ambroise2002PNAS | leakage / validation bias | VERIFIED | PNAS DOI `10.1073/pnas.102102699`; PubMed PMID 11983868 |
| Vabalas2019PLOSOne | ML validation sample-size bias | VERIFIED | PLoS One DOI `10.1371/journal.pone.0224365`; PubMed PMID 31697686 |
| Kapoor2023Patterns | leakage in ML-based science | VERIFIED | Patterns DOI `10.1016/j.patter.2023.100804`; PubMed PMID 37720327 |

## Items Not Yet Added

- Additional SOTA spatial prediction/foundation-model references: **UNVERIFIED_REFERENCE** until the exact methods discussed in the final Introduction/Discussion are fixed.
- Journal reporting/checklist references: **UNVERIFIED_REFERENCE** unless the target journal requires them.
"""
    bib = r"""
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
"""
    write(REPORTS / "REFERENCE_AUDIT_FINAL.md", audit)
    write(MANUSCRIPT / "references_master.bib", bib)


def reproducibility_and_release():
    py = cmd(["python3", "--version"])
    deps = cmd([
        "python3",
        "-c",
        "import importlib.metadata as m; "
        "pkgs=['anndata','numpy','pandas','scipy','scikit-learn','PyYAML','torch','scanpy']; "
        "print('\\n'.join(f'{p}=='+m.version(p) for p in pkgs if p in {p:p for p in pkgs}))",
    ])
    text = f"""
# Reproducibility Audit

## Runtime

- Operating system: `{platform.platform()}`
- Python: `{py}`
- Key dependency versions:

```text
{deps}
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
"""
    write(REPORTS / "REPRODUCIBILITY_AUDIT.md", text)

    release = f"""
# GitHub Release Checklist

## Repository State

- Git repository detected: `{'no' if cmd(['git','rev-parse','--is-inside-work-tree']).startswith('UNAVAILABLE') else 'yes'}`
- Suggested release tag after repository initialization/cleanup: `v1.0.0`
- No push was performed.

## Large Files

- `data/` is approximately 4.0 GB and should not be committed to a normal GitHub repository.
- `results/` is approximately 97 MB and may need selective inclusion.
- Recommended release strategy: commit source code, configs, manuscript, reports, and small paper asset tables; deposit large processed data and raw-data-derived objects separately.

## Secret/Path Audit

No `.env`, `.pem`, `.key`, `*secret*`, or `*token*` files were detected by the Phase 18 shell audit. Absolute local paths remain in documentation where they record local execution context; remove or generalize them before public release if the repository should be machine-portable.

## Pre-Release Tasks

- Add a top-level reproducibility section to `README.md`.
- Confirm data redistribution rights for 10x Genomics demo files and downloaded public matrices.
- Move large raw/processed data to an external repository or release artifact.
- Add `manuscript/references_master.bib`.
- Confirm author names, affiliations, funding, competing interests, and acknowledgements.
- Create a clean git repository or move this workspace into git before tagging.
"""
    write(REPORTS / "GITHUB_RELEASE_CHECKLIST.md", release)


def reviewer_defense():
    answers = [
        ("Is this ordinary distribution shift rather than leakage?", "We frame LI/RLI as apparent generalization inflation, not causal proof that all loss is leakage.", "LEAKAGE_VS_DISTRIBUTION_SHIFT.md; V3 Discussion.", "Strict splits can contain legitimate distribution shift.", "Discussion, paragraph 2 and Methods metrics."),
        ("Does buffering simply reduce sample size?", "Phase 18 random-size-matched controls show delta_spatial exceeds delta_size in DLPFC and Visium breast and for GSE PCA.", "table_random_size_matched_control.csv; SAMPLE_SIZE_MATCHING_AUDIT.md.", "Some validation/test exact matching was capped where random partitions were smaller.", "Results subsection 2 and Methods."),
        ("Is GSE278936 patient validation?", "No. It is spatial-channel Visium replication only.", "GSE public design 52 patients/52 sections; V3 wording.", "Patient and section effects cannot be separated.", "Results subsection 2; Data availability."),
        ("Is Visium breast patient-held-out?", "No. It is section-level transfer and spatial-buffer evidence.", "EVIDENCE_HIERARCHY.md.", "Single-patient design limits generalization tier.", "Results subsection 2; Discussion limitations."),
        ("Why use simple baselines?", "PCA+Ridge and Spatial kNN are diagnostic baselines; GraphSAGE tests whether graph models follow the same split dependence.", "Model comparisons in table_two_channel_leakage.csv.", "Not a SOTA leaderboard.", "Methods models; Discussion."),
        ("Why not add SOTA models?", "The question is evaluation design under frozen splits, not model competition.", "FINAL_EXPERIMENT_LOCK.md.", "Reviewers may ask for one application-specific method.", "Discussion limitations."),
        ("Why use mean Pearson?", "It summarizes per-gene predictive association and is standard for gene-expression prediction comparisons.", "Metrics method and source tables.", "Correlation ignores calibration.", "Methods metrics."),
        ("How are near-zero random denominators handled?", "RLI is not interpreted when random performance is near zero.", "CLAIM_STATISTICS_AUDIT.md; source tables.", "Threshold is a reporting rule rather than a biological cutoff.", "Methods metrics; Results boundary paragraphs."),
        ("Are spots treated as independent?", "No statistical claims are framed as spot-level independent replication.", "CLAIM_STATISTICS_AUDIT.md.", "Some descriptive metrics are spot-level predictions aggregated by gene.", "Methods statistics."),
        ("Does Moran explain patient/batch loss?", "No. Patient-channel mixed model Moran coefficient was near zero.", "final_stats mixed-effects report.", "Patient/batch effects remain mechanistically unresolved.", "Results subsection 3."),
        ("Is kNN collapse universal?", "No. kNN is boundary-setting in low-density ST v1.0 and GSE278936.", "two-channel table; GSE pilot table.", "Model/data geometry affects kNN utility.", "Results subsections 2 and 4."),
        ("Can high retention be legitimate biology?", "Yes. Spatial dependence is not intrinsically leakage if it transfers across the intended tier.", "LEAKAGE_VS_DISTRIBUTION_SHIFT.md.", "Cannot fully decompose biology from technical structure.", "Discussion."),
        ("Are target genes cherry-picked?", "Target panels are frozen by Moran-ranking or shared_panel_50 before model comparison.", "configs and gene panel files.", "Moran-selected genes enrich spatial signal.", "Methods target panels."),
        ("Are patient and batch separated?", "Only partly. Patient-held-out tests patient-associated structure, which may include batch/sample/cohort effects.", "EVIDENCE_HIERARCHY.md.", "Causal decomposition requires designs not available in all public datasets.", "Results subsection 3; Discussion."),
        ("Can the work be reproduced?", "Yes for paper assets from processed files; full reproduction requires public downloads and larger storage.", "REPRODUCIBILITY_AUDIT.md.", "Large data release/deposition decision remains open.", "Data and code availability."),
    ]
    rows = "\n".join(f"| {q} | {a} | {e} | {w} | {loc} |" for q, a, e, w, loc in answers)
    text = f"""
# Pre-Submission Reviewer Defense

| Reviewer question | Current answer | Evidence | Residual weakness | Exact manuscript location |
|---|---|---|---|---|
{rows}
"""
    write(REPORTS / "PRE_SUBMISSION_REVIEWER_DEFENSE.md", text)


def manuscript_v3(master_abstract: str):
    s = summary_strings()
    manuscript = f"""
# Leakage-resistant benchmarking reveals two channels of inflated generalization in spatial omics prediction

## Abstract

{master_abstract}

## Introduction

Spatial transcriptomics measures molecular state while preserving tissue location, making it possible to connect gene expression with tissue architecture. This has motivated prediction tasks in which measured genes, spatial expression profiles, or molecular states are inferred from other genes, neighboring spots, graph structure, or matched tissue morphology [1,8,9]. These tasks are now used to compare model classes and to decide whether spatial context improves prediction.

The interpretation of these benchmarks depends on the split design. A random spot-level split can place neighboring tissue locations, spots from the same section, and samples from the same patient on both sides of the train-test boundary. In that setting, high test performance can reflect local neighborhood dependence or patient-associated structure as much as transportable prediction. This problem is familiar in machine learning and genomics, where leakage and validation bias can produce optimistic performance estimates [12-14].

Spatial omics adds a specific difficulty: spatial dependence is not automatically an error. A model that uses laminar brain architecture or conserved tumor organization may be learning meaningful biology if the signal transfers across the intended evaluation tier. The practical problem is therefore not to remove all spatial information. It is to match the evaluation design to the claim being made: local interpolation, transfer across sections, patient-level generalization, dataset transfer, or cross-platform transportability.

Here we present SpatialLeak, a leakage-resistant benchmark framework for spatial omics prediction. SpatialLeak compares random spot splits with spatial-buffer, slide-held-out, patient-held-out, and dataset-held-out tests across public spatial transcriptomics datasets [2-7]. It reports leakage inflation (LI), relative leakage inflation (RLI), and strict-split retention for PCA+Ridge, Spatial kNN, and GraphSAGE. The framework separates two channels of apparent generalization inflation: local spatial-neighborhood dependence and patient/batch-associated shortcuts.

## Results

### Random spot-level splitting inflates apparent predictive generalization

How much random-split performance is retained when the train-test boundary matches a stricter generalization claim? Across the frozen paper tables, random spot-level splits produced higher apparent performance than stricter patient, section, or spatial-buffer evaluations in multiple datasets and model classes. The pattern was not limited to a single platform or tissue.

In the patient-channel datasets, PCA+Ridge showed clear random-to-patient losses in DLPFC, Andersson HER2-positive breast cancer, and Thrane melanoma. The same channel was reproduced by GraphSAGE in the tumor datasets, with patient RLI values of {s['anders_gsage_patient']} in Andersson and {s['thrane_gsage_patient']} in Thrane. These results show that graph-based spatial models can remain sensitive to patient- or sample-associated structure.

The spatial-channel datasets showed a different pattern. DLPFC and Visium breast retained some strict-split signal but lost performance under spatial separation, especially for Spatial kNN. Visium breast was the clearest dense-platform example, with Spatial kNN hop5 RLI of {s['vis_knn_rli']}. These findings support the central premise of SpatialLeak: random spot-level performance is not a sufficient estimate of the generalization claimed by a model.

### Non-zero spatial buffers reveal neighborhood dependence

Does a non-overlapping spatial partition remove local train-test neighborhood overlap? The matched-hop experiments show that hop0 partitions can still be too permissive. A non-zero spatial buffer was needed to reveal the full loss associated with local neighborhood separation.

In Visium breast, Spatial kNN performance dropped sharply as the hop buffer increased, while the slide-held-out result retained substantial signal. This contrast indicates that a local-neighborhood channel and section-level transportable structure can coexist. DLPFC showed a related but milder pattern, with Spatial kNN spatial RLI of {s['dlpfc_knn_rli']}.

GSE278936 prostate was used only as a spatial-channel Visium replication. In the public GEO portion, 52 patients correspond to 52 sections, so patient and section effects cannot be separated. Within that boundary, PCA+Ridge showed the expected distance response: random and hop0 performance were nearly identical, while hop5 decreased to {s['gse_pca_hop5']} (RLI {s['gse_pca_rli5']}). Spatial kNN was near zero in this dataset, so its RLI was not interpreted.

The Phase 18 random-size-matched control addressed whether these decreases were artifacts of smaller test sets. In DLPFC and Visium breast, the loss from imposing the spatial buffer exceeded the loss from reducing the random split to comparable sample size. GSE278936 PCA+Ridge showed the same direction with smaller magnitude. This control supports the interpretation that the main spatial-buffer losses were not explained by sample count alone.

### Patient-held-out evaluation identifies a distinct patient-associated channel

Does patient separation reveal a channel that spatial buffers miss? Andersson and Thrane answer yes. In these ST v1.0 tumor datasets, patient-held-out performance losses were large for PCA+Ridge and GraphSAGE even when some spatial-buffer comparisons were weak or near zero.

Andersson showed the clearest contrast. GraphSAGE had a small matched_hop0 loss but a large patient-held-out loss, indicating that a model can appear robust to within-section block separation while still depending on patient-associated structure. Thrane showed the same patient-channel pattern for GraphSAGE, despite low-density geometry that made high-hop kNN curves difficult to interpret.

DLPFC was a mixed case. Patient-held-out losses were present but smaller than the strongest tumor-dataset patient losses, and Spatial kNN retained substantial patient-held-out signal. This is consistent with a setting where some spatial structure is transportable across donors. The result also shows why the manuscript should not equate every strict-split loss with leakage.

### Dominant inflation channels vary across datasets and model classes

Which channel dominates depends on the dataset and model. DLPFC contains both spatial and patient-associated components. Andersson and Thrane are patient-channel dominant for PCA+Ridge and GraphSAGE. Visium breast is spatial-channel dominant but cannot support patient-level claims. GSE278936 supports a PCA+Ridge spatial-channel replication and a kNN boundary condition.

This heterogeneity is a result, not a nuisance. It shows that a single benchmark split cannot diagnose all forms of apparent generalization. It also explains why simple diagnostic baselines are useful: Spatial kNN can directly reveal local neighborhood dependence when it has signal, while PCA+Ridge provides a strong non-graph baseline and GraphSAGE tests whether graph learning follows the same split-dependent patterns.

### Model advantage depends on evaluation regime

Does a model remain advantaged after the split changes? The answer was evaluation-dependent. GraphSAGE reproduced patient-channel sensitivity in Andersson and Thrane, rather than eliminating it. Spatial kNN was strong under random or dense local conditions but collapsed in several low-signal or spatially isolated settings. PCA+Ridge often retained more performance under broader transfer than purely spatial kNN.

These observations argue against interpreting random-split leaderboards as model rankings for patient- or dataset-level generalization. A model can be useful for local interpolation while being weak for patient-held-out transfer. Conversely, a method with lower random-split performance may retain more signal under the evaluation tier that matches the intended use.

### SpatialLeak defines a hierarchy for robust evaluation

SpatialLeak organizes evaluation evidence into a hierarchy. Random spot splits test local interpolation and should be reported as permissive. Spatial-buffer splits test within-section neighborhood separation. Slide-held-out tests section transfer. Patient-held-out tests patient-, sample-, and batch-associated structure. Dataset-held-out and cross-platform tests evaluate broader transportability.

This hierarchy clarifies the role of each dataset in the manuscript. DLPFC contributes both spatial and donor separation. Andersson and Thrane contribute patient/batch-channel evidence. Visium breast contributes dense Visium spatial-buffer and section-level evidence. GSE278936 contributes high-density Visium spatial-channel replication only. Andersson-to-Visium transfer is retained as a supplementary stress test, not as a main patient-level validation result.

## Discussion

SpatialLeak shows that random spot-level evaluation can overstate apparent performance in spatial omics prediction. The effect separates into at least two channels: local spatial-neighborhood dependence and patient/batch-associated structure. These channels require different split designs and should not be collapsed into a single random-split leakage claim.

The sample-size control strengthens the spatial-channel interpretation. Buffering can reduce the number of evaluable test spots, so a performance decrease could in principle arise from smaller samples. The random-size-matched control showed that reducing the random split to similar sizes had little effect in DLPFC and Visium breast compared with imposing spatial separation. This does not prove a single causal mechanism, but it rules out a simple sample-count explanation for the main spatial-buffer losses.

The patient-channel findings have a different interpretation. Andersson and Thrane showed large patient-held-out losses for PCA+Ridge and GraphSAGE. These losses may combine patient identity, section background, processing batch, cohort structure, and biological heterogeneity. The public data do not allow every component to be decomposed. The correct conclusion is that random spot splits can benefit from patient-associated structure that is not retained under patient-held-out evaluation.

Spatial dependence should not be treated as intrinsically invalid. If tissue architecture transfers across patients or sections, using that information can be biologically meaningful. DLPFC and Visium breast both illustrate this boundary: strict-split performance was reduced but not eliminated in all settings, and slide-held-out or patient-held-out retention can reflect transportable organization. SpatialLeak therefore measures whether performance is retained under the intended claim, not whether spatial information is forbidden.

The study has limitations. It uses public datasets with heterogeneous platforms, tissues, densities, and sample structures. Visium breast contains one patient and supports section-level, not patient-level, evidence. GSE278936 public data contain one section per patient, preventing clean patient-versus-section decomposition. The model set is intentionally diagnostic rather than exhaustive. The dataset-held-out stress test remains supplementary because cross-platform transfer changes more than leakage risk.

These boundaries do not weaken the main recommendation. Spatial omics prediction papers should report split designs that match their stated generalization claims, include simple diagnostic baselines, avoid interpreting near-zero RLI denominators, and separate local spatial interpolation from patient-level or dataset-level generalization. SpatialLeak provides a practical framework for doing so.

## Methods

### Benchmark overview

SpatialLeak evaluated spatial omics prediction under progressively stricter train-test separation. The benchmark compared random spot-level splits with matched spatial block splits, non-zero spatial exclusion buffers, slide-held-out splits, patient-held-out splits, and dataset-held-out stress tests. The main unit of prediction was a spatial spot or capture location, and the output was expression of a frozen target-gene panel.

### Datasets

DLPFC Visium data were derived from the human dorsolateral prefrontal cortex dataset. Andersson HER2-positive breast cancer and Thrane melanoma represented ST v1.0 tumor datasets with patient-held-out evaluation. Visium breast used public 10x Genomics breast cancer demonstration sections and was treated as section-level and spatial-buffer evidence. GSE278936 prostate Visium was used as a public spatial-channel replication only.

### Target genes and features

Dataset-specific target panels used the top 50 Moran-ranked genes available after preprocessing. Shared-panel analyses used `shared_panel_50` where required. Predictor features were selected from highly variable genes after excluding target genes. All panels were frozen before model comparison.

### Split definitions

Random spot splits used an 80/10/10 train/validation/test partition. Matched spatial block splits assigned grid blocks within each section to train, validation, or test folds and selected the candidate assignment with balanced spot count, library size, Moran signal, and layer composition where available. Hop-buffered splits removed test spots within the specified kNN graph distance from the training set. Patient-held-out splits held out all sections from a patient or donor where the dataset design allowed it.

### Models

The Mean baseline predicted target expression from training-set means. PCA+Ridge applied principal component reduction to predictor genes followed by Ridge regression for each target gene. Spatial kNN predicted each test spot from spatially nearest training spots within normalized section coordinates. GraphSAGE was included as a representative inductive graph neural network.

### Metrics

The primary metric was mean Pearson correlation across target genes. Leakage inflation was defined as `Perf_random - Perf_strict`. Relative leakage inflation was defined as `(Perf_random - Perf_strict) / Perf_random`. Retention was defined as `Perf_strict / Perf_random`. RLI was not interpreted when random-split performance was near zero.

### Sample-size control

For Phase 18, random-size-matched controls were run for DLPFC, Visium breast, and GSE278936 prostate. For each seed and matched_hop2 or matched_hop5 reference, the original random split was downsampled toward the strict split's train, validation, and test sizes, with slide composition matched where feasible. The control did not use strict-split performance to select observations.

## Data Availability

All analyses used public or project-derived data. DLPFC data are available from the source study and associated public resources [2]. Andersson HER2-positive breast cancer data are available through the Nature Communications article and Zenodo record [3,4]. Thrane melanoma data are available through the Cancer Research article and linked public dataset resources [5]. Visium breast data are available from 10x Genomics public demonstration datasets [7]. GSE278936 prostate data are available through GEO accession GSE278936 and the associated Nature Communications article [6]. Restricted EGA data from the GSE278936 study were not used. Project-derived processed objects, split manifests, and paper tables should be deposited before submission; repository DOI or accession: `[to be added]`.

## Code Availability

Analysis code, split definitions, benchmark scripts, and manuscript asset generation scripts are contained in this project workspace. Public repository URL and archival DOI: `[to be added]`.

## Author Contributions

`[Author contribution statement to be added.]`

## Funding

`[Funding statement to be added.]`

## Competing Interests

`[Competing interests statement to be added.]`

## Acknowledgements

`[Acknowledgements to be added.]`

## References

1. Ståhl, P. L. et al. Visualization and analysis of gene expression in tissue sections by spatial transcriptomics. *Science* 353, 78-82 (2016).
2. Maynard, K. R. et al. Transcriptome-scale spatial gene expression in the human dorsolateral prefrontal cortex. *Nature Neuroscience* 24, 425-436 (2021).
3. Andersson, A. et al. Spatial deconvolution of HER2-positive breast cancer delineates tumor-associated cell type interactions. *Nature Communications* 12, 6012 (2021).
4. Andersson, A. et al. Spatial deconvolution of HER2-positive breast cancer delineates tumor-associated cell type interactions. Zenodo (2021).
5. Thrane, K. et al. Spatially resolved transcriptomics enables dissection of genetic heterogeneity in stage III cutaneous malignant melanoma. *Cancer Research* 78, 5970-5979 (2018).
6. Kiviaho, A. et al. Single cell and spatial transcriptomics highlight the interaction of club-like cells with immunosuppressive myeloid cells in prostate cancer. *Nature Communications* 15, 9949 (2024).
7. 10x Genomics. Human Breast Cancer (Block A Section 1): Spatial Gene Expression dataset (2020).
8. Abdelaal, T. et al. SpaGE: Spatial Gene Enhancement using scRNA-seq. *Nucleic Acids Research* 48, e107 (2020).
9. He, B. et al. Integrating spatial gene expression and breast tumour morphology via deep learning. *Nature Biomedical Engineering* 4, 827-834 (2020).
10. Hamilton, W. L., Ying, R. & Leskovec, J. Inductive representation learning on large graphs. *Advances in Neural Information Processing Systems* (2017).
11. Moran, P. A. P. Notes on continuous stochastic phenomena. *Biometrika* 37, 17-23 (1950).
12. Ambroise, C. & McLachlan, G. J. Selection bias in gene extraction on the basis of microarray gene-expression data. *Proceedings of the National Academy of Sciences* 99, 6562-6566 (2002).
13. Vabalas, A. et al. Machine learning algorithm validation with a limited sample size. *PLOS ONE* 14, e0224365 (2019).
14. Kapoor, S. & Narayanan, A. Leakage and the reproducibility crisis in machine-learning-based science. *Patterns* 4, 100804 (2023).
"""
    write(MANUSCRIPT / "SPATIALLEAK_MANUSCRIPT_V3.md", manuscript)


def main():
    final_experiment_lock()
    figure_architecture()
    terminology_audit()
    abstract = title_abstract_lock()
    references()
    reproducibility_and_release()
    reviewer_defense()
    manuscript_v3(abstract)


if __name__ == "__main__":
    main()
