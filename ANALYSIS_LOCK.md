# ANALYSIS_LOCK.md — 分析决策锁定

> 用途: 所有关键分析在运行前预注册；主结果完成后不随意修改 primary endpoint。
> 状态: 🔒 LOCKED = 已冻结 · 🟡 PROPOSED = 候选定义 (Pilot 后冻结)

## 1. 🔒 Pilot 设计 (Phase 6)

- **数据集**: SpatialLIBD DLPFC (12 切片, 3 donors, 47,681 spots) — D1
- **任务**: 多基因表达预测。目标基因 = 全数据 Moran's I top-50 (数据属性特征选择，非 test-label 学习；在报告中说明)。特征基因 = 排除目标基因后的 top-2000 HVG (scanpy `highly_variable_genes`, flavor="seurat", n_top_genes=2000)。
- **预处理**: per-slide `normalize_total(target_sum=1e4)` + `log1p` (scanpy 默认); 坐标 = fullres pixel (pxl_col/row_in_fullres)。
- **Splits (3)**: Random spot 80/10/10 · Spatial block (per-slide grid 2×2, buffer ∈ {0, 2 array-step}) · Patient-held-out (3-fold LOO donor, train 2 donors / test 1 donor; val = 8 训练切片中 1 切片)
- **Models (4)**: Mean · PCA+Ridge (n=64, α=1.0) · Spatial kNN (k=15, 反距离加权, per-slide 坐标缩放) · GraphSAGE (2 层, hidden=64, CPU, 可选)
- **Seeds**: 全局 seed 42; 每配置 5 个 seed (0–4)。所有 split/模型/采样同源。
- **指标**: per-gene Pearson / Spearman / RMSE (normalized scale); 聚合 = mean / median / SD across genes; **保留 per-feature、per-seed 结果 CSV**。
- **主比较**: Random vs Patient-held-out (mean Pearson) — primary；Random vs Spatial-block — secondary。
- **统计**: slide-level bootstrap (Pilot 200, 正式 ≥1000); 95% CI; paired comparison; BH-FDR。

## 2. 🔒 泄漏量化指标 (Phase 4 主体定义)

对每个模型 m 和每个严格划分 s ∈ {spatial-block, patient-held-out, dataset-held-out}:

- **LI(m, s) = Perf_random(m) − Perf_strict(m, s)**
- **RLI(m, s) = LI / Perf_random(m)** (相对膨胀率; Perf 为 mean Pearson)

## 3. 🔒 Leakage Sensitivity Score (LSS) — **PILOT 后已冻结 (2026-08-07)**

| 候选 | 定义 | 冻结决定 |
|------|------|----------|
| A | LSS = mean_s RLI(m, s) | **主定义 (PRIMARY)** — 平均相对膨胀率, 跨模型可比较 |
| B | LSS = min_s Perf_strict / Perf_random | **敏感性定义 (SENSITIVITY)** — 最坏保留率 |

**Pilot 冗余性检查 (ANALYSIS_LOCK 冻结依据, 来自 results/pilot/analysis/LI_RLI.csv)**:
- PCA+Ridge: A = (0.211+0.210+0.217)/3 = **0.213**; B = 1−min(0.789,0.790,0.783) = **0.217** → 接近但不等价
- Spatial kNN: A = (0.274+0.287+0.120)/3 = **0.227**; B = 1−0.713 = **0.287** → **不等价** (patient 远低于 block)
- GraphSAGE (2 seeds, patient_Br5595): A ≈ **0.478**; block seed0 RLI ≈ 0.55 → 模型间区分度大
- 结论: A 与 B 在"泄漏渠道异质"的模型上不冗余 (kNN 的 patient 渠道远低于 block 渠道) → 均保留: A 主报告, B 敏感性。ρ>0.9 舍弃规则未触发。

**LSS 区分度 (Pilot 实证)**: PCA+Ridge ≈ 0.21 · Spatial kNN ≈ 0.12–0.29 (渠道异质) · GraphSAGE ≈ 0.48 → LSS 能区分模型对泄漏的敏感度 (H5 初步支持)。

**LSS 计算规格 (冻结)**: strict 集合 s ∈ {spatial_block (buffer=2), patient-held-out, dataset-held-out}; RLI 在 per-seed 水平计算后取 mean; LSS 的 95% CI 由 slide-level bootstrap 给出。

## 4. 🟡 Spatial Generalization Curve (Phase 8)

