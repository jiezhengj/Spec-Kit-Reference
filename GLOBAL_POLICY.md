<!-- SPEC-KIT-GLOBAL-POLICY:START version=3.0.0 -->

# 适用范围

本规则只判断一个尚未 Spec 化的软件或技术项目是否需要启用 Spec Kit，并在适合时询问用户。它不决定项目内具体工作的 SDD 流程。

判断前读取目标项目根目录 `AGENTS.md`，并检查项目是否已有 `.specify/`：

- 已有 `.specify/`：遵循项目提交的规则和 Spec Kit 状态。本机全局规则不再判断该项目的流程，不读取、探测或使用中央 Reference。
- 没有 `.specify/`：只有当项目属于软件或技术项目，且当前任务要创建或改变技术能力时，才询问用户是否启用 Spec Kit。纯问答、只读调查、代码审查和不改变技术能力的常规维护不触发询问。
- 用户明确要求为项目 Spec 化时视为同意。用户拒绝后，本次工作按普通项目任务继续，不运行 `specify init`；同一任务中不重复询问。

Feature 的短流程或完整流程、缺陷修复、想法评估等项目内路径由目标项目自己的 `AGENTS.md` 决定。

# 新项目 Spec 化

只有用户同意且目标项目不存在 `.specify/` 时，才执行本节。Reference 只用于新项目引导和提供目标项目规则模板，不是目标项目的运行时依赖。

只查当前电脑对应的固定目录，不扫描其他目录、不从工作目录猜测，也不读取其他机器的路径：

- Windows：`C:\Users\jiezhengj\Documents\Project\SpecKitReference`
- macOS：`/Users/jiezhengj/Documents/Project/SpecKitReference`

若对应目录不可用，说明路径并暂停 Spec Kit 初始化；不得只运行官方 CLI 而省略本地项目规则块。

找到 Reference 后，仅在本次新项目初始化期间读取 `docs/PROJECT_INITIALIZATION.md` 和 `docs/PROJECT_AGENTS_TEMPLATE.md`：前者说明初始化操作，后者提供一次性写入目标项目 `AGENTS.md` 的规则块。目标项目 Agent 后续不读取这些 Reference 文档；其规则和组件刷新要求已写入项目自身的 `AGENTS.md`。

初始化完成后，目标项目提交的 `AGENTS.md` 和 Spec Kit 状态成为项目级规则来源。后续会话不需要全局政策或中央 Reference；两者是否存在都不改变该项目的流程和更新行为。

<!-- SPEC-KIT-GLOBAL-POLICY:END -->
