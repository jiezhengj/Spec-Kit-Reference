> 阅读对象：维护本仓库政策或审阅 Spec Kit 上游的人。本页记录官方 CLI 的组件检查和更新行为；目标项目 Agent 运行初始化时复制的更新助手，不把本页作为运行时输入。

# 更新助手的入口和缓存

新项目初始化时，Reference 将 `scripts/spec_kit_component_updater.py` 复制到目标项目 `.agent-support/spec_kit_component_updater.py`。Agent 每个新会话先读缓存中的 `last_full_check`，只有缺少成功记录或记录已满 7×24 小时时才启动脚本。脚本只使用 Python 标准库和官方 `specify` CLI。

入口门禁读取 `.agent-state/spec_kit_component_update_cache.json` 中的 `last_full_check.status` 和 `last_full_check.checked_at_utc`。只有整轮检查无失败或未知状态时，助手才写入 `success`。发现 CLI 更新但需用户批准仍视为检查完成，因此七天内不会重复启动助手或重复提示。检查开始时，助手先写入 `running`；中断、失败或状态未知时保留非成功状态，下次会话会重试。缓存缺失、损坏、时间格式无效、时间在未来或已满 7×24 小时时，Agent 启动助手。用户要求立即检查时，Agent 使用 `--recheck`。

启动后，脚本仍逐组件缓存远端 CLI 发布、扩展目录和工作流目录检查的最近成功时间、结果、CLI 版本、本地版本和官方目录标识。`--recheck` 绕过这些远端缓存，但不强制刷新组件文件。CLI 版本或组件本地版本、活动官方目录发生变化时，相应组件缓存身份不再匹配。

缓存路径为 `.agent-state/spec_kit_component_update_cache.json`。初始化流程在目标项目 `.gitignore` 精确追加 `/.agent-state/spec_kit_component_update_cache.json`；助手不提交状态文件。每条官方 CLI 子进程最多运行 180 秒。失败、取消、超时、未知来源、版本无法比较或更新后核实失败时，脚本不记录新的成功时间，并使被强制重查但失败的旧记录失效。下次运行会重试。

# 组件检查与更新

| 组件 | 检查信号 | 只在何时更新 | 未知状态时 |
| --- | --- | --- | --- |
| Spec Kit CLI | `specify --version` 每次本地读取；`specify self check` 的远端结果缓存 7 天 | CLI 有新版本时只报告候选版本。Agent 取得用户明确批准后运行 `specify self upgrade` | CLI 检查失败或输出无法识别时不写成功缓存，下次重试 |
| Agent 集成 | `specify integration status --json` 列出已安装键；读取每个 `.specify/integrations/<key>.manifest.json` 的 `version` | 清单版本低于当前 CLI 版本时运行 `specify integration upgrade <key> --force`，并确认升级后清单版本与 CLI 一致 | 键、清单或版本无法确认时跳过并报告；不写入成功状态 |
| `assess`、`bug` 扩展 | `specify extension list --json` 读取安装状态和版本；`specify extension catalog list` 验证官方活动目录；`specify extension update <id>` 按 CLI 结果检查并更新 | 官方活动目录确认后，由 CLI 发现有新版时更新并覆盖旧文件；最新版时 CLI 不改扩展文件 | 活动目录被项目/用户配置或环境变量改写、输出不可识别、命令失败或取消时不记录成功检查时间，下次重试 |
| `speckit` 工作流 | `.specify/workflows/workflow-registry.json` 读取来源和本地版本；`specify workflow info` 与 `specify workflow search` 比较本地和官方目录版本 | `source: catalog` 时运行 `specify workflow update speckit`；`source: bundled` 时只有官方目录版本更高才运行 `specify workflow add speckit`，随后确认本地版本达到候选版本 | 目录顺序或来源不能确认为官方、查询结果不唯一、版本不可比较或命令失败时跳过并报告 |

集成清单版本是 CLI 发布版本代理，不是集成文件内容哈希；CLI 版本变化可能触发该集成一次刷新，即便文件内容没有变化。版本解析只接受助手明确支持的稳定点分数字版本；其他格式按未知处理。

扩展和工作流目录支持项目级、用户级和环境变量覆盖。助手只有在活动目录的首选来源是 Spec Kit 官方目录且可安装时才更新。若项目或用户目录配置存在，或环境变量指向其他来源，助手保守跳过，不自行解析 YAML，也不根据目录名称猜测信任。扩展安装来源字段不参与更新资格判断；官方 CLI 的 `extension update <id>` 负责比较版本，并在发现新版时替换现有扩展。

官方扩展 `update` 和 `workflow update` 命令会在发现更新后要求确认；助手只对已验证官方活动目录下的 `assess`、`bug` 和 `speckit` 更新提示自动输入确认。其他 CLI 确认提示一律拒绝。扩展检查发现无更新时，CLI 在安装事务前退出，不覆盖文件；发现新版时，CLI 更新命令会覆盖现有扩展。工作流 `add` 可事务式重装已安装工作流；无需先移除。

# 工作流信任边界

目录收录不代表维护者已对工作流代码进行安全审计。首次运行或更新后的首次运行前，项目 Agent 必须检查 `.specify/workflows/<id>/workflow.yml` 中 shell 步骤的 `run` 字段。`specify workflow info` 只展示元数据，不足以替代对实际 shell 内容的审阅。助手只刷新文件，不运行工作流。

# 检查结果

脚本将组件结果分别报告为本地版本一致、成功更新、复用成功缓存、发现 CLI 更新、来源未知或检查/更新失败。只有整轮无失败或未知状态时，脚本才保存可供入口门禁使用的成功时间。入口门禁命中时，Agent 直接开始用户任务，无需汇报检查；助手启动后命中组件缓存时，Agent 应说“复用最近一次成功检查”，不能说“本会话刚检查”。任何未知、跳过或失败组件都不得报告为最新。用户批准并完成 CLI 自身升级后，Agent 立即再运行助手，避免沿用升级前的门禁记录。

# 上游依据

行为依据为已审阅的 Spec Kit 上游提交 `fcc7d35fd36fd4efe3cc281d08361cea53a78cd7`。CLI 实现文件包括 `src/specify_cli/selfs/command_check.py`、`src/specify_cli/integrations/manifest.py`、`src/specify_cli/integrations/command_upgrade.py`、`src/specify_cli/integration_status.py`、`src/specify_cli/extensions/command_update.py`、`src/specify_cli/extensions/_command_update_discovery.py`、`src/specify_cli/extensions/_command_update_transaction.py`、`src/specify_cli/extensions/catalog/command_list.py`、`src/specify_cli/workflows/command_update.py`、`src/specify_cli/workflows/command_add.py` 和 `src/specify_cli/workflows/catalog/_domain.py`。上游参考文档 `docs/reference/bundles.md`、`docs/reference/presets.md`、`docs/reference/workflows.md` 及 `workflows/PUBLISHING.md` 说明目录来源和工作流 shell 内容的信任边界。
