# 数据契约

`governance/` 是项目治理包的中央可移植源。所有 JSON 文件使用 UTF-8、LF 和 JSON Schema Draft 2020-12。

## 固定文件

- `project/PROJECT_CONFIG.default.json` 是新项目提交的 `docs/spec-kit/PROJECT_CONFIG.json` 唯一初始模板。
- `capability-baseline.json` 是实施前能力守恒清单；它不是运行时配置，不能被项目安装器覆盖。
- `schemas/` 定义治理 manifest、项目配置、adapter registry、解析结果、operation plan 和能力基线的 V1 契约。

中央仓库还保留详细实施契约和验收材料：

- `docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md`：本次实施的完整架构、状态、命令和完成定义快照。
- `docs/PROJECT_GOVERNANCE_MIGRATION.md`：升级、回滚和项目迁移规则。
- `docs/PROJECT_GOVERNANCE_OPERATIONS.md`：面向实施 Agent 的运行手册。
- `docs/PROJECT_GOVERNANCE_SECURITY.md`：路径、外部 CLI、日志和恢复安全边界。
- `docs/PROJECT_GOVERNANCE_TEST_MATRIX.md`：release-blocking 测试矩阵。

这些文档属于中央治理仓库的实施与审查层，不会复制进业务项目治理包。带日期的实施快照用于本次 rollout 的审计，不是长期运行时依赖；业务项目只携带 `docs/spec-kit/` 中的可移植运行时文件。

## 校验顺序

1. 先校验 `PROJECT_CONFIG.default.json` 与 `project-config.schema.json`。
2. 再校验 `capability-baseline.json` 与 `capability-baseline.schema.json`。
3. manager 生成或读取其他治理 JSON 时，必须先按同名 schema 校验，未知 schema version 或未知 enum 一律停止。

## 维护边界

中央升级不得覆盖项目拥有的 `LOCAL_OVERRIDES.md`、`PROJECT_CONFIG.json` 或 `ADAPTERS.json`。任何 schema、固定路径或枚举的不兼容变更均为治理包 major 变更，必须提供迁移器和回滚测试。
