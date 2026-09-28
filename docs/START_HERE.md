# 选择当前任务

本页用于选择一份本地操作说明。Agent 只读取当前任务对应的页面，不需要先浏览整套文档或打开在线网页。

- 新建项目并开展功能开发：阅读 [功能流程](FEATURE_WORKFLOW.md)。
- 已经知道系统行为出错，需要诊断和修复：阅读 [缺陷流程](BUGFIX_WORKFLOW.md)。
- 用户还在判断某个想法是否值得投入：阅读 [想法评估](ASSESSMENT_WORKFLOW.md)。
- 检查或刷新 CLI、Agent 集成和扩展：阅读 [更新操作](CLI_UPDATES.md)。
- 修改本仓库政策、参考或检查器：阅读根目录 AGENTS.md 和 [上游审查规则](UPSTREAM_UPDATE_POLICY.md)。

# 阅读顺序

确定任务类型后，只读对应说明中的当前阶段。每次单独运行一个官方 Agent 技能，检查并审阅该阶段结果，再决定是否进入下一阶段。技能名称和具体生成内容以当前项目已安装的官方 Agent 集成为准。

本地说明是供 Agent 离线阅读的中文摘要，不是另一个工作流实现。它不安装组件、不生成 Spec 产物，也不要求目标项目引用 SpecKitReference。

新项目 Spec 化时，Agent 会将自包含的 Spec Kit 规则块写入并提交目标项目的 `AGENTS.md`。后续协作者从项目自己的 `AGENTS.md`、`.specify/` 和 `specs/` 继续；全局 POLICY 和中央 Reference 是否存在，不改变已初始化项目的会话更新检查和流程规则。

# 上游依据

当前摘要依据已审阅提交 c00dc0551583428a10a94443c58c6a41e5e0138c。上游源文件为：

- 功能流程：docs/quickstart.md
- 缺陷流程：docs/guides/bugfix.md
- 想法评估：docs/guides/assessment.md
- 更新操作：docs/upgrade.md

维护者更新这些摘要时，先按照 UPSTREAM_UPDATE_POLICY.md 审查上游，再记录本地影响。
