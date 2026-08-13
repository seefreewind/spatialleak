# Nature Communications Submission Materials Guide

Date: 2026-08-11  
Project: SpatialLeak  
Target journal: Nature Communications  
Article type: Article / primary research manuscript

This file organizes the submission materials according to the attached Nature Communications submission guide revised on May 3, 2019, and the current SpatialLeak portal package. It is intended as the practical upload checklist for the journal portal.

## Upload Priority

Use the following order during portal submission.

| Priority | Portal item | File to use | Status | Notes |
|---|---|---|---|---|
| P0 | Main manuscript | `submission/nature_communications/SpatialLeak_NatCommun_V9_language_polished.docx` | Ready | Current polished main manuscript. Use this instead of V8. |
| P0 | Cover letter | `submission/nature_communications/portal_materials_final/COVER_LETTER_V8_FINAL.docx` | Ready | Cover letter remains compatible with V9 because the title, claims, DOI and declarations are unchanged. |
| P0 | Supplementary Information | `submission/nature_communications/portal_materials_final/Supplementary_Information_V4.docx` | Ready | Single combined Word file with supplementary figures and tables. PDF copy is for visual checking or portal fallback. |
| P0 | Source Data | `submission/nature_communications/SpatialLeak_NatCommun_SourceData_final.zip` | Ready | Dedicated source-data archive. Use if the portal has a Source Data category. |
| P0 | Main figures | `portal_materials_final/figures/Figure1_final.pdf` to `Figure4_final.pdf` | Ready | Upload PDF vector files first where accepted. TIFF files are fallback only. |
| P0 | Reporting Summary | `official_forms/nr-reporting-summary.pdf` | Manual action required | Complete in Adobe Reader using the draft answers in `reporting/Reporting_Summary_Draft.md`. |
| P0 | Machine Learning Checklist | `official_forms/machine-learning-checklist_filled.pdf` | Verify manually | Locally filled draft exists; open in Adobe Reader and verify all fields before upload. |
| P0 | Code and Software Checklist | `official_forms/nr-software-policy.pdf` | Manual action required | Complete in Adobe Reader using `reporting/Code_Software_Checklist_Draft.md`. |
| P1 | Data Availability text | `portal_materials_final/DATA_AVAILABILITY.md` | Ready | Also present inside the main manuscript. Use for portal fields if requested. |
| P1 | Code Availability text | `portal_materials_final/CODE_AVAILABILITY.md` | Ready | Includes GitHub and Zenodo archive. |
| P1 | Portal support bundle | `submission/nature_communications/SpatialLeak_NatCommun_portal_materials_upload_slim.zip` | Ready | Slim package excludes TIFF backups and passed zip integrity check. Use as an assembly package only if the portal allows/needs a zipped support upload. |

## Main Manuscript

The submission guide asks for title, authors, abstract, main text, Methods, references, author contributions, competing interests, data availability and code availability. These are all included in the current main manuscript.

Use:

```text
submission/nature_communications/SpatialLeak_NatCommun_V9_language_polished.docx
```

Editable source:

```text
submission/nature_communications/SpatialLeak_NatCommun_V9_language_polished.md
```

Current manuscript metadata:

| Item | Value |
|---|---|
| Title | Evaluation design reshapes apparent generalization in spatial omics prediction |
| Corresponding author | Da Lin |
| Correspondence email | 212574@wzhealth.com |
| ORCID | 0009-0009-4410-0218 |
| Funding | No specific funding was received for this work. |
| Competing interests | The authors declare no competing interests. |
| Acknowledgements | None / leave blank if the portal allows. |
| GitHub | https://github.com/seefreewind/spatialleak |
| Zenodo DOI | https://doi.org/10.5281/zenodo.21881438 |

Guide checks:

- Abstract is unreferenced.
- Main text is under 5,000 words.
- Main display items are Figures 1-4, below the 10-display-item guideline.
- Methods contain preprocessing, split construction, models, metrics and statistics.
- References include article or dataset titles and one cited work per number.
- Author contributions and competing interests are present.
- Data Availability and Code Availability appear before References.

## Cover Letter

The guide states that the cover letter is optional but useful for explaining the context, importance and fit for the journal without repeating the abstract.

Use:

```text
submission/nature_communications/portal_materials_final/COVER_LETTER_V8_FINAL.docx
```

Fallback visual copy:

```text
submission/nature_communications/portal_materials_final/COVER_LETTER_V8_FINAL.pdf
```

Portal entry points:

- Manuscript title: `Evaluation design reshapes apparent generalization in spatial omics prediction`
- Article type: Article / primary research
- Confidential declarations: no competing interests; no funding; no acknowledgements.
- Confirm before submission: all authors approve the submission and author order.

## Figures

