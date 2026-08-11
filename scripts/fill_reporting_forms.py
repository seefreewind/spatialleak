from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject


ROOT = Path(__file__).resolve().parents[1]
FORMS = ROOT / "submission" / "nature_communications" / "portal_materials_final" / "official_forms"


def fill_machine_learning_checklist():
    src = FORMS / "machine-learning-checklist.pdf"
    out = FORMS / "machine-learning-checklist_filled.pdf"
    reader = PdfReader(str(src))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    if "/AcroForm" in reader.trailer["/Root"]:
        writer._root_object.update({
            NameObject("/AcroForm"): reader.trailer["/Root"]["/AcroForm"]
        })

    fields = {
        "Corresponding authors": "Da Lin; manuscript title: Evaluation design reshapes apparent generalization in spatial omics prediction",
        "The source code is included in the submission or a": "/On",
        "Textfield": "https://github.com/seefreewind/spatialleak; archived at https://doi.org/10.5281/zenodo.21881438",
        "A test dataset and instructionsscripts for replica": "/On",
        "Textfield-1": "Public data accessions/URLs, Source Data and run instructions are provided in the manuscript, Supplementary Information and repository README.",
        "A Readme file with instructions for installing and": "/On",
        "Textfield-2": "Repository README, requirements.txt, environment.yml and scripts/.",
        "The code is made available to reviewers during rev": "/On",
        "The paper contains information on how to obtain co": "/On",
        "A All data sources are listed in the paper": "/On",
        "B The train test and validation datasets are publi": "/On",
        "C We have reported and discussed potential dataset": "/On",
        "Yes": "Main text Methods, Data Availability, Supplementary Table 1 and Source Data. Restricted EGA data were not used.",
        "D The data cleaning and preprocessing steps are cl": "/On",
        "Yes-0": "Methods and Supplementary Methods describe normalization, target-panel definition, HVG selection, scaling/PCA and split generation.",
        "E Instances of combining data from multiple source": "/On",
        "Yes-1": "Dataset-held-out/cross-platform stress test is reported separately; GSE278936 is restricted to spatial-channel replication.",
        "A What model architecture is the current model bas": "Diagnostic benchmark models: Mean, PCA+Ridge, Spatial kNN and GraphSAGE. The study evaluates leakage-resistant split design rather than proposing a production predictive model.",
        "C The model clearly splits data into different set": "/On",
        "D The method of data splitting eg random cluster o": "/On",
        "Yes-2": "Methods define random, matched spatial hop0/hop2/hop5, section-held-out, subject-held-out and dataset-held-out regimes.",
        "E The data splitting mimics anticipated realworld": "/On",
        "Yes-3": "The hierarchy maps split design to local interpolation, section transfer, subject transfer and dataset transfer claims.",
        "F The data splitting procedure has been chosen to": "/On",
        "Yes-4": "Strict split definitions and non-zero spatial buffers were prespecified to assess neighbourhood leakage and subject-associated shortcuts.",
        "G The interpretability of the model has been studi": "/On",
        "Yes-5": "Interpretation focuses on evaluation-dependent performance inflation (RLI), retention and channel-specific behaviour rather than feature attribution.",
        "A The performance metrics used are described and j": "/On",
        "Yes-6": "Mean Pearson correlation is the primary metric; RLI and retention are defined in Methods.",
        "B Crossvalidation of the results is included": "/On",
        "C Communityaccepted benchmark datasetstasks are us": "/On",
        "Yes-7": "Public spatial transcriptomics datasets are used; the task is diagnostic evaluation rather than a community leaderboard.",
        "D Baseline comparisons to simpletrivial models for": "/On",
        "Yes-8": "Mean predictor, PCA+Ridge, Spatial kNN and GraphSAGE are compared under identical split regimes.",
        "E Benchmarks with current stateoftheart are provid": "/Off",
        "No-9": "No. The model set is diagnostic and selected to probe evaluation design rather than to establish a SOTA leaderboard.",
        "F Ablation experiments are included": "/Off",
        "No-10": "No formal architecture ablation is claimed. Robustness analyses instead test split regimes, sample-size matching and shared_panel_50 targets.",
        "G The model has been tested on a fully independent": "/On",
        "A The paper contains information on hardwarecomput": "/On",
        "B The paper includes information on the computatio": "/On",
        "DD-MM-YYYY": "11-08-2026",
    }

    for page in writer.pages:
        writer.update_page_form_field_values(page, fields, auto_regenerate=False)
        if "/Annots" in page:
            for annot in page["/Annots"]:
                obj = annot.get_object()
                name = obj.get("/T")
                if name in fields and fields[name] in {"/On", "/Off"}:
                    obj.update({NameObject("/V"): NameObject(fields[name]), NameObject("/AS"): NameObject(fields[name])})

    writer.set_need_appearances_writer(True)
    with out.open("wb") as f:
        writer.write(f)
    return out


