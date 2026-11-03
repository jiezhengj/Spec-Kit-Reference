<!-- SPEC-KIT-GLOBAL-POLICY:START -->

# 适用范围

本规则只管一件事：尚未 Spec 化的软件/技术项目是否需要启用 Spec Kit，并在合适时询问用户。项目内的 SDD 流程不归它管——Feature 短流程/完整流程、缺陷修复、想法评估等由目标项目自己的 `AGENTS.md` 决定。

判断前读目标项目根目录 `AGENTS.md`，并检查是否已有 `.specify/`：

- 已有 `.specify/`：遵循项目提交的规则与 Spec Kit 状态，全局规则不再介入，也不读、不探测、不使用中央 Reference。
- 没有 `.specify/`：仅当项目属于软件/技术项目、且当前任务要创建或改变技术能力时，才询问是否启用 Spec Kit；纯问答、只读调查、代码审查、不改变技术能力的常规维护不触发询问。
- 用户明确要求 Spec 化即视为同意；用户拒绝后按普通项目任务继续，不跑 `specify init`，同一任务中不再重复询问。

# 新项目 Spec 化

仅在用户同意且目标项目还没有 `.specify/` 时执行。Reference 只用于新项目引导和提供规则模板，不是运行时依赖。

只查当前电脑的固定目录，不扫描其他目录、不按工作目录猜、不读其他机器的路径：

- Windows：`C:\Users\jiezhengj\Documents\Project\SpecKitReference`
- macOS：`/Users/jiezhengj/Documents/Project/SpecKitReference`

目录不可用就说明路径并暂停初始化；不得只跑官方 CLI 而省掉本地项目规则块。

找到 Reference 后，仅本次初始化期间读 `docs/PROJECT_INITIALIZATION.md`（怎么做）和 `docs/PROJECT_AGENTS_TEMPLATE.md`（一次性写入目标项目 `AGENTS.md` 的规则块）。目标项目之后不再读这两份文档，其规则与组件刷新要求已在项目自己的 `AGENTS.md` 里。

初始化完成后，目标项目提交的 `AGENTS.md` 和 Spec Kit 状态即成为项目级规则来源；后续会话不再需要全局政策或中央 Reference，二者存不存在都不影响该项目的流程。

<!-- SPEC-KIT-GLOBAL-POLICY:END -->
