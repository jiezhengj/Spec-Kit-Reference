> 阅读对象：已经得到用户同意、正在为新目标项目执行一次性 Spec Kit 初始化的 Agent。目标项目完成后，其 Agent 不需要在本仓库读取本页。

# 初始化前检查

本页只用于用户同意为新项目启用 Spec Kit、且项目尚无 `.specify/` 时。若 `.specify/` 已存在，不要重新初始化；遵循项目现有 `AGENTS.md` 和 Spec Kit 状态。

确认目标项目根目录和当前 Agent 的原生集成键。集成键必须来自用户、宿主或 Agent 运行时声明，不得从安装目录或其他文件推断。若 CLI 不支持该原生集成或 Python 脚本，停止并报告，不退回 `generic`。

CLI 缺失时，先询问用户是否从官方来源安装。用户同意后运行：

~~~bash
uv tool install specify-cli
~~~

CLI 已存在或安装完成后，检查 CLI 版本：

~~~bash
specify self check
~~~

发现 CLI 更新时，告知可用版本并取得明确批准后再运行 `specify self upgrade`。用户拒绝、离线、超时或 CLI 不支持所需操作时，停止相应步骤，不重复询问。

# 选择初始化方式

初始化命令使用已确认的原生集成，并明确选择 `--script py`。只有运行环境确认为非交互时才增加 `--non-interactive`。

## 新目录

在目标目录的父目录中运行：

~~~bash
specify init <project-name> --integration <native-agent-key> --script py
~~~

非交互环境运行：

~~~bash
specify init <project-name> --integration <native-agent-key> --script py --non-interactive
~~~

## 已有代码目录

先阅读官方 `docs/guides/existing-projects.md`。该流程只为下一项有界变更接入 Spec Kit，不追溯生成既有功能的规格。先提交或 stash 现有改动，并为接入工作创建分支；再向用户展示并取得对确切初始化命令的批准。`--force` 可能覆盖 Spec Kit 托管路径，初始化后检查完整差异再继续。

交互环境运行：

~~~bash
specify init --here --force --integration <native-agent-key> --script py
~~~

非交互环境运行：

~~~bash
specify init --here --force --integration <native-agent-key> --script py --non-interactive
~~~

# 写入目标项目规则

从[项目规则模板](PROJECT_AGENTS_TEMPLATE.md)取得完整规则块，按下列合并规则写入目标项目根目录 `AGENTS.md`：

- 恰有一对完整标记时，只替换标记之间的内容，保留块外全部字节和顺序。
- 没有标记时，在文件末尾追加；原文件全部字节保留为前缀，只有末尾没有换行时才增加分隔换行。文件不存在时，创建只含规则块的 `AGENTS.md`。
- 标记缺失、重复、顺序错误或边界不明确时停止，不猜测范围，也不追加第二个块。
- 按原始字节定位区间，保留编码、BOM 和换行格式。无法可靠保留时停止。

写入后检查差异，确认只新增或替换受管规则块。用户可审阅后提交 `AGENTS.md`、`.specify/**`、`specs/**` 和团队需要共享的官方集成文件；不要提交 CLI 缓存、个人凭据或机器专属状态。目标项目后续会话只依赖项目自身提交的规则和 Spec Kit 状态。

# 上游依据

初始化步骤依据已审阅提交 c00dc0551583428a10a94443c58c6a41e5e0138c 的 `docs/quickstart.md` 和 `docs/guides/existing-projects.md`。目标项目规则块见[独立模板](PROJECT_AGENTS_TEMPLATE.md)；模板复制到目标项目后，目标 Agent 不再依赖本仓库。
