# 仓库用途

本仓库维护简体中文的 GitHub Spec Kit 使用政策、渐进式流程说明和上游变更审查记录。下游项目使用官方 Spec Kit CLI 及其官方 Agent 集成。新项目 Spec 化时会把自包含的 Spec Kit 规则块写入并提交目标项目 `AGENTS.md`；后续运行不依赖全局 POLICY 或本仓库。

# 从这里开始

Agent 应先读 [任务导航](docs/START_HERE.md)，再只打开当前任务所需的页面。政策与摘要按步骤说明流程，具体规格、计划、任务和缺陷记录由当前项目的官方 Agent 技能生成。

# 当前维护范围

- [全局政策](GLOBAL_POLICY.md)：新项目初始化、功能开发、缺陷修复和更新规则。
- [渐进式阅读入口](SPEC_KIT_REFERENCE.md)：按当前工作选择本地中文说明。
- docs/：功能、缺陷、评估、更新和上游维护说明。
- scripts/check_upstream.py：比较已审阅上游基线的检查器。获取时会更新 Git 远端跟踪引用，但不会改政策或基线。
- 每周 GitHub Actions：发现上游提交并提醒维护者，不会自动改政策。

本仓库不再包含自建扩展、工作流、预设、Bundle、项目管理器、下游运行时包、发布器或对应的合同测试。目标项目只携带 `AGENTS.md` 受管规则块和官方 CLI 生成的项目状态，不携带 Reference 管理器或中央更新程序。
