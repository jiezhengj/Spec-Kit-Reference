# 仓库定位

本仓库维护 GitHub Spec Kit 的中文政策与操作参考，以及供新项目初始化复制的单一组件更新助手；本仓库不是 Spec Kit 分支，也不是下游业务项目。维护本仓库时，不初始化 `.specify/`，不运行下游项目流程。上游只作事实依据，不合并其历史、不复制整个仓库、不改写上游生成文件。

# 上游维护

涉及上游政策、参考文档或 CLI 行为时，按 [上游审查规则](docs/UPSTREAM_UPDATE_POLICY.md) 执行。该规则负责检查提交和完整差异、分类影响、记录审查并在完成后推进 `UPSTREAM_BASELINE`。

- `NONE`、`REFERENCE`、`POLICY` 按上游审查规则分类；只按证据修改本地中文文档，并记录 `docs/CHANGE_IMPACT.md`。
- `POLICY` 候选必须先交由用户审阅；获批前不得部署或合并。
- `GLOBAL_POLICY.md` 与个人全局 `AGENTS.md` 的 Spec Kit 受管块使用固定的 `SPEC-KIT-GLOBAL-POLICY:START`、`SPEC-KIT-GLOBAL-POLICY:END` 标记，不维护政策版本号。Git 差异和 `docs/CHANGE_IMPACT.md` 记录变更；不得为普通政策修改要求版本号递增。
- 当前变更影响记录在 `docs/CHANGE_IMPACT.md`；Git 保存提交历史，不另建重复历史归档。

# 下游边界

- 下游项目的流程和组件使用官方 Spec Kit CLI、官方目录、官方文档及 Agent 原生集成。本仓库维护简明政策、中文操作摘要、上游影响记录、基线、上游检查器和唯一允许复制到新项目的组件更新助手。
- 不新增本地扩展、工作流、预设、Bundle、命令覆盖、第二套生命周期、任务状态机、项目管理器或自定义审批合同。唯一例外是 `scripts/spec_kit_component_updater.py`：该标准库脚本只调用官方 CLI，供初始化后的项目按缓存结果刷新官方组件，不定义新的 SDD 流程。
- 新项目初始化时，官方 CLI 可按其职责生成托管文件；Reference 额外只允许在目标项目根目录精准追加或替换 `PROJECT-SPEC-KIT-GOVERNANCE` 受管块、复制 `.agent-support/spec_kit_component_updater.py`，并在 `.gitignore` 精确忽略 `.agent-state/spec_kit_component_update_cache.json`。AGENTS 标记外内容和 `.gitignore` 的既有内容必须逐字节保留；不得手工修改下游 `.specify/**`、`specs/**`、Agent 集成文件或业务文件。
- 本仓库只支持新项目初始化，不兼容迁移既有项目规则、旧治理组件或旧 Spec 产物；既有项目迁移须作为独立任务处理。
- 初始化后，目标项目提交的 `AGENTS.md` 和 Spec Kit 状态是项目级依据；运行时不依赖本机全局政策、中央 Reference 或在线网页。

# 文档维护

新增或修改的 Markdown 正文使用简体中文，产品名、命令、文件名和官方术语保留原文。操作摘要记录已审阅的上游提交和源文件路径；若摘要与当前 CLI 或技能不符，先核对实际帮助和项目状态，再安排上游审查。

从根目录 `SPEC_KIT_REFERENCE.md` 进入，先确认当前工作是新项目的一次性初始化，还是本仓库维护/人工查阅；只读取对应页面。目标项目已完成初始化后，不要求其 Agent 回读本仓库的流程摘要。

# 验证与 GitHub 操作

至少运行 `git diff --check` 和 `python scripts/check_upstream.py`。不新增或运行已退役的治理合同测试；只有用户明确要求时才运行测试套件。

GitHub 的认证、查询、Issue、Pull Request、Review、Actions 和 Release 操作只使用 `gh` CLI；不得用浏览器或直接 HTTP/API 替代。
