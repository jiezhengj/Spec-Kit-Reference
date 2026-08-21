# 进入项目

1. 确认实际项目根目录。
2. 读取 `docs/spec-kit/PROJECT_CONFIG.json`、`LOCAL_OVERRIDES.md`、`POLICY.md` 和 `MANIFEST.json`。
3. 涉及 CLI、integration、extension、init、upgrade、rollback 或恢复时，继续读取 `REFERENCE.md` 和 `OPERATING_PROTOCOL.md`。
4. 检查 `.specify/`。存在则恢复现有状态，不得重复初始化。
5. 不把项目 default integration 当成当前 Agent 身份；当前 Agent 必须提供 runtime ID 和精确 integration key。
6. 未完成当前 Agent onboarding 前，不得宣称该 Agent 已完成原生 Spec Kit 接入。
7. 所有 mutation 先生成 operation plan，再由当前操作者以精确 plan ID 和 hash 授权，最后运行唯一的 `apply-plan`。
8. native integration 的目标不可写、权限不足、sandbox 阻断、managed-file repair 失败或安装失败时，停止并返回 `NATIVE_INSTALL_BLOCKED`，不得转 generic 或其他 key。

项目治理包是团队共同基线，不依赖个人全局规则或中央 Reference 目录。中央 Reference 只能用于显式更新审查。