def write_form_answer_pack():
    out = FORMS / "OFFICIAL_FORM_COMPLETION_GUIDE.md"
    out.write_text(
        """# Official Nature Reporting Form Completion Guide

Date: 2026-08-11

## Status

- `machine-learning-checklist_filled.pdf` was generated from the official Machine learning checklist PDF.
- `nr-reporting-summary.pdf` and `nr-software-policy.pdf` are official smart/XFA PDFs. They expose no standard AcroForm fields to local PDF tooling and should be completed manually in Adobe Reader or equivalent software.
- The Markdown reporting drafts remain evidence maps, not substitutes for official forms.

## Bio and Life Sciences Reporting Summary

Recommended answers:

- Study design: computational benchmark and evaluation-design analysis using public spatial transcriptomics datasets.
- Sample collection: no new biological samples were collected.
- Randomization: random seeds and matched block-candidate assignments were frozen before final evaluation.
- Blinding: not applicable; no human participant assignment, diagnostic reader, or outcome adjudication was performed.
- Inclusion/exclusion: public datasets and sections are described in the manuscript, Supplementary Table 1 and data availability statement. Restricted EGA data were not used.
- Replication: DLPFC, Andersson, Thrane, Visium breast and GSE278936 support distinct evaluation tiers; GSE278936 is spatial-channel replication only.
- Statistics: mean Pearson correlation, RLI, retention, paired Wilcoxon tests with BH-FDR correction, mixed-effects models with Moran's I and model class as fixed effects and dataset as random intercept.
- Software: Python; NumPy 1.26.4, pandas 2.3.3, SciPy 1.13.1, scikit-learn 1.6.1, Scanpy 1.10.3, AnnData 0.10.9, statsmodels 0.14.6, PyTorch 2.8.0.

## Code and Software Submission Checklist

Recommended answers:

- Code availability: public GitHub repository https://github.com/seefreewind/spatialleak, release v1.0.0, Zenodo DOI https://doi.org/10.5281/zenodo.21881438.
- Scope: preprocessing, target-panel definition, split generation, benchmarking, statistical analysis, figure generation and source-data generation.
- Installation: use README, requirements.txt and environment.yml.
- Test/replication data: public data sources and Source Data are listed; scripts are provided for reproducing analyses.
- Dependencies: listed in repository environment files and Supplementary Information.
- Hardware/runtime: analyses were run on local CPU/GPU-capable Python environments; no proprietary hardware or closed service is required. If the portal requires exact hardware, enter the workstation/server used by the submitting author.
- License: use the repository license as listed on GitHub.

## Machine Learning Checklist Notes

Key conservative entries used in the filled PDF:

- SOTA benchmarks: No. The model set is diagnostic rather than a SOTA leaderboard.
- Ablation experiments: No formal architecture ablation is claimed. Robustness analyses include split regimes, sample-size matching and shared_panel_50 targets.
- Model Card: No separate Model Card is provided because no deployable production model is proposed.
- Independent dataset: Yes with scope limitation. GSE278936 is an independent spatial-channel replication dataset, not clean patient-level validation.
- Hardware/computational cost: provide exact local hardware in the portal if requested; the manuscript/SI provide software versions and reproducibility files.
""",
        encoding="utf-8",
    )
    return out


if __name__ == "__main__":
    print(fill_machine_learning_checklist())
    print(write_form_answer_pack())
