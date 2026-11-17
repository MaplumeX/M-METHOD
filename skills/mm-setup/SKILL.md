---
name: mm-setup
description: 配置仓库，使编程 agent 在 .agents/ADR/ 下以 ADR 形式记录决策（安装 ADR 规范并在 AGENTS.md 中添加指引）。适用于初始化仓库、用户询问决策/ADR/设计文档应放在哪里（如「决策记在哪」「ADR 放哪」「记一下这个决定」「setup ADR」），或 AGENTS.md 存在但未说明如何记录决策时。
disable-model-invocation: true
---

# 初始化决策记录

每个仓库只需运行一次。它会将 ADR 规范安装到 `.agents/ADR/`，并在根目录 `AGENTS.md` 中添加指向该目录的说明。仅此而已——不创建示例 ADR，也不对项目做任何猜测。

## 为什么需要这个

Agent 会反复争论已经定下来的问题，因为选择背后的推理过程不在任何人的上下文里。代码只展示**选了什么**，从不展示**为什么选**以及**排除了什么**。如果决策没有固定的书面落脚点，每次新会话都会重新推导一遍，并悄然推翻上一次的结论。

`.agents/ADR/` 就是这个落脚点。它与 `.agents/skills/` 并列，随仓库一起流转，不绑定任何单一的 agent 工具。

## 执行流程

1. 查找仓库根目录：

   ```bash
   git rev-parse --show-toplevel
   ```

   如果命令失败，说明当前不在 git 仓库中。在写入任何文件前，先向用户确认目标根目录。

2. 如果根目录存在 `AGENTS.md`，先通读它。记录现有约定——文档目录结构、命名规范、语言习惯。若与 ADR 规范冲突，先询问用户以哪个为准，不要静默覆盖。

   如果缺少 `AGENTS.md` 但存在 `CLAUDE.md`，询问用户是新建 `AGENTS.md`、写入 `CLAUDE.md`，还是两者都写。

3. 创建目录：

   ```bash
   mkdir -p .agents/ADR
   ```

4. 安装规范文件。源文件为当前 skill 目录下的 `references/adr-standard.md`——请基于 skill 所在路径解析，而非项目路径。

   - 目标 `.agents/ADR/AGENTS.md` 不存在 → 将该文件复制过去。
   - 已存在且内容完全一致 → 跳过，报告「已安装」。
   - 已存在但内容不同 → 展示 diff 并询问用户。项目可能有意收紧了规范，此 skill 绝不能擅自将其还原为默认版本。

5. 将指引块写入根目录 `AGENTS.md`，使用 `<!-- BEGIN: decision-records -->` 和 `<!-- END: decision-records -->` 标记包裹：

   ```markdown
   <!-- BEGIN: decision-records -->
   ## Decision records

   Decisions live in `.agents/ADR/`, one file per decision, path-encoded as
   `{proposed|implemented|rejected|archived}/{architecture|feature|bug-fix|design|process}/yyyy-mm-dd-title.md`.
   Read `.agents/ADR/AGENTS.md` before writing or changing one.
   <!-- END: decision-records -->
   ```

   - 标记已存在 → 替换标记之间的全部内容，保留标记本身。
   - 文件存在但没有标记 → 空一行后追加在末尾。
   - 文件不存在 → 创建文件并只写入上述指引块。

   这段指引块特意保持极简：因为每次会话都会加载它，所以只保留位置与入口指针。具体规则放在规范文件里，只有真正需要撰写或修改记录时才会去读取。

6. 向用户报告所有涉及的文件路径，以及对应的操作（新建、追加、替换或跳过）。除非用户明确要求，否则不要编写示例 ADR。

## 退出条件

- `.agents/ADR/AGENTS.md` 已存在且与标准一致，或用户明确选择保留其自定义版本。
- 根目录 `AGENTS.md` 中恰好包含一个 `decision-records` 区块，且起止标记完整。
- `AGENTS.md` 的其他部分未被改动。
