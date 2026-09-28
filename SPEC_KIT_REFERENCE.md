# 渐进式阅读入口

先读 [任务导航](docs/START_HERE.md)，再只读当前任务对应的本地中文说明：

| 当前任务 | 阅读 |
| --- | --- |
| 初始化项目、开发功能 | [功能流程](docs/FEATURE_WORKFLOW.md) |
| 修复已知缺陷 | [缺陷流程](docs/BUGFIX_WORKFLOW.md) |
| 判断一个想法是否值得投入 | [想法评估](docs/ASSESSMENT_WORKFLOW.md) |
| 更新 CLI、Agent 集成或扩展 | [更新操作](docs/CLI_UPDATES.md) |
| 审查 Spec Kit 上游变化 | [上游审查规则](docs/UPSTREAM_UPDATE_POLICY.md) |

项目全局执行规则见 [GLOBAL_POLICY.md](GLOBAL_POLICY.md)。官方 Agent 技能负责具体产物生成；此参考只帮助 Agent 找到对应步骤，不创建第二套工作流。

新项目初始化后，项目根目录 `AGENTS.md` 会携带自包含的 Spec Kit 规则块。后续会话使用该提交内容；中央 Reference 不更新或覆盖已 Spec 化项目。

# 维护者依据

本地中文摘要依据已审阅的 Spec Kit 上游提交 c00dc0551583428a10a94443c58c6a41e5e0138c。逐页记录的源文件和本地校订日期见对应文档末尾及 [上游影响记录](docs/CHANGE_IMPACT.md)。

进入下游项目时，优先使用该项目当前安装的 specify CLI、Agent 集成和技能内容。本仓库的本地摘要不能覆盖它们，也不是下游运行时依赖。
