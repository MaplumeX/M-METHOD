---
name: mm-ui
description: 提炼自《Refactoring UI》并融合结构探索、全状态设计、设计系统双向同步与多画布适配的 Web UI 设计工作流。包含六种模式——Explore（多方案结构探索）、System（设计系统）、Sync（代码/设计同步）、Build（构建）、Refine（调优）、Review（评审）——以及贯穿始终的三项工程纪律。适用于探索页面布局方案、构建或修改页面/组件/设计系统、补齐加载/空/错误/边界状态，或界面「看起来不对劲但说不出哪里怪」时（如「界面设计」「给几个方案」「样式调整」「UI 太丑」「设计评审」「全状态」「设计规范」「同步组件库」「explore」「state matrix」「design brief」）。不适用于后端逻辑、纯文案修改或没有视觉呈现的改动。
---

# UI · 界面设计与调优

负责所有带视觉呈现的界面工作：六种模式，三项纪律，兼顾多方案结构探索、全状态体验完整度与静态/视觉证据门禁。

**不在范围内**：后端逻辑、纯文案编辑、用户不可见的底层重构。

## 核心前提

1. **脚本只是底线，不是全部交付标准**：`check_ui_rules.py` 与 `check_contrast.py` 仅校验静态规则与契约；对应模式要求的 **Read Gate、结构探索比选、程序生色、全状态矩阵（State Matrix + 拟真数据）、Pass 1 → Pass 2、对照截图（或逐项未核验清单）、`§id` 追溯与 AI Slop Test 5 项裁决** 同样是硬性交付要求。
2. **先读剧本再动手**：命中模式后，必须先完整读取对应的 `references/mode-*.md` 剧本及必读透镜文件。
3. **画布与介质解耦**：依据 [`canvas-adapters.md`](references/canvas-adapters.md)，按阶段选择 **独立 HTML 原型**、**设计工具 MCP 画布**（仅当当前会话确实可用时，否则透明回退 HTML / ASCII）或 **生产框架代码**，先验证结构与状态再落业务代码。

## 规划期只读边界

若当前处于 `mm-plan` 规划阶段，或用户尚未确认方案 / 授权实施，本 skill 全程保持**只读**：
- **严禁写入任何文件**（`tokens.*`、`DESIGN.md`、`preview.html`、业务 UI 代码、简报注释、`proposed/design/` ADR 或 `.plan.md`）。
- 需要校验配色时，直接向 `scripts/check_contrast.py` 传入内联 `"fg:bg"` 参数，不写临时文件。
- 仅向 `mm-plan` 返回结构探索草案、组件索引摘要、设计系统决策草案或 UI 方向/步骤建议，等待用户确认后再按 `mm-plan` 流转规则落盘。

## Step 0 · 先读项目，再做判断

在提出任何设计结论前，先查清并简短汇报以下 5 项（若存在 `DESIGN.md` 一并读取其受众、语调与组件索引）：

1. **框架（Framework）**：React / Vue / Svelte / 原生 HTML；SSR 还是 SPA。
2. **现有 Token**：CSS 自定义属性、theme 对象、`tokens.json`、`theme/` 或 Tailwind 配置。
3. **组件库与既有组件**：shadcn/ui、MUI、Ant Design、Radix 或项目 `components/` 索引及其支持状态。
4. **深色模式**：已支持、规划中，还是不支持。
5. **既有字号与间距刻度**：从配置文件提取真实值，绝不凭记忆猜测。

**项目既有体系永远优先**：已有设计系统与组件时翻译并索引使用（必要时先走 `Sync` 纳入 `DESIGN.md`），绝不擅自覆盖、重复造轮子、静默迁移或引入新的构建依赖。

## 模式路由

命中第一条即停止；任务混杂时按 `Explore → System / Sync → Build → Refine` 分段推进：

