# 2026-09-28：重做 Spec Kit 规则分层

分类：POLICY

## 决策边界

个人全局规则只判断是否询问用户为尚未 Spec 化的软件或技术项目启用 Spec Kit，并引导新项目初始化。目标项目根目录 `AGENTS.md` 负责项目内流程和每会话检查。Reference 只在新项目初始化时使用，不是已 Spec 项目的运行时依赖。

## 上游依据

已审阅基线 `c00dc0551583428a10a94443c58c6a41e5e0138c` 与当前 `upstream/main` 一致，无待审阅提交。审查了 `docs/quickstart.md`、`docs/guides/existing-projects.md`、`docs/guides/bugfix.md`、`docs/guides/assessment.md`、`docs/upgrade.md`，以及 `src/specify_cli/integrations/command_upgrade.py`、`src/specify_cli/extensions/command_add.py`、`src/specify_cli/extensions/_command_update_discovery.py`、`src/specify_cli/extensions/_command_update_transaction.py` 和 `src/specify_cli/workflows/command_update.py`。

## 本地调整

- 精简 `GLOBAL_POLICY.md`，只保留项目触发判断、本机 Reference 定位、初始化说明入口和初始化后的规则边界；Reference 不可用时停止初始化。
- 将新项目初始化操作和字节级合并规则放在 `docs/PROJECT_INITIALIZATION.md`，把可写入目标项目的自包含规则块单独放在 `docs/PROJECT_AGENTS_TEMPLATE.md`。
- 以 `SPEC_KIT_REFERENCE.md` 作为唯一任务索引，删除重复的 `docs/START_HERE.md`。
- 精简根目录 `AGENTS.md`，由 `docs/UPSTREAM_UPDATE_POLICY.md` 统一维护上游审查步骤；保留下游边界、POLICY 审阅、版本、文档、验证和 GitHub 规则。
- 精简 CLI 更新摘要；明确集成升级覆盖官方托管文件，扩展和工作流按各自不带 `--force` 的官方更新命令刷新。
- 更正扩展来源说明：官方 CLI 可能随包提供扩展，CLI 安装时优先使用随包副本；更新说明区分 CLI 捆绑版本和目录版本。
- Bug Fix 与 Assessment 文档分别说明用途、官方步骤和所需扩展，不插入本地生命周期。
- 明确文档受众：将初始化说明命名为 `PROJECT_INITIALIZATION.md`；将 Bug Fix、Assessment 和 CLI 更新摘要命名为参考页，并标明它们不属于目标项目运行时输入。初始化步骤和规则模板只在新项目首次接入时由初始化 Agent 读取。
- 调整 `SPEC_KIT_REFERENCE.md` 为按使用阶段索引，分开一次性初始化文档与本仓库维护/人工参考文档；目标项目后续不回读 Reference。
- 按目标项目 Agent 的实际执行顺序重写规则模板：先说明权威来源，再说明每会话 CLI/组件检查，再选择任务流程；将 Feature SDD 的 Constitution 前置步骤设为两种模式共用，并并列短路径、完整路径、Bug Fix 和 Assessment。规则块内不链接或依赖 Reference。
- 政策版本仍为 `3.0.0`。本次不修改个人全局 `AGENTS.md`，不迁移已有目标项目。

## 验证

`git diff --check` 和 `python scripts/check_upstream.py` 均通过；上游检查器确认基线与 `upstream/main` 一致、没有待审阅提交。额外检查了 12 份 Markdown、16 个内部链接、代码围栏、规则块标记、流程结构和目标规则块的 Reference 自包含性，均通过；政策标记仍为 `3.0.0`。未运行测试套件。

用户已批准将本地 POLICY 候选推送到 `main`。个人全局 `AGENTS.md` 仍由用户人工更新；GitHub Releases `v3.0.0`、`v2.1.1`、`v2.1.0` 均已删除，Git tags 保留。
