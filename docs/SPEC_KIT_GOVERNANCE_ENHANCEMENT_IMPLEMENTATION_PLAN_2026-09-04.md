# 目标与结论

本方案解决目标项目使用 GitHub Spec Kit 时的三个系统性缺口：需求收集不足、各阶段缺少人工审阅停点、任务无法稳定交给无对话上下文的极小模型执行。

本方案采用“治理规则 + Spec Kit 原生扩展面 + 只读验证器 + 可审计审批证据”的组合，不手工修改上游生成的 `.agents/skills/**`、`.specify/**` 或 `specs/**`，也不在 Reference manager 中实现第二套 specification 生命周期。

本仓库自身不初始化 Spec Kit，不创建 `.specify/` 或 `specs/`。这是用户于 2026-09-04 明确作出的项目级决定。本方案作为 Reference 维护文档存在；目标项目仍按各自已安装的 Spec Kit 状态运行。

方案状态为 `DRAFT_FOR_REVIEW`。它可以指导后续实现，但在用户明确批准边界、文件清单、版本策略和试点项目之前，不授权修改 `GLOBAL_POLICY.md`、portable governance package、manager、schemas、release artifacts、DriversLicense、memoir 或任何目标项目的 Spec Kit artifacts。

# 成功标准

实现完成后必须同时满足以下结果：

1. 当用户表达“按 Spec 规范制定方案”“开始一个 Feature”或同等意图时，Agent 必须先进入需求发现，而不是直接生成 plan 或依靠行业默认值补齐产品决策。
2. specification、clarified specification、plan bundle、task package 和 analyze remediation 均有明确的 `REVIEW_REQUESTED → APPROVED/CHANGES_REQUESTED` 停点；没有对应批准证据时不得进入下一阶段。
3. 每个 implementation task 是一个自包含、可验证、可停止的执行包，单独交给无原对话记录的小模型时，不需要询问实质性需求、架构或验收问题。
4. Agent 自检不能代替用户审阅；上游 requirements checklist 不能冒充人工批准。
5. 所有增强均通过已安装 `specify` CLI、项目上下文规则或只读治理检查实现；Reference manager 不直接写入上游所有权范围。
6. 目标项目在没有中央 Reference、没有个人全局 Policy、离线的情况下，仍可依赖已提交的本地治理包运行。
7. 旧项目升级可审阅、可回滚；未完成迁移时保持旧行为并明确报告，不得半启用新门禁。

# 非目标

本方案不做以下工作：

- 不 fork GitHub Spec Kit，也不复制或维护上游 core command 的私有分支。
- 不直接修改 `.agents/skills/speckit-*/SKILL.md`。
- 不让 Reference manager 生成或改写 `spec.md`、`plan.md`、`tasks.md`。
- 不要求所有微小、只读或低风险修改执行完整 Feature 生命周期。
- 不把文档长度、任务数量或 token 数量当成质量指标。
- 不保证极小模型能完成本身需要高级推理、跨系统架构决策或外部人工权限的任务；这类工作必须在任务分类时路由给更合适的执行者。
- 不在本轮实施 DriversLicense 或 memoir 的业务 Feature，也不重写它们既有历史 Spec。

# 已确认事实与设计约束

## 上游默认能力边界

上游 `specify` 倾向于使用合理默认值，只保留少量高影响澄清；独立 `clarify` 执行结构化歧义扫描，但不是完整需求访谈协议。

上游 bundled `speckit` workflow 1.0.1 只有 specification 和 plan 后的两个人工 gate，随后直接进入 tasks 和 implement。它没有 discovery、clarify loop、task review、analyze、validation 或 convergence。

上游 tasks command 虽要求任务“无需额外上下文即可执行”，其硬性格式主要是 ID、Story、动作和文件路径，没有完整的输入、输出、禁止范围、验收命令、预期结果和停止条件。

workflow `slot` 是可用扩展点，但只有 workflow 预先声明 slot 时才能由 overlay 填充；当前 bundled workflow 没有 slot。因此不能仅靠 overlay 给现有 workflow 补齐完整治理链。

## 本地所有权边界

Reference 可以修改自己的治理源、portable package、manager、schemas、测试、release metadata 和目标项目内的 Reference-owned additions。