The guide prefers editable vector files for graphs, charts and schematics, and asks that figures be understandable with their legends. SpatialLeak figures are graph/schematic figures, so use PDF vector files first.

Upload these main figures:

```text
submission/nature_communications/portal_materials_final/figures/Figure1_final.pdf
submission/nature_communications/portal_materials_final/figures/Figure2_final.pdf
submission/nature_communications/portal_materials_final/figures/Figure3_final_matrix.pdf
submission/nature_communications/portal_materials_final/figures/Figure4_final.pdf
```

Local fallback raster files:

```text
submission/nature_communications/portal_materials_final/figures/Figure1_final.tiff
submission/nature_communications/portal_materials_final/figures/Figure2_final.tiff
submission/nature_communications/portal_materials_final/figures/Figure3_final_matrix.tiff
submission/nature_communications/portal_materials_final/figures/Figure4_final.tiff
```

Figure-specific checks:

| Figure | Upload file | Source data | Status |
|---|---|---|---|
| Figure 1 | `Figure1_final.pdf` | `Figure1_SourceData.csv` | Conceptual schematic; source-data file documents no numerical data. |
| Figure 2 | `Figure2_final.pdf` | `Figure2_SourceData.csv` | Caption defines error bars and n. |
| Figure 3 | `Figure3_final_matrix.pdf` | `Figure3_SourceData.csv` | RLI, NA and boundary cases are represented. |
| Figure 4 | `Figure4_final.pdf` | `Figure4_SourceData.csv` | Caption defines seed-level s.d. and n for GSE278936. |

## Supplementary Information

The attached guide says supplementary figures, small tables and text should be submitted as a single combined PDF. The current project has both Word and PDF versions. Use Word if the portal accepts it; use PDF if the portal follows the 2019 guide strictly or refuses Word.

Preferred file:

```text
submission/nature_communications/portal_materials_final/Supplementary_Information_V4.docx
```

Fallback / visual QA copy:

```text
submission/nature_communications/portal_materials_final/Supplementary_Information_V4.pdf
```

Contents:

- Supplementary Fig. 1: evaluation-regime-dependent model behavior.
- Supplementary Fig. 2: random-size-matched controls.
- Supplementary Fig. 3: shared_panel_50 robustness.
- Supplementary Table 1: dataset and sample structure.
- Supplementary Table 2: split sample counts.
- Supplementary Table 3: Visium breast section-held-out summary.
- Supplementary Table 4: mixed-effects/statistical summary.
- Supplementary Table 5: boundary and non-interpretable cases.
- Supplementary Table 6: two-sided paired Wilcoxon signed-rank results with paired n, W statistics, P values and BH-FDR-adjusted q values.
- Supplementary methods: GraphSAGE settings, split definitions, full output availability, Moran analysis and Andersson-to-Visium stress test.

## Source Data

The guide states that source data may be requested as an Excel file or zipped folder, with raw values underlying graphs and charts. Use the prepared zipped folder.

Use:

```text
submission/nature_communications/SpatialLeak_NatCommun_SourceData_final.zip
```

