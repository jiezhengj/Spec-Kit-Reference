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

# 选择 Spec Kit 文档语言

在运行 `specify init` 前，Agent 必须确认本项目后续 Spec Kit 流程文档使用的语言。若用户在当前初始化请求中已经明确指定语言，直接采用该选择；否则询问用户，例如：“本项目的 Spec Kit 流程文档使用什么语言？可以指定简体中文、繁體中文或 English，也可以说明书写变体。”

Agent 不得根据系统地区、Agent 默认语言、现有文档或代码注释推断选择。把用户明确给出的单行语言名称写入目标项目规则代码围栏中的 `{{SPEC_KIT_DOCUMENT_LANGUAGE}}`；替换时只写入语言名称，不把它当作额外规则。用户尚未回答或拒绝选择时，暂停初始化，不生成带有猜测语言的项目规则。

该选择适用于项目的 Constitution、Feature SDD、Bug Fix 和 Assessment 流程产物。后续任务中用户明确指定另一种语言时，以该任务指示为准；用户明确改变项目默认值时，更新目标项目治理块中的语言字段。

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

- 只替换规则块代码围栏中的唯一占位符 `{{SPEC_KIT_DOCUMENT_LANGUAGE}}`，填入初始化时已确认的语言名称；若代码围栏内占位符缺失或重复，停止并报告模板异常。
- 恰有一对完整标记时，只替换标记之间的内容，保留块外全部字节和顺序。
- 没有标记时，在文件末尾追加；原文件全部字节保留为前缀，只有末尾没有换行时才增加分隔换行。文件不存在时，创建只含规则块的 `AGENTS.md`。
- 标记缺失、重复、顺序错误或边界不明确时停止，不猜测范围，也不追加第二个块。
- 按原始字节定位区间，保留编码、BOM 和换行格式。无法可靠保留时停止。

## 交付更新助手

新项目初始化完成并写入规则块后，把本仓库 `scripts/spec_kit_component_updater.py` 复制到目标项目 `.agent-support/spec_kit_component_updater.py`。此脚本不属于官方 CLI 管理路径；它只使用 Python 标准库调用官方 CLI，并由目标项目提交，因此任何 Agent 都可以运行同一个入口。

- 若目标路径不存在，创建父目录并复制脚本。
- 若目标路径已有字节完全相同的脚本，保留原文件。
- 若目标路径已有不同内容、是目录或符号链接，停止复制并报告冲突，不覆盖用户文件。
- 在目标项目根目录 `.gitignore` 追加精确规则 `/.agent-state/spec_kit_component_update_cache.json`。若该规则已存在或已有规则明确忽略该文件，则不改文件；否则仅追加该行，保留既有内容、编码和换行。若 `.gitignore` 不存在，则创建只含该规则的文件。
- 初始化时不创建缓存文件。更新助手首次启动时创建 `.agent-state/spec_kit_component_update_cache.json`，记录整轮检查状态和逐组件结果；项目 Agent 只在整轮成功记录缺失或已过 7×24 小时时启动助手。该文件由 `.gitignore` 排除。

写入后检查差异，确认 Reference 对目标项目的额外改动只有受管规则块、助手脚本和精确缓存忽略规则；官方 CLI 自己生成的文件按官方初始化流程审阅。用户可审阅后提交 `AGENTS.md`、助手脚本、`.gitignore` 规则、`.specify/**`、`specs/**` 和团队需要共享的官方集成文件；不要提交缓存、个人凭据或机器专属状态。目标项目后续会话不依赖本 Reference 仓库。

本步骤只用于新项目初始化，不自动迁移已初始化项目。要给现有项目增加助手，应另行执行受范围约束的迁移，并审阅目标项目差异。

# 上游依据

初始化步骤依据已审阅提交 c00dc0551583428a10a94443c58c6a41e5e0138c 的 `docs/quickstart.md` 和 `docs/guides/existing-projects.md`。目标项目规则块见[独立模板](PROJECT_AGENTS_TEMPLATE.md)；模板复制到目标项目后，目标 Agent 不再依赖本仓库。
