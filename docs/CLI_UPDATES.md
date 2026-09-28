# 每个会话进入已有 Spec 项目时

Spec Kit CLI 本体和项目中安装的 Agent 文件、扩展是分开的更新对象。先按本页选择对应对象，再使用当前安装的 CLI 实际支持的命令。

新项目初始化时写入并提交的 `AGENTS.md` 规则块负责此检查，所以即使电脑没有全局 POLICY 或 Reference，Agent 仍执行相同步骤。

只要项目存在 `.specify/`，Agent 必须在每个新会话首次实质性操作前最多运行一次只读检查：

~~~bash
specify self check
~~~

如果 CLI 不存在，Agent 先询问用户是否从官方来源安装；用户拒绝时交还给 Agent 并返回 `HANDOFF_TO_AGENT`。如果检查发现较新 CLI，Agent 告知可用版本并取得明确批准后才运行升级。拒绝、无更新、离线或超时后，本会话不重复询问。升级后重新读取实际 CLI 帮助和项目状态。

不论 CLI 是否升级，Agent 都要按当前 CLI 实际的 `help`、`status` 和 `list` 命令检查活动集成、已安装扩展及工作流。正常刷新不需另行审批，不安装缺失组件，也不使用 `--force`：

~~~bash
specify integration status
specify integration upgrade <active-integration-key>
specify extension list
specify extension update
specify workflow list
specify workflow update
~~~

只有当前 CLI 帮助确认某个更新命令可用且对应组件已安装时才运行该命令。Agent 集成升级刷新其托管技能文件；扩展和工作流更新各自独立。当前任务需要的官方能力缺失时，Agent 单独询问是否通过官方 CLI 安装；缺少原生集成时使用 `specify integration install <native-key>`，缺少缺陷或 Assessment 扩展时分别使用 `specify extension add bug` 或 `specify extension add assess`。如果当前 Agent 没有官方原生集成，停止并报告，不得退回 `generic`。用户拒绝安装时返回 `HANDOFF_TO_AGENT`。中央 Reference 不参与此更新检查，也不自动更新本地规则块。

# 检查和更新 CLI

~~~bash
specify self check
specify self upgrade --dry-run
specify self upgrade
~~~

self check 只检查版本，不修改环境。dry-run 显示升级方式和目标，不执行升级。self upgrade 默认更新到最新稳定版；它会自动更新 uv tool 和 pipx 安装。临时运行的 uvx、源码检出或不支持的安装方式不会由该命令自动升级，CLI 会给出对应说明。

旧版 CLI 如果没有 self upgrade，应先查看当前 CLI 的实际 help 和本机安装方式，再选择与安装方式相符的升级命令；不要照抄固定版本号或假设所有安装器都受支持。

升级后重新读取 specify --help、specify integration status 和项目状态。不要假设命令参数或组件版本没有变化。

# 刷新项目集成

先查看已安装的 Agent 集成：

~~~bash
specify integration status
~~~

每个已安装的集成都单独刷新一次：

~~~bash
specify integration upgrade <integration-key>
~~~

CLI 使用安装清单判断托管文件是否被修改。若本地修改导致升级停止，先检查差异并保留修改；不要在自动刷新中添加 --force。

# 刷新官方扩展

~~~bash
specify extension update
~~~

不指定扩展时，命令更新当前项目安装的扩展；也可按当前 CLI help 指定单个扩展。扩展应由官方目录安装，才能由官方目录提供可比较和可刷新的版本。

# 来源判断

如果 CLI 报告组件来源为 local，或组件记录的是 Reference 本地路径，不能据此判断它已是最新版本。官方更新器只会处理它能从官方目录识别的来源。不要重复安装或发布本仓库自建的同名组件；若官方目录没有等价能力，应报告该能力没有官方替代。

官方升级命令与项目集成负责更新其托管文件。不要手工改写 Agent 集成文件，也不要用本地工作流或预设覆盖官方技能。

# 上游依据

本页根据已审阅提交 c00dc0551583428a10a94443c58c6a41e5e0138c 的 docs/upgrade.md 整理，校订日期为 2026-09-28。
