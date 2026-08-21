# 只读预检

确认项目根目录，读取本目录全部治理文件，检查 Git 状态、`.specify/`、manifest、config、adapter、CLI 版本和 integration status。只读命令不得创建 `.specify/`、plan、backup 或 binding。

# 治理包 bootstrap

Portable artifact 解压到 `.spec-kit-governance/staging/<plan-id>/`，校验 manifest 和 SHA-256，从 staging manager 生成 `plan-governance-bootstrap`。Bootstrap 只写 `docs/spec-kit/`、根 Loader、manager、manifest 和 config，不安装当前 Agent integration。用户按精确 plan ID/hash 授权后运行 apply，再用项目 manager verify。

# 新项目

没有 `.specify/` 时，先取得明确 approved key，在临时目录用同 CLI/key rehearsal，生成 external mutation scope。非空 brownfield 只允许专用 `plan-init` 使用 `specify init --here --force --non-interactive --integration <key>`；空项目使用无 force 命令。实际变更后比较 scope inventory、status 和 managed files；逃逸或恢复不完整返回 `RECOVERY_REQUIRED`。

# 已有项目

运行 `specify integration status --json`。缺失、modified、invalid 或阻断 finding 返回 `STATE_BROKEN`；当前 runtime 对应 native repair 不可写时返回 `NATIVE_INSTALL_BLOCKED`。不得重跑 init 制造重复规范。

# Native onboarding

候选 key 安装健康只产生 `NATIVE_CANDIDATE_INSTALLED_UNVERIFIED`。必须写入用户提供的 anchor，并在 `plan-onboard` 中提供 `--anchor-evidence <project-relative-json>`；随后执行 fresh-session loader 验证，并确认 runtime ID 与 key 一致；验证前不得 active、READY 或宣称完整。

Fresh-session 证据必须是项目相对 JSON，至少证明 runtime ID、integration key、fresh session、Loader 已加载和 managed files 已验证。使用 `plan-activate-binding` 及精确 approval hash 后，binding 才能变成 `active`。

只有 Loader fresh-session 明确失败且用户主动选择时，才允许 Materialized；此时 `plan-onboard` 必须同时提供 `--delivery-mode materialized --loader-failure-evidence <project-relative-json>`。不得把 Materialized 当作 native 写入失败时的降级路径。

# Generic

`generic` 不得进入 native 分支。V1 只允许在 project config 允许、current-version native-absence attestation 有效、installed integration set 为空、Markdown Commands 兼容性已验证且用户批准时使用。项目已有任一 integration 时返回 `INTEGRATION_CONFLICT`；V1 不实现迁移到 generic。

# Native blocker

Native init target、integration target、managed file repair、anchor 或父目录不可写，权限拒绝，sandbox 阻断或部分安装失败时：保留并清点现有状态；返回 `NATIVE_INSTALL_BLOCKED`；请求可写 checkout 或权限；修复后使用同一 claimed key 重新生成 plan。不得 generic fallback、切换其他 key 或删除已有产物。

# 升级与回滚

中央 source 只读读取固定 release index。先生成 `plan-upgrade`，审查 Policy、Reference、manager、adapter、manifest 和 capability inventory，再用 apply。升级前后 inventory 必须等价，除非每项变化都有批准的 `REPLACE`。回滚不卸载 integration、不删除用户工作；失败恢复不完整返回 `RECOVERY_REQUIRED`。
