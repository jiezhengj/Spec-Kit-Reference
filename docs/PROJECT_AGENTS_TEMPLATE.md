> 用途：首次为新项目初始化 Spec Kit 时，把下方围栏内的规则块写入目标项目根目录 `AGENTS.md`：只写入围栏内内容，只把唯一占位符 `{{SPEC_KIT_DOCUMENT_LANGUAGE}}` 替换为初始化时用户明确选择的语言名称；更新助手由初始化步骤另行复制。写入后目标项目不依赖本模板、Reference 或全局规则。

# 目标项目规则块

~~~~markdown
<!-- PROJECT-SPEC-KIT-GOVERNANCE:START -->

# Spec Kit 项目规则

## 权威来源

本项目以官方 Spec Kit CLI、项目内 `.agents/skills` 技能和 `.specify/**` 状态为准；本规则块与 `.specify/**`、`specs/**`、`.agents/skills/**` 共同构成工作基线，不得依赖全局规则或中央 Reference。

- `.specify/**` 和 `.agents/skills/**` 由官方 CLI 管理，`specs/**` 由官方技能生成：不重新初始化已有 `.specify/` 的项目，不手工覆盖 CLI 托管文件。
- 技能统一位于 `.agents/skills/speckit-*/SKILL.md`，调用写作 `/speckit-<name>`。技能路径与 Harness 无关：任何 Agent 在同一项目内都读同一份技能，不按当前 Harness 换成 `.github/skills`、`.dsh/skills` 等其他目录，也不因换 Harness 重新初始化。
- 细节以当前 CLI 帮助和已安装技能为准；与本规则冲突时先说明受影响步骤，再按工具实际支持的方式处理，不臆造命令，不以本地仿制品替代官方能力。

## 文档语言

流程文档语言：`{{SPEC_KIT_DOCUMENT_LANGUAGE}}`。Constitution、Feature SDD、Bug Fix 和 Assessment 产生的新文档或实质改写都用该语言，不得从本机地区、集成默认值或英文示例推断或切换。

命令、路径、代码标识符、产品名和官方术语保留原文；用户在单项任务中指定其他语言时按该指示处理；用户更改默认语言时更新本字段。

## 每会话入口

项目存在 `.specify/` 时，在首次实质性操作前先读 `.agent-state/spec_kit_component_update_cache.json` 的 `last_full_check`：

- `status` 为 `success` 且 `checked_at_utc` 距今不足 7×24 小时：不运行助手，直接开始任务。
- 其余情况（缺失、过期、时间在未来、无法解析或状态非 `success`）：运行 `.agent-support/spec_kit_component_updater.py`，Windows 用 `python`，macOS/Linux 用 `python3`。

助手只在整轮无失败或未知状态时写入成功时间；发现 CLI 更新但待用户批准也算完成，本次说明候选版本，用户完成升级后立即再运行一次以核对新 CLI 的组件。组件识别、来源校验、失败处理和 CLI 交互由助手负责，Agent 只按报告处理需用户决定的事项。

- 用户要求立即检查时加 `--recheck`：重查远端版本，不强制覆盖文件。
- 助手无法启动或非零退出时说明原因；找不到 `specify` 时询问是否从官方来源安装，拒绝则返回 `HANDOFF_TO_AGENT`；Python 低于 3.10 或助手缺失时说明检查未完成，不假称已检查。

## 任务路由

按用户要达成的结果选择入口，不因任务在代码仓库就自动启动 Feature SDD：

| 工作目标 | 流程 |
| --- | --- |
| 问答、只读调查、代码审查、常规维护，或不改变预期行为的修改 | 不启动 Spec Kit 流程，按用户要求与项目规则处理 |
| 尚未决定想法是否值得投入 | 可询问是否用 Assessment；不实现代码，不自动启动 SDD |
| 已有行为违反既定预期 | 用 Bug Fix，不要求先跑 SDD 或 Constitution |
| 新增或明显改变预期技术能力、用户可观察行为 | 用 Feature SDD，按影响与风险选短路径或完整路径 |

缺陷修复与新增行为可拆分时分别处理；不可拆分时先澄清交付目标和行为预期，不得把新增行为当缺陷修复。

## Feature SDD

每个项目在首次 Feature SDD 前建立一次 Constitution，两种路径共用，不必每个 Feature 重做。之后每个 Feature 选一条：

| 路径 | 适用 | 步骤 |
| --- | --- | --- |
| 短路径 | 范围小、需求清楚、风险低，且不改外部接口、持久化数据格式、安全边界或核心架构 | `specify → plan → tasks → implement → converge` |
| 完整路径 | 生产级功能，或影响 API、数据格式、架构、安全、隐私，涉及多组件或难以回退 | `specify → clarify → plan → checklist → tasks → analyze → implement → converge` |

风险无法判断时先澄清，仍不确定就用完整路径。每次只调用一个官方技能，审阅该阶段结果再继续；调用方式为 `/speckit-<name>`。

## Bug Fix

已有行为不符合明确预期时，按 `assess → fix → test` 使用官方 Bug Fix 技能，进入下一阶段前审阅产物：

- `assess`：记录症状、复现、预期、诊断和建议范围，不改源码；证据不足或并非缺陷时不进入 `fix`。
- `fix`：按已审阅诊断修复并记录变更；唯一修改源码的阶段，范围扩大时先说明并审阅。
- `test`：重做原始复现并记录结果，不用改源码掩盖失败；只跑测试套件不算已验证。

## Assessment

用户尚未决定想法是否值得投入、且选择评估时，按 `intake → research → define → shape → decide` 使用官方 Assessment 技能，逐阶段审阅证据和产物。适用于软件和非软件想法，不要求已有代码，不修改源代码。

`go`、`needs-clarification`、`kill` 都是有效结果；`go` 只表示可继续考虑，是否实施由用户决定。用户决定实现软件想法后交给 Feature SDD；项目还没有 Constitution 的先建立。

## 执行边界

- 三个入口相互独立；短路径和完整路径只是 Feature SDD 内的两种模式，不串成一条强制流程。
- 缺少当前任务需要的官方扩展时先询问是否安装（Bug Fix 的 `bug`、Assessment 的 `assess` 用 `specify extension add`）；扩展装在 `.specify/` 内，与 Harness 无关。官方能力不可用时说明缺什么、影响哪些步骤，不安装本地替代品，也不为换 Harness 追加第二套集成。
- 官方目录收录工作流不代表已审计其 shell 内容：首次运行或更新后首次运行前，检查 `.specify/workflows/<id>/workflow.yml` 中 shell 步骤的 `run` 字段。
- 不增加本地自建生命周期、工作流、预设、Bundle、额外 Discovery 阶段、审批台账或任务状态机；未运行的 CLI 检查、技能或扩展不得报告为已完成，结果与证据须如实汇报。
<!-- PROJECT-SPEC-KIT-GOVERNANCE:END -->
~~~~

# 上游依据

本模板按官方 CLI、官方技能和官方流程说明整理；最近一次核对使用 `specify` 1.4.2（2026-11-18），核对了 `specify init` 的 `generic` 集成与 `--integration-options` 行为、`speckit` 工作流元数据和官方技能集（含 `converge`）。维护本模板时按[上游依赖兼容性规则](UPSTREAM_UPDATE_POLICY.md)核对当前 CLI 与官方文档；这些来源说明不复制进目标项目。
