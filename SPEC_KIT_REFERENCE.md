# 本仓库文档索引

本索引面向维护 SpecKitReference 的人，以及按照个人全局规则为新项目执行一次性初始化的 Agent。目标项目完成初始化后，其 Agent 只依据目标项目已提交的 `AGENTS.md`、官方 CLI、原生集成和技能工作；不需要读取本仓库。

## 新项目初始化时

只有在用户同意为尚未 Spec 化的项目启用 Spec Kit 后，初始化 Agent 才读取以下两份文件：

| 文件 | 用途 |
| --- | --- |
| [新项目初始化步骤](docs/PROJECT_INITIALIZATION.md) | 检查 CLI、选择原生集成、初始化项目，并把规则块合并到目标项目。 |
| [目标项目 AGENTS 规则块模板](docs/PROJECT_AGENTS_TEMPLATE.md) | 原样复制到目标项目根目录 `AGENTS.md`；复制后不再依赖本仓库中的模板。 |

目标项目已存在 `.specify/` 时，不走本节，也不因本索引重新初始化。

## 本仓库维护和人工参考

以下中文摘要供本仓库维护者或希望了解官方流程的读者参考。它们不会随初始化复制到目标项目，也不是目标 Agent 的运行时输入。目标 Agent 按项目自己的 `AGENTS.md` 和当前官方 CLI/技能执行；发生差异时，以实际 CLI 帮助、安装的官方技能及官方文档为准。

| 主题 | 文件 | 适用场景 |
| --- | --- | --- |
| Bug Fix | [官方缺陷流程参考](docs/BUGFIX_REFERENCE.md) | 了解官方 Bug Fix 的阶段和产物；目标项目 Agent 不需从 Reference 读取。 |
| Assessment | [官方想法评估参考](docs/ASSESSMENT_REFERENCE.md) | 了解官方 Assessment 的阶段和产物；目标项目 Agent 不需从 Reference 读取。 |
| CLI 与组件更新 | [官方组件更新行为参考](docs/COMPONENT_UPDATE_REFERENCE.md) | 维护或审阅本地政策时核对更新行为；目标项目 Agent 按项目规则与当前 CLI 操作。 |
| 上游变化 | [上游审查规则](docs/UPSTREAM_UPDATE_POLICY.md) | 检查 Spec Kit 上游变化并更新本仓库摘要、影响记录和基线。 |
| 全局规则部署 | [人工部署说明](docs/GLOBAL_POLICY_DEPLOYMENT.md) | 由使用者手动更新个人全局规则。 |

本仓库自身的维护边界和验证要求见根目录 `AGENTS.md`。
