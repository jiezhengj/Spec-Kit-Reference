# 适用范围

本规则约束本仓库如何应对官方 Spec Kit 的变化。本仓库不再逐提交审查 `github/spec-kit` 历史，不维护上游提交基线，也不镜像官方文档；参考摘要不是权威资料。

# 依赖面

- `scripts/spec_kit_component_updater.py` 解析官方 CLI 的版本、CLI 更新检查、集成状态、扩展清单、扩展与工作流目录、工作流元数据输出。
- `docs/PROJECT_INITIALIZATION.md` 和 `docs/PROJECT_AGENTS_TEMPLATE.md` 使用官方 CLI 的初始化命令和官方流程阶段名。
- Bug Fix、Assessment 和组件更新摘要描述官方行为，但以当前 CLI 帮助、已安装官方技能和官方文档为准。

# 自动检查

`.github/workflows/check-spec-kit-cli-contract.yml` 每月 1 日（UTC 03:00）运行：

- Ubuntu 与 Windows 上运行 `python -m unittest tests.test_spec_kit_component_updater -v`。
- Ubuntu 上安装最新官方 CLI，运行 `scripts/check_cli_contract.py`，在临时初始化的项目里校验上述输出仍能被本仓库解析器识别。

本地运行 `python3 scripts/check_cli_contract.py`（`--offline` 跳过联网检查）和 `python3 -m unittest tests.test_spec_kit_component_updater -v`。

检查失败表示官方 CLI 的输出或命令已经变化。按失败项更新解析器、测试和对应文档，不靠猜测兼容。

# 人工核对

出现以下情况时人工核对官方 CLI 帮助和官方文档：契约检查失败、目标项目报告行为与文档不符、准备发布政策变更。

每次只核对入口文档：官方 quickstart、existing-projects、bugfix、assessment，以及 CLI 的 `init`、`self`、`integration`、`extension`、`workflow` 命令帮助。建议每季度一次，不按上游提交逐个分类。

核对结果记入 `docs/CHANGE_IMPACT.md`。文档使用 CLI 版本锚点（例如 `specify` 1.2.5），不再记录上游提交 SHA。

# 分类

## CONTRACT

CLI 输出或命令变化导致解析器或命令失效。更新脚本、测试与对应文档。

## REFERENCE

官方说明变化但本地摘要仍成立。按需更新摘要，不强制逐条同步。

## POLICY

官方流程、完成条件或工具权威边界改变，可能影响目标项目规则块。审查 `GLOBAL_POLICY.md`、`docs/PROJECT_INITIALIZATION.md` 和 `docs/PROJECT_AGENTS_TEMPLATE.md`；部署或合并前必须由用户审阅。

# 自动化边界

自动检查只报告契约是否仍然成立，不修改政策、不更新目标项目、不创建 Issue；失败以工作流失败呈现，由维护者处理。