`.specify/**`、`specs/**` 和 native Agent-generated files 继续由上游 CLI 和 Agent 执行的上游 Skills 所有。Reference 只能读取它们，或通过经批准的外部 `specify` CLI 操作安装 workflow、preset、extension 或生成 artifacts。

## 本仓库运行边界

SpecKitReference 本身继续采用维护型 `docs/CHANGE_IMPACT.md`、`docs/HISTORY.md`、实施设计和测试矩阵，不初始化 Feature state。这项例外必须只适用于本仓库，不能被 portable Policy 扩散为目标项目跳过 Spec Kit 的通用许可。

# 总体架构

增强分为五层：

```text
用户意图
  → 项目治理入口规则
  → Discovery 与人工审批协议
  → 上游 Spec Kit Skills / 自定义 workflow、extension、preset
  → 只读 readiness validator 与 cold-start review
  → implement / validate / converge
```

各层职责如下：

| 层 | 职责 | 权威产物 |
|---|---|---|
| 项目 Policy | 判断何时必须进入增强流程、定义禁止跳过条件 | `docs/spec-kit/POLICY.md`、context anchor loader |
| Operating Protocol | 定义阶段、状态转换、暂停及恢复规则 | `docs/spec-kit/OPERATING_PROTOCOL.md` |
| Spec Kit-native companion | 使用 upstream workflow/extension/preset 执行 discovery、artifact handoff 和 task template | 由 `specify` 安装和维护的项目状态 |
| Approval evidence | 保存用户批准对象、摘要、hash、时间和取代关系 | `docs/spec-kit/features/<feature-id>/REVIEW_LEDGER.json` |
| Readiness validator | 只读检查 artifact 状态、traceability 和 task package 完整性 | `tools/spec-kit-governance/governance.py audit-feature-readiness` 输出 |

# 强制需求发现协议

## 触发条件

以下任一情况触发 Discovery：

- 用户明确要求创建、设计、规划或实施实质性 Feature；
- 用户说“按 Spec”“按 Spec Kit”“形成方案和计划”；
- 需求会改变公共接口、数据模型、权限、安全、持久化、跨模块行为或发布条件；
- 当前 specification 缺少用户刚批准的新方向；
- 实施过程中发现需求、假设、风险或受影响组件发生变化。

只读调查、解释、极小 typo、纯格式修复和明确低风险的小改动可以跳过，但 Agent 必须说明判定依据。

## Discovery 输出

Discovery 先形成结构化需求台账，再允许运行 upstream `specify`。台账至少覆盖：

- business objective 和不做的后果；
- actors、权限和角色差异；
- primary journeys、alternative journeys、negative journeys；
- inputs、outputs、数据来源和所有权；
- data lifecycle、identity、retention、迁移和删除；
- error、empty、loading、partial failure、retry 和 recovery；
- security、privacy、compliance 和审计；
- performance、scale、availability 和 platform constraints；
- external dependencies、版本、失败模式和降级；
- accessibility、localization 和支持矩阵；
- explicit in-scope、out-of-scope 和 deferred；
- measurable acceptance、release gate 和 evidence requirements。

台账必须将信息分类为：

```text
CONFIRMED_FACT
USER_DECISION
ASSUMPTION_PENDING_APPROVAL
OPEN_QUESTION
OUT_OF_SCOPE
DEFERRED_WITH_OWNER
```

## 提问规则

1. 每轮只问一个逻辑主题，优先最高影响未决项。
2. 可以给出推荐选项，但必须说明影响，不能把推荐自动记为用户决定。
3. 上游 specify 的 3 个问题和 clarify 的 5 个问题只约束各自命令，不构成 Discovery 总问题上限。
4. 多轮提问持续到 exit criteria 满足，或用户明确接受记录在案的假设和风险。
5. 对仓库可以直接查明的事实不得询问用户；先进行只读调查。
6. 产品选择、发布范围、安全例外和数据保留不得仅用“industry default”替代用户决定。

## Discovery exit criteria

只有同时满足以下条件才能生成 specification：

