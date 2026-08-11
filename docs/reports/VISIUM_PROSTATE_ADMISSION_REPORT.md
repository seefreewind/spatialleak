# VISIUM_PROSTATE_ADMISSION_REPORT.md

> Date: 2026-08-10  
> Phase: 16 Priority 1 — Multi-patient Visium dataset admission  
> Candidate: GSE278936, human prostate Visium spatial transcriptomics  
> Decision: **CONDITIONAL GO**

## 1. Executive Decision

GSE278936 is suitable as a large public **multi-patient high-density Visium cohort** for random and within-section spatial-buffer leakage testing. It has public processed 10x-style matrices, spatial coordinates, scale factors, and images for 52 GEO samples.

It is **not a full GO** for the intended two-channel upgrade because the publicly available GSE278936 portion contains **52 public sections from 52 patients**, so each public patient has one section. Patient-held-out and slide/section-held-out evaluation are therefore effectively the same public split. This design can test cross-patient/cross-section generalization, but it cannot cleanly separate patient-level shortcut from slide/site/section effects inside the public GEO data alone.

The associated validation cohort has **32 sections from 8 patients**, which would be ideal for patient-versus-slide separation, but the paper and reporting summary state that this validation cohort is available through EGA restricted access, not directly public GEO.

## 2. Official Sources Checked

| Source | Evidence used |
|---|---|
| GEO GSE278936 accession page | Public status, sample count, overall design, platform, processed supplementary TAR, raw data restriction |
| GEO FTP `filelist.txt` | Exact public file inventory and file sizes |
| GEO MINiML / series matrix | Sample titles, sample accessions, tissue/treatment metadata, supplementary file URLs |
| Nature Communications article | Cohort structure, publication details, discovery/validation split, processing context |
| Nature Portfolio Reporting Summary | Data availability, public GEO versus restricted EGA validation cohort, Space Ranger/software notes |
| Supplementary Dataset 1 | Discovery cohort patient/sample/spot metadata |
| Supplementary Dataset 10 | Metastatic sample patient/sample/spot metadata |

Primary URLs:

- GEO: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE278936`
- GEO supplement directory: `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE278nnn/GSE278936/suppl/`
- Article: `https://www.nature.com/articles/s41467-024-54364-1`
- Reporting Summary: `https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-024-54364-1/MediaObjects/41467_2024_54364_MOESM14_ESM.pdf`

Local audit files:

- `data/external_audit/gse278936/filelist.txt`
- `data/external_audit/gse278936/GSE278936_family.xml`
- `data/external_audit/gse278936/GSE278936_series_matrix.txt.gz`
- `data/external_audit/gse278936/MOESM3.xlsx`
- `data/external_audit/gse278936/MOESM12.xlsx`
- `data/external_audit/gse278936/public_sample_audit.csv`
- `data/external_audit/gse278936/shared_panel_50_gse278936_usable_ensg.csv`
- `data/external_audit/gse278936/shared_panel_50_gse278936_usable_symbols.csv`

## 3. Required Admission Checks

| Check | Status | Evidence |
|---|---|---|
| 1. Processed count matrix public | **YES** | GEO `GSE278936_RAW.tar` contains 52 `matrix.mtx.gz` files. Raw FASTQ is not public. |
| 2. Spatial coordinates public | **YES** | Each sample has `tissue_positions_list.csv.gz`. |
| 3. Section IDs | **YES** | Supplementary Dataset 1/10 provide `Sample ID` / `Visium ID`; GEO files provide sample labels such as `BPH_1`, `TRNA_1`, `MET_A`. |
| 4. Patient IDs | **YES, but one public section per patient** | Supplementary Dataset 1 has 48 discovery `Patient ID` values; Supplementary Dataset 10 has 4 metastatic patient IDs. |
| 5. Sections per patient | **LIMITED** | Public GEO: 52 patients, 52 sections, one section per patient. Validation cohort: 8 patients, 32 sections, but restricted EGA. |
| 6. Platform | **YES** | 10x Genomics Visium Spatial Gene Expression, fresh frozen tissue, Space Ranger v1.1.0. |
| 7. Spot count | **YES** | Public samples total 134,509 spots under tissue; mean 2,587; range 578-4,899. |
| 8. shared_panel_50 usable genes | **YES** | 50/50 usable by ENSG and 50/50 usable by gene symbol in downloaded 10x `features.tsv.gz`. |
| 9a. Random split feasible | **YES** | All public samples have count matrices and spot barcodes. |
| 9b. Matched spatial block feasible | **YES** | Coordinates and multiple spots per section are available. |
| 9c. Spatial hop-buffer feasible | **YES** | Coordinates support within-section kNN graph construction. |
| 9d. Slide-held-out feasible | **YES** | Each GEO sample can be treated as a section/slide unit. |
| 9e. Patient-held-out feasible | **YES, but confounded** | Patient-held-out can be implemented, but because each public patient has one section, it is equivalent to holding out that section. |
| 10. Batch/site confounding | **YES / likely** | Public data mix BPH, treatment-naive, neoadjuvant-treated, CRPC, and metastatic samples; multiple ethics/cohort sources are reported; 13 Visium slide serials contain multiple capture areas. |
| 11. Download size/resources | **MODERATE-LARGE** | GEO TAR is 1.6 GiB listed as 1,741,076,480 bytes; processed public files total 1.741 GB; 52 sections and 134,509 spots. |

## 4. Public File Structure

GEO `filelist.txt` lists 365 entries:

