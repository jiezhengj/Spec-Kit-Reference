# 初始化项目

本页说明如何逐步使用官方 Spec Kit 技能开发功能。Agent 每次只运行一个技能，检查并审阅输出后再继续。不要把技能名称当作终端命令。

在项目目录安装官方 CLI，并明确使用当前 Agent 的原生集成。非交互初始化明确指定 Python 脚本：

~~~bash
uv tool install specify-cli
specify init <project-name> --integration <native-agent-key> --script py --non-interactive
~~~

如果运行环境是交互式，省略 --non-interactive；其余步骤遵循根目录 GLOBAL_POLICY.md。

若目标项目已经存在 `.specify/`，恢复现有状态，不重新运行 `specify init`；只在缺少受管规则块或其内容需要按当前政策模板更新时精准更新该块，不根据版本号判断。

CLI 初始化完成后，将本地 Spec Kit 规则块写入 `AGENTS.md`。若已有唯一且完整的 `PROJECT-SPEC-KIT-GOVERNANCE` 标记块，只替换该块；若没有标记块，在文件末尾追加。保留标记外全部内容。若存在边界明确的旧 Reference 更新检查块，精准删除该块；边界缺失或标记重复时停止，不覆盖文件或追加第二块。提交 `AGENTS.md`、官方 CLI 生成且需团队共享的集成文件、`.specify/` 与 `specs/`，使项目不依赖其他电脑上的全局 POLICY 或 Reference。

目标项目规则块还负责每个新 Agent 会话的 CLI 与已安装组件更新检查；见 [更新操作](CLI_UPDATES.md)。中央 Reference 不更新或覆盖已经 Spec 化项目中的规则块。

# 选择流程

每个项目首次进入功能 SDD 时建立 Constitution；后续功能复用它。

以下技能名采用官方 Copilot 示例。其他 Agent 使用当前原生集成提供的等价技能名称和调用方式，不要将示例强行转成终端命令。

小型功能采用短流程：

~~~text
/speckit-constitution（项目仅首次执行）
→ /speckit-specify → /speckit-plan → /speckit-tasks
→ /speckit-implement → /speckit-converge
~~~

生产级功能采用完整流程：

~~~text
/speckit-constitution（项目仅首次执行）
→ /speckit-specify → /speckit-clarify → /speckit-plan
→ /speckit-checklist → /speckit-tasks → /speckit-analyze
→ /speckit-implement → /speckit-converge
~~~

短流程和完整流程都是官方 Quickstart 路径。不要在其间插入自建 Discovery、审批台账或就绪检查。

# 各阶段做什么

## Constitution

只在项目首次采用功能 SDD 时建立项目原则。原则应来自用户已确认的要求或项目事实，后续计划和分析会以此为依据。

## Specify

描述要构建什么、为什么需要以及用户可观察到的结果。先说明问题和需求，不要先把技术栈当作需求。

## Clarify

在完整流程中使用。针对规格中未说明或容易产生不同理解的内容提问，并把答案写回规格；在规划前解决影响实现的歧义。

## Plan

根据已审阅的规格记录技术栈、架构和实现方案。实现细节在此阶段确定，不应倒灌到 specify 的问题描述中。

## Checklist

在完整流程中使用。检查规格是否完整、清晰、一致。清单检查的是需求质量；勾选项不代表实现已经完成。

## Tasks

把规格和计划拆成有依赖顺序、可以执行的任务。

## Analyze

在完整流程中使用。只读检查 spec.md、plan.md 和 tasks.md 之间的冲突、遗漏和歧义。发现问题时先修改对应源文件，再重新 analyze。

## Implement

按照 tasks.md 的依赖顺序执行。官方技能会检查自定义 checklist 的勾选状态；有未勾选项时会在继续前询问。大型功能可以按阶段分批实现。

## Converge

对照规格、计划、任务和当前代码检查是否还有差距。如果产生新任务，继续 implement 并再次 converge，直到报告 Converged。

# 活跃功能目录

Spec Kit 根据 .specify/feature.json 记录的目录识别当前功能；可由 SPECIFY_FEATURE_DIRECTORY 环境变量覆盖。Git 当前分支本身不会切换 Spec Kit 的活跃功能。

# 上游依据

本页根据已审阅提交 c00dc0551583428a10a94443c58c6a41e5e0138c 的 docs/quickstart.md 整理，校订日期为 2026-09-28。