- 无阻塞级 `OPEN_QUESTION`；
- 所有高影响假设已获用户批准或被明确排除；
- 至少一个 primary journey 有完整 Given/When/Then 骨架；
- 范围边界和 non-goals 明确；
- 验收、失败处理和证据来源可定义；
- 用户批准 Discovery snapshot。

# Artifact 人工审批协议

## 审批对象

审批对象分为五类：

| 类型 | 内容 | 允许的下一步 |
|---|---|---|
| `DISCOVERY` | 需求台账、问题答案、假设、范围 | upstream specify |
| `SPECIFICATION` | `spec.md` 及 clarify 后修订 | plan |
| `PLAN_BUNDLE` | `plan.md`、research、data model、contracts、quickstart | checklist/tasks |
| `TASK_PACKAGE` | `tasks.md`、traceability、readiness report、cold-start report | implement |
| `REMEDIATION` | analyze 或实施漂移产生的修订集合 | 修订 artifacts 或恢复 implement |

## 状态机

```text
DRAFT
  → REVIEW_REQUESTED
  → APPROVED
  → SUPERSEDED

REVIEW_REQUESTED
  → CHANGES_REQUESTED
  → DRAFT

APPROVED
  → STALE  （审批对象内容 hash 改变或上游依赖被取代）
```

以下转换被禁止：

- `DRAFT → APPROVED`：必须先形成可展示的 review request；
- `CHANGES_REQUESTED → implement`：必须修订并重新审批；
- hash 改变后继续使用旧批准；
- Agent 根据自己勾选的 requirements checklist 创建用户批准证据；
- 模糊语句在没有明确审批对象时同时批准多个阶段。

## 审批证据格式

新增 project-local sidecar 根目录 `docs/spec-kit/features/<feature-id>/`：

```text
docs/spec-kit/features/<feature-id>/
├── DISCOVERY.md
├── REVIEW_LEDGER.json
├── TASK_READINESS.json
└── COLD_START_VALIDATION.json
```

该目录保存目标项目实例的需求发现和审批证据，中央同步必须逐字节保留，release builder 不得把它当成 portable template 覆盖。`REVIEW_LEDGER.json` 使用 append-only events；当前状态由事件和实时 artifact hashes 推导，不单独维护一份可任意改写的状态字段。

每个 ledger event 至少包含：

```json
{
  "schema_version": 1,
  "feature_id": "003-example",
  "artifact_type": "TASK_PACKAGE",
  "decision": "APPROVED",
  "artifact_paths": ["specs/003-example/tasks.md"],
  "content_sha256": {"specs/003-example/tasks.md": "..."},
  "review_summary": "...",
  "open_risks": [],
  "approved_by": "current-user",
  "approved_at": "RFC3339 timestamp",
  "evidence": "conversation turn or reviewed record identifier",
  "supersedes_event_id": null
}
```

批准记录只证明对应 hash 的 artifact 被批准，不证明实现完成或验证通过。

# Tiny-model task contract

## 单任务必填字段

每个 implementation task 必须包含：

1. `id`：稳定、唯一、可追踪。
2. `objective`：一个可观察结果，不是活动清单。
3. `traceability`：关联 US、FR、AC、contract 或 defect。
4. `context_summary`：执行该任务必须知道的最小业务和技术背景。
5. `preconditions`：依赖任务、现有 symbol、版本和状态。
6. `allowed_files`：可修改的精确文件；新文件必须给出精确目标路径。
7. `read_only_references`：允许读取但不得修改的 artifacts。
8. `forbidden_changes`：禁止修改的模块、接口、依赖或行为。
9. `inputs_outputs`：函数、API、数据、状态或文件输入输出。
10. `invariants_and_edge_cases`：必须保持的不变量和错误边界。
11. `implementation_steps`：顺序明确、无隐藏设计选择的操作要求。
12. `verification`：可运行命令、fixture、人工步骤及预期结果。
13. `completion_evidence`：完成时必须提交的测试、diff 或记录。
14. `stop_conditions`：发现哪些情况必须停止并上报，不得自行扩大范围。
15. `handoff`：下一任务可依赖的具体结果。

## 原子度规则

满足任一条件必须拆分：

