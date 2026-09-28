> 用途：首次为新项目初始化 Spec Kit 时，把下方代码围栏中的完整规则块写入目标项目根目录 `AGENTS.md`。只复制围栏内内容；目标项目提交该副本后，不依赖本模板、Reference 或个人全局规则。

# 目标项目规则块

~~~~markdown
<!-- PROJECT-SPEC-KIT-GOVERNANCE:START -->
# Spec Kit 项目规则

## 项目规则和文件的权威来源

本项目使用官方 Spec Kit CLI、当前 Agent 的官方原生集成及其技能。此规则块与项目提交的 `.specify/**`、`specs/**` 和官方集成文件共同构成本项目的 Spec Kit 工作基线。目标项目 Agent 不需要也不得依赖个人全局规则或中央 Reference。

- `.specify/**` 和 Agent 集成文件由官方 CLI 管理；`specs/**` 中的流程产物由官方技能生成。不要重新初始化已有 `.specify/` 的项目，也不要手工覆盖 CLI 托管文件。
- 细节以本项目当前 CLI 的实际帮助和已安装官方技能为准。若它们与本规则存在差异，先说明受影响的步骤，再按当前工具实际支持的操作处理；不得臆造替代命令或以本地仿制品替代官方能力。

## 每个新会话的入口

只要项目存在 `.specify/`，Agent 必须在首次实质性操作前最多运行一次只读 CLI 版本检查：

~~~bash
specify self check
~~~

- CLI 缺失时，询问用户是否从官方来源安装。用户拒绝时返回 `HANDOFF_TO_AGENT`，不得假称已检查或初始化。
- CLI 报告有更新时，告知用户可用版本和当前版本；只有用户明确批准后才运行 `specify self upgrade`。用户拒绝、离线、超时或无更新后，本会话不重复询问。
- 无论 CLI 是否升级，都用当前 CLI 实际支持的 `help`、`status` 和 `list` 命令检查活动集成及已安装扩展、工作流；不存在新鲜度字段时，以官方更新命令的实际结果为准。
- 对已安装的官方集成和扩展执行强制刷新：集成使用 `specify integration upgrade <key> --force`；扩展使用 `specify extension add <id> --force`，以官方目录版本覆盖现有扩展文件。不要把扩展更新命令的“已是最新”当作文件内容校验。
- 工作流命令不支持 `--force`。为覆盖现有官方工作流并取得可更新的 catalog 来源，先用官方 CLI 移除该工作流，再按官方 catalog ID 重新添加；不得使用本地副本或自建来源替代。
- 本项目已授权覆盖官方管理的集成技能、脚本、扩展和目录工作流。若命令支持 `--force`，必须使用；不支持时使用上述官方移除后重装流程。此授权不适用于本规则块、`specs/**`、业务文件或本地来源组件。每次刷新后重新检查 CLI 帮助和项目状态，记录实际结果。
- 当前任务需要的官方集成或扩展缺失时，先询问用户是否安装。只有当前 Agent 的官方原生集成可用时，才可在获准后运行 `specify integration install <native-key>`；缺少原生集成时停止并报告，不得改用 `generic`。拒绝安装时返回 `HANDOFF_TO_AGENT`。
- Bug Fix 需要而 `bug` 扩展缺失时，询问是否运行 `specify extension add bug`；用户选择 Assessment 且 `assess` 缺失时，询问是否运行 `specify extension add assess`。
- 刷新后重新检查 CLI 帮助和项目状态。离线、超时、失败或组件被跳过时，说明哪些内容无法核实；不得把未检查或被跳过的组件报告为最新。

## 选择工作流程

先按用户要达成的结果选择入口，不因任务发生在代码仓库中就自动启动 Feature SDD：

| 工作目标 | 采用的流程 |
| --- | --- |
| 问答、只读调查、代码审查、常规维护，或不改变预期技术行为的修改 | 不启动 Spec Kit 流程，按用户要求和项目规则处理。 |
| 用户尚未决定一个想法是否值得投入 | 可询问是否使用独立的 Assessment；它不实现代码，也不自动启动 Feature SDD。 |
| 已有行为违反既定预期 | 使用独立的 Bug Fix 流程；不要求先运行 Feature SDD 或 Constitution。 |
| 需要新增或明显改变预期技术能力、用户可观察行为 | 使用 Feature SDD；按下面的影响和风险标准选择短路径或完整路径。 |

