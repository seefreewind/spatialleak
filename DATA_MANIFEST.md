# DATA_MANIFEST.md — 数据清单

> 更新: 2026-08-07 · 核验方式: 所有 URL/accession 于 2026-08-07 实测 (HTTP 200 / GEO eutils / Zenodo API)。
> 标注: ✅ = 已核实 · UNVERIFIED = 未能核实 · 分类: Primary(主分析) / Secondary(次分析) / External(外部验证) / Backup(备用)

## 汇总

| # | 数据集 | 平台 | #患者 | #切片 | #spots | 角色 | 状态 | GO/NO-GO |
|---|--------|------|-------|-------|--------|------|------|----------|
| D1 | SpatialLIBD DLPFC (Maynard 2021) | 10x Visium | 3 | 12 | 47,681 | **Primary (Pilot)** | 待下载 | ✅ GO |
| D2 | Andersson HER2+ 乳腺癌 (2021) | ST v1.0 | **8** | **36** | ~446/切片 | **Primary (patient-held-out)** | 待下载 | ✅ GO |
| D3 | 10x Visium 乳腺癌 v1.1.0 | 10x Visium | 1 | 2 | 3,798+3,987 | Secondary | 待下载 | ✅ GO |
| D4 | Thrane 黑色素瘤 (2018) | ST v1.0 | **4** | **8** | ~250–500/切片 | Secondary | 待下载 | ⚠️ 坐标待核验 |
| D5 | 10x Visium 结直肠癌 | 10x Visium | 1 | 1 | 3,138 | Secondary | 待下载 | ✅ GO |
| D6 | 10x Visium 前列腺癌 FFPE | 10x Visium | 1 | 1 | 4,371 | Secondary | 待下载 | ✅ GO |
| D7 | spatialDLPFC (Science 2024) | 10x Visium | **10** | **30** | UNVERIFIED | External (脑) | 待核验途径 | ⚠️ |
| D8 | Spatial CITE-seq tonsil (GSE213264) | CITE-seq | UNVERIFIED | 18 样本 | UNVERIFIED | External (蛋白任务) | 待下载 | ⚠️ |
| D9 | SpatialGlue tonsil+LN (GSE263617) | Visium RNA+蛋白 | 2 | 4 | 4,337/4,519 | Backup (多组学) | 待下载 | ✅ GO |
| D10 | 10x Visium 人淋巴节 | 10x Visium | 1 | 1 | 4,039 | Backup | 待下载 | ✅ GO |
| D11 | 10x CytAssist tonsil RNA+蛋白 | Visium CytAssist | 1 | 1 | 4,908 | Backup (蛋白任务) | 待下载 | ✅ GO |
| D12 | 10x Visium 小鼠脑 (sagittal) | 10x Visium | 1 | 2 | 2,696/3,353 | Backup (cross-species) | 待下载 | ✅ GO |

---

## D1. SpatialLIBD DLPFC Visium — **Primary / Pilot 数据**

- Organism/Tissue/Disease: Human / 背外侧前额叶皮层 (DLPFC) / 神经正常对照
- Platform/Modality: 10x Visium v1 / 全转录组 RNA
- **3 donors / 12 切片 / 47,681 spots** (每切片 3,460–4,789) ✅
- 空间坐标: ✅ pixel (pxl_col/row_in_fullres) + array (array_row/col)；层标注 (L1–L6+WM) ✅
- 患者 ID: Br5292 (151507–151510), Br5595 (151669–151672), Br8100 (151673–151676) ✅
- URL (实测 200):
  - 表达矩阵: `https://spatial-dlpfc.s3.us-east-2.amazonaws.com/h5/{SAMPLE}_filtered_feature_bc_matrix.h5` (9–15 MB/切片)
  - 坐标: `https://raw.githubusercontent.com/LieberInstitute/HumanPilot/master/10X/{SAMPLE}/tissue_positions_list.txt`
  - 层标注: `https://raw.githubusercontent.com/LieberInstitute/HumanPilot/master/10X/barcode_level_layer_map.tsv`
- License: 数据无需注册可直接下载；明确 license 声明 UNVERIFIED (包为 Artistic-2.0)
- 下载状态: ⏳ 待下载 (~160 MB, 仅 filtered h5 + 坐标 + 层标注；省略 6.4 GB 全分辨率 TIF)
- 质量状态: ✅ 核验完整
- **GO/NO-GO: ✅ GO** — 同时支持 within-slide (random vs spatial-block)、slide-held-out (12)、patient-held-out (3)、cross-dataset (D7)
- 注意: 无 GEO accession (已核实)；GSE186538 是**另一个**数据集 (Franjic hippocampus) — **勿混用**

## D2. Andersson HER2+ 乳腺癌 ST — **Primary (patient-held-out 金标准)**

- Organism/Tissue/Disease: Human / HER2+ 乳腺癌 / 癌症
- Platform/Modality: Spatial Transcriptomics v1.0 (pre-Visium, 低密度 ~446 spots/切片) / RNA
- **8 patients (A–H) / 36 切片** (每肿瘤 3 或 6) ✅
- URL: Zenodo `10.5281/zenodo.4751624` ✅ (count-matrices.zip 37 MB, images.zip 592 MB, spot-selections.zip 坐标, meta.zip 病理标注 — **zip 有密码，密码在记录描述中**)
- 原始 FASTQ: EGA EGAD00001008031 (受限，**不采用**) ✅
- License: CC BY 4.0 (Zenodo 记录) ✅
- **GO/NO-GO: ✅ GO** (patient-held-out 主场景；Phase 14 外部验证 + Phase 6 后扩展)

