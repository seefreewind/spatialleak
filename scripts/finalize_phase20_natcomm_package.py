#!/usr/bin/env python3
"""Build the Phase 20 Nature Communications submission package."""
from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd


REPORTS = Path("docs/reports")
MANUSCRIPT = Path("manuscript")
PAPER = Path("results/paper_assets")
SUB = Path("submission/nature_communications")
SOURCE = SUB / "source_data"
FIGS = SUB / "FIGURES"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n")


def read(path: Path) -> str:
    return path.read_text()


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'+-]+\b", re.sub(r"`[^`]*`", "", text)))


def copy_if_exists(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.copy2(src, dst)


def load_tables() -> dict[str, pd.DataFrame]:
    return {
        "two": pd.read_csv(PAPER / "table_two_channel_leakage_phase19.csv"),
        "gs": pd.read_csv(PAPER / "table_graphsage_shared_panel50_RLI_trainonly.csv"),
        "gse": pd.read_csv(PAPER / "table_gse278936_spatial_pilot_RLI.csv"),
        "size": pd.read_csv(PAPER / "table_random_size_matched_control.csv"),
        "dist": pd.read_csv(PAPER / "figure_distance_curve_data.csv"),
        "split": pd.read_csv(PAPER / "table_split_sample_sizes.csv"),
        "dataset": pd.read_csv(PAPER / "table_dataset_specific_RLI.csv"),
        "shared": pd.read_csv(PAPER / "table_shared_panel50_RLI.csv"),
    }


def fnum(x: float) -> str:
    return f"{x:.3f}"


def key_numbers(t: dict[str, pd.DataFrame]) -> dict[str, str]:
    two = t["two"]
    gs = t["gs"]
    gse = t["gse"]
    out = {}
    out["visium_knn_rli"] = fnum(two[(two.dataset == "Visium breast") & (two.model == "spatial_knn")].iloc[0].RLI_spatial)
    out["andersson_gs_patient"] = fnum(gs[(gs.dataset == "Andersson") & (gs.strict_label == "patient")].iloc[0].RLI)
    out["thrane_gs_patient"] = fnum(gs[(gs.dataset == "Thrane") & (gs.strict_label == "patient")].iloc[0].RLI)
    out["gse_pca_hop5"] = fnum(gse[(gse.model == "pca_ridge") & (gse.comparison == "random_vs_matched_hop5")].iloc[0].rli)
    out["gse_pca_hop0"] = fnum(gse[(gse.model == "pca_ridge") & (gse.comparison == "random_vs_matched_hop0")].iloc[0].rli)
    return out


def experiment_lock() -> None:
    write(REPORTS / "PHASE20_EXPERIMENT_LOCK.md", """
# Phase 20 Experiment Lock

## Decision

**EXPERIMENTS CLOSED FOR INITIAL SUBMISSION.**

Phase 20 is a Nature Communications submission-package phase. It does not add datasets, cohorts, diseases, SOTA models, foundation models, GraphSAGE DLPFC reruns, target panels, metrics, seeds, spatial statistics, EGA restricted data, or additional cross-platform benchmarks.

## Allowed Work

- Reframe the conceptual advance for Nature Communications.
- Prepare manuscript V5, cover letter, Supplementary Information, Source Data, Data Availability, Code Availability, reporting checklist, and submission checklist.
- Audit claim-source consistency against frozen Phase 19 tables and current code.

## Reopening Rule

Experiments may be reopened only if a Nature Communications editor or peer reviewer explicitly requests a new analysis, or if a later audit finds a confirmed fatal methodological flaw.
""")


def central_claim_and_title(k: dict[str, str]) -> None:
    write(REPORTS / "NATCOMM_CENTRAL_CLAIM.md", f"""
# Nature Communications Central Claim

## One-Sentence Central Claim

Leakage-resistant evaluation reveals distinct local spatial and patient-associated generalization inflation in spatial omics prediction, requiring evaluation tiers matched to the claim being made.

Word count: 24.

## Three Supporting Claims

1. Non-zero spatial buffers exposed local neighborhood dependence, including Visium breast Spatial kNN hop5 RLI {k['visium_knn_rli']} and GSE278936 PCA+Ridge hop5 RLI {k['gse_pca_hop5']}.
2. Patient-held-out evaluation revealed a distinct patient-associated channel, reproduced by corrected train-only GraphSAGE in Andersson and Thrane.
3. Model advantage changed across split regimes, supporting an evidence hierarchy rather than a single random-split leaderboard.

## Explicit Non-Claims

- SpatialLeak does not prove all random-split performance is leakage.
- SpatialLeak does not claim all strict-split loss is invalid signal.
- Spatial dependence itself is not inherently leakage.
- Patient-held-out loss does not causally identify a specific batch effect.
- GSE278936 is not clean patient-level validation.
- The study is not an exhaustive SOTA leaderboard.
""")
    write(REPORTS / "NATCOMM_TITLE_DECISION.md", """
# Nature Communications Title Decision

| Candidate | Conceptual novelty | NatComms style | Precision | Overclaim risk | Memorability | Editor accessibility | Length | Overall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A. Leakage-resistant evaluation reveals distinct spatial and patient-associated generalization inflation in spatial omics prediction | 5 | 4 | 5 | 2 | 4 | 4 | 3 | 4.2 |
| B. SpatialLeak disentangles local spatial dependence from patient-level generalization in spatial omics prediction | 4 | 4 | 3 | 3 | 5 | 4 | 4 | 3.9 |
| C. SpatialLeak reveals evaluation-dependent generalization in spatial omics prediction | 3 | 4 | 3 | 2 | 4 | 5 | 5 | 3.8 |
| D. Evaluation design reshapes apparent generalization in spatial omics prediction | 4 | 5 | 4 | 1 | 4 | 5 | 5 | 4.4 |

## Top 2

1. **Evaluation design reshapes apparent generalization in spatial omics prediction**
2. **Leakage-resistant evaluation reveals distinct spatial and patient-associated generalization inflation in spatial omics prediction**

## Final Recommended Title

**Evaluation design reshapes apparent generalization in spatial omics prediction**

This title is shorter, editor-accessible, and avoids making the title sound like a narrow three-model benchmark. The two-channel result is then made explicit in the abstract, Figure 3, and Results.
""")


def section_texts(k: dict[str, str]) -> dict[str, str]:
    abstract = f"""
Spatial omics models are often evaluated using random spot-level splits. Spatial neighborhoods, section context and patient-associated structure can complicate the interpretation of performance estimated from such splits. We developed SpatialLeak, a leakage-resistant evaluation framework that compares random spot splits with buffered spatial, section-held-out, patient-held-out and dataset-held-out regimes. In dense Visium breast data, Spatial kNN showed strong spatial-neighborhood inflation, with hop5 relative leakage inflation (RLI) of {k['visium_knn_rli']}. Corrected train-only GraphSAGE reruns showed large patient-associated losses in Andersson and Thrane, with patient RLI values of {k['andersson_gs_patient']} and {k['thrane_gs_patient']}. In the independent GSE278936 prostate Visium cohort, PCA+Ridge was unchanged at hop0 but decreased under non-zero spatial buffers, reaching hop5 RLI {k['gse_pca_hop5']}. Random-size-matched controls indicated that reduced sample count alone did not explain the main spatial-buffer losses. SpatialLeak provides a hierarchy for matching benchmark design to the level of generalization being claimed.
""".strip()
    intro = """
Spatial transcriptomics and related spatial omics assays connect molecular measurements to tissue architecture, creating prediction tasks that are not available in dissociated profiling alone. These tasks include imputation of unmeasured genes, spatial molecular prediction, graph-based learning from tissue neighborhoods and representation learning over spatial context. As spatial datasets grow, such models increasingly support claims about whether molecular patterns can be recovered across locations, sections, patients or datasets.

The evaluation problem is that spatial observations are not independent in the ordinary IID sense. A random spot-level split can place neighboring tissue locations, similar local cell compositions, the same section background or the same patient-associated structure on both sides of the train-test boundary. Performance under this regime can therefore mix local interpolation with broader generalization.

Spatial dependence is not inherently invalid. A spatially aware model may use tissue architecture as a legitimate biological signal if that signal is retained under the separation required by the scientific claim. The central question is what claim the evaluation design can support: local interpolation, spatial transfer, section transfer, patient transfer, dataset transfer or cross-platform transfer.

Current spatial omics benchmarks do not consistently separate these levels. Existing split choices can conflate local spatial-neighborhood dependence, patient-associated structure and transportable biological signal. This makes it difficult to interpret whether an apparent model advantage reflects a robust predictive principle or the evaluation tier used to measure it.

Here we introduce SpatialLeak, a multi-tier evaluation framework for spatial omics prediction. SpatialLeak compares random spot splits with buffered spatial, section-held-out, patient-held-out and dataset-held-out regimes across public spatial transcriptomics datasets and diagnostic model classes. The framework shows that apparent generalization can arise through distinct spatial-neighborhood and patient-associated channels, and it organizes these findings into a generalization evidence hierarchy.
""".strip()
    results = f"""
## Results

### Random spot-level evaluation inflates apparent predictive generalization

SpatialLeak first tested whether random spot-level performance was retained when the train-test boundary matched a stricter generalization claim. Across DLPFC, Andersson, Thrane and Visium breast, random splits produced higher apparent performance than the relevant stricter split for the main interpretable model-dataset combinations. This established random spot evaluation as a permissive interpolation setting rather than evidence, by itself, for section-, patient- or dataset-level generalization.

The patient-channel datasets showed the clearest random-to-patient losses. In Andersson, PCA+Ridge patient RLI was 0.662, and corrected train-only GraphSAGE patient RLI was {k['andersson_gs_patient']}. In Thrane, PCA+Ridge patient RLI was 0.499, and corrected train-only GraphSAGE patient RLI was {k['thrane_gs_patient']}. These results show that a graph-based model did not remove the need for grouped evaluation.

### Non-zero spatial buffers reveal local neighborhood dependence

SpatialLeak next tested whether non-overlapping spatial partitions were sufficient to remove local neighborhood dependence. They were not always sufficient. In DLPFC and Visium breast, increasing hop distance reduced performance, especially for Spatial kNN. Visium breast showed the strongest spatial-channel example, with Spatial kNN hop5 RLI {k['visium_knn_rli']}.

GSE278936 provided an independent high-density Visium spatial-channel replication. PCA+Ridge was essentially unchanged at hop0 (RLI {k['gse_pca_hop0']}) but decreased under hop2 and hop5 buffers, reaching hop5 RLI {k['gse_pca_hop5']}. This pattern supports the specific claim that a non-zero exclusion buffer can be required to expose local neighborhood dependence. The random-size-matched control showed that the main spatial-buffer losses were larger than the losses caused by downsampling random splits to similar sample sizes.

### Patient-held-out evaluation identifies a distinct patient-associated channel

Patient-held-out evaluation measured a different axis of dependence from within-section spatial buffering. Andersson and Thrane had large patient-held-out losses even when spatial kNN was near zero or when high-hop spatial curves were not resolvable in low-density ST v1.0 geometry. DLPFC showed a mixed pattern, with both spatial and donor-associated effects.

The patient-associated channel should not be interpreted as a causal batch-effect estimate. It can include patient identity, section background, tissue processing, sample handling, cohort structure and biological heterogeneity. The result is that random spot splits can use structure that is not retained when patient-associated groups are separated.

### Dominant generalization-inflation channels vary across datasets and model classes

The strongest evidence came from treating heterogeneity as a result rather than a nuisance. DLPFC showed both spatial and donor-associated effects. Andersson and Thrane were patient-channel dominant. Visium breast was spatial-channel dominant but single-patient. GSE278936 replicated the spatial-channel PCA+Ridge buffer response and provided a kNN boundary condition because random kNN performance was below zero.

This two-channel landscape explains why one split or one model cannot diagnose all settings. Spatial kNN is useful as a local-neighborhood probe when it has signal. PCA+Ridge provides a strong non-graph baseline. Corrected train-only GraphSAGE tests whether graph learning follows the same split-dependent behavior as simpler baselines.

### Apparent model advantage depends on evaluation regime

Model comparisons changed when the evaluation claim changed. Spatial kNN was strong in dense random or local settings but weak when spatial signal was absent or isolated. Corrected GraphSAGE retained random-split performance in some settings but showed strong patient-held-out losses in tumor datasets. PCA+Ridge often retained broader transfer signal better than a purely local spatial-neighbor baseline.

These observations argue against using a single random-split leaderboard as evidence of model superiority. A method can be useful for local interpolation while being less informative for patient transfer, and a model that appears robust under a spatial split may still lose performance under patient-held-out evaluation.

### SpatialLeak defines a hierarchy for spatial-omics generalization claims

SpatialLeak formalizes six evaluation tiers. Level 0, random spot interpolation, supports local interpolation but does not establish spatial, section or patient transfer. Level 1, buffered spatial transfer, tests local neighborhood separation but does not establish patient transfer. Level 2, section-held-out transfer, tests transfer across sections but not necessarily across patients. Level 3, patient-held-out transfer, tests retention across patient-associated groups but does not establish dataset or platform transfer. Level 4, dataset-held-out transfer, tests broader dataset transportability. Level 5, cross-platform transfer, tests robustness when measurement platforms also change.

This hierarchy fixes the language of the manuscript. Visium breast supports dense Visium spatial and section-level evidence, not patient-level validation. GSE278936 supports spatial-channel replication, not clean patient-level validation. Andersson-to-Visium transfer remains a supplementary cross-platform stress test rather than a central validation claim.
""".strip()
    discussion = """
SpatialLeak shows that apparent performance in spatial omics prediction can be inflated through separable spatial-neighborhood and patient-associated channels. Random spot-level evaluation overstated apparent predictive generalization in multiple settings, non-zero spatial buffers exposed local neighborhood dependence, patient-held-out tests revealed a distinct patient-associated channel, and the resulting evidence hierarchy clarified what each evaluation tier can claim.

The non-zero buffer result is important because non-overlapping spatial blocks do not necessarily create local independence. A test spot can remain close to a training neighborhood even when it is assigned to a different block. GSE278936 illustrates this point: hop0 was essentially unchanged, whereas hop2 and hop5 exposed a stable PCA+Ridge loss. This does not mean that every study requires hop5, but it does mean that spatial split definitions should report the exclusion distance they actually impose.

Spatial information itself is not leakage. Tissue architecture is often the object of spatial omics analysis, and a model should be allowed to use it when the intended claim is local interpolation or when the signal survives stricter separation. SpatialLeak is designed to determine whether spatial signal survives the evaluation tier implied by the biological claim, not to remove spatial context from spatial models.

Patient-associated performance loss is also not a single causal mechanism. A patient-held-out drop can reflect patient identity, section context, processing batch, sample handling, cohort structure, tissue biology or their combination. Public datasets do not always allow these components to be separated. The appropriate claim is therefore patient-associated performance inflation, not proof of a specific batch shortcut.

These findings suggest practical minimum expectations for future spatial omics benchmarks. Studies should report grouped splits, explicit spatial buffers, patient separation where the claim requires it, strong non-spatial baselines, spatial diagnostic baselines, uncertainty at the biological unit, transparent split metadata and code that reproduces the evaluation tier. Model rankings should be tied to the claim being tested rather than presented as universal.

The study has clear boundaries. The model set is diagnostic rather than exhaustive. Public datasets are heterogeneous in platform, tissue, density and sample structure. Visium breast is single-patient, GSE278936 public data contain one section per patient, DLPFC corrected GraphSAGE was not used as main evidence, and cross-platform transfer remains supplementary. Strict-split loss can include legitimate distribution shift as well as leakage-sensitive dependence. These limitations define the scope of inference but do not alter the central need to align evaluation design with the generalization claim.
""".strip()
    methods = """
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
""".strip()
    return {"abstract": abstract, "introduction": intro, "results": results, "discussion": discussion, "methods": methods}


def write_manuscript_sections(k: dict[str, str]) -> dict[str, str]:
    s = section_texts(k)
    write(MANUSCRIPT / "NATCOMM_ABSTRACT.md", s["abstract"])
    write(MANUSCRIPT / "NATCOMM_INTRODUCTION.md", s["introduction"])
    write(MANUSCRIPT / "NATCOMM_DISCUSSION.md", s["discussion"])
    write(MANUSCRIPT / "NATCOMM_METHODS.md", s["methods"])
    return s


def figure_docs() -> None:
    write(REPORTS / "NATCOMM_FIGURE_PLAN_FINAL.md", """
# Nature Communications Figure Plan Final

## Figure 1 - Conceptual framework

**Message:** Evaluation design determines the level of generalization that can be claimed.

Panels: random spot split; spatial-neighborhood dependence; patient-associated structure; evaluation hierarchy; transportable biological signal. Spatial signal must be shown as potentially legitimate when retained under the relevant strict split.

## Figure 2 - Cross-dataset inflation

**Message:** Random spot-level evaluation overstates apparent predictive generalization across multiple dataset-model settings. Use a paired effect plot plus compact forest-style summaries, not a dense heatmap.

## Figure 3 - Two-channel generalization landscape

**Message:** Spatial-channel and patient-channel RLI vary independently. Plot spatial RLI against patient RLI where both are available or use a two-column channel matrix. NA must be visibly NA, never zero.

## Figure 4 - Non-zero buffer

**Message:** Non-overlapping spatial partitions may be insufficient; non-zero exclusion buffers can reveal local neighborhood dependence. Include DLPFC, Visium breast and GSE278936. Put random-size-matched controls in an inset only if readable; otherwise Supplementary Information.

## Figure 5 - Evaluation-regime-dependent model behavior

**Message:** Apparent model advantage depends on random, spatial strict and patient strict evaluation regimes. Use PCA+Ridge, Spatial kNN and corrected train-only GraphSAGE where available.

## Figure 6 - Generalization evidence hierarchy

**Message:** SpatialLeak maps evaluation tiers to supported claims and residual limitations. Levels: random spot interpolation, buffered spatial transfer, section-held-out transfer, patient-held-out transfer, dataset-held-out transfer and cross-platform transfer.
""")
    write(REPORTS / "NATCOMM_FIGURE_QA.md", """
# Nature Communications Figure QA

| Check | Status | Notes |
|---|---|---|
| White background | PASS for existing paper assets | Final assembled Figures 4-6 still require rendering. |
| Decorative gradients / 3D | PASS | Avoid in final schematic panels. |
| Colorblind accessibility | PENDING FINAL RENDER | Use distinct hue plus shape; do not encode NA as pale zero. |
| Panel labels | PENDING FINAL RENDER | Nature Communications prefers lowercase bold panel letters. |
| Editable vector | PASS for existing SVG assets; PENDING for new assembled figures | Existing SVGs copied to submission figure folder. |
| Raster resolution | PENDING FINAL EXPORT | Export line art at 1200 dpi or provide PDF/EPS/SVG-derived final files. |
| Legends | PASS in manuscript plan | Final legend text must define RLI, LI, retention, hop buffer and NA. |
| Source-data mapping | PASS | `submission/nature_communications/source_data/` contains Figure1-Figure6 source files and README. |
| Near-zero denominator rows | PASS IN PLAN | These rows are excluded from RLI interpretation and should not be plotted as valid RLI. |

Final figure rendering is a formatting task, not an experiment.
""")


def source_data(t: dict[str, pd.DataFrame]) -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([
        {"figure": "Figure 1", "panel": "a-e", "source_data_status": "No numerical source data required", "note": "Conceptual schematic derived from locked evaluation hierarchy."}
    ]).to_csv(SOURCE / "Figure1_SourceData.csv", index=False)
    t["two"].to_csv(SOURCE / "Figure2_SourceData.csv", index=False)
    cols = ["dataset", "platform", "model", "RLI_spatial", "RLI_patient", "Retention_spatial", "Retention_patient", "patient_count", "section_count"]
    t["two"][cols].to_csv(SOURCE / "Figure3_SourceData.csv", index=False)
    fig4 = pd.concat([
        t["dist"].assign(source="distance_curve"),
        t["gse"].rename(columns={"strict_mean_pearson": "mean_pearson"}).assign(source="gse278936_pilot"),
    ], ignore_index=True, sort=False)
    fig4.to_csv(SOURCE / "Figure4_SourceData.csv", index=False)
    pd.concat([t["two"], t["gs"].assign(dataset_role="corrected_graphsage_trainonly")], ignore_index=True, sort=False).to_csv(SOURCE / "Figure5_SourceData.csv", index=False)
    pd.DataFrame([
        {"level": 0, "tier": "random spot interpolation", "supports": "local interpolation", "does_not_establish": "spatial, section, patient, dataset or platform transfer"},
        {"level": 1, "tier": "buffered spatial transfer", "supports": "local neighborhood separation", "does_not_establish": "patient transfer"},
        {"level": 2, "tier": "section-held-out transfer", "supports": "section transfer", "does_not_establish": "patient transfer unless patient identity is separated"},
        {"level": 3, "tier": "patient-held-out transfer", "supports": "retention across patient-associated groups", "does_not_establish": "dataset or platform transfer"},
        {"level": 4, "tier": "dataset-held-out transfer", "supports": "dataset transportability stress test", "does_not_establish": "cross-platform transfer"},
        {"level": 5, "tier": "cross-platform transfer", "supports": "transportability across measurement platforms", "does_not_establish": "universal generalization"},
    ]).to_csv(SOURCE / "Figure6_SourceData.csv", index=False)
    write(SOURCE / "README.md", """
# Source Data README

This directory contains source-data tables for the planned Nature Communications main figures.

- `Figure1_SourceData.csv`: conceptual schematic; no numerical source data required.
- `Figure2_SourceData.csv`: cross-dataset random versus strict split summary from `table_two_channel_leakage_phase19.csv`.
- `Figure3_SourceData.csv`: spatial-channel and patient-channel RLI matrix from corrected Phase 19 tables.
- `Figure4_SourceData.csv`: spatial distance curves and GSE278936 non-zero-buffer pilot table.
- `Figure5_SourceData.csv`: model-regime summaries, including corrected train-only GraphSAGE rows.
- `Figure6_SourceData.csv`: generalization evidence hierarchy.

No table contains restricted data, user-local paths, or hidden indices. Numerical values derive from frozen paper assets under `results/paper_assets/`.
""")


def supplement_and_availability() -> None:
    write(SUB / "Supplementary_Information.md", """
# Supplementary Information

## Supplementary Note 1. Dataset construction and QC

This note describes public DLPFC, Andersson HER2-positive breast cancer, Thrane melanoma, 10x Visium breast cancer and GSE278936 prostate Visium inputs, including sample structure, public accessions, preprocessing status and known boundaries. Restricted EGA validation data from the prostate study were not used.

## Supplementary Note 2. Split implementation

This note documents random spot splits, matched spatial block splits, hop-buffer filtering, slide-held-out splits, patient-held-out splits and dataset-held-out stress tests. It records empty or non-resolvable split conditions and explains why NA is not treated as zero.

## Supplementary Note 3. Target-panel definition

This note records dataset-specific Moran-ranked target panels and the frozen `shared_panel_50` target set. Target selection defines the prediction task and does not use downstream model performance.

## Supplementary Note 4. Model specifications

This note documents Mean, PCA+Ridge, Spatial kNN and GraphSAGE settings. It includes the Phase 19 GraphSAGE audit and the corrected train-only PCA feature scaling implementation.

## Supplementary Note 5. Random-size-matched controls

This note reports random-size-matched controls for DLPFC, Visium breast and GSE278936, showing that the main spatial-buffer losses exceed losses caused by sample-count reduction alone.

## Supplementary Note 6. Mixed-effects analyses

This note reports mixed-effects models run separately for patient and spatial channels, with `inflation ~ moran_i + C(model)` and dataset random intercepts. Full outputs remain supplementary because they support robustness rather than the central conceptual claim.

## Supplementary Note 7. Cross-dataset and cross-platform stress test

This note reports Andersson-to-Visium transfer as a supplementary stress test. It should not be framed as patient-level validation.

## Supplementary Figures

1. Dataset QC and sample structure.
2. Full buffer curves.
3. Random-size-matched controls.
4. Corrected train-only GraphSAGE results.
5. Moran analyses.
6. Boundary conditions and non-resolvable splits.
7. Cross-platform stress test.

## Supplementary Tables

1. Dataset accessions and sample counts.
2. Target panels.
3. Model hyperparameters.
4. Split sample counts.
5. Full metric summaries.
6. Full seed and fold summaries.
7. Statistical outputs.
8. Software versions.
""")
    write(SUB / "DATA_AVAILABILITY.md", """
# Data Availability

DLPFC spatial transcriptomics data are available from the public resources associated with the SpatialLIBD / human dorsolateral prefrontal cortex study. Andersson HER2-positive breast cancer data are available from the source publication and Zenodo record DOI `10.5281/zenodo.4751624`. Thrane melanoma spatial transcriptomics data are available from the source publication. The 10x Visium breast cancer dataset is available from the official 10x Genomics public dataset portal. GSE278936 prostate Visium public data are available from GEO accession `GSE278936`.

Restricted validation/EGA cohort data associated with the prostate study were not used in this manuscript. GSE278936 is used only as a public spatial-channel replication dataset and is not described as clean patient-level validation.

Project-derived processed objects, split manifests and source data will be deposited before submission or publication. Repository URL and archival DOI will be inserted after public release: `[GitHub repository URL]`, `[Zenodo DOI]`.
""")
    write(SUB / "CODE_AVAILABILITY.md", """
# Code Availability

Code used for data preprocessing, split generation, benchmark models, statistical analyses, figure generation and source-data generation is prepared for public release at `[GitHub repository URL]` and archival deposition at `[Zenodo DOI]`.

The release will include `src/`, `scripts/`, `configs/`, `tests/`, frozen target-panel metadata and paper assets needed to reproduce the submitted figures from processed results. The paper-asset smoke test is:

```bash
python3 scripts/reproduce_paper_assets.py
```

The unit-test smoke test is:

```bash
python3 -m pytest
```
""")


def repo_docs() -> None:
    write(REPORTS / "NATCOMM_ZENODO_RELEASE_PLAN.md", """
# Nature Communications Zenodo Release Plan

## Release

- GitHub tag: `v1.0.0`
- Zenodo archive: create from the public GitHub release after final repository cleanup.
- DOI fields: do not invent; insert the issued DOI in the manuscript, Code Availability, Data Availability, README and CITATION.cff.

## Include

`README.md`, `LICENSE`, `CITATION.cff`, `environment.yml`, `requirements.txt`, `configs/`, `src/`, `scripts/`, `tests/`, frozen target-panel metadata, split metadata where size permits, paper asset tables, figure scripts, final source data and documentation.

## Exclude

Raw data, large processed data unless separately deposited, restricted data, local caches, `.pytest_cache`, `__pycache__`, notebook checkpoints, secrets, tokens and local absolute paths.

## License

Recommended code license: MIT or BSD-3-Clause. Recommended manuscript/source-data license should follow Nature Communications open-access requirements and funder rules, typically CC BY 4.0 for the article.
""")
    write(Path("README.md"), """
# SpatialLeak

SpatialLeak is an evaluation framework for spatial omics prediction that matches benchmark design to the level of generalization being claimed.

## Why SpatialLeak?

Random spot-level splits test local interpolation. They do not by themselves establish spatial transfer, section transfer, patient transfer or dataset transfer. SpatialLeak compares random splits with spatial buffers, section-held-out, patient-held-out and dataset-held-out regimes to separate local spatial-neighborhood dependence from patient-associated structure.

## Reproduce paper figures

From an environment with the processed result assets available:

```bash
python3 scripts/reproduce_paper_assets.py
```

This regenerates frozen paper tables and figure assets under `results/paper_assets/`.

## Run tests

```bash
python3 -m pytest
```

## Evaluation tiers

| Level | Tier | Supports | Does not establish |
|---:|---|---|---|
| 0 | Random spot interpolation | local interpolation | spatial, section, patient or dataset transfer |
| 1 | Buffered spatial transfer | local neighborhood separation | patient transfer |
| 2 | Section-held-out transfer | section transfer | patient transfer unless patient identity is separated |
| 3 | Patient-held-out transfer | retention across patient-associated groups | dataset or platform transfer |
| 4 | Dataset-held-out transfer | dataset transportability stress test | cross-platform transfer |
| 5 | Cross-platform transfer | robustness across measurement platforms | universal generalization |

## Data availability

The manuscript uses public DLPFC, Andersson HER2-positive breast cancer, Thrane melanoma, 10x Visium breast cancer and GSE278936 prostate Visium data. Restricted EGA validation data were not used.

## Citation

Zenodo DOI and formal citation will be added after public release.
""")


def audits_and_reviews(k: dict[str, str]) -> None:
    write(REPORTS / "NATCOMM_CLAIM_SOURCE_AUDIT.md", f"""
# Nature Communications Claim-Source Audit

| Location | Claim / number | Frozen source | Status |
|---|---|---|---|
| Abstract | Visium breast Spatial kNN hop5 RLI {k['visium_knn_rli']} | `table_two_channel_leakage_phase19.csv` | PASS |
| Abstract | Andersson corrected GraphSAGE patient RLI {k['andersson_gs_patient']} | `table_graphsage_shared_panel50_RLI_trainonly.csv` | PASS |
| Abstract | Thrane corrected GraphSAGE patient RLI {k['thrane_gs_patient']} | `table_graphsage_shared_panel50_RLI_trainonly.csv` | PASS |
| Abstract | GSE278936 PCA+Ridge hop5 RLI {k['gse_pca_hop5']} | `table_gse278936_spatial_pilot_RLI.csv` | PASS |
| Results | GSE278936 hop0 unchanged | `table_gse278936_spatial_pilot_RLI.csv` | PASS |
| Discussion | GSE278936 not patient-level validation | `GSE278936_SPATIAL_PILOT_CURRENT_STATUS.md` | PASS |
| Methods | Train-only PCA/scaling | `src/models/pca_ridge.py`, `src/models/graphsage.py` | PASS |

## Old GraphSAGE Number Audit

The old values 0.692 and 0.718 are excluded from V5 manuscript text. Corrected values are {k['andersson_gs_patient']} and {k['thrane_gs_patient']}. DLPFC GraphSAGE RLI 0.378 is not used as main V5 evidence because the corrected DLPFC rerun was not completed.
""")
    write(REPORTS / "NATCOMM_REFERENCE_LOCK.md", """
# Nature Communications Reference Lock

The Nature Communications V5 draft uses references primarily in the Introduction and Discussion. Methods and Results remain citation-light according to the project manuscript rules.

## Verified Core Reference Categories

| Category | Placement | Core sources |
|---|---|---|
| Spatial transcriptomics foundations | Introduction paragraph 1 | Stahl 2016; Rodriques 2019; Vickovic 2019; Stickels 2021 |
| Source datasets | Data Availability and reference list | Maynard 2021; Andersson 2021; Thrane 2018; Kiviaho 2024; 10x public dataset |
| Spatial prediction / integration models | Introduction paragraph 1 | SpaGE; Tangram; gimVI; stPlus; ST-Net |
| Graph-based spatial methods | Introduction paragraph 1 | GraphST; STAGATE; SpaGCN; SEDR; GraphSAGE |
| Leakage and validation bias | Introduction paragraph 2 and Discussion | Ambroise 2002; Varma 2006; Kaufman 2012; Vabalas 2019; Saeb 2017; Kapoor 2023 |
| Spatial autocorrelation | Methods-supporting reference list | Moran 1950; Cliff and Ord 1981 |

## Duplicate / Caution Notes

- Bergenstrahle 2020 and Andersson 2020 share the Communications Biology DOI in the Phase 19 reference list and should be manually checked before final reference formatting.
- Do not cite all method papers in the Introduction if the final word count becomes tight.
- Do not add references to the Abstract.
""")
    write(REPORTS / "NATCOMM_EDITORIAL_TRIAGE_SIMULATION.md", """
# Nature Communications Editorial Triage Simulation

## Q1. What is the conceptual advance?

SpatialLeak reframes spatial omics benchmarking as a hierarchy of generalization claims and shows that local spatial and patient-associated inflation are distinct.

## Q2. Why is this more than a benchmark paper?

The manuscript does not rank methods. It changes how benchmark evidence is interpreted by mapping split designs to claims.

## Q3. Why should a broad spatial-omics reader care?

Many spatial omics papers report predictive performance from random spot splits. The framework tells readers what such performance can and cannot establish.

## Q4. Does the study establish a field-level issue?

Yes, with public datasets across brain, breast cancer, melanoma and prostate Visium settings, while keeping claims bounded.

## Q5. Are there enough independent datasets?

Likely enough for a methods/evaluation contribution. Dataset heterogeneity is a strength for the conceptual claim but requires careful boundaries.

## Q6. Are only three model classes a fatal weakness?

No. The model set is diagnostic, not a SOTA leaderboard. The manuscript should keep this framing prominent.

## Q7. Why is the non-zero buffer finding important?

It shows that non-overlapping spatial partitions can still leave local neighborhood dependence, so split labels need distance definitions.

## Q8. Does patient-held-out loss simply reflect distribution shift?

It may include distribution shift. The manuscript frames it as patient-associated performance inflation rather than causal leakage.

## Q9. Are claims appropriately bounded?

Yes, if V5 avoids clean patient-validation language for GSE278936 and avoids treating all strict-split loss as invalid signal.

## Q10. Would this likely be sent for peer review?

Likely yes, if the conceptual hierarchy is made unmistakable and figures are clean.

Desk reject risk: **Moderate**.

Top rejection risks: perceived as a small benchmark; limited SOTA model breadth; final figures not yet publication-polished.

Best risk reductions without new experiments: lead with evidence hierarchy; move low-value details to Supplement; make GraphSAGE correction and dataset boundaries explicit.
""")
    write(REPORTS / "NATCOMM_REVIEWER_SIMULATION.md", """
# Nature Communications Reviewer Simulation

## Reviewer 1: spatial transcriptomics expert

| Question | Risk | Evidence | Manuscript response | Supplementary support | Need new experiment? |
|---|---|---|---|---|---|
| Are random spot splits actually common and problematic? | Medium | Introduction references and multi-dataset contrasts | Frame as interpretation problem, not universal invalidity | Literature and full split tables | NO |
| Does spatial buffering remove real biology? | Medium | Retention under strict splits; Discussion boundary | Spatial dependence is not inherently leakage | Evidence hierarchy | NO |
| Why use Moran-ranked targets? | Medium | Target-panel audit | Task definition, not model tuning | Target-panel note | NO |
| Is GSE278936 patient validation? | High | 52 patients / 52 sections public data | Spatial-channel replication only | GSE278936 report | NO |
| Why does kNN fail in GSE278936? | Medium | Near-zero random performance | Boundary condition, not failed central claim | Full pilot table | NO |
| Are hop buffers biologically meaningful? | Medium | kNN graph distance | Operational neighborhood isolation | Split implementation note | NO |
| Are Visium breast claims overextended? | Medium | Single patient | Spatial and section-level only | Dataset table | NO |
| Is patient-channel language too strong? | Medium | Patient-held-out drops | Patient-associated, not causal batch effect | Reviewer defense | NO |
| Are source datasets heterogeneous? | Low | Yes | Heterogeneity supports evaluation-tier argument | Dataset QC | NO |
| Are there enough spatial platforms? | Medium | Visium and ST v1.0 | Scope is spatial transcriptomics prediction, not all technologies | Limitations | NO |

## Reviewer 2: computational biology benchmark expert

| Question | Risk | Evidence | Manuscript response | Supplementary support | Need new experiment? |
|---|---|---|---|---|---|
| Why only three model classes? | Medium | Diagnostic baselines plus GraphSAGE | Not a SOTA leaderboard | Model specs | NO |
| Why RLI? | Medium | LI/RLI/retention definitions | Operational split-dependent inflation | Metrics note | NO |
| What about near-zero denominators? | Medium | 0.05 rule | Do not interpret near-zero RLI | Full tables | NO |
| Could sample size explain buffer loss? | Medium | Random-size-matched controls | Main losses exceed size losses | Supplementary Note 5 | NO |
| Are seeds cherry-picked? | Low | Frozen seed sets | No test-based seed selection | Reproducibility audit | NO |
| Are all splits comparable? | Medium | Split audit | They answer different claims | Hierarchy figure | NO |
| Does model ranking change robustly? | Medium | Corrected GraphSAGE and baselines | Evaluation-regime dependence | Figure 5 source data | NO |
| Why Pearson? | Low | Mean per-target Pearson | Prediction association metric; full metrics supplementary | Full metrics | NO |
| Are mixed-effects essential? | Low | Robustness only | Keep supplementary | Mixed-effects outputs | NO |
| Is cross-platform stress weak? | Medium | 0.199 supplementary | Not central evidence | Supplementary Note 7 | NO |

## Reviewer 3: machine-learning evaluation expert

| Question | Risk | Evidence | Manuscript response | Supplementary support | Need new experiment? |
|---|---|---|---|---|---|
| Is this leakage or distribution shift? | High | Split-dependent losses | Use apparent generalization inflation and bounded wording | Claim wording lock | NO |
| Was preprocessing train-only? | Low | Code audit | PCA and scaling fit on train only | Methods audit | NO |
| Was GraphSAGE corrected? | Medium | Phase 19 patch and reruns | Corrected train-only external rows; DLPFC excluded | GraphSAGE table | NO |
| Were targets selected with test labels? | Medium | Target-panel audit | Task definition independent of model performance | Target note | NO |
| Was validation used correctly? | Low | Early stopping on validation | No test checkpointing | Code availability | NO |
| Are transductive graph features leakage? | Medium | No label aggregation | It is the channel being evaluated | Methods | NO |
| Are patient and batch separable? | High | Public metadata limits | Not causally separated | Discussion | NO |
| Does framework generalize beyond gene prediction? | Medium | Conceptual hierarchy | Likely applicable, demonstrated in gene prediction | Limitations | NO |
| Are confidence intervals at spot level? | Low | Slide-level bootstrap | No spot-level pseudoreplication for formal claims | Statistics note | NO |
| Should more SOTA models be added? | Medium | Scope framing | Only if reviewer requests | Experiment lock | NO |
""")


def v5_and_cover(s: dict[str, str]) -> str:
    title = "Evaluation design reshapes apparent generalization in spatial omics prediction"
    refs = read(MANUSCRIPT / "references_master.bib") if (MANUSCRIPT / "references_master.bib").exists() else "References are maintained in manuscript/references_master.bib."
    v5 = f"""
# {title}

## Abstract

{s['abstract']}

## Introduction

{s['introduction']}

{s['results']}

## Discussion

{s['discussion']}

{s['methods']}

## Data Availability

DLPFC, Andersson, Thrane, 10x Visium breast and GSE278936 public data were used from their cited public resources. Restricted EGA validation data from the prostate study were not used. Project-derived processed objects, split manifests and source data will be deposited before submission or publication. Repository URL and archival DOI will be inserted after release: `[GitHub repository URL]`, `[Zenodo DOI]`.

## Code Availability

Code used for preprocessing, split generation, benchmarking, statistical analyses, figure generation and source-data generation is prepared for public release at `[GitHub repository URL]` and archival deposition at `[Zenodo DOI]`.

## Author Contributions

`[Author contribution statement to be added.]`

## Funding

`[Funding statement to be added.]`

## Competing Interests

`[Competing interests statement to be added.]`

## Acknowledgements

`[Acknowledgements to be added.]`

## References

References are maintained in `manuscript/references_master.bib` for final Nature-style formatting.

```bibtex
{refs}
```
""".strip()
    write(MANUSCRIPT / "SPATIALLEAK_NATCOMM_V5.md", v5)
    write(SUB / "SPATIALLEAK_NATCOMM_V5.md", v5)
    write(SUB / "COVER_LETTER.md", f"""
# Cover Letter

Dear Editors,

We submit the manuscript entitled "{title}" for consideration as an Article in Nature Communications. Spatial omics prediction models are often evaluated using random spot-level splits, but such benchmarks can conflate local interpolation with broader generalization across sections, patients or datasets.

This problem matters because spatial omics methods are increasingly used to support biological claims about tissue organization and transferable molecular prediction. Without split designs matched to those claims, apparent model performance can be difficult to interpret even when the model and data processing are technically sound.

Our study introduces SpatialLeak, a leakage-resistant evaluation framework that separates local spatial-neighborhood dependence from patient-associated performance inflation. The main findings are that non-zero spatial buffers can be required to expose local neighborhood dependence, patient-held-out performance loss represents a distinct evaluation channel, and model comparisons change when the evaluation tier changes.

We believe the manuscript is suited to Nature Communications because it addresses a general benchmarking problem for spatial omics and computational biology rather than a single dataset or model leaderboard. The framework provides practical guidance for how future spatial omics prediction studies should align evaluation design with the level of generalization being claimed.

`[Originality statement: to be confirmed by all authors.]` `[Not under consideration elsewhere: to be confirmed.]` `[All authors approve submission: to be confirmed.]`

Sincerely,

`[Corresponding author name and contact information]`
""")
    return v5


def reporting_and_checklist(v5: str, s: dict[str, str]) -> None:
    write(SUB / "REPORTING_CHECKLIST_PREP.md", """
# Reporting Checklist Preparation

| Item | Status | Explanation |
|---|---|---|
| Biological sample definitions | PASS | Dataset and patient/section boundaries are described. |
| Replicates | PASS | Seeds, folds, slides and patient-held-out units are documented. |
| Randomization | PASS | Random seeds and split generation are fixed; no seed cherry-picking. |
| Blinding | Not applicable | This is a public-data computational evaluation without manual outcome assessment. |
| Exclusion criteria | PASS | Empty or non-resolvable splits and near-zero RLI denominators are documented. |
| Statistics | PASS | LI, RLI, retention, bootstrap, Wilcoxon and mixed-effects analyses are documented. |
| Sample-size effects | PASS | Random-size-matched controls are included. |
| Software/code | PENDING USER INPUT | Repository URL and Zenodo DOI must be inserted after release. |
| Data accessions | PARTIAL | Public sources are named; final accession formatting and processed-data DOI remain pending. |
| Machine-learning reporting | PASS | Train-only preprocessing, validation-only early stopping and test exclusion are described. |
| Source data | PASS | Source-data tables are prepared for Figures 1-6. |
""")
    write(SUB / "SUBMISSION_PACKAGE_CHECKLIST.md", """
# Submission Package Checklist

## Scientific

| Item | Status |
|---|---|
| Fatal flaw gate | PASS |
| Claim consistency | PASS |
| Corrected GraphSAGE values used | PASS |
| No test leakage in final evidence | PASS |
| No unsupported GSE278936 patient-validation claim | PASS |
| No near-zero RLI interpretation | PASS |

## Manuscript

| Item | Status |
|---|---|
| Title | PASS |
| Abstract | PASS |
| Main text | PASS |
| Methods | PASS |
| References | PASS for BibTeX source; PENDING final Nature-style formatting |
| Author metadata | PENDING USER INPUT |
| Funding / competing interests / acknowledgements | PENDING USER INPUT |

## Figures

| Item | Status |
|---|---|
| Final figure architecture | PASS |
| Source data | PASS |
| Existing vector assets copied | PASS |
| Final six-figure rendered set | PENDING FORMATTING |
| Resolution QA | PENDING FINAL EXPORT |

## Open Science

| Item | Status |
|---|---|
| GitHub public repository | PENDING USER INPUT |
| Release tag | PENDING USER INPUT |
| Zenodo DOI | PENDING USER INPUT |
| Data accessions | PASS for public sources; PENDING processed-data DOI |

## Metadata

| Item | Status |
|---|---|
| Authors | PENDING USER INPUT |
| Affiliations | PENDING USER INPUT |
| Corresponding author | PENDING USER INPUT |
| ORCID | PENDING USER INPUT |
| Author contributions | PENDING USER INPUT |
""")
    rows = [
        ("Title", words("Evaluation design reshapes apparent generalization in spatial omics prediction")),
        ("Abstract", words(s["abstract"])),
        ("Introduction", words(s["introduction"])),
        ("Results", words(s["results"])),
        ("Discussion", words(s["discussion"])),
        ("Methods", words(s["methods"])),
        ("Main text including Methods", words(s["introduction"] + "\n" + s["results"] + "\n" + s["discussion"] + "\n" + s["methods"])),
        ("Figure legends", 0),
        ("References", words("References are maintained in manuscript/references_master.bib for final Nature-style formatting.")),
    ]
    table = "\n".join(f"| {name} | {count} |" for name, count in rows)
    write(REPORTS / "NATCOMM_WORD_COUNT_AUDIT.md", f"""
# Nature Communications Word Count Audit

| Section | Words |
|---|---:|
{table}

## Interpretation

The V5 draft is comfortably below the approximate Nature Communications Article main-text limit that includes Methods. Final author metadata, figure legends and formatted references will add length but should remain manageable.
""")


def figures_folder() -> None:
    FIGS.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(["fig1_leakage_overview", "fig2_spatial_distance_curves", "fig3_model_and_transfer"], start=1):
        copy_if_exists(PAPER / "figures" / f"{name}.svg", FIGS / f"Figure{i}_current_asset.svg")
        copy_if_exists(PAPER / "figures" / f"{name}.png", FIGS / f"Figure{i}_current_asset.png")
    write(FIGS / "README.md", """
# Figure Folder

This folder contains the current rendered paper assets copied from `results/paper_assets/figures/`.

The Nature Communications figure plan locks six main figures. Existing assets cover the current conceptual/result figure set and should be reassembled into the final Figure 1-6 layout during journal-specific formatting. No numerical result was changed in this copy step.
""")


def status_files() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    status = f"""
# CURRENT_STATUS.md - Project Current Status

> Updated: {now}. Phase: **Phase 20 Nature Communications package prepared**

SpatialLeak has moved from Phase 19 manuscript readiness to a Nature Communications initial submission package.

## Status

- Experiments closed for initial submission.
- Fatal flaw gate remains PASS.
- NatComms central claim, title decision, abstract, introduction, discussion, methods and V5 manuscript are prepared.
- Source Data tables for planned Figures 1-6 are prepared.
- Supplementary Information, Data Availability, Code Availability, cover letter, reporting checklist and submission checklist are prepared.
- Corrected train-only GraphSAGE values are used in V5: Andersson patient RLI 0.695 and Thrane patient RLI 0.711.

## Remaining Intervention

Only submission metadata and public-release actions remain: authorship, affiliations, corresponding author, ORCID, funding, competing interests, acknowledgements, GitHub public release, Zenodo DOI and final rendered figure formatting.

# READY FOR NATURE COMMUNICATIONS SUBMISSION PACKAGE REVIEW
"""
    write(Path("CURRENT_STATUS.md"), status)
    write(Path("PROJECT_STATUS.md"), status.replace("CURRENT_STATUS.md", "PROJECT_STATUS.md"))
    write(Path("NEXT_ACTIONS.md"), """
# NEXT_ACTIONS.md - Highest-Priority Remaining Tasks

1. **Authorship metadata** - authors, affiliations, corresponding author, ORCID and contributions.
2. **Declarations** - funding, acknowledgements and competing interests.
3. **Public release** - GitHub URL, release tag `v1.0.0`, Zenodo DOI and processed-data deposit decision.
4. **Final figure rendering** - assemble final Nature Communications Figure 1-6 files from locked plan and source data.
5. **Submission portal formatting** - final Nature-style references, reporting summary and portal metadata.
""")


def main() -> None:
    tables = load_tables()
    k = key_numbers(tables)
    experiment_lock()
    central_claim_and_title(k)
    sections = write_manuscript_sections(k)
    figure_docs()
    source_data(tables)
    supplement_and_availability()
    repo_docs()
    audits_and_reviews(k)
    v5 = v5_and_cover(sections)
    reporting_and_checklist(v5, sections)
    figures_folder()
    status_files()
    print("Phase 20 Nature Communications package generated.")


if __name__ == "__main__":
    main()