- 有两个以上可以独立验收的结果；
- 同时修改契约生产者和多个消费者；
- 同一任务包含设计、实现、迁移、删除和发布中的两个以上阶段；
- 任务横跨两个以上高耦合模块且没有先行 contract task；
- 描述中存在多个独立的“并且、同时、以及、and”，且每部分有独立失败模式；
- 无法写出一个确定的 verification result；
- 执行者仍需选择核心架构、产品行为或安全策略。

不采用单纯的“最多一个文件”限制。一个原子变化可能需要生产代码与对应测试两个文件；判断标准是单一可验证结果和无隐藏决策。

## 推荐表达方式

保留 upstream `tasks.md` 的 checkbox、ID、Story 和 file path 兼容格式，并在每条 task 下增加结构化 detail block。这样 upstream analyze/implement 仍能识别 task，同时 validator 可以读取必填字段。

若 upstream preset 能稳定解析并维护该格式，则通过经过批准的 preset 安装；否则先由项目治理要求 Agent 在运行 upstream tasks 时传入增强参数，再用只读 validator 阻止不合格任务进入 implement。不得手改生成的 tasks skill。

# 冷启动可执行性验证

## 验证模型

在 `TASK_PACKAGE` 审批前，选择至少以下样本：

- 一个数据或 domain task；
- 一个 UI/API integration task；
- 一个 migration、security 或 failure-handling task；若 Feature 不包含该类别，则选择最高风险任务。

独立 reviewer 只获得：

- 单个 task detail block；
- task 明确列出的 read-only references；
- 仓库只读访问；
- 不提供原始对话和生成 tasks 的 Agent 工作记忆。

reviewer 必须输出：

```text
EXECUTABLE
NEEDS_CONTEXT
HIDDEN_DECISION
CONFLICT
UNVERIFIABLE
```

任何 `NEEDS_CONTEXT`、`HIDDEN_DECISION`、`CONFLICT` 或 `UNVERIFIABLE` 都会使 task package 返回 `CHANGES_REQUESTED`。

## 自动化与人工边界

validator 可以机械检查字段、路径、traceability、命令存在性、重复 ID、依赖环和 hash；不能宣称理解业务语义。冷启动 reviewer 负责判断隐藏决策和语义完整性，用户负责最终批准。

# Spec Kit 原生编排设计

## 推荐组件

实现一个 Reference 维护、由 upstream CLI 安装的 companion bundle，包含：

- `discovery` extension：提供需求台账和退出条件；
- task-detail preset：增强 tasks template，不替换 core lifecycle；
- `governed-sdd` workflow：声明完整阶段和人工 gates；
- workflow slots：为项目特有 security、design、localization 或 release gates 提供已声明扩展点；
- hook/validator adapter：在 tasks review 和 implement 前运行只读 readiness audit。

目标工作流：

```text
discovery
→ review-discovery
→ specify
→ clarify-loop
→ review-spec
→ plan
→ review-plan-bundle
→ checklist
→ tasks
→ audit-task-readiness
→ cold-start-review
→ review-task-package
→ analyze
→ remediation-gate-if-needed
→ implement
→ validate
→ converge
→ completion-review
```

## 定制边界

- 使用新的 workflow ID，例如 `governed-sdd`，不覆盖 upstream bundled `speckit`。
- 使用 upstream `specify workflow add`、`preset add`、`extension add` 安装；不直接写 `.specify/**`。
- 所有 external CLI mutation 必须出现在 manager 生成的精确 operation plan 中，并列出允许路径和恢复步骤。
- bundled workflow 保留可用，项目 Policy 决定何种任务必须使用 governed workflow。
- companion bundle 不是第二生命周期引擎；它仅用 upstream workflow/extension/preset primitives 编排既有 Spec Kit commands 和本地治理 gates。
- 若当前 CLI 不支持某能力，返回 `COMPANION_CAPABILITY_UNAVAILABLE`，不得静默退回弱流程。

# 配置与 schema 设计

## PROJECT_CONFIG v2

建议将 governance package 和 project-config schema 升为 major version 2，避免将新硬门禁悄悄注入现有 v1 项目。

新增顶级对象：