## D3. 10x Visium 乳腺癌 v1.1.0 (Block A, 2 sections)

- 1 patient / 2 sections / 3,798 + 3,987 spots ✅ (同 block 相邻切片)
- URL: `https://www.10xgenomics.com/datasets/human-breast-cancer-block-a-section-1-1-standard-1-1-0` (及 section-2) ✅；矩阵 `cf.10xgenomics.com/samples/spatial-exp/1.1.0/V1_Breast_Cancer_Block_A_Section_{1,2}/..._filtered_feature_bc_matrix.tar.gz` ✅ (77.6 MB / 9.96 MB spatial)
- License: CC BY 4.0 ✅ | 无注册
- **GO/NO-GO: ✅ GO** (within-slide 主场景; slide-held-out 2 切片)

## D4. Thrane 黑色素瘤 ST (2018)

- 4 patients (mel1–4) / 8 sections (rep1/rep2) ✅；~250–500 spots/切片 (ST v1.0 低密度)
- URL: `https://www.spatialresearch.org/wp-content/uploads/2019/03/ST-Melanoma-Datasets_1.zip` ✅ (6.2 MB, counts 仅)
- **坐标文件 UNVERIFIED** (ST 网格坐标可由 array 布局重建) → **GO 条件: Phase 2 完成坐标重建**
- License: 免费下载 (明确 license UNVERIFIED)

## D5. 10x Visium 结直肠癌

- 1 donor / 1 section / 3,138 spots ✅ | URL ✅ (`human-colorectal-cancer-whole-transcriptome-analysis-1-standard-1-2-0`) | CC BY 4.0 ✅
- **GO/NO-GO: ✅ GO** (within-slide 场景)

## D6. 10x Visium 前列腺癌 FFPE

- 1 donor / 1 section / 4,371 spots ✅ (Gleason 7) | URL ✅ (`human-prostate-cancer-adenocarcinoma-with-invasive-carcinoma-ffpe-1-standard-1-3-0`) | CC BY 4.0 ✅
- **GO/NO-GO: ✅ GO** (within-slide 场景)

## D7. spatialDLPFC (Science 2024, Huuki-Myers) — External (脑)

- 10 donors / 30 blocks / DLPFC 10x Visium ✅ (存在性核实: PMC11398705)
- 下载途径 UNVERIFIED (Globus/LIBD 服务器，待 Phase 2 核验)
- **GO/NO-GO: ⚠️ 条件 GO** — DLPFC 外部验证首选；途径核验后转正

## D8. Spatial CITE-seq tonsil 等 (GSE213264, Liu et al. 2023, Nat Biotechnol)

- Human tonsil/spleen/thymus/skin/GBM + mouse；tonsil: **273 蛋白 + 全转录组**；18 样本 ✅
- GEO eutils 核验 ✅ (GEO FTP 开放)；样本级 patient 数 UNVERIFIED
- **GO/NO-GO: ⚠️ 条件 GO** — 蛋白预测任务 (Phase 2 选蛋白任务时启用)

## D9. SpatialGlue tonsil+LN (GSE263617, Nat Methods 2024)

- 2 donors (A1/D1) / 4 Visium 切片 / 每切片 RNA (18,085 基因) + **31 蛋白** 共测；tonsil A1 4,337 / D1 4,519 spots ✅ | GEO 页面核验 ✅ (RAW tar 1.2 GB)
- **GO/NO-GO: ✅ GO** (多组学 patient-held-out 场景, Phase 2)

## D10. 10x Visium 人淋巴节

- 1 section / 4,039 spots ✅ | URL ✅ (`human-lymph-node-1-standard-1-0-0`) | CC BY 4.0 ✅
- **GO/NO-GO: ✅ GO** (Backup)

## D11. 10x CytAssist tonsil RNA+蛋白

- 1 section / 4,908 spots / FFPE / 基因+蛋白文库 (4 加装抗体) ✅ | URL ✅ | CC BY 4.0 ✅
- **GO/NO-GO: ✅ GO** (Backup, 蛋白任务)

## D12. 10x Visium 小鼠脑 (sagittal anterior/posterior)

- 1 mouse each / 2 sections / 2,696 + 3,353 spots ✅ | URL ✅ | CC BY 4.0 ✅
- **GO/NO-GO: ✅ GO** (Backup, cross-species 或 slide-held-out 冒烟测试)

---

## 数据需求映射 (任务 × 划分)

| 划分层级 | 需求 | 数据集 |
|----------|------|--------|
| Tier 1 within-slide | 每切片大量 spots | D1, D3, D5, D6 |
| Tier 2 cross-slide | 多切片/个体 | D1 (12), D2 (36), D3 (2), D12 (2) |
| Tier 3 cross-patient | 多患者 | **D1 (3), D2 (8), D4 (4), D9 (2)** |
| Tier 4 cross-dataset | 独立研究 | D1→D7 (脑); D2→D3 (乳腺) |
| Tier 5 cross-platform | 不同平台 | D2 (ST) vs D3/D5 (Visium); D8/D11 (CITE-seq/CytAssist) |
| RNA+蛋白任务 | 配对双模态 | D8, D9, D11, Xenium RCC (10x 官方, 465,534 cells, 蛋白 27-plex, URL 已核验) |

## 下载优先级 (Phase 2)

1. **D1 DLPFC** (~160 MB) — Pilot 唯一必需
2. D3 乳腺癌 2 切片 (~180 MB) — 第二场景
3. D4 黑色素瘤 (6.2 MB) — 坐标重建后启用
4. D2 Andersson (37 MB counts) — patient 主场景
5. D5/D6 (各 ~80 MB) — within-slide 扩展
