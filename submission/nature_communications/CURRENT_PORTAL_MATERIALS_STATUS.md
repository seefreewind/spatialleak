# SpatialLeak Nature Communications Portal Materials Current Status

Date: 2026-08-11

## One-line status

SpatialLeak has entered the final submission-package stage for Nature Communications. No new experiments are recommended. The current task is to upload the prepared Supplementary Information, Source Data, reporting/checklist drafts, figures, cover letter, and availability statements through the journal portal.

## Scientific status

The manuscript content is considered scientifically locked. The current framing is:

> Evaluation design reshapes apparent generalization in spatial omics prediction by separating spatial-neighbourhood leakage from subject-associated shortcuts.

The two evidence channels remain:

- Spatial-neighbourhood leakage: supported by DLPFC, Visium breast, and GSE278936 spatial-buffer analyses.
- Subject-associated shortcut risk: supported by Andersson and Thrane subject-held-out analyses.

GSE278936 should continue to be described only as an external spatial-channel Visium replication dataset. It should not be described as clean patient-level validation because the public GEO portion contains 52 patients and 52 sections, making patient-held-out and section-held-out designs effectively non-separable.

## Main manuscript

Current main manuscript file:

```text
submission/nature_communications/SpatialLeak_NatCommun_V8.docx
```

Current clean Markdown source:

```text
submission/nature_communications/SpatialLeak_NatCommun_V8_clean.md
```

The manuscript already includes:

- Zenodo DOI: https://doi.org/10.5281/zenodo.21881438
- GitHub repository: https://github.com/seefreewind/spatialleak
- GitHub release: v1.0.0
- Full author and correspondence information
- Funding statement: no funding
- Acknowledgements: none
- Competing interests: no competing interests

## Prepared portal package

Final assembled portal folder:

```text
submission/nature_communications/portal_materials_final/
```

Full portal upload archive:

```text
submission/nature_communications/SpatialLeak_NatCommun_portal_materials_final.zip
```

Source Data-only archive:

```text
submission/nature_communications/SpatialLeak_NatCommun_SourceData_final.zip
```

Both zip files passed archive-integrity checks.

## Supplementary Information

Current Supplementary Information file:

```text
submission/nature_communications/portal_materials_final/Supplementary_Information_V3.md
```

This file is intended to hold methods-level defence and supplementary results rather than expanding the main text. It covers:

- evaluation-regime-dependent model behaviour
- random-size-matched control
- shared-panel robustness
- per-seed and per-fold result availability
- mixed-effects analyses
- Moran analysis
- GraphSAGE parameter details
- dataset and sample structure
- split sample counts
- near-zero denominator and non-resolvable RLI cases
- Andersson-to-Visium cross-platform stress test

## Source Data

Current Source Data folder:

```text
submission/nature_communications/portal_materials_final/source_data/
```

Included files:

```text
Figure1_SourceData.csv
Figure2_SourceData.csv
Figure3_SourceData.csv
Figure4_SourceData.csv
SupplementaryFigure1_SourceData.csv
SupplementaryTable_VisiumBreastSectionHeldOut.csv
SourceData_Index.csv
README.md
```

Recommended portal handling:

- Upload the Source Data-only zip as the dedicated Source Data file if the portal provides a Source Data category.
- If the portal asks for per-figure source data separately, upload each CSV individually and use `SourceData_Index.csv` as the index.
- Figure 1 is conceptual, so its source-data file documents that no numerical source data are required.

## Figures

Current figure folder:

```text
submission/nature_communications/portal_materials_final/figures/
```

Included files:

```text
Figure1_final.pdf
Figure1_final.tiff
Figure2_final.pdf
Figure2_final.tiff
Figure3_final_matrix.pdf
Figure3_final_matrix.tiff
Figure4_final.pdf
Figure4_final.tiff
```

Figure status:

- Figure 1: conceptual logic locked.
- Figure 2: evidence-tier grouping locked; caption should keep the explicit standard-deviation definition.
- Figure 3: two-channel RLI matrix locked.
- Figure 4: spatial-buffer trajectory locked; GSE278936 includes seed-level error bars.

## Reporting and checklist materials

Current reporting folder:

```text
submission/nature_communications/portal_materials_final/reporting/
```

Included files:

```text
Reporting_Summary_Draft.md
Machine_Learning_Checklist_Draft.md
Code_Software_Checklist_Draft.md
REPORTING_FORM_EVIDENCE_MAP.md
```

These are draft portal-support documents. They should be used to complete the Nature Communications reporting summary and any machine-learning/code/software checklist fields in the online system.

## Cover letter and availability statements

Included in the final portal folder:

```text
COVER_LETTER_V8_FINAL.md
DATA_AVAILABILITY.md
CODE_AVAILABILITY.md
SUBMISSION_PACKAGE_CHECKLIST.md
UPLOAD_MANIFEST.md
```

Current Code Availability statement is no longer phrased as a pending release. It states that code is available on GitHub and archived at Zenodo.

Current Data Availability statement specifies the two public 10x Genomics Visium breast cancer sections rather than referring vaguely to a single 10x Visium breast dataset.

## Suggested Nature Communications upload grouping

Use the following upload grouping unless the portal enforces a different structure:

1. Manuscript file

```text
SpatialLeak_NatCommun_V8.docx
```

2. Supplementary Information

```text
Supplementary_Information_V3.md
```

3. Source Data

```text
SpatialLeak_NatCommun_SourceData_final.zip
```

4. Figures

```text
Figure1_final.tiff
Figure2_final.tiff
Figure3_final_matrix.tiff
Figure4_final.tiff
```

Keep the PDF versions available as editable/vector backups if requested.

5. Cover letter

```text
COVER_LETTER_V8_FINAL.md
```

6. Reporting/checklist material

Use the files in:

```text
reporting/
```

7. Availability statements

Use:

```text
DATA_AVAILABILITY.md
CODE_AVAILABILITY.md
```

## Residual checks already passed

The final portal bundle was scanned for major residual placeholders and stale wording. No hits remained for:

```text
PENDING
prepared for deposition
will include
10x Visium breast cancer dataset
patient transfer
e107-e107
1e-3
1e-4
Perf_
inflation ~
Acknowledgements
```

The archive files also passed zip integrity tests.

## Last manual checks before portal submission

Before pressing submit, manually verify the following in the online portal:

- The uploaded manuscript is `SpatialLeak_NatCommun_V8.docx`.
- The title matches exactly: `Evaluation design reshapes apparent generalization in spatial omics prediction`.
- The corresponding author is Da Lin, 212574@wzhealth.com, ORCID 0009-0009-4410-0218.
- Funding is entered as no funding.
- Acknowledgements are left empty or entered as none, according to portal requirements.
- Competing interests are entered as no competing interests.
- Zenodo DOI is entered exactly as https://doi.org/10.5281/zenodo.21881438.
- GitHub URL is entered exactly as https://github.com/seefreewind/spatialleak.
- Source Data files are linked to Figures 1-4 and Supplementary Figure 1.
- Figure 2 and Figure 4 captions retain the explicit error-bar definition.
- GSE278936 is described only as spatial-channel external replication.

## Do not do next

Do not add new datasets, new SOTA models, new patient-held-out analyses for GSE278936, restricted EGA downloads, or new scientific claims at this stage.

The remaining work is administrative submission assembly, portal-field completion, and final human confirmation of uploaded files.

