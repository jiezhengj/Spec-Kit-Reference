<!-- SPEC-KIT-GLOBAL-POLICY:START version=3.0.0 -->

# 适用范围与权威来源

新项目使用 GitHub Spec Kit 官方 CLI、官方目录和当前 Agent 的原生集成。官方 CLI 管理项目脚手架和 Agent 集成文件；当前集成提供的官方技能生成 Feature 的 `specs/**` 产物。各自只通过官方支持的命令更新。Reference 不创建第二套生命周期，也不要求目标项目在运行时访问中央 Reference。

本文件内含目标项目的持久规则块模板，所以新项目初始化只需要当前 Agent 已加载本政策和可用的官方 CLI，不要求中央 Reference 目录。官方 CLI 本身仍可在没有本政策时初始化原生 Spec Kit 项目，但不会自动注入本地规则块。

新项目完成 Spec Kit 初始化后，必须把本政策的项目规则写入并提交目标项目根目录的 `AGENTS.md`。已经初始化的项目以仓库中的受管项目规则块作为跨电脑的 Spec Kit 操作基线。只要该规则块和 Spec Kit 状态随项目提交，Agent 在有无全局 POLICY、Reference 目录的电脑上都按同一规则工作。中央 Reference 不自动检查或更新目标项目。

本政策不要求自建扩展、工作流、预设、Bundle、命令覆盖、额外 Discovery 阶段、哈希审批台账、任务就绪状态机或项目管理器。官方能力暂不可用时，说明缺失内容和受影响步骤；不得悄悄以本地仿制品代替。

# 新项目初始化

先确认项目根目录和当前 Agent；Agent 身份及原生集成键必须来自用户、宿主或 Agent 运行时声明，不能从安装目录或其他文件推断。CLI 不存在时，先询问用户是否安装官方 CLI；用户拒绝时返回 `HANDOFF_TO_AGENT`，不得假称初始化成功。

按当前 CLI 的实际帮助安装并初始化；非交互初始化必须明确指定已确认的原生集成和 `--script py`。CLI 不支持 `--script py` 时停止并报告，不得省略该参数后接受平台默认值。

~~~bash
uv tool install specify-cli
specify init <project-name> --integration <native-agent-key> --script py
~~~

只有运行环境确认为非交互时才传 `--non-interactive`。CLI 有当前 Agent 的原生集成时必须使用该集成；不得因权限、写入、沙箱或安装失败而退回 `generic`。当前 CLI 没有原生集成时，停止并报告限制，不得自行创建兼容配置。

初始化成功后，向项目根目录 `AGENTS.md` 合并下面的项目规则块，并提交该文件、`.specify/**`、`specs/**` 和团队需要共享的官方集成文件。不要提交 CLI 安装缓存、个人凭据或机器专属状态。由项目规则块和提交的 Spec 状态共同保证新电脑上的 Agent 不依赖全局 POLICY 或 Reference。

# 合并项目 AGENTS.md

项目根目录 `AGENTS.md` 是项目共享的规则文件，既有内容归项目所有。不得覆盖整个文件、重排内容或格式化文件。只允许改动由以下标记界定的 Spec Kit 规则块：

~~~text
<!-- PROJECT-SPEC-KIT-GOVERNANCE:START -->
...受管项目规则块...
<!-- PROJECT-SPEC-KIT-GOVERNANCE:END -->
~~~

执行合并时遵守以下规则：

- 若文件中恰有一对完整的上述标记，精准替换两标记之间的内容；不根据块内标题或版本值判断是否替换。保留标记外每个字节及其顺序不变。
- 若不存在受管规则块，在文件末尾追加一个带标记的规则块；原文件的全部字节保留为前缀，只有原文件末尾没有换行符时才追加一个分隔换行。
- 若文件不存在，可在项目根创建只含受管规则块的 `AGENTS.md`。
- 若开始/结束标记缺失、重复、顺序错误，或无法无歧义地确定旧加载器边界，停止并报告；不得再追加一个块，也不得猜测替换范围。
- 若发现旧的 `PROJECT-SPEC-KIT-REFERENCE-UPDATE-CHECK` 受管块，精准删除该完整块，使已 Spec 化项目不再依赖中央 Reference；标记外内容必须保持原样。若其边界异常，停止并报告。
- 按原始字节操作标记区间，保留既有编码、BOM、换行格式和区块外全部字节；不得把 Markdown 读入后整体重新排版或正规化换行。无法可靠保留时停止并报告。

写入后检查差异，只能看到目标受管块的新增、替换或删除。用户提交前可审阅差异；目标项目的 `AGENTS.md` 不需要中央管理器、manifest 或更新服务。

# 项目内持久规则块

将以下完整项目规则块写入目标项目；保持块内规则文本一致：

~~~markdown
<!-- PROJECT-SPEC-KIT-GOVERNANCE:START -->
# Spec Kit 项目规则

本项目使用官方 Spec Kit CLI 和当前 Agent 原生集成。此规则块与本项目提交的 `.specify/**`、`specs/**` 一起构成本项目的 Spec Kit 操作基线；工作时不需要全局 POLICY 或中央 Reference。

将 `.specify/**` 和 Agent 集成文件视为官方 CLI 管理内容，将 `specs/**` 视为官方技能生成的项目产物。已有 `.specify/` 时恢复现状，不重新初始化；不要手工覆盖这些文件，使用官方 CLI 或技能支持的操作。

