---
name: mm-land
description: 在工作验收通过后收尾归档：删除对应的 .plan.md 文件，并将计划列出的 ADR 从 proposed/ 升格移入 implemented/。适用于用户明确表示验收通过（如「验收通过」「做完了」「可以了」「land it」「close it out」），或明确要求放弃/归档某份 ADR 时。严禁仅凭主观判断「代码看起来写完了」就自行调用。
disable-model-invocation: true
---

# Land · 验收归档

「归档（Landing）」是把提案固化为既成事实的唯一状态迁移。在此之前，`proposed/` 中的提案仍可随实施微调；一旦进入 `implemented/`，记录就必须与已交付现实严格一致。

## 准入闸门

- **必须有明确授权**：只有用户明确确认验收通过（或明确指示放弃/归档某份记录）时才可执行迁移。测试通过、diff 干净、步骤跑完只是验收前提，不等于验收本身。若用户尚未表态，先停下来询问——过早升格会导致 `implemented/` 与事实脱节，且生命周期迁移痕迹不可逆。
- **未通过验收时**：不要归档，询问具体未通过 `## Verification` 中的哪一项；此时应修订计划，而非升格记录。

## 主流程：交付升格（`proposed/` → `implemented/`）

1. **定位计划文件**

   ```bash
   find .agents/ADR/proposed -name '*.plan.md' 2>/dev/null | sort
   ```

   - 存在多个且用户未指定 → 询问用户（可优先列出所有步骤 `Verify:` 均已记录完成的计划供确认），不要按时间戳猜测。
   - 不存在任何 `.plan.md` → 仍可对单份 ADR 归档，但必须明确说明缺少计划文件，并以用户指定的记录作为本次处理对象。

2. **收集待交付 ADR**

   读取计划头部的全部 `ADR:` 行，其中列出的所有记录都将随本次交付一并升格；第一条为主记录。

3. **核对实际交付状态**

   逐条检查列出的 ADR：它的 `## Acceptance criteria` 是否均已满足，决策是否在代码中真实落地。若有记录尚未完全交付，立即停下并给出两个选项：补完剩余工作，或将其 `ADR:` 行从计划中移除（留在 `proposed/` 等待后续交付）。`implemented/` 代表「已交付」，不代表「尝试过」。

4. **核对验收清单（`## Verification`）**

   `## Verification` 代表用户的人工验收签字。每一行都必须已勾选，且旁注了实际核验结果。禁止未经确认擅自替用户勾选。
   - 若仍存在未勾选项：停下并列出具体未勾条目，请用户在对话中逐项确认测试结果，或明确声明豁免某项（如缺少真机设备、接受该缺口）。
   - 仅当用户在对话中对每一项未勾条目都给出了明确核验结论或豁免指令后，才可代为更新为 `[x] ... — verified by user, YYYY-MM-DD` 或 `[x] ... — waived by user (<reason>), YYYY-MM-DD`，再继续下一步。

5. **核对步骤验证与事实漂移**

   - 逐条检查 `## Steps` 中每一步内联 `Verify:` 旁记录的实测结果；若存在未记录或未运行的步骤，先补跑并核实。
   - 对照当前代码检查计划与 ADR 是否发生漂移（前提失效或核心决策已变更）。若核心决策与交付不符，停下并改为修订计划或起草替代 ADR，严禁带着过时决策静默升格。

6. **删除计划文件**

   ```bash
   rm .agents/ADR/proposed/{delivery}.plan.md
   ```

7. **逐一升格 ADR**

   先确保目标分类目录存在，再移动文件（一次交付可能横跨 `architecture`、`feature`、`design`、`process` 等多个分类，每份记录按各自所属分类移动，不可套用计划文件所在目录）：

   ```bash
   mkdir -p .agents/ADR/implemented/{class}
   mv .agents/ADR/proposed/{class}/{name}.md \
      .agents/ADR/implemented/{class}/{name}.md
   ```

   按 `.agents/ADR/AGENTS.md` 更新每份记录：
   - 将 `Status: proposed` 改为 `Status: implemented`。
   - 将 `## Proposal` 改为 `## Decision`，改用现在时态陈述已交付的现实。
   - 将 `## Acceptance criteria` 和 `## Risks` 归并入 `## Consequences`。
   - 仅修正实施中变更的客观事实（路径、符号名、默认值）；若核心决策本身改变，停下并按替代记录流程处理。

