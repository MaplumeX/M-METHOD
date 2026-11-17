---
name: mm-land
description: 在工作验收通过后收尾归档：删除对应的 plan 文件，并将该 plan 列出的所有 ADR 从 proposed/ 升格移入 implemented/。适用于用户明确表示验收通过（如「验收通过」「做完了」「可以了」「land it」「close it out」），或要求收尾、归档某个 ADR 时。绝不要仅凭你主观判断「代码看起来做完了」就擅自调用。
---

# Land · 验收落盘

「落盘（Landing）」是唯一能把提案变成既成事实的状态迁移。在它运行之前，`proposed/` 里的记录允许有偏差；一旦它运行之后，`implemented/` 里的记录必须与现实完全一致。

## 准入闸门

仅在用户明确表示验收通过（或明确指示放弃/归档某份记录）时才能执行生命周期迁移。测试通过、diff 干净、计划步骤全部跑完，这些都只是验收的**输入条件**，而不是验收本身。如果用户还没有明确说「验收通过 / 可以了」，停下来询问。过早移动记录会让 `implemented/` 撒谎，哪怕事后改回来也无法抹去痕迹——生命周期本身就是历史。

如果用户表示工作未通过验收，不要执行落盘。询问是计划中 `## Verification` 的哪一行未通过；此时应当修订计划，而不是升格记录。

## 执行流程（交付升格：`proposed/` → `implemented/`）

1. 查找计划文件：

   ```bash
   find .agents/ADR/proposed -name '*.plan.md' 2>/dev/null | sort
   ```

   如果存在多个且用户未指定哪一个 → 询问用户，绝不根据时间戳猜测。如果完全没有 plan 文件 → 依然可以落盘，但必须明确说明这一情况，并以用户指定的单份记录作为待处理列表。

2. 读取文件头部所有的 `ADR:` 行。其中列出的所有记录都将随本计划一并交付；第一条是主记录。

3. 针对每条列出的记录，核对它是否真的已经落地：它的 `## Acceptance criteria` 是否已满足，它的决策是否在代码中真实可见。如果其中任何一份记录并未实际落地，停下并给出两条出路——补完剩余工作，或将该 `ADR:` 行从计划中移除、让该记录继续留在 `proposed/` 等待后续交付。绝不要升格只交付了一半的记录：`implemented/` 代表「已交付」，不代表「尝试过」。

4. 检查计划的 `## Verification` 复选框。每一行都必须已勾选，且在旁边记录了实际结果。只要有未勾选的行，就意味着该部分尚未通过验收——报告具体是哪几行并停下。这一节代表的是人的验收，不是你的。

5. 逐条核对 `## Steps`，确认每一步的内联验证确实实际执行过。如果某一步的验证命令从未运行，无论复选框怎么写的，这一步都不算完成。接着检查计划、ADR 记录与实际代码之间是否存在漂移：计划是在当时的代码状态基础上批准的，后续环境可能已经变化。如果某步的前提已不存在，或某份记录的决策与实际交付不再吻合，停下。此时要么修订计划，要么用一份新记录替代旧决策——绝不要带着过时的决策静默升格。

6. 删除计划文件：

   ```bash
   rm .agents/ADR/proposed/{class}/{delivery}.plan.md
   ```

7. 逐一升格移动每份记录（先确保目标分类目录存在）：

   ```bash
   mkdir -p .agents/ADR/implemented/{class}
   mv .agents/ADR/proposed/{class}/{name}.md \
      .agents/ADR/implemented/{class}/{name}.md
   ```

   一次交付可能横跨多个分类（`architecture/`、`feature/`、`design/`、`process/` 等）；每份记录都要从它各自所属的分类目录移出，而不是全按 plan 文件的目录处理。

   随后按照 `.agents/ADR/AGENTS.md` 编辑每份记录：

   - 将 `Status: proposed` 改为 `Status: implemented`
   - 将 `## Proposal` 改为 `## Decision`，改用现在时态描述已交付的现实
   - 将 `## Acceptance criteria` 和 `## Risks` 的内容归并进 `## Consequences`
   - 修正实施过程中发生变化的客观事实——路径、名称、默认值。仅限修正事实；如果核心决策本身变了，停下：那需要起草一份新记录。

