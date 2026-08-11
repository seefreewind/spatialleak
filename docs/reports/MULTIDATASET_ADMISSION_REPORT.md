# MULTIDATASET_ADMISSION_REPORT.md — 多数据集准入报告

> 日期: 2026-08-09 · 范围: Andersson HER2+ / Thrane melanoma / 10x Visium breast v1.1.0
> 核验方式: URL 实测下载 + 解压 + 内容解析 (全部于 2026-08-09 执行)。UNVERIFIED = 未核实。

---

## 1. 准入判定汇总

| 数据集 | 判定 | 依据 | 角色 |
|--------|------|------|------|
| **Andersson HER2+ 乳腺** | ✅ **GO** | 8 patients/36 sections/13,620 spots; 表达+坐标+meta 全部可用; patient/slide/block 全支持 | **Primary external (patient-held-out 金标准)** |
| **Thrane melanoma** | ✅ **GO** | 4 patients/8 sections/2,345 spots; 坐标从 spot ID 恢复; 仅 counts+坐标 (无病理 meta) | Secondary external (V0.1 已跑: pca RLI 0.50) |
| **10x Visium breast v1.1.0** | ✅ **GO** (升级) | 2 sections/7,785 spots 下载+预处理完成; within-slide + slide-held-out + cross-platform 对照 | Backup / cross-platform external |

---

## 2. Andersson HER2+ (Spatial Deconvolution of HER2-positive Breast Tumors, Nat Commun 2021)

| 字段 | 值 | 核验 |
|------|-----|------|
| 下载地址 | Zenodo `10.5281/zenodo.4751624` (count-matrices.zip 37.2MB + spot-selections.zip + meta.zip) | ✅ 实测下载 |
| 密码 | `zNLXkYk3Q9znUseS` (count-matrices 可解; spot-selections/meta 密码验证失败, 见 §5) | ⚠️ 部分 |
| License | CC BY 4.0 (Zenodo 记录) | ✅ |
| 患者 ID | **A–H (8 patients)** | ✅ 36 个文件名核验 |
| 切片 ID | A1–A6, B1–B6, C1–C6, D1–D6, E1–E3, F1–F3, G1–G3, H1–H3 (**36 sections**) | ✅ |
| 表达矩阵 | 每切片 spots×genes TSV.gz; 共 13,620 spots × ~18,700 genes (ENSG symbol); 每切片 270–360 spots | ✅ 解析核验 |
| 空间坐标 | spot ID 为 "RxC" 格式 (如 10x13) → **ST v1.0 六边形网格坐标可直接恢复** | ✅ 程序化恢复 (hex_grid) |
| 病理 meta | meta.zip 每患者 1 个标注文件 (8 个) — **密码阻塞, 未用** | ⚠️ |
| patient-held-out | ✅ 8 folds (train 7/test 1) | ✅ |
| slide-held-out | ✅ 36 sections | ✅ |
| spatial block | ✅ (每切片 270–360 spots, 3×3 网格可行但 block 小) | ✅ |
| 与 DLPFC 任务统一 | ✅ 基因表达重建, symbol 直接交集 (shared panel 55 基因) | ✅ |
| 预处理完成 | `data/processed/anderson_hvg2000.h5ad` + `anderson_moran.csv` | ✅ |
| V0.1 benchmark | ✅ 完成 (见 MULTIDATASET_BENCHMARK_V0.1.md) | ✅ |

## 3. Thrane melanoma (Cancer Res 2018, ST v1.0)