8. **修复全仓引用链接与替代反向链接**

   由于相对路径编码了生命周期目录（同目录用裸文件名 `{name}.md`，跨目录按相对层级计算；位于 `proposed/` 根目录的 `.plan.md` 引用 `proposed/{class}/{name}.md` 时写作 `{class}/{name}.md`，记录移入 `implemented/` 或 `rejected/` 后应更新为 `../implemented/{class}/{name}.md` 或 `../rejected/{class}/{name}.md`），仅搜 `proposed/{class}/{name}` 会漏改。按文件名全仓检索：

   ```bash
   grep -rn --exclude-dir=.git --exclude-dir=node_modules "{name}.md" . 2>/dev/null
   ```

   - 根据引用方所在目录，将相对路径更新为新位置（同目录使用裸文件名，跨目录按相对层级计算）。
   - 代码注释中的 `ADR <date>-<slug>` 不含路径，无需改动。
   - 严禁修改 `archived/` 中的历史冻结记录。
   - 若本次记录替代了某份既有的 `implemented/` 记录，检查旧记录是否已补齐指向本新记录的替代链接（并将原本指向 `proposed/` 的链接更新为 `implemented/`），确保双向引用闭合。

9. **汇报收尾**

   向用户报告：已删除的 `.plan.md`、已升格的 ADR、调整的章节、修复的链接，以及后续待办（如提 PR、发版说明等）。若第 8 步更新了仍在 `proposed/` 中的其他 `.plan.md` 的 `Depends on:` / `Constrained by:` 链接，一并说明哪些后续 Plan 由此变为 **Ready**（或因前置移入 `rejected/` 而失效需修订）。保持工作区改动处于未提交状态，由用户决定何时暂存与提交。

## 其他生命周期迁移（仅在用户明确指示时）

### 放弃提案（`proposed/` → `rejected/`）

1. 若该提案对应的独立 `.plan.md` 存在，删除它；若属于多记录联合计划且其他记录仍在推进，仅从计划头部移除此 `ADR:` 行。
2. 按 `.agents/ADR/AGENTS.md` 判断：若属于有保留价值的误区/否决方向，先 `mkdir -p .agents/ADR/rejected/{class}` 并移入 `rejected/{class}/{name}.md`，将 `Status: proposed` 改为 `Status: rejected — <one line why>`，其余正文保持冻结；否则直接删除提案文件。
3. 按主流程第 8 步检索 `{name}.md` 并修复或清理活跃文件的入站链接，汇报变更并保持未提交。

### 归档历史记录（`implemented/` → `archived/`）

1. 确认该记录已完全交付、不再指导未来工作，且不涉及 `.agents/ADR/AGENTS.md` 中需保持活跃的豁免条件。
2. `mkdir -p .agents/ADR/archived/{class}` 后移入 `archived/{class}/{name}.md`。
3. 仅修改头部元数据：将 `Status: implemented` 改为 `Status: archived`，紧随其后新增一行 `Archived: YYYY-MM-DD`，再空一行。**正文一字不改**（保留 `implemented/` 结构且永久冻结）。
4. 按主流程第 8 步检索 `{name}.md` 并更新仍需指向该历史记录的活跃文件链接（跳过其他 `archived/` 文件），汇报变更并保持未提交。

## 退出条件

- **交付升格**：对应 `.plan.md` 已删除；计划所列全部记录均已迁入 `implemented/` 且 `Status: implemented`，不再残留 `## Proposal`、`## Plan`、`## Acceptance criteria`、`## Risks` 标题。
- **放弃或归档**：对应 `.plan.md` 已清理（如适用），记录已迁入 `rejected/` 或 `archived/` 且元数据符合 `.agents/ADR/AGENTS.md`（`archived/` 正文零改动）。
- 除 `archived/` 历史文件外，全仓无因本次迁移失效的入站链接。
- 已向用户完整报告所有变更路径与待跟进项。