若缺陷修复与新增行为可以拆开，分别处理。若不能拆开，先澄清交付目标和行为预期；不得把新增行为当作缺陷修复。

## Feature SDD：两种路径

每个项目在首次开始 Feature SDD 前建立一次 Constitution；它是两种路径共用的项目级前置步骤，不必为每个 Feature 重做。之后每个 Feature 选择以下一条路径：

| 路径 | 适用情况 | 每个 Feature 的步骤 |
| --- | --- | --- |
| 短路径 | 范围较小、需求清楚、风险低，且不改变外部接口、持久化数据格式、安全边界或核心架构。 | `specify → plan → tasks → implement → converge` |
| 完整路径 | 生产级功能，或影响 API、数据格式、架构、安全、隐私，涉及多个组件，或难以回退。 | `specify → clarify → plan → checklist → tasks → analyze → implement → converge` |

风险无法判断时先澄清；仍不确定时采用完整路径。每次只调用一个当前集成提供的官方技能，审阅该阶段结果后再继续。具体技能调用方式以当前 Agent 的原生集成为准。

## Bug Fix：诊断、修复、验证

当已有行为不符合明确的预期时，按 `assess → fix → test` 顺序使用官方 Bug Fix 技能，并在进入下一阶段前审阅当前产物。

- `assess` 记录症状、复现证据、预期行为、诊断和建议修复范围；此阶段不修改源代码。诊断没有证据支持或问题并非缺陷时，不进入 `fix`。
- `fix` 按已审阅的诊断实施修复并记录变更；这是此流程中实施源码修复的阶段。若新证据要求扩大范围，先说明并审阅偏差。
- `test` 重做原始复现并记录验证结果；此阶段不通过修改源代码来掩盖失败。仅测试套件通过、但没有重做原始复现，不足以证明缺陷已修复。

## Assessment：决定是否投入

当用户尚未决定一个想法是否值得投入、且选择了评估流程时，按 `intake → research → define → shape → decide` 顺序使用官方 Assessment 技能，并逐阶段审阅证据和产物。

Assessment 可以用于软件或非软件想法，不要求已有源代码，不修改源代码。`go`、`needs-clarification` 和 `kill` 都是有效结果；`go` 只表示可继续考虑，是否实施仍由用户决定。用户决定实现软件想法后，再把评估结论交给 Feature SDD；如项目尚未建立 Constitution，应在首次 Feature SDD 前建立。

## 共同执行边界

- Feature SDD、Bug Fix、Assessment 是三类不同工作入口；短路径和完整路径是 Feature SDD 内的两种模式。不得把三类入口串成一条强制流程。
- 按官方 CLI 安装需要的官方集成或扩展；每个阶段使用当前集成提供的官方技能。官方能力不可用时，说明缺失内容和受影响步骤，不安装本地替代品。
- 不增加本地自建生命周期、工作流、预设、Bundle、额外 Discovery 阶段、审批台账或任务状态机。
- 不把未运行的 CLI 检查、技能或扩展报告为已完成；操作结果、阶段产物和验证证据须如实汇报。
<!-- PROJECT-SPEC-KIT-GOVERNANCE:END -->
~~~~

# 上游依据

本模板依据已审阅提交 `c00dc0551583428a10a94443c58c6a41e5e0138c` 的 `docs/quickstart.md`、`docs/guides/bugfix.md`、`docs/guides/assessment.md`、`docs/upgrade.md`，以及 `src/specify_cli/integrations/command_upgrade.py`、`src/specify_cli/extensions/command_add.py`、`src/specify_cli/extensions/command_update.py`、`src/specify_cli/extensions/_command_update_discovery.py` 和 `src/specify_cli/workflows/command_update.py` 整理。每次维护本模板时，应按 `docs/UPSTREAM_UPDATE_POLICY.md` 重新核对上游当前内容；这些来源说明不复制进目标项目。