```json
{
  "workflow_governance": {
    "mode": "governed-sdd-required",
    "discovery": "required-for-substantive",
    "artifact_reviews": [
      "DISCOVERY",
      "SPECIFICATION",
      "PLAN_BUNDLE",
      "TASK_PACKAGE",
      "REMEDIATION"
    ],
    "approval_evidence": "committed-project-local",
    "tiny_model_tasks": "required",
    "cold_start_review": {
      "required": true,
      "minimum_samples": 3
    }
  }
}
```

`quality_gates.clarify` 和 `checklist` 在 governed mode 下必须为 `required`。`analyze`、`validate`、`converge` 继续为 `required`。

## 新 schemas

新增：

- `governance/schemas/artifact-review.schema.json`；
- `governance/schemas/task-readiness-report.schema.json`；
- `governance/schemas/cold-start-review.schema.json`；
- `governance/schemas/workflow-governance.schema.json`，或作为 project-config schema 的 `$defs`；
- v1 → v2 migration record schema。

所有 schemas 使用 `additionalProperties: false`，明确版本、枚举、hash 格式、RFC3339 timestamp、项目相对安全路径和 evidence 字段。

# Manager 变更

## 新的只读命令

在 `governance/manager/speckit_governance.py` 增加：

- `audit-feature-readiness --feature-dir <project-relative-path>`；
- `check-artifact-approval --feature-dir ... --artifact-type ...`；
- `verify-task-package --feature-dir ...`；
- `check-companion-status`。

这些命令只读 `.specify/**` 和 `specs/**`，不得修改。

## 新的计划操作

增加经批准的 Reference-owned/external operations：

- `plan-upgrade-governance-v2`；
- `plan-install-governed-workflow`；
- `plan-record-artifact-review`；
- `plan-remove-governed-workflow`；
- `plan-rollback-governance-v2`。

`plan-record-artifact-review` 只能向 `docs/spec-kit/features/<feature-id>/REVIEW_LEDGER.json` 追加 event，必须绑定当前 artifact hashes、ledger old hash、plan TTL、Git/config snapshot 和用户证据。任何值不匹配都拒绝写入。

安装 companion 的 plan 只调用 upstream CLI，必须先解析当前 CLI help、integration status、workflow/preset/extension status，并记录确切 argv、目标路径、备份和回滚命令。

## Manager 禁止事项

manager 仍必须拒绝：

- 直接 mutation `.specify/**`、`specs/**`、`.agents/skills/**`；
- 伪造或自动生成 `approved_by=current-user`；
- 将 Agent checklist pass 转换为用户批准；
- 未经审批修改项目默认 integration；
- 使用 `--force` 安装 companion；
- 因 companion 不可用而将 governed mode 标记为 READY。

# 文件级实施清单

## 中央 Policy 与 Reference

| 文件 | 计划变更 |
|---|---|
| `GLOBAL_POLICY.md` | 增加 substantive discovery、artifact approval、tiny-model readiness 和本仓库明确例外的边界；不包含具体 Agent 命令 |
| `SPEC_KIT_REFERENCE.md` | 记录 governed workflow、companion layer、审批证据、validator、CLI/version discovery |
| `AGENTS.md` | 只增加本仓库“不初始化 Spec Kit”的显式维护规则；不得扩散到 portable package |
| `docs/CHANGE_IMPACT.md` | 记录本地 `POLICY` 决策、批准证据和发布影响 |
| `docs/HISTORY.md` | 记录 implementation、pilot 和 rollout 结果 |

## Portable governance package

| 文件 | 计划变更 |
|---|---|
| `governance/project/POLICY.md` | 增加 Discovery、审批门禁和禁止跳过规则 |
| `governance/project/OPERATING_PROTOCOL.md` | 加入完整阶段状态机、暂停/恢复、hash 失效规则 |
| `governance/project/START_HERE.md` | 增加自然语言触发映射和最短操作入口 |
| `governance/project/REFERENCE.md` | 说明 companion 与 core CLI/skills 的分层和版本检查 |
| `governance/project/PROJECT_CONFIG.default.json` | 新增 `workflow_governance` v2 defaults |
| `governance/project/AGENT_ONBOARDING.md` | 验证 companion status 和 fresh-session governed workflow 可见性 |
| `governance/project/LOCAL_OVERRIDES.template.md` | 允许项目加严 sample count 或 review 类型，但不允许降低 required gates |

## Manager、schemas 和 release

