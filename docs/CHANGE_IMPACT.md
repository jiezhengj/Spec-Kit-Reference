# 2026-09-28：按需刷新组件并取消全局政策版本号

分类：POLICY

## 决策边界

新项目初始化额外交付一份通用 Python 更新助手。目标项目每个新会话运行一次；助手逐组件缓存最近一次成功的远端检查结果七天，只更新确认为官方来源且实际有更新的组件。失败和未知结果不刷新成功时间。个人全局 Spec Kit 规则块不再携带政策版本号；Git 差异与本影响记录保留审阅依据。

扩展范围限于 `assess`、`bug`，工作流范围限于 `speckit`。自定义目录、来源不明、CLI 输出不匹配或版本无法比较时，按未知状态跳过。

## 上游依据

已审阅 `UPSTREAM_BASELINE` `c00dc0551583428a10a94443c58c6a41e5e0138c` 到当前 `upstream/main` `fcc7d35fd36fd4efe3cc281d08361cea53a78cd7` 的完整提交列表、路径和差异。上游提交只更改 `docs/reference/bundles.md`、`docs/reference/presets.md`、`docs/reference/workflows.md`、`workflows/PUBLISHING.md` 并新增 `tests/test_catalog_trust_docs.py`；没有改变本助手使用的 CLI 更新实现。新文档指出目录配置可能来自项目、preset/bundle 可以拉取其他目录组件，并提醒目录列出的工作流不代表 shell 代码通过安全审计。

本地助手限制更新来源为官方目录；目标项目规则要求首次运行或更新后的首次运行前检查工作流 shell `run` 字段。组件更新本身不执行工作流。

## 本地调整

- 新增 `scripts/spec_kit_component_updater.py`，并为其添加标准库 `unittest` 覆盖；目标项目初始化时复制到 `.agent-support/`。
- 助手只自动确认已识别的官方扩展/工作流更新提示；遇到其他 CLI 确认时按安全默认值拒绝。
- 更新 `docs/PROJECT_INITIALIZATION.md`、`docs/PROJECT_AGENTS_TEMPLATE.md` 和 `docs/COMPONENT_UPDATE_REFERENCE.md`，记录交付路径、运行入口、逐组件七天缓存、错误重试、官方来源限制和工作流审阅边界。
- 更新 `SPEC_KIT_REFERENCE.md`，把助手列入新项目初始化交付项。
- 将个人全局政策块标记改为不带版本字段的稳定标记，并更新人工部署说明。政策变更不再要求版本号递增；历史记录中原有 `3.0.0` 只表示当时标记。
- 放宽初始化的精确写入范围，仅新增助手文件和缓存状态的单条 `.gitignore` 规则；保留目标项目原有内容，不自动迁移已初始化项目。

## 验证

`python -m unittest tests.test_spec_kit_component_updater -v` 通过 22 项标准库测试，覆盖七天缓存、失败重试、官方目录识别、健康集成状态、不同 Agent 集成键、CLI 更新提示边界、组件按需更新和读/交互命令超时。`python -m py_compile scripts/spec_kit_component_updater.py tests/test_spec_kit_component_updater.py` 通过。

使用本机 `specify 1.0.12` 在临时初始化项目中运行助手两次：真实 `integration status --json` 接受项目状态，两次助手均以 0 退出；首次成功缓存 CLI 发布检查，第二次报告缓存命中且保留原检查时间。另在临时 `.specify/` 项目中读取真实扩展目录、工作流目录和工作流搜索输出，解析器识别了官方默认目录及 `speckit` 版本。测试仅使用临时目录，没有刷新 Reference 仓库或其他项目中的组件。

`git diff --check` 已通过。更新基线前运行 `python scripts/check_upstream.py`，检查器列出的最新提交与本记录审阅的 `fcc7d35fd36fd4efe3cc281d08361cea53a78cd7` 一致，未发现新增上游差异；基线将在文档、助手和测试完成后推进到该提交，再由检查器复核。

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
- 精简 CLI 更新摘要；根据用户决定，目标项目对官方集成和扩展强制覆盖，对不支持 `--force` 的工作流用官方 CLI 移除并从 catalog 重装。
- 更正扩展来源说明：官方 CLI 可能随包提供扩展，CLI 安装时优先使用随包副本；更新说明区分 CLI 捆绑版本和目录版本。
- Bug Fix 与 Assessment 文档分别说明用途、官方步骤和所需扩展，不插入本地生命周期。
- 明确文档受众：将初始化说明命名为 `PROJECT_INITIALIZATION.md`；将 Bug Fix、Assessment 和 CLI 更新摘要命名为参考页，并标明它们不属于目标项目运行时输入。初始化步骤和规则模板只在新项目首次接入时由初始化 Agent 读取。
- 调整 `SPEC_KIT_REFERENCE.md` 为按使用阶段索引，分开一次性初始化文档与本仓库维护/人工参考文档；目标项目后续不回读 Reference。
- 按目标项目 Agent 的实际执行顺序重写规则模板：先说明权威来源，再说明每会话 CLI/组件检查，再选择任务流程；将 Feature SDD 的 Constitution 前置步骤设为两种模式共用，并并列短路径、完整路径、Bug Fix 和 Assessment。规则块内不链接或依赖 Reference。
- 本次记录时政策标记仍为 `3.0.0`。本次不修改个人全局 `AGENTS.md`，不迁移已有目标项目；下一条政策变更记录取消数字版本标记。

## 验证

