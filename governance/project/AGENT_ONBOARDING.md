# 首次 Agent 入驻

1. 当前 Agent 必须提供 runtime ID 和精确 integration key。只有 display name 时返回 `KEY_REQUIRED`。
2. 读取 `specify version`、`specify --help`；CLI 缺失时输出固定安装建议，等待授权，不静默安装。
3. 运行只读 `doctor` 和 `resolve-agent`。不得把 default、PATH 工具、目录名或相似产品当身份。
4. `.specify/` 已存在时运行 `specify integration status --json`。健康且已有 active binding 时复用；否则生成 onboarding plan。
5. `.specify/` 不存在时先完成 Agent-neutral governance bootstrap，再生成显式 integration 的 `plan-init`。禁止省略 `--integration`。
6. 原生 integration 未安装时，plan 使用 `specify integration install <claimed-key>`，不加 `--force`；multi-install safety 由 CLI gate 决定。
7. 任何 native 目标不可写、权限、sandbox、repair 或安装错误均返回 `NATIVE_INSTALL_BLOCKED`，保留现有状态并停止。
8. context anchor 只能来自 active binding 或用户显式提供的项目相对路径，并需通过 `plan-onboard --anchor-evidence <project-relative-json>` 携带 compatibility evidence。未知或不支持格式时停止。
9. 仅 Loader fresh-session 失败且用户显式请求时才允许 Materialized；此时必须同时提供 `--loader-failure-evidence <project-relative-json>`。
10. 用户使用 `apply-plan --approve-plan-id <id> --approve-plan-sha256 <hash>` 授权后，才执行唯一 apply。
11. 新会话验证 anchor、Loader、Policy version、probe token、runtime ID、integration key、原生 workflow 和既有 inventory 后，保存项目相对 verification evidence，再生成 `plan-activate-binding`；在该计划 apply 前，binding 只能是 `provisional`，不能报告 `READY`。

12. 如果项目已有 `AGENTS.md`，onboarding 只能向其中注入 managed loader；必须保留原有项目规则的全部字节，禁止覆盖、删除、重排或全文件格式化。