- 候选: SG-AUC (曲线下面积)。**仅当曲线单调且提供独立信息时引入**，否则只报告曲线本身。防指标膨胀。

## 5. 🔒 不可为 (Research Integrity)

- 禁止: 根据 test 结果反复调参 / 用 test 选 best seed / 删除不利结果 / cherry-pick / 将同 patient 不同 slide 当作外部验证 / 把 spot 当独立统计单位算窄 CI / 数据集重复使用冒充 external。
- 所有关键比较预先注册于本文件；Pilot 主结果完成后冻结 LSS 与全部 primary endpoint。

## 6. 🔒 记录要求

- 固定种子 (全局 42 + 每配置 5 seeds)
- 每次运行保存: config (yaml) + 软件版本 (`pip freeze`) + 数据版本 (data/processed/VERSION.json) + 运行日志 (results/*/run.log)
- 结果 CSV 为脚本产物; 人工修改视为违规 (git 保护 + 校验和)

## 7. 附录: SOEMC — Spatial Omics Evaluation Minimum Checklist (提案, 论文贡献)

1. patient-level separation
2. slide-level separation
3. spatial coordinate leakage audit
4. overlapping patch audit
5. spatial buffer specification
6. external validation
7. strong non-spatial baseline
8. spatial kNN baseline
9. patient-level CI
10. complete split metadata

> 不强行制造缩写；若论文阶段发现 SOEMC 名称无自然性，可改为 "Spatial Omics Evaluation Checklist (SOEC)" 或直述 10 条清单。

## 8. 🔒 Phase 7A 形式化设计 (2026-08-08 冻结)

**DLPFC 正式 benchmark (results/formal_dlpfc/)**:
- Seeds: 0–9 (10)。所有主实验 ≥10 seeds。
- Splits (per seed): random · matched_hop{0,1,2,5} (matched 3×3 blocks, kNN-hop buffer) · matched_coord{0.25,0.5,1.0} (z-坐标 buffer) · patient_{3 donors} · region_hop{5,10} (seed-invariant, 高 hop 扩展)
- **Matched block 定义**: 每切片 3×3 网格 block；每 seed 抽样 300 个候选指派，按 test–train 组成距离 (spot 数/log、library size、top-Moran 基因信号、layer 分数，各特征按全局 SD 标准化) 选最优 — 消除指派随机性造成的方差 (Pilot 观察: block seed 方差 0.107–0.364)。
- **hop buffer**: 每切片 kNN 图 (k=15)，test spot 到最近 train spot 的最短路径边数 ≥ h。hop∈{0,1,2,5,10} 覆盖: matched 可解析 0–5 (hop5 保留 ~13%)，region(edges-only train) 可解析 6–14 (hop10 保留 ~64%)。**Pilot 已证 array-step 欧氏 buffer ≤2 无效 → 正式版以 hop 为主距离度量**。
- Models: mean / pca_ridge / spatial_knn ×10 seeds; GraphSAGE (hidden=128, lr=1e-3, patience=60, k=10 自环图) ×10 seeds × {random, matched_hop0} + 3 patient folds。
- 统计: slide-level bootstrap ×1000 (seed=42); paired Wilcoxon (per-seed 配对) + BH-FDR; Spearman/Kendall 排名相关; mixed-effects (Phase 14 数据齐后)。
- 记录: per-fold/per-seed/per-slide/per-gene CSV + splits/seed{i}.json (含 match score 与 dropped 比例)。

**GraphSAGE block 高值异常调查 (Pilot seed1=0.478)**: 保留该异常值；在 formal 数据中检验 (a) 是否可重复 (b) 是否由 block 组成/指派导致 (match score vs 性能相关) (c) 是否属正常抽样方差 → 报告于 DLPFC_FORMALIZATION_REPORT。

**统一任务 (Priority 3)**: A 面板 = 每数据集自身 top-50 Moran 靶基因 (HVG-2000 特征)；B 面板 = 跨数据集 shared gene panel — **程序冻结**: 全部候选数据集 HVG-2000 交集基因，按跨数据集平均 Moran rank 排序取 top-50；冻结于 data/processed/gene_panels/shared_panel_50.txt；**在计算任何模型性能之前冻结，禁止按性能选基因**。

**Retention (Priority 5)**: Retention = Perf_patient / Perf_random (per model, mean Pearson)；与 RLI 联合展示；kNN vs GraphSAGE 对比。Retention 高 + RLI(patient) 低 = transportable spatial signal；Retention 低 + RLI 高 = shortcut-dominated dependence。
