# 适用范围

GitHub Spec Kit 用于实质性软件工程工作。只读调查、解释、极小 typo 修复和极低风险小改动不要求完整生命周期。

# 项目与 brownfield

变更前必须确认真实项目根目录，读取所有适用项目本地规则、README、架构、测试、依赖和 CI，理解真实 brownfield 系统并保护现有用户工作。存在 `.specify/` 时恢复已有项目状态，不得例行重新初始化。

如果项目已经有 `AGENTS.md`，它属于项目共同维护的规则内容。Spec Kit loader 只能通过已审查的 manager plan 追加到该文件，绝不得替换、删除、重排、规范化或覆盖既有字节。只有项目没有 `AGENTS.md` 时，manager 才能通过同一类已审查 plan 创建 loader 文件。

# Agent-neutral 与原生 integration

治理包不预先枚举 Agent 产品。当前 Agent 必须由用户、宿主或 Agent runtime 明确声明 runtime ID 和精确 integration key；display name 不能生成 mutation plan。不得从 PATH、目录名、default integration、相似产品名或 Rich catalog 输出猜测身份。

当前 CLI 为当前 Agent 提供原生 integration 时，原生 integration 是强制要求。Skills/Commands 目标不可写、父目录不可写、权限不足、sandbox 阻断、managed-file repair 失败或 CLI 安装失败均为 `NATIVE_INSTALL_BLOCKED`。不得因为方便、权限、路径或冲突降级 generic、改用其他 key 或报告完成。只有 fresh-session 验证 runtime ID 与 key 匹配、context anchor 已加载且 managed files 健康后，binding 才能为 `active`。

只有当前 CLI 没有原生 integration、项目配置允许、当前版本有人工审查的 native-absence attestation、目标 Agent 与 generic Markdown Commands 契约兼容、项目 installed integration set 为空且用户批准精确 plan 时，才允许 generic。Generic 必须标记为非原生且有限支持。

# Spec Kit 状态与生命周期

新项目必须使用显式 `specify init --here --non-interactive --integration <approved-key>`。非交互 init 省略 key 时 CLI 可能选择默认产品，治理器必须拒绝该命令。非空 brownfield 的 `--force` 只能出现在专用 `plan-init`，且必须有 rehearsal、scope snapshot、备份、精确授权和失败恢复；其他命令不得使用 `--force`。

实质性工作概念上遵循：

`constitution → specify → clarify → plan → checklist → tasks → analyze → implement → validate → converge`

是否触发 clarify、checklist、analyze 由 operation plan 的固定 risk assessment 公式决定；validate 和 converge 是完成门。实现必须与已接受 specification、plan、tasks、项目约束和测试同步。

# Default 与 integration 共存

项目 default integration 使用 pinned 策略。普通 onboarding 不得改变 default。Default change 只有在项目配置一次性开启变更窗口、生成独立 plan、执行 `specify integration use <key>`、status 验证成功后才可更新配置；失败必须恢复旧 default。非 default integration 的 extensions、presets、events 和 shared infrastructure 必须单独验证，不得声称 parity。

# 权威顺序

政策权威顺序为：当前用户指令、更高优先级 runtime、安全规则、所有适用项目本地规则、项目 `LOCAL_OVERRIDES.md`、项目 `POLICY.md`、个人全局 Bootstrap、项目 `REFERENCE.md`、个人中央 Reference、upstream 文档。

运行时事实顺序为：当前项目 `.specify/`、已安装 integration 及 manifest、已安装 CLI、项目 `REFERENCE.md`、个人中央 Reference、upstream 文档。运行时与项目快照冲突时以运行时为准，并记录差异。

# 验证、升级与完成

必须运行相关测试、build、lint、schema、reproduction、validation 和 convergence；不得隐藏失败。CLI、integration、extension、治理包和 Skills 是分离层，升级其中一层不得假定其他层自动升级。中央 upstream 变更必须分类为 `NONE`、`REFERENCE` 或 `POLICY`，checker 只读，baseline 在审查完成后最后推进；不得合并 upstream 历史或自动部署 Policy。

完成必须同时满足用户意图、accepted artifacts、实现、项目约束、validation、convergence、原生 integration、adapter verification 和 capability inventory 守恒。存在 blocker、未映射旧能力、非计划删除、降级、失效或 default 变化时不得报告完成。
