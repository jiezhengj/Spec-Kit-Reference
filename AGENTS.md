# 仓库边界

本仓库维护 GitHub Spec Kit 中文政策与参考、个人全局规则来源、新项目模板、上游检查器和唯一组件更新助手；不是下游项目。不初始化 `.specify/`、不运行下游 SDD、不迁移既有项目，也不合并上游历史或复制其生成文件。

# 维护规则

- 下游使用官方 CLI、原生集成和技能。Reference 只支持新项目初始化；初始化后，目标项目以自身提交的 `AGENTS.md` 和 Spec Kit 状态为准，不依赖 Reference。
- Reference 对新项目的额外写入限于 `PROJECT-SPEC-KIT-GOVERNANCE` 规则块、组件更新助手和缓存忽略规则；助手只调用官方 CLI，不定义 SDD 流程。
- 从 `SPEC_KIT_REFERENCE.md` 选择当前任务所需页面；新项目初始化只读 `docs/PROJECT_INITIALIZATION.md` 和 `docs/PROJECT_AGENTS_TEMPLATE.md`。
- 新增或修改的 Markdown 正文使用简体中文；命令、文件名、产品名和官方术语保留原文。
- 上游审查遵循 `docs/UPSTREAM_UPDATE_POLICY.md`，结果记入 `docs/CHANGE_IMPACT.md`；审查和文档修改完成后最后更新 `UPSTREAM_BASELINE`。
- POLICY 候选须经用户审阅后才能部署或合并。`GLOBAL_POLICY.md` 的个人规则块使用固定标记，不维护政策版本号。

# 验证与 GitHub

- 运行 `git diff --check` 和 `python3 scripts/check_upstream.py`。
- GitHub 服务操作只使用 `gh` CLI。
