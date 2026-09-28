# 上游审查规则

UPSTREAM_BASELINE 记录已完成语义审查的官方 Spec Kit 提交，不要求始终等于 upstream/main。

# 审查步骤

1. 阅读 AGENTS.md 和 UPSTREAM_BASELINE。
2. 获取 upstream/main，并确认基线提交仍是当前上游的祖先。
3. 查看提交列表、变更路径和完整差异。
4. 完整阅读与功能流程、官方扩展、CLI 命令、Agent 集成或升级方式相关的文件。
5. 按 NONE、REFERENCE 或 POLICY 分类。
6. 只修改有证据支持的中文文档，并记录 docs/CHANGE_IMPACT.md；需要时更新 docs/HISTORY.md。
7. 运行 git diff --check 和 scripts/check_upstream.py。
8. 变更审查和文档修改完成后，最后更新 UPSTREAM_BASELINE。

如果 upstream/main 无法快进包含本地基线，先检查上游历史是否被改写或本地远端引用是否过期，不得直接推进基线。

# 优先检查的上游内容

根据本次变更涉及的功能，检查官方 Quickstart、Bug Fix、Assessment、Upgrade、已有项目接入指南，扩展和工作流目录，以及 CLI 的安装、集成升级、扩展更新命令。完整提交列表和变更路径用于发现这些重点文件之外的影响；优先清单不是忽略其他差异的理由。

# 影响分类

## NONE

上游变化不影响本地政策或操作参考。记录审查结果后可以推进基线。

## REFERENCE

CLI 参数、组件目录、集成、生成文件或升级方式改变。按需要更新 SPEC_KIT_REFERENCE.md，通常不改 GLOBAL_POLICY.md。

## POLICY

官方流程、工作完成条件或工具权威边界改变，可能影响 Agent 行为。审查 GLOBAL_POLICY.md 与 SPEC_KIT_REFERENCE.md。部署或合并前必须由用户审阅。

# 自动化边界

scripts/check_upstream.py 和 GitHub Actions 只负责发现变化并提醒维护者，不修改政策、合并上游或推进基线。