| File type | Count | Total size |
|---|---:|---:|
| TAR archive | 1 | 1,741,076,480 bytes |
| `matrix.mtx.gz` | 52 | 1,426,539,899 bytes |
| `features.tsv.gz` | 52 | 15,845,856 bytes |
| `barcodes.tsv.gz` | 52 | included in TSV total |
| `tissue_positions_list.csv.gz` | 52 | 3,274,854 bytes |
| `scalefactors_json.json.gz` | 52 | 8,174 bytes |
| tissue images PNG | 104 | 294,014,243 bytes |

Each public sample has the expected 10x-style processed files:

- barcodes
- features
- matrix
- scale factors
- high-resolution image
- low-resolution image
- tissue positions

## 5. Sample and Patient Structure

Public GSE278936 samples:

| Public subset | Samples | Patient IDs | Sections | Spots under tissue |
|---|---:|---:|---:|---:|
| Discovery primary tumors, Supplementary Dataset 1 | 48 | 48 | 48 | 124,556 |
| Metastatic samples, Supplementary Dataset 10 | 4 | 4 | 4 | 9,953 |
| **Total public GEO** | **52** | **52** | **52** | **134,509** |

Sections per public patient:

| Statistic | Value |
|---|---:|
| Minimum | 1 |
| Median | 1 |
| Maximum | 1 |
| Patients with >1 public section | 0 |

The article reports a validation cohort of 32 sections from 8 patients. The Reporting Summary states that this validation cohort is available under restricted EGA access, not public GEO. Therefore it is not immediately usable for this no-permission admission path.

## 6. Batch and Confounding Assessment

GSE278936 is useful but not clean for isolating patient-level shortcuts.

Observed confounding risks:

- Treatment and disease-state groups are mixed: BPH, treatment-naive primary prostate cancer, neoadjuvant-treated prostate cancer, CRPC, and metastatic disease.
- Reporting Summary states that samples came from multiple cohorts and ethical approvals, including Tampere, ARNEO/UZ Leuven, and metastatic collections.
- Public sample IDs include 13 Visium slide serials; several serials contain four capture areas, so capture-area/slide-level technical effects may exist.
- Since public patient ID and public section ID are one-to-one, a patient-held-out split cannot distinguish patient identity from section, slide, tissue block, processing batch, or site.

Implication for SpatialLeak:

- Good for **within-section spatial-neighborhood leakage**.
- Good for **cross-section/cross-patient strict performance loss** as a conservative external-style split.
- Not sufficient by itself to prove a separate patient/batch shortcut channel in high-density Visium, because public patient-held-out equals public section-held-out.

## 7. Split Feasibility

| Split | Feasible? | Interpretation |
|---|---|---|
| random spot split | YES | Leakage-prone comparator. |
| matched spatial block | YES | Primary within-section spatial leakage test. |
| spatial hop-buffer | YES | Strong within-section neighborhood leakage test. |
| slide-held-out | YES | Hold out whole public GEO sample/section. |
| patient-held-out | YES, confounded | Equivalent to slide-held-out in public GEO because each public patient has one section. |

Validation rule:

- If patient-held-out is run on public GSE278936, validation must be selected only from training patients/sections. It must not use spots from the held-out patient/section.

## 8. shared_panel_50 Admission

One public `features.tsv.gz` file was downloaded and checked:

- Feature rows: 33,538
- Feature type: all rows `Gene Expression`
- shared_panel_50 by ENSG: 50/50 present
- shared_panel_50 by gene symbol: 50/50 present

Frozen usable panel outputs:

- `data/external_audit/gse278936/shared_panel_50_gse278936_usable_ensg.csv`
- `data/external_audit/gse278936/shared_panel_50_gse278936_usable_symbols.csv`

No gene was removed based on model performance.

## 9. Resource Estimate

Expected preprocessing:

- Download: 1.6 GiB TAR / 1.741 GB processed files.
- Extracted working size: likely several GB after decompressing MTX/TSV/CSV/PNG files.
- Spots: 134,509 under tissue.
- Genes: 33,538 features in the checked sample.
- Shared-panel benchmark target dimension: 50 genes.

Expected benchmark resource:

- Mean/PCA+Ridge/Spatial kNN, 5 seeds: feasible on CPU after preprocessing, but larger than current DLPFC and external datasets.
- 10 seeds: feasible if the 5-seed pilot is directionally stable and runtime is acceptable.
- GraphSAGE: defer until after minimal baselines. With 134k spots, graph construction and transductive training should be treated as a separate resource decision.

## 10. Decision

**CONDITIONAL GO**

Conditions:

1. Use GSE278936 first for spatial-channel evidence, especially random versus matched spatial block and hop-buffer splits.
2. If running patient-held-out on public GSE278936, label it as **section/patient-held-out** or explicitly state that public patient and public section are one-to-one.
3. Do not claim that public GSE278936 alone disentangles patient shortcut from slide/site/batch effects.
4. Do not proceed to the full Phase 16 Priority 2 benchmark as a clean high-density multi-patient two-channel validation unless the user accepts this limitation.
5. If clean patient-versus-slide separation is required, pursue restricted EGA validation cohort access or audit another public multi-section-per-patient Visium cohort.

## 11. Recommended Next Step

Do **not** immediately run the full Priority 2 benchmark under the original claim.

Recommended options:

1. Run a limited GSE278936 spatial-channel pilot only:
   - Mean
   - PCA+Ridge
   - Spatial kNN
   - shared_panel_50
   - random, matched_hop0, matched_hop2, matched_hop5
   - 5 seeds

2. Separately look for a public high-density Visium cohort with repeated sections per patient, or seek access to the GSE278936-linked EGA validation cohort.

3. Keep GSE278936 as a strong supplementary high-density spatial leakage dataset if the manuscript needs more Visium evidence, but do not use it as the central proof of the patient/batch shortcut channel.