8. 修复入站链接与替代反向链接（inbound & supersession links）。因为相对路径编码了生命周期目录，且同目录下使用裸文件名（`{name}.md`）、同处 `proposed/` 跨分类的文件及 `.plan.md` 的 `Constrained by:` 使用 `../{class}/{name}.md`，仅搜索 `proposed/{class}/{name}` 会漏检。对每份被移动的记录按文件名全仓检索：

   ```bash
   grep -rn --exclude-dir=.git --exclude-dir=node_modules "{name}.md" . 2>/dev/null
   ```

   根据每处引用文件所在目录，计算并改写为指向新路径的正确相对链接（同目录用裸文件名，跨目录按相对层级定位）。代码注释中的 `ADR <date>-<slug>` 不含路径，无需改动。绝不要为了修复出站链接而修改 `archived/` 中的历史记录。

   如果本次升格的记录替代了某份旧的 `implemented/` 记录，检查旧记录中是否已添加指向本新记录的替代说明链接（或将原本指向 `proposed/` 的链接更新为 `implemented/`），确保双向交叉引用完整。

9. 向用户汇报：已删除的 plan 文件、已移动的记录、已重写的章节、已修复的链接，以及任何仍待跟进的事项（如提 PR、写发布说明、补充后续记录等）。保持改动处于未提交状态并告知用户；何时暂存与提交由用户决定。

## 其他生命周期迁移（仅在用户明确指示时）

### 放弃提案（`proposed/` → `rejected/`）

1. 若该提案对应的独立 `.plan.md` 存在，删除它；若属于多记录联合 `.plan.md` 且其他记录仍继续推进，仅从该 `.plan.md` 头部移除此 `ADR:` 行。
2. 若属于值得保留否决理由的诱人方向（按 `.agents/ADR/AGENTS.md`），先 `mkdir -p .agents/ADR/rejected/{class}` 并 `mv` 到 `rejected/{class}/{name}.md`，将 `Status: proposed` 改为 `Status: rejected — <one line why>`，其余正文保持冻结；否则直接删除提案文件。
3. 按主流程第 8 步按 `{name}.md` 检索并修复（或清理）入站链接，汇报变更并保持未提交。

### 归档历史记录（`implemented/` → `archived/`）

1. 确认该记录完全已交付、不再指导未来工作且不符合 `.agents/ADR/AGENTS.md` 中需保持活跃的豁免条件。
2. 先 `mkdir -p .agents/ADR/archived/{class}`，再 `mv` 到 `.agents/ADR/archived/{class}/{name}.md`。
3. 严格只改元数据：将 `Status: implemented` 改为 `Status: archived`，紧随其后新增一行 `Archived: YYYY-MM-DD`，再空一行。**正文一字不改**（保留 `implemented/` 骨架且永久冻结）。
4. 按主流程第 8 步检索 `{name}.md` 并修复仍需指向该历史记录的活跃文件入站链接（跳过其他 `archived/` 文件），汇报变更并保持未提交。

## 退出条件

- 执行交付升格时：对应 `.plan.md` 已删除，计划中列出的每份记录均已位于 `implemented/` 且状态为 `Status: implemented`，不再残留 `## Proposal`、`## Plan`、`## Acceptance criteria` 或 `## Risks` 标题。
- 执行放弃提案或归档历史时：对应 `.plan.md` 已清理（如适用），记录已移入 `rejected/` 或 `archived/` 且元数据符合 `.agents/ADR/AGENTS.md`（`archived/` 正文一字未改）。
- 不存在任何因本次迁移而失效的活跃文件入站链接（`archived/` 除外）。
- 已明确向用户报告所有变更细节。