| 触发条件 | 模式 | 必读剧本与透镜（Read Gate） | 必跑脚本门禁 |
|---|---|---|---|
| 布局结构/交互流未定，或要求「给几个方案 / 对比方向」 | **Explore** | [`mode-explore.md`](references/mode-explore.md) + `01`、`03`、`15`、`16`、`canvas-adapters.md` | Peer Analysis + 3 个结构/交互/密度差异方案 + 1 个主推（授权写原型时可用 `build_explorer.py` + `shoot.py` 生成并排对比与 `sheet.png`） |
| 尚无或需替换设计系统 | **System** | [`mode-system.md`](references/mode-system.md) + `11-tokens.md`、`05-color.md`、`15-direction.md` | `generate_ramp.py` + `check_contrast.py` + `check_ui_rules.py --tokens` |
| 将既有代码 Token/组件同步进 `DESIGN.md`，或按规范改动同步回代码 | **Sync** | [`mode-sync.md`](references/mode-sync.md) + `11-tokens.md`、`13-beyond.md`、`canvas-adapters.md` | 入站跑 `check_ui_rules.py` 盘点缺口；出站先出影响 Diff 再跑全套校验 |
| 新增页面 / 组件 / 区块 | **Build** | [`mode-build.md`](references/mode-build.md) + `02`、`03`、`04`、`06`、`08`、`09`、`10`、`15`（展示/工作台补读 `16`） | `check_ui_rules.py --pass1` → 终检（`--brief`、`--report`、`check_contrast.py`、`shoot.py --strict`） |
| 修改现有界面 | **Refine** | [`mode-refine-review.md`](references/mode-refine-review.md) + `09-antipatterns.md` + 命中透镜 | `check_ui_rules.py` + `shoot.py` 前后对照（改配色补 `check_contrast.py`） |
| 只评审不改代码 | **Review** | [`mode-refine-review.md`](references/mode-refine-review.md) + `09-antipatterns.md`、`15-direction.md` | 独立视角审图（`shoot.py`）+ CRAP/认知负荷 + 5 项 AI Slop Test + 全状态覆盖裁决 |

## 贯穿始终的三项纪律

1. **每次只改一个维度（透镜）**：不把间距、字重、阴影混在同一轮改动中，改完一个维度并验证对比效果后再进下一个。
2. **事实证据先于修改建议**：先摆出客观现状（如实际用了几档间距、行宽 `ch` / 对比度数值、重复元素、缺失状态），再给出调整方案。
3. **`§id` 是最小讨论单元**：每条评审发现与每处修改都必须附带对应的 `§id` 规则编号（见 [`00-coverage.md`](references/00-coverage.md)）。

## 视觉证据与决策归档

- **无渲染不做视觉结论，无对照不做质量判定**：
  - `Explore` 授权出原型时，可用 `scripts/build_explorer.py` 生成并排 `style-explorer.html`，用 `scripts/shoot.py` 输出 `sheet.png`。
  - `Build` 确认全状态矩阵（`default` 拟真数据 + `empty` + `loading` + `error` + `edge`），优先运行 `scripts/shoot.py --states ... --strict` 校验真实视口（`1440px` + `400px` + 异常态）无横向溢出、断图与运行时报错，并查看 `sheet.png` / 对照截图。
  - `Refine` 查看修改前后的桌面与移动对比图；`Review` 对同会话产出遵循**独立视角审计**（仅依据真实截图、DOM 检查与源码，不带创作自辩上下文）。
  - 若运行环境确实无法渲染截图，**必须在汇报中逐项列出「未核验项清单」**，禁止只用一句「没有浏览器」带过。
- **ADR 归档边界**：作用域跨越单页的长期决策（色板、刻度、跨组件契约、组件库选型、深色策略）在获确认后记入 `proposed/design/`（遵循 `.agents/ADR/AGENTS.md`）；单页局部布局权衡留在 `.plan.md`。

## 参考资料索引

- **模式剧本与画布**：[`mode-explore.md`](references/mode-explore.md) · [`mode-system.md`](references/mode-system.md) · [`mode-sync.md`](references/mode-sync.md) · [`mode-build.md`](references/mode-build.md) · [`mode-refine-review.md`](references/mode-refine-review.md) · [`canvas-adapters.md`](references/canvas-adapters.md)
- **规则与配方（151 条规则，总索引 [`00-coverage.md`](references/00-coverage.md)）**：`01-starting` / `02-hierarchy` / `03-spacing` / `04-typography` / `05-color` / `06-depth` / `07-images` / `08-finishing` / `09-antipatterns` / `10-recipes` / `11-tokens` / `12-tailwind` / `13-beyond` / `14-laws` / `15-direction` / `16-layout-patterns`
- **自动化脚本**：[`check_ui_rules.py`](scripts/check_ui_rules.py) · [`check_contrast.py`](scripts/check_contrast.py) · [`generate_ramp.py`](scripts/generate_ramp.py) · [`shoot.py`](scripts/shoot.py) · [`build_explorer.py`](scripts/build_explorer.py)