If the portal asks for individual files, upload files from:

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
SupplementaryFigure2_SourceData.csv
SupplementaryFigure3_SourceData.csv
SupplementaryTable1_DatasetSampleStructure.csv
SupplementaryTable2_SplitSampleCounts.csv
SupplementaryTable3_VisiumBreastSectionHeldOutSummary.csv
SupplementaryTable4_MixedEffectsSummary.csv
SupplementaryTable5_BoundaryCases.csv
SupplementaryTable6_WilcoxonSignedRankResults.csv
SupplementaryTable_VisiumBreastSectionHeldOut.csv
SourceData_Index.csv
README.md
```

Portal handling:

- If there is a Source Data upload category, upload `SpatialLeak_NatCommun_SourceData_final.zip`.
- If the portal asks figure by figure, upload each CSV and use `SourceData_Index.csv` to map figure panels to data.
- Keep Figure 1 source data as the conceptual-source manifest.

## Reporting Forms And Checklists

The guide says life-science articles need a completed reporting summary, and papers using central custom code need a code/software checklist. It also notes that Nature forms should be opened and completed in Adobe Reader rather than a browser.

Official forms are stored in:

```text
submission/nature_communications/portal_materials_final/official_forms/
```

Use these files:

| Form | File | Current action |
|---|---|---|
| Bio and life sciences reporting summary | `nr-reporting-summary.pdf` | Complete manually in Adobe Reader. |
| Machine learning checklist | `machine-learning-checklist_filled.pdf` | Verify manually in Adobe Reader before upload. |
| Code and Software submission checklist | `nr-software-policy.pdf` | Complete manually in Adobe Reader. |
| Manual guide | `OFFICIAL_FORM_COMPLETION_GUIDE.md` | Use as field-by-field support. |

Draft answer files:

```text
submission/nature_communications/portal_materials_final/reporting/Reporting_Summary_Draft.md
submission/nature_communications/portal_materials_final/reporting/Machine_Learning_Checklist_Draft.md
submission/nature_communications/portal_materials_final/reporting/Code_Software_Checklist_Draft.md
submission/nature_communications/portal_materials_final/reporting/REPORTING_FORM_EVIDENCE_MAP.md
```

Do not upload the Markdown drafts as substitutes for official forms unless the portal explicitly asks for supporting documentation. They are answer sources for filling the official PDFs and portal fields.

## Data And Code Availability

The guide requires separate Data Availability and Code Availability sections after Methods and before References. These are already in the manuscript.

Portal text files:

```text
submission/nature_communications/portal_materials_final/DATA_AVAILABILITY.md
submission/nature_communications/portal_materials_final/CODE_AVAILABILITY.md
```

Required permanent links:

```text
GitHub: https://github.com/seefreewind/spatialleak
Zenodo DOI: https://doi.org/10.5281/zenodo.21881438
```

Dataset access notes to preserve:

- DLPFC, Andersson, Thrane, 10x Visium breast and GSE278936 data are public.
- The two 10x Visium breast sections are public 10x Genomics Block A Section 1 and Section 2.
- Restricted EGA validation data from the prostate study were not used.
- GSE278936 is spatial-channel external replication, not clean patient-level validation.

## Declarations And Portal Metadata

Enter these values consistently in the portal.

| Field | Entry |
|---|---|
| Funding | No specific funding was received for this work. |
| Competing interests | The authors declare no competing interests. |
| Acknowledgements | None, or leave blank if allowed. |
| Ethics / human subjects | Public datasets only; no restricted EGA validation data used. Follow portal wording if a field is mandatory. |
| Related manuscripts | None, unless the authors have another overlapping manuscript under consideration. |
| Preprint | Enter only if a preprint exists. Otherwise select no / not applicable. |
| Transparent peer review | Author preference to be selected in portal. |
| Double-blind peer review | Do not select unless a fully anonymized manuscript is prepared. Current manuscript is not anonymized. |

## Author And Correspondence Information

Use exactly:

```text
Yu Zhang1, Ying Chen2, Yue Liu2, Da Lin1

1 Department of Ophthalmology, The Second Affiliated Hospital of Wenzhou Medical University, No. 109 Xueyuan West Road, Lucheng District, Wenzhou, Zhejiang Province, China

2 Wenzhou Medical University, Wenzhou, Zhejiang Province, China

Correspondence: Da Lin, 212574@wzhealth.com; ORCID 0009-0009-4410-0218
```

Portal check before submission:

- Confirm corresponding author is correctly marked.
- Confirm all authors approve submission and author order.
- Confirm author contribution statement is included in the manuscript.

## What Not To Upload

Do not upload these unless the portal explicitly requests them:

- Old V5, V6, V7 or V8 manuscript drafts.
- Full TIFF-containing archive `SpatialLeak_NatCommun_portal_materials_final.zip`, unless raster backups are requested.
- Rendered page PNG folders.
- Markdown reporting drafts as replacements for official PDF forms.
- Prototype figures such as `Figure3_prototype_scatter.*`.
- Any restricted EGA data.

## Final Portal Checklist

Before pressing submit, verify:

- Main manuscript is `SpatialLeak_NatCommun_V9_language_polished.docx`.
- Supplementary Information is `Supplementary_Information_V4.docx` or the V4 PDF if the portal requires PDF.
- Source Data zip is uploaded and linked to Figures 1-4 and Supplementary Figures 1-3 where possible.
- Figure files are uploaded in order: Figure 1, Figure 2, Figure 3, Figure 4.
- Figure 2 and Figure 4 captions still define error bars and n values.
- Code availability includes GitHub v1.0.0 and Zenodo DOI.
- Data availability includes all public datasets and states that restricted EGA validation data were not used.
- Funding, competing interests and acknowledgements match the manuscript.
- Reporting Summary, ML Checklist and Code/Software Checklist are completed in Adobe Reader or the portal.
- GSE278936 is described only as spatial-channel replication.
- No new experiments, new datasets or expanded claims are added during portal entry.

## Submission Package Bottom Line

The scientific manuscript, figures, Supplementary Information, source data, cover letter, code/data availability and open-science links are ready. The only remaining non-scientific tasks are:

1. Complete or verify the official Nature reporting PDFs in Adobe Reader.
2. Upload the V9 manuscript and prepared portal materials.
3. Check the system-generated submission PDF for figure order, special characters and file links.
4. Submit.