| 文件/目录 | 计划变更 |
|---|---|
| `governance/manager/speckit_governance.py` | 新 audit、approval 和 companion plan/apply operations |
| `governance/schemas/project-config.schema.json` | schema v2 和 workflow governance contract |
| `governance/schemas/operation-plan.schema.json` | 新 operations、external CLI scope、review evidence mutations |
| `governance/schemas/governance-manifest.schema.json` | companion/version 以及 `docs/spec-kit/features/**` project-local preserved subtree metadata |
| `governance/schemas/adapters.schema.json` | workflow/preset/extension capability status |
| `governance/capability-baseline.json` | 新 capabilities 和 approved replacement records |
| `governance/release/COMPATIBILITY.md` | v1/v2、CLI range、upgrade/rollback compatibility |
| `governance/release/CHANGELOG.md` | 2.0.0 breaking governance semantics |
| `scripts/build_governance_release.py` | 打包 companion source、schemas、source metadata |
| `scripts/validate_governance_release.py` | 验证 companion artifact hashes 和 deterministic build |

## Spec Kit-native companion source

建议新增中央源目录：

```text
governance/spec-kit-native/
├── bundle.yml
├── extensions/discovery/
├── presets/tiny-model-tasks/
├── workflows/governed-sdd/
└── validators/
```

该目录是可安装源，不是目标项目的 `.specify/`。目标项目内容必须由 upstream CLI 安装并由 status/manifest 证明。

# 测试计划

## Policy 与触发测试

- “按 Spec 制定方案”必须进入 Discovery；
- “解释当前实现”保持只读且不触发完整生命周期；
- Agent 有合理默认值时仍不能跳过产品/安全决策；
- 本仓库例外不允许目标项目跳过 Spec Kit；
- conversation approval 只批准明确 artifact type/hash。

## 审批状态机测试

- 缺少 review record 时 plan/tasks/implement 被阻断；
- `CHANGES_REQUESTED` 不可进入下一阶段；
- artifact hash 改变使 approval 变为 stale；
- superseded approval 不可复用；
- Agent 自签 approval 被拒绝；
- review path traversal、symlink escape 和绝对路径被拒绝；
- central upgrade 保留 target-local reviews 字节不变。

## Task contract 测试

- 每个必填字段缺失均产生稳定错误码；
- duplicate IDs、dependency cycles、unknown traceability 被拒绝；
- 目录级模糊路径、不可验证命令和空 expected result 被拒绝；
- 多结果 task 产生 split warning；
- producer/consumer 跨模块任务要求 contract-first decomposition；
- upstream checkbox 格式仍可被 analyze/implement 使用；
- validator 只读，运行前后 artifacts hash 完全一致。

## Companion workflow 测试

- 每个 gate 在 non-interactive 环境进入 `PAUSED`，不能自动 approve；
- reject 后回到正确修订阶段；
- clarify loop 有退出条件，不能无限循环；
- tasks audit failure 不得到达 implement；
- unfilled project slots 安全 skip；
- filled slot 保持后续步骤所需 outputs；
- CLI/integration/preset/extension 缺失产生显式 blocker；
- workflow removal/rollback 恢复原状态但不删除 feature artifacts。

## Ownership 与回归测试

- manager 对 `.specify/**`、`specs/**` 和 native Skills 的直接写入继续失败；
- external upstream CLI mutation 有精确 allowlist 和 diff inventory；
- v1 项目未批准升级时行为不变；
- v2 upgrade 不改业务文件和 feature artifacts；
- rollback 保留 reviews、user work 和既有 Spec Kit artifacts；
- 现有 89 项测试继续通过；
- release ZIP deterministic、hash 和 schema validation 通过。

# 分阶段实施

## Phase 0：决策冻结

交付物：经用户批准的本方案修订版。

必须明确批准：

- 使用 governance package 2.0.0 和 project-config schema v2；
- 引入 Spec Kit-native companion bundle；
- 新增 committed project-local review evidence；
- DriversLicense 和 memoir 作为先后两个 pilot；
- 本仓库永久不初始化 Spec Kit 的局部例外。

退出条件：所有 boundary-changing 决策都有明确用户批准；没有待决的存储路径、版本或 rollout 选择。

