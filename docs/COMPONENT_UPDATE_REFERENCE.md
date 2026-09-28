> 阅读对象：维护本仓库政策或审阅 Spec Kit 上游更新的人。本页解释官方 CLI 的组件刷新行为，不是目标项目 Agent 的运行手册；目标项目 Agent 按项目 `AGENTS.md` 和当前 CLI 帮助操作，无需读取 Reference。

# CLI 与项目组件的官方更新行为

在项目根目录先运行只读版本检查：

~~~bash
specify self check
~~~

发现更新时，向用户说明版本和安装方式，取得明确批准后再运行：

~~~bash
specify self upgrade
~~~

升级后重新检查 CLI 帮助和项目状态。较旧 CLI 若不支持自助升级，按实际安装方式查阅官方升级说明；不要套用固定版本号或假设所有安装方式都能由该命令升级。

# 刷新项目组件

在已 Spec 化项目中，先按当前 CLI 帮助确认操作可用，再检查和刷新已安装组件：

| 组件 | 检查 | 更新 | 更新行为 |
| --- | --- | --- | --- |
| Agent 集成及其技能、脚本 | `specify integration status` | `specify integration upgrade <key> --force` | 每个已安装集成单独升级；`--force` 覆盖集成托管文件的本地修改。 |
| 扩展 | `specify extension list` | `specify extension add <id> --force` | `--force` 以官方目录版本覆盖现有扩展文件；不要只凭版本号声称本地文件内容未改动。 |
| 工作流 | `specify workflow list` | 移除后运行 `specify workflow add <catalog-id>` | 当前命令不接受 `--force`。移除并从官方目录重装，以覆盖旧文件并记录 `catalog` 来源；本地来源不得用于替代官方组件。 |

目标项目规则授权强制刷新已安装的官方组件：集成和扩展使用表中的 `--force` 命令；工作流使用官方 CLI 移除后从 catalog 重装。缺失组件不是刷新对象；只有任务需要且项目规则允许时，才询问用户是否通过 CLI 安装官方随包组件或官方目录组件。不得把覆盖授权用于项目 `AGENTS.md`、`specs/**` 或业务文件。

# 检查结果

只有 CLI 明确报告无更新时，才能说该对象未发现更新。离线、超时、失败或命令不支持时，指出无法核实的对象；被跳过或未检查的组件不能报告为最新。

# 上游依据

本页依据已审阅提交 c00dc0551583428a10a94443c58c6a41e5e0138c 的 `docs/upgrade.md`、`src/specify_cli/integrations/command_upgrade.py`、`src/specify_cli/extensions/command_update.py`、`src/specify_cli/extensions/_command_update_discovery.py`、`src/specify_cli/extensions/_command_update_transaction.py` 和 `src/specify_cli/workflows/command_update.py` 整理。实际参数以当前 CLI 帮助为准。