`git diff --check` 和 `python scripts/check_upstream.py` 均通过；上游检查器确认基线与 `upstream/main` 一致、没有待审阅提交。额外检查了 12 份 Markdown、16 个内部链接、代码围栏、规则块标记、流程结构和目标规则块的 Reference 自包含性，均通过；政策标记仍为 `3.0.0`。未运行测试套件。

用户已批准将本地 POLICY 候选推送到 `main`。个人全局 `AGENTS.md` 仍由用户人工更新；GitHub Releases `v3.0.0`、`v2.1.1`、`v2.1.0` 均已删除，Git tags 保留。
# 2026-09-28：把七天门禁移到助手启动之前

分类：POLICY

## 决策边界

按用户澄清后的目标，项目 Agent 读取一次缓存门禁记录：距上次完整检查不足 7×24 小时时，直接开始任务，不启动更新助手。记录缺失、过期、损坏、非成功或用户要求立即检查时，才启动助手。助手只有整轮没有失败或未知状态时才写入成功时间；发现 CLI 更新但等待用户批准仍算检查完成。用户批准并完成 CLI 升级后，Agent 立即再运行助手。

## 上游依据

本次上游审查分类为 `NONE`。唯一新增提交 `40e93bbbcb3fd0fe55f995cc790a92bd8fcbe463` 只更新社区 OWASP LLM Threat Model 扩展到 v2.1.2 及其说明，不影响本地会话门禁、CLI 命令或官方组件更新规则。本地改动只调整会话入口和检查频率，不修改 Spec Kit CLI 行为。

## 本地调整

- 更新助手在启动时先记录 `running`；完整检查通过后记录 `success`，检查失败或状态未知时记录非成功状态。CLI 更新等待批准不重复触发助手。进程中断也不会留下可跳过的成功状态。
- 精简新项目规则块，只保留读取成功时间、到期后启动、用户要求时 `--recheck` 和异常处理；组件识别、来源校验和 CLI 交互留在脚本与维护参考中。
- 项目规则只保留 Agent 需要执行的动作和判断；脚本负责组件识别和更新细节。
- 保留本机缺少 CLI 时询问是否从官方来源安装、用户拒绝时交接的规则；Python 版本或助手缺失时明确说明检查未完成。
- 将新入口同步到 13 个可工作的 SDD 项目。`#SyncVersion` 下的 13 个目录没有根 `AGENTS.md`，也不是有效 Git 工作树，因此未写入这些不完整同步目录。

## 验证

Reference 的 28 项标准库单元测试和 Python 编译检查通过。13 个直接 SDD 项目的规则块已与模板一致，助手文件与 Reference 字节一致，缓存路径被忽略且助手文件未被忽略；13 个项目的 `git diff --check`、助手 `--help` 和块外字节保留检查通过。递归发现的 13 个 `#SyncVersion` 目录缺少根 `AGENTS.md` 且不是有效 Git 工作树，未修改。组件刷新命令未在目标项目运行。

# 2026-09-28：审查上游 stale 指引变更

分类：NONE

上游新增提交 `6d6881ed803325f14057fad123894ff70b2c6e03` 只调整 GitHub stale workflow 中 issue 和 pull request 的提示文字，不影响本地 Spec Kit 政策、CLI 命令或组件更新助手。本次未修改对应文档；审查后将 `UPSTREAM_BASELINE` 推进到该提交。

# 2026-09-28：扩展来源兼容和 CLI 覆盖

分类：POLICY（用户已确认）

## 上游审查

审查范围为 `6d6881ed803325f14057fad123894ff70b2c6e03` 至 `9b8e5d815d06853ea0d7fb274e9a4cc9e7e3982a`，包含 mcode 集成、monorepo feature 目录说明、社区目录条目、`SPECKIT_PYTHON` 覆盖以及随包 `agent-context` 版本更新。它们不改变本地更新助手行为，分类为 `NONE`；本次上游基线推进到 `9b8e5d815d06853ea0d7fb274e9a4cc9e7e3982a`。

Spec Kit CLI 把扩展安装来源记为 `local` 时，不能据此判断扩展是否来自官方目录；上游问题 #4208 记录了目录安装来源被写成 `local` 的已知限制。本地 1.0.12 CLI 实测表明，`specify extension update` 会按官方目录版本比较：新版时可覆盖本地记录的旧版，当前版时退出且不改扩展目录或注册表。

## 本地调整

- 更新助手只验证活动扩展目录为官方目录，不再用安装注册表的 `source` 字段阻止 `assess`、`bug` 更新，也不输出来源字段提示。
- 官方 CLI 报告当前版时记录七天成功缓存；官方 CLI 发现新版时，助手自动确认更新提示并由官方 CLI 覆盖旧文件。目录被改写、命令失败或更新结果无法核实时仍不缓存成功。
- 更新助手已同步到 13 个可工作的 SDD 项目；目标项目规则块和 `.gitignore` 未改动。

## 验证

`python -m unittest tests.test_spec_kit_component_updater -v` 的 28 项测试通过；Python 编译检查、Reference 和 13 个目标项目的 `git diff --check` 通过。隔离临时项目实测：`source: local` 的 1.0.0 扩展被 CLI 更新到官方 1.0.1；已是 1.0.1 时扩展目录和注册表均未改动。MySkills 实际运行助手退出码为 0，`assess` 1.0.1 和 `bug` 1.0.0 均已是最新，`last_full_check.status` 为 `success`。13 个目标项目的规则块、助手文件、缓存忽略规则和助手 `--help` 检查均通过。