## Phase 1：Policy 与数据合同

先只实现文档、schemas、capability baseline 和测试，不实现 workflow 或 manager mutation。

退出条件：Policy/Reference/portable docs 一致；所有新 schemas 有正反例；测试证明 approval 和 task contracts 无矛盾。

## Phase 2：只读 validator

实现 readiness audit、approval hash check 和 task package validator。使用 fixture feature directories 测试，不触碰真实项目。

退出条件：validator 对合格 fixture 通过、对每类缺陷返回稳定错误码、运行前后 hash 不变。

## Phase 3：Companion bundle

实现 discovery extension、task preset 和 governed workflow；使用临时初始化项目和 Codex native integration 进行隔离 rehearsal。

退出条件：完整 happy path、reject/revise path、non-interactive pause、rollback 和 upstream ownership 测试通过。

## Phase 4：兼容 Bridge release

先发布兼容的 `1.3.x` bridge，不启用 strict workflow。Bridge 必须：

- 将 manager 的 governance upgrade 文件清单从硬编码迁移为 manifest/hash 约束的清单；
- 同时理解 v1 和 v2 manifest/config，但只写 v1；
- 增加 major migration planner、完整 backup inventory 和 rollback journal；
- 声明并保护 `docs/spec-kit/features/**` project-local subtree；
- 让旧目标项目能够生成一个原子的 v2 migration plan；
- 保持原有 Feature 行为不变。

退出条件：现有 v1 项目升级到 bridge 后字节级保持业务文件、`.specify/**`、`specs/**`、native Skills 和 project-local evidence；bridge rollback 通过。

## Phase 5：Manager v2、companion install 与 release 2.0.0

实现 v1 → v2 upgrade、companion install/remove、review record 和 rollback operations。构建 portable/extension artifacts，但不部署到目标项目。

退出条件：所有 operation plans 可复现、hash-bound、可回滚；release validation 通过；无未映射 capability。

不允许用 v1 manager 直接覆盖 v2 manager/config。目标项目必须先进入 bridge，再由 bridge 生成单一原子 v2 migration plan。若无法提供 bridge，必须显式进入 `MIGRATION_REQUIRED`，不能出现半迁移状态。

## Phase 6：DriversLicense pilot

先生成只读现状报告和精确 upgrade plan。用户批准后升级 governance layer 和 companion，不重写历史 Specs。

选择一个新的、中等范围、非发布阻塞 Feature 试跑完整 governed workflow。抽样至少三个 task 做 cold-start review。

退出条件：用户批准记录完整；没有阶段被自动跳过；任务无需原对话即可执行；现有业务测试不回归；rollback rehearsal 通过。

## Phase 7：memoir pilot

吸收 DriversLicense 发现后再单独生成计划。memoir 的 Apple platform、隐私、PCC、三语和 accessibility 风险决定其 review/checklist 不得降级。

退出条件同 DriversLicense，并额外验证平台支持矩阵、隐私和人工证据 task 可以被正确分类为不能交给极小模型自动完成。

## Phase 8：推广与收敛

完成两个 pilot 后才更新默认 release 指针和迁移文档。记录失败案例、task split 统计、review 返工来源和 cold-start 追问率。

退出条件：两个 pilot 均通过、没有未解决 blocker、release index 和 rollback 文档完成、中央与目标项目 governance manifests 一致。

# Rollout 指标

不使用文档长度评价质量。收集以下指标：

- Discovery 后进入 specification 时的阻塞未决项数量，应为 0；
- 各 artifact 首轮批准率和 changes requested 原因；
- task package 中 validator errors 数量；
- cold-start reviewer 的实质性追问率，目标为 0；
- 实施中因隐藏需求或隐藏架构决策返回 artifacts 的次数；
- task 平均独立验收结果数，目标为 1；
- stale approval 被正确识别的次数；
- governed workflow 被绕过或错误触发的次数；
- rollback 和离线运行成功率。