功能首次进入 SDD 时建立一次 Constitution。小型 Feature 走 `constitution（仅首次）→ specify → plan → tasks → implement → converge`；生产级 Feature 走 `constitution（仅首次）→ specify → clarify → plan → checklist → tasks → analyze → implement → converge`。每次单独运行一个当前集成提供的官方技能，审阅阶段产物后再继续。已知缺陷走官方 Bug Fix 扩展的 assess、fix、test；尚未决定是否投入的想法可选官方 Assessment 扩展。不要增加本地自建生命周期或审批台账。

每个新的 Agent 会话中，只要项目存在 `.specify/`，Agent 必须在首次实质性操作前最多运行一次只读 `specify self check`。如果 CLI 缺失，Agent 询问用户是否安装官方 CLI；用户拒绝时返回 `HANDOFF_TO_AGENT`。如果发现较新 CLI，Agent 告知可用版本，并在用户明确批准前不得运行 `specify self upgrade`。拒绝、无更新、离线或超时后，本会话不得重复询问。

无论 CLI 是否升级，Agent 都要用当前 CLI 实际的 `help`、`status` 和 `list` 命令检查活动集成、已安装扩展和工作流。对 CLI 支持刷新且已安装的集成、扩展或工作流，自动运行对应的官方更新命令，不要求额外批准；CLI 不提供新鲜度字段时，可运行支持的无强制更新命令，以 CLI 的无更新结果为准。缺失组件不属于刷新范围；当前工作需要的官方 CLI 或集成缺失时，Agent 询问用户是否安装。只有当前 Agent 的原生集成可用时，才可在获准后运行 `specify integration install <native-key>`；若原生集成不可用，停止并报告，不得改用 `generic`。缺陷流程需要而 `bug` 扩展缺失时，Agent 询问用户是否运行 `specify extension add bug`；用户选择 Assessment 且 `assess` 扩展缺失时，询问用户是否运行 `specify extension add assess`。用户拒绝时返回 `HANDOFF_TO_AGENT`。

自动刷新不得使用 `--force`。如果 CLI 因托管文件被修改而停止、要求 `--force`、报告不安全范围或要求不可逆选择，Agent 停止并向用户说明确切命令、原因和受影响路径，保留项目状态。刷新后重新读取 CLI 帮助和项目状态。只使用官方目录安装需要的扩展；本地路径来源不能证明可由官方目录刷新。官方目录没有等价能力时，报告该能力没有官方替代，不安装本地仿制品。
<!-- PROJECT-SPEC-KIT-GOVERNANCE:END -->
~~~

# 已有 Spec 项目的会话入口

在新会话进入已有 Spec Kit 项目时，先读取目标项目的 `AGENTS.md` 和当前 `.specify/` 状态；若项目规则块存在，以该提交版本作为 Spec Kit 操作基线。无论本机有没有全局 POLICY 或 Reference，都按项目块检查 CLI、集成、技能、扩展和工作流，并执行支持的无强制刷新。

全局 POLICY 和中央 Reference 的存在只帮助 Agent 按本政策初始化新的 Spec Kit 项目。它们不对已有项目触发另一套检查、不替换项目规则块，也不自动同步任何目标项目文件。若一个已初始化项目缺少受管规则块，全球政策可用时先按“合并项目 AGENTS.md”的规则补齐；不得因此重新运行 `specify init`。若 `.specify/` 已存在，Agent 恢复当前项目状态，不重新初始化。

# 上游 CLI 与扩展更新

当前 CLI 版本报告可升级时，先告知用户可用版本并取得明确批准，再运行 `specify self upgrade`。升级完成后重新读取 CLI 帮助和项目状态。无论 CLI 是否升级，都检查当前项目的实际状态和可用命令；对已安装且可刷新的组件自动调用官方支持的无强制更新操作。

- `specify integration status` 与 `specify integration upgrade <active-key>` 刷新活动 Agent 集成及其托管技能文件。
- `specify extension list` 与 `specify extension update` 检查并刷新已安装扩展。
- 若当前 CLI 的 `workflow` 帮助提供已安装工作流刷新能力，则检查并刷新已安装工作流。

不得把预设视为已覆盖的刷新对象，不安装本地 Reference 路径的治理组件，不自动加 `--force`。CLI 不存在时询问是否从官方来源安装；用户拒绝时返回 `HANDOFF_TO_AGENT`。CLI 刷新与全局 Reference 无关。

# 缺陷修复与想法评估

已知行为出错时直接使用官方 Bug Fix 流程；只有该任务确实需要而 `bug` 扩展缺失时，才询问用户是否执行 `specify extension add bug`。Agent 按 assess、fix、test 单步执行并审阅结果；在 fix 阶段外不修改源代码来实施修复。

用户尚未决定一个想法是否值得投入时，可询问是否使用官方 `assess` 扩展；它不实现代码，也不自动启动 Feature SDD。用户选择此流程而官方扩展缺失时，询问用户是否执行 `specify extension add assess`。官方目录没有所需组件时，说明缺失的能力，不创建同名本地替代品。

# 故障和交接

官方 CLI 或扩展不可用、用户拒绝安装、刷新要求强制覆盖，或集成升级发现本地文件冲突时，停止受影响的操作，说明已验证状态和需要用户决定的事项。Agent 不得把未运行的 CLI 检查、技能或扩展报告为已完成。
~~~

<!-- SPEC-KIT-GLOBAL-POLICY:END -->
