---
name: mm-ui
description: 提炼自《Refactoring UI》的 Web UI 设计规则与工作流。包含四种模式——System（设计系统）、Build（构建）、Refine（调优）、Review（评审）——以及贯穿始终的三项工程纪律。适用于构建或修改页面、组件、设计系统，或界面「看起来不对劲但说不出哪里怪」时（如「界面设计」「样式调整」「UI 太丑」「设计评审」「视觉层级」「配色」「对比度」「间距」「排版」「阴影」「空状态」「设计规范」）。不适用于后端逻辑、纯文案修改或没有视觉呈现的改动。
---

# UI · 界面设计与调优

处理一切带有视觉呈现的工作。四种模式，三项纪律。本 skill 负责约束与检查，不凭空编造品味。

不在范围内：后端逻辑、纯文案编辑、用户看不见的底层改动。

**执行前提**：
- **脚本不是全部完成标准**：`check_ui_rules.py` 与 `check_contrast.py` 仅校验静态项与契约；对应模式的 **Read Gate、程序生色、Pass 1→Pass 2、对照截图（或逐项未核验清单）、`§id` 追溯与 AI Slop Test 5 项裁决** 同样是硬性交付要求。
- **先读模式剧本再动手**：命中模式后，必须先完整读取对应的 `references/mode-*.md` 剧本及其要求的透镜文件。

## 规划期只读边界

若处于 `mm-plan` 规划期，或用户尚未确认方案 / 授权实施，本 skill 全程**只读**：
- **严禁写入任何文件**（`tokens.*`、`DESIGN.md`、`preview.html`、业务 UI 代码、简报注释、`proposed/design/` ADR 或 `.plan.md`）；运行 `scripts/check_contrast.py` 时直接传 `"fg:bg"` 参数校验，不写临时清单文件。
- 规划期仅将设计系统决策草案或 UI 方向/步骤建议交回 `mm-plan` 呈递；待用户确认后，再按 `mm-plan`「确认与流转」规则落盘。

## Step 0 · 先读项目，再做判断

在提出任何设计结论前先简短汇报以下 5 项：

1. **框架（Framework）** — React / Vue / Svelte / 原生 HTML；SSR 还是 SPA。
2. **现有 Token（Existing tokens）** — CSS 自定义属性、theme 对象、`tokens.json`、`theme/`、Tailwind 配置。
3. **组件库（Component library）** — shadcn/ui、MUI、Ant Design、Chakra、Radix 等及其 token 契约。
4. **深色模式（Dark mode）** — 已支持、规划中，还是无。
5. **现有字号与间距刻度（Existing scales）** — 从配置文件提取真实值，绝不凭记忆瞎猜。

**项目现有系统永远优先。** 已有体系时翻译成项目词汇使用；绝不直接覆盖、静默迁移或擅自引入构建依赖。

## 模式路由（命中第一项即停止；混杂时按 `System → Build → Refine` 分段推进）

| 排查条件 | 模式 | 必读剧本与透镜（Read Gate） | 必跑脚本门禁 |
|---|---|---|---|
| 尚无或需替换设计系统 | **System** | [`mode-system.md`](references/mode-system.md) + `11-tokens.md`、`05-color.md` | `generate_ramp.py` + `check_contrast.py` + `check_ui_rules.py --tokens` |
| 新增页面 / 组件 / 区块 | **Build** | [`mode-build.md`](references/mode-build.md) + `02`、`03`、`04`、`06`、`10`、`15` | `check_ui_rules.py --pass1` → 终检（含 `--brief`、`--report`、`check_contrast.py`） |
| 修改现有界面 | **Refine** | [`mode-refine-review.md`](references/mode-refine-review.md) + `09-antipatterns.md` + 命中透镜 | `check_ui_rules.py`（改配色补 `check_contrast.py`） |
| 只给意见不改代码 | **Review** | [`mode-refine-review.md`](references/mode-refine-review.md) + `09-antipatterns.md`、`15-direction.md` | 可选静态扫描 + 5 项 AI Slop Test（只读不改） |

## 贯穿始终的三项纪律

1. **每次只改一个透镜。** 不把间距、字重、阴影混在一起改，改完一个维度看对比效果再进下一个。
2. **事实证据先于修改意见。** 先说出客观现状（用了几档间距、行宽/对比度数值、重复元素），再给改动方案。
3. **`§id` 规则编号是唯一可讨论的最小单元。** 每条评审发现与每处改动都必须附带 `§id`（见 `00-coverage.md`）。

## 视觉证据与决策归档

- **不看渲染不做视觉结论，不看对照不作质量判定。** Build 看 `1440px` + `400px` + 空状态对照（含 Pass 1 或 sibling/`preview.html` 对照）；Refine 看修改前后桌面/移动对比图。若环境确实无法渲染，**必须在汇报中逐项列出「未核验项清单」**，禁止只写一句“没有浏览器”。
- **ADR 归档**：生命周期超过单页的决策（色板、刻度、跨组件契约、组件库选型、深色策略）在获确认后记入 `proposed/design/`（遵循 `.agents/ADR/AGENTS.md`）；单页局部布局权衡留在 `.plan.md`。

## 参考资料库

- **模式剧本**：[`mode-system.md`](references/mode-system.md) · [`mode-build.md`](references/mode-build.md) · [`mode-refine-review.md`](references/mode-refine-review.md)
- **规则与配方（151 条规则，总索引 `00-coverage.md`）**：`01-starting` / `02-hierarchy` / `03-spacing` / `04-typography` / `05-color` / `06-depth` / `07-images` / `08-finishing` / `09-antipatterns` / `10-recipes` / `11-tokens` / `12-tailwind` / `13-beyond` / `14-laws` / `15-direction`