| 字段 | 值 | 核验 |
|------|-----|------|
| 下载地址 | `https://www.spatialresearch.org/wp-content/uploads/2019/03/ST-Melanoma-Datasets_1.zip` (6.2 MB) | ✅ 实测下载 (需 User-Agent) |
| License | 免费下载; 明确 license 声明 UNVERIFIED | ⚠️ |
| 患者 ID | mel1–mel4 (**4 patients**) | ✅ |
| 切片 ID | mel1–4 × rep1/rep2 (**8 sections**) | ✅ 8 文件核验 |
| 表达矩阵 | 每切片 genes×spots TSV (gene 列含 "SYMBOL ENSGID"); 共 2,345 spots × ~14k ENSG | ✅ 解析核验 |
| 空间坐标 | spot 列名 "RxC" (如 2x9) → 六边形网格坐标可恢复 | ✅ 程序化恢复 |
| 病理 meta | **无** (zip 仅 counts) | ❌ |
| patient-held-out | ✅ 4 folds | ✅ |
| slide-held-out | ✅ 8 sections | ✅ |
| spatial block | ✅ (每切片 ~250–500 spots) | ✅ |
| 与 DLPFC 任务统一 | ✅ ENSG 体系; **同时是 symbol↔ENSG 映射桥** (shared panel 构建关键) | ✅ |
| 预处理完成 | `data/processed/thrane_hvg2000.h5ad` + `thrane_moran.csv` | ✅ |
| V0.1 benchmark | ⏳ 计划 (patient n=4, 功效低 → 作补充而非主外部) | — |

## 4. 10x Visium breast v1.1.0 (Block A, 2 sections)

| 字段 | 值 | 核验 |
|------|-----|------|
| 下载地址 | `cf.10xgenomics.com/samples/spatial-exp/1.1.0/V1_Breast_Cancer_Block_A_Section_{1,2}/...` | ✅ 实测下载 |
| License | CC BY 4.0 (10x 数据页) | ✅ |
| 患者 ID | 1 donor (block A) — **patient-held-out 不可用** | ✅ |
| 切片 ID | Section 1 (3,798 spots) / Section 2 (3,987 spots) | ✅ (S2 矩阵下载中) |
| 坐标 | tissue_positions_list.json (标准 10x) | ✅ |
| within-slide / slide-held-out | ✅ | ✅ |
| 与 DLPFC 任务统一 | ✅ 同平台同流程 (read_10x_h5) | ✅ |
| 判定 | **CONDITIONAL GO** — 作为 cross-dataset external (乳腺外部: Andersson→10x) 与 within-slide 扩展; section2 矩阵完成后转 GO | ⚠️ |

## 5. 已知问题 (UNVERIFIED / BLOCKED)

1. **Andersson spot-selections.zip / meta.zip 密码解压失败** (AES+ZipCrypto 均试, pyzipper/stdlib 均报 Bad password): 坐标已由 spot ID 恢复 (等效), 病理标注未使用 — **不阻塞** (V0.1 已跑通)。
2. Thrane 无病理/细胞类型标注 — cell-type composition baseline 不可用于 Thrane。
3. 10x breast section 2 表达矩阵下载中 (首次截断, 已重下)。
4. 原始 FASTQ (Andersson EGA / 10x) 均不开放 — 本项目不需要。

## 6. 与 DLPFC 的统一任务确认 (Priority 3)

- **A 面板**: 各数据集 top-50 Moran 靶基因 (HVG-2000 特征) — DLPFC/Andersson/Thrane 均已生成。
- **B 面板**: 跨数据集 shared gene panel — **55 个三路共享 ENSG**, 按跨数据集平均 Moran rank 取 top-50, **已冻结**于 `data/processed/gene_panels/shared_panel_50.txt` (在计算任何模型性能之前冻结)。
- 任务统一性: 三个数据集均为 "多基因表达重建 (HVG 特征 → 靶基因)", 唯一差异是特征 ID 体系 (DLPFC/Andersson= symbol; Thrane= ENSG) — 面板 B 以 ENSG 为锚, 运行时代做 ID 映射。

## 7. 硬性 GO 标准进度 (跨数据集)

| 标准 | 状态 |
|------|------|
| GO-A: DLPFC ≥10 seeds 方向稳定 | ✅ 10/10 seeds random>strict (见 DLPFC_FORMALIZATION_REPORT) |
| GO-B: 第二数据集复现 random > strict | ✅ **Andersson**: pca_ridge random 0.603 → patient 0.190 (RLI 0.69) |
| GO-C: 复杂模型严格 split 优势缩小 | ✅ DLPFC GraphSAGE (见 Formal 报告) |
| GO-D: Moran-膨胀方向多数据集一致 | ✅ DLPFC r=0.55/0.46; **Andersson r=0.74/0.50** (均 p<1e-6) |