# 风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| 流程过重 | 小改动效率下降 | 保留明确 low-risk exemption，并测试触发边界 |
| 用户审批疲劳 | 审批流于形式 | 按 artifact bundle 审批，不逐文件机械审批；突出差异、风险和待决项 |
| task 文档膨胀 | 阅读成本增加 | 结构化 detail blocks、引用稳定 contracts、避免重复背景 |
| 小模型能力仍不足 | 执行失败 | readiness 只证明自包含，不证明能力匹配；增加 task complexity routing |
| approval evidence 泄漏敏感信息 | 安全风险 | 只记录摘要/hash/引用，不保存 token、全文或隐私数据 |
| central upgrade 覆盖项目审批 | 审计丢失 | `features/**` 明确为 project-local preserved subtree，并做字节级回归测试 |
| companion 与 CLI 版本漂移 | workflow 失效 | manifest 记录 tested range；安装前 runtime discovery；不兼容时 fail closed |
| preset 与其他项目 preset 冲突 | 模板解析不确定 | 显式 priority、resolve evidence、multi-install audit、可回滚安装 |
| workflow gate 在非交互环境卡住 | 自动化中断 | 将 `PAUSED` 视为正确状态；由明确 resume approval 恢复 |
| 误成第二生命周期 | ownership 混乱 | 只编排 upstream commands，不由 manager 生成 feature artifacts |

# 回滚策略

回滚分三层：

1. Companion rollback：通过 upstream CLI remove/disable governed workflow、preset 和 extension，保留 feature artifacts 和 review evidence。
2. Governance rollback：通过 bridge 恢复 v1 portable Policy/config/manager，但保留 v2 feature sidecar 为只读归档，不删除用户证据。
3. Feature rollback：不由 Reference manager执行；由目标项目既有 Spec Kit artifacts、Git 和业务迁移策略处理。

任一回滚失败返回 `RECOVERY_REQUIRED`。不得通过删除 `.specify/`、`specs/`、native Skills 或 reviews 伪造恢复成功。

# 验证命令

实现阶段至少运行：

```bash
python3 -m unittest discover -s tests -p 'test*.py'
python3 -m compileall -q governance scripts tests
git diff --check
python3 scripts/check_upstream.py --no-fetch
```

Release 阶段还要在临时目录构建并验证 2.0.0 artifacts：

```bash
python3 scripts/build_governance_release.py \
  --version 2.0.0 \
  --output-dir <temporary-release-directory>

python3 scripts/validate_governance_release.py \
  <temporary-release-directory>/latest.json
```

目标项目 pilot 还必须运行：

```text
specify version
specify integration status --json
specify workflow resolve governed-sdd
specify preset resolve tasks-template
specify extension list
```

具体命令以安装时 CLI help 为准，不在实现中硬编码可能漂移的参数。

# 实施完成定义

只有以下条件全部满足才能宣布该治理增强完成：

- 用户批准最终 Policy boundary 和 2.0.0 release；
- 中央文档、portable package、schemas、manager、companion 和 tests 同步；
- capability baseline 中每个新增、替换能力都有 disposition、证据和回归测试；
- Reference manager 仍无法直接修改 upstream-owned artifacts；
- release build 和 validation 通过；
- DriversLicense 与 memoir 两个 pilot 均通过各自人工审批；
- cold-start reviewer 对抽样任务没有实质性追问；
- 所有已知失败和 blocker 已解决或由用户明确移出范围；
- upstream baseline、installed CLI、target integration 和 generated Skills 的版本状态分别记录，不相互推断；
- rollout、rollback、离线运行和审计证据完整。

# 待用户评审的关键决策

实施前需要用户逐项确认：

1. 是否接受 governance package 与 project-config 升级为 2.0.0/v2，而不是向 v1 静默加入强制行为。
2. 是否授权在中央仓库新增 `governance/spec-kit-native/` companion source，并在目标项目中通过 upstream CLI 安装 workflow、preset 和 extension。
3. 是否接受 `docs/spec-kit/features/**` 作为提交到目标项目仓库、由中央同步永久保留的 Discovery 与审批证据路径。
4. 是否接受所有实质性 Feature 强制 Discovery、SPECIFICATION、PLAN_BUNDLE、TASK_PACKAGE 和 REMEDIATION 审批。
5. 是否同意先 DriversLicense、后 memoir 的 pilot 顺序。
6. 是否同意本仓库“不初始化 Spec Kit”作为仅限 SpecKitReference 的永久项目规则写入 `AGENTS.md`。
