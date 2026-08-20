# Purpose

Spec-Kit-Reference is a compatibility and governance layer for GitHub Spec Kit. It turns a moving upstream project into stable, reviewed, local operational knowledge for coding Agents.

This repository is not a fork of `github/spec-kit` and must not merge upstream history. The two remotes have separate meanings:

- `origin`: this governance repository.
- `upstream`: the official Spec Kit repository used for fetch, diff, and review.

## Repository contents

- `AGENTS.md`: maintenance rules for this repository.
- `global-policy.md`: Agent-neutral policy suitable for deployment to an Agent's global instruction location.
- `SPEC_KIT_REFERENCE.md`: reviewed operational facts and runtime discovery guidance.
- `UPSTREAM_BASELINE`: the latest upstream commit whose impact review is complete.
- `docs/`: update policy, the latest impact assessment, and maintenance history.
- `scripts/`: cross-platform deterministic upstream checkers.
- `.github/workflows/check-spec-kit-upstream.yml`: scheduled and manual notification workflow.

## First-time setup

```powershell
git remote -v
$upstreamUrl = git remote get-url upstream 2>$null
if (-not $upstreamUrl) { git remote add upstream https://github.com/github/spec-kit.git }
git fetch upstream main
git rev-parse upstream/main
```

On macOS/Linux:

```bash
git remote -v
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream https://github.com/github/spec-kit.git
git fetch upstream main
git rev-parse upstream/main
```

The resulting full SHA belongs in `UPSTREAM_BASELINE` only after the initial local review is complete. The baseline means “reviewed through”, not “latest upstream”.

## Checking upstream

From the repository root, use the wrapper for the current platform:

```powershell
.\scripts\check-upstream.ps1
```

On macOS/Linux:

```bash
python3 scripts/check_upstream.py
```

The command fetches `upstream/main`, compares it with `UPSTREAM_BASELINE`, and prints the unreviewed commit list and changed paths. Exit codes are:

- `0`: no unreviewed changes.
- `2`: unreviewed upstream changes exist.
- `1`: the check could not be completed.

The checker never changes `AGENTS.md`, `global-policy.md`, `SPEC_KIT_REFERENCE.md`, `docs/`, or `UPSTREAM_BASELINE`.

The same check is also available as `sh scripts/check-upstream.sh` on POSIX shells.
The PowerShell wrapper uses `python` when available and falls back to the Windows `py -3` launcher.

## Platform support

This repository is intended to be used locally on both Windows and macOS. The Python checker and repository documents are shared; only the shell wrapper and the deployment-time absolute locator vary by platform. The scheduled workflow validates both the POSIX and PowerShell wrappers.

## Reviewing an update

1. Read `AGENTS.md` and `UPSTREAM_BASELINE`.
2. Run the checker and inspect commits, changed paths, and relevant diffs.
3. Classify the update as `NONE`, `REFERENCE`, or `POLICY`.
4. Update only the local documents justified by the evidence.
5. Record the rationale in `docs/CHANGE_IMPACT.md` and `docs/HISTORY.md`.
6. Run local validation.
7. Advance `UPSTREAM_BASELINE` last.

Do not automatically convert upstream prose into Agent instructions. A `POLICY` change requires human review before it is merged or deployed.

## Global policy deployment

`global-policy.md` is the single logical source for the Spec Kit policy. Agent-specific global files should be deployment targets, not independent copies with separate maintenance. The policy is intentionally Agent-neutral and does not prescribe one universal command syntax.

The policy intentionally does not contain a machine-specific path. When deploying it to a global `AGENTS.md`, append a small deployment-specific locator for the canonical local `SPEC_KIT_REFERENCE.md`; otherwise an Agent working in another project has no reliable way to find this repository. The locator must match the machine where that global file is installed. Examples for this project are:

- Windows: `C:\path\to\SPEC_KIT_REFERENCE.md`
- macOS/Linux: `/path/to/SPEC_KIT_REFERENCE.md`

Verify the actual file exists on the target machine before relying on offline reference discovery. Do not copy either example unchanged to a machine with a different user or checkout location.

After copying `global-policy.md`, append the locator in the deployment-only section of the target global `AGENTS.md`. Keep that locator out of this repository's logical policy source so the source remains portable across machines and Agents.

## Runtime reality

For installed command behavior, inspect the local runtime rather than relying only on this repository:

```bash
specify version
specify --help
specify integration list
specify integration status
```

The installed CLI, the generated project integration, this reviewed reference, and upstream may be at different versions. That mismatch is a reason to investigate, not a reason to silently rewrite governance policy.

# Durable design decisions

This section is the durable design record for this repository. Even if the original implementation-plan document is deleted, future Agents must preserve these semantics and must not infer opposite behavior from the repository name or file layout.

## Repository identity

This repository is a Compatibility / Governance Layer for GitHub Spec Kit. It is not a fork, source mirror, or submodule of `github/spec-kit`. `origin` is this governance repository; `upstream` is official Spec Kit and is used only for `fetch`, `log`, `diff`, and impact analysis. Never merge `upstream/main`.

### Authority layers

Keep these layers distinct:

1. The user's explicit instruction and higher-priority runtime rules;
2. Current project-local rules, `.specify/`, `specs/`, and generated integrations;
3. The actually installed `specify` CLI;
4. The local `SPEC_KIT_REFERENCE.md`;
5. Upstream documentation and source.

Global Policy and project rules determine how an Agent should work. The installed runtime determines what the current CLI actually supports. Upstream is reviewed evidence, not a dynamically imported highest-priority instruction source.

### Global Policy and local Reference

`global-policy.md` is the single logical maintenance source for the cross-Agent Policy. Deploy it to each Agent's global instruction file, but do not let deployment copies become independently maintained forks.

The global Policy intentionally contains no machine-specific path. Every global `AGENTS.md` deployment must add a machine-specific absolute path to `SPEC_KIT_REFERENCE.md`; an Agent must not be expected to find this repository by scanning arbitrary directories or by assuming the current project is this repository.

`SPEC_KIT_REFERENCE.md` is an offline operational reference. It is not the highest Policy and must not become a copy of the entire upstream documentation set.

### Engineering workflow principles

For substantive software engineering, identify the real project root, read its rules, and understand the existing brownfield system before changing it. If `.specify/` exists, resume the existing Spec Kit state rather than routinely reinitializing. If it does not exist, initialize only when substantive project-changing work actually requires it.

The Agent-neutral conceptual lifecycle is:

`constitution → specify → clarify → plan → checklist → tasks → analyze → implement → validate → converge`

Use `clarify`, `checklist`, and `analyze` as risk- and ambiguity-driven quality gates, not ceremony. `converge` is the completion gate: append missing tasks when gaps are found, then repeat implement, validate, and converge. Passing tests or exhausting the original task list is not sufficient by itself.

Use the dedicated `bug` extension for substantive bugs when appropriate. The global CLI and project-generated integrations are separate layers. For existing projects, prefer the supported integration/extension upgrade lifecycle; do not assume a global CLI install provides global Agent Skills or manually copy bundled Skills into global directories.

### Upstream review and baseline

`UPSTREAM_BASELINE` means the latest upstream commit whose semantic impact has been reviewed; it does not mean the latest upstream commit. For maintenance: read the baseline, fetch, compare commits/files, inspect relevant diffs, classify impact, update local documents, validate, and advance the baseline last.

Classify impact as:

- `NONE`: no local operational or Policy change;
- `REFERENCE`: operational facts changed, so update the Reference only;
- `POLICY`: methodology, lifecycle, completion semantics, or authority model changed, so review the global Policy.

Never modify or deploy `AGENTS.md` merely because an upstream commit exists. Path priority is only a review aid; combine it with commit messages, diff semantics, and release notes. The detection phase is deterministic; semantic judgment and Policy changes require human review.

### Monitoring and automation boundary

The first automation phase is:

`git fetch → baseline comparison → commit/file report → GitHub Issue notification`

It supports a weekly schedule and `workflow_dispatch`. Do not merge upstream automatically, and do not automatically merge or deploy Policy changes. Future Agent-assisted review and PR creation are possible, but governance Policy PRs still require human review.

### Runtime caveats

`specify integration list` and `specify integration status` are project-aware and may require `.specify/` in the current project. Outside a Spec Kit project, use `specify --help` or `specify integration --help` instead of initializing a project just to discover commands.

Generated Agent integration artifacts may migrate from command layouts to Skills layouts. Treat current project integration status, managed-file metadata, and the installed CLI as authoritative; do not infer current behavior from an older project's directory layout.

# 目的

Spec-Kit-Reference 是 GitHub Spec Kit 的兼容性与治理层。它把持续变化的上游项目转换为稳定、经过审查、可在本地使用的编码 Agent 操作知识。

本仓库不是 `github/spec-kit` 的 fork，禁止合并 upstream 历史。两个 remote 的含义不同：

- `origin`：本治理仓库。
- `upstream`：官方 Spec Kit 仓库，仅用于 fetch、diff 和审查。

## 仓库内容

- `AGENTS.md`：本仓库自身的维护规则。
- `global-policy.md`：适合部署到 Agent 全局规则位置的 Agent-neutral Policy。
- `SPEC_KIT_REFERENCE.md`：经过审查的操作事实和运行时发现指南。
- `UPSTREAM_BASELINE`：已经完成影响审查的最新 upstream commit。
- `docs/`：更新政策、最近一次影响评估和维护历史。
- `scripts/`：跨平台、确定性的 upstream 检查器。
- `.github/workflows/check-spec-kit-upstream.yml`：定期和手动通知工作流。

## 首次设置

Windows PowerShell：

```powershell
git remote -v
$upstreamUrl = git remote get-url upstream 2>$null
if (-not $upstreamUrl) { git remote add upstream https://github.com/github/spec-kit.git }
git fetch upstream main
git rev-parse upstream/main
```

macOS/Linux：

```bash
git remote -v
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream https://github.com/github/spec-kit.git
git fetch upstream main
git rev-parse upstream/main
```

只有在完成首次本地审查后，才能把得到的完整 SHA 写入 `UPSTREAM_BASELINE`。baseline 的含义是“已经审查到这里”，不是“当前 upstream 最新版本”。

## 检查 upstream

在仓库根目录使用当前平台对应的包装器：

Windows PowerShell：

```powershell
.\scripts\check-upstream.ps1
```

macOS/Linux：

```bash
python3 scripts/check_upstream.py
```

命令会 fetch `upstream/main`，将它与 `UPSTREAM_BASELINE` 比较，并输出尚未审查的 commit 列表和变更路径。退出码为：

- `0`：没有尚未审查的变化。
- `2`：存在尚未审查的 upstream 变化。
- `1`：检查无法完成。

检查器不会修改 `AGENTS.md`、`global-policy.md`、`SPEC_KIT_REFERENCE.md`、`docs/` 或 `UPSTREAM_BASELINE`。

在 POSIX shell 中也可以使用 `sh scripts/check-upstream.sh`。PowerShell 包装器优先使用 `python`，不可用时回退到 Windows 的 `py -3` 启动器。

## 平台支持

本仓库设计为同时在 Windows 和 macOS 本地使用。Python 检查器和仓库文档是共用的；只有 shell 包装器以及部署时使用的绝对路径随平台变化。定期工作流会验证 POSIX 和 PowerShell 两种包装器。

## 审查更新

1. 读取 `AGENTS.md` 和 `UPSTREAM_BASELINE`。
2. 运行检查器，检查 commit、变更路径和相关 diff。
3. 将影响分类为 `NONE`、`REFERENCE` 或 `POLICY`。
4. 只更新有证据支持的本地文档。
5. 将理由记录到 `docs/CHANGE_IMPACT.md` 和 `docs/HISTORY.md`。
6. 执行本地验证。
7. 最后推进 `UPSTREAM_BASELINE`。

不要自动把 upstream 文案转换为 Agent 指令。`POLICY` 变化在合并或部署前必须经过人工审查。

## 全局 Policy 部署

`global-policy.md` 是 Spec Kit Policy 的唯一逻辑源。各 Agent 的全局文件应是部署目标，不应成为分别维护的独立副本。Policy 有意保持 Agent-neutral，不规定一种统一命令语法。

Policy 有意不包含机器专属路径。部署到全局 `AGENTS.md` 时，必须追加一个指向本地规范 `SPEC_KIT_REFERENCE.md` 的部署专属 locator；否则，在其他项目中工作的 Agent 没有可靠方式找到本仓库。locator 必须匹配安装该全局文件的机器。本项目的示例为：

- Windows：`C:\path\to\SPEC_KIT_REFERENCE.md`
- macOS/Linux：`/path/to/SPEC_KIT_REFERENCE.md`

依赖离线 Reference 前，应先在目标机器验证实际文件存在。不同用户或 checkout 位置不能直接照搬上述示例。

复制 `global-policy.md` 后，将 locator 追加到目标全局 `AGENTS.md` 的部署专属区段。该 locator 应留在部署层，不要写回本仓库的逻辑 Policy 源，以保持源文件跨机器、跨 Agent 可移植。

## 运行时现实

对于已安装命令的行为，应检查本地运行时，而不能只依赖本仓库：

```bash
specify version
specify --help
specify integration list
specify integration status
```

本机 CLI、生成的项目 integration、本地 Reference 和 upstream 可能处于不同版本。出现不一致时应调查原因，而不是静默改写治理 Policy。

# 持久化设计决策

本节记录删除原始实施方案后仍必须保留的语义。后续 Agent 必须保持这些约束，不能根据仓库名称或文件结构自行推断出相反行为。

## 仓库定位

本仓库是 GitHub Spec Kit 的 Compatibility / Governance Layer，不是 `github/spec-kit` 的 fork、源码镜像或 submodule。`origin` 是本治理仓库；`upstream` 是官方 Spec Kit，仅用于 `fetch`、`log`、`diff` 和影响分析。禁止 merge `upstream/main`。

### 权威层次

必须区分以下层次：

1. 用户当前明确指令和更高优先级运行时规则；
2. 当前项目本地规则、`.specify/`、`specs/` 和已生成的 integration；
3. 当前实际安装的 `specify` CLI；
4. 本地 `SPEC_KIT_REFERENCE.md`；
5. upstream 文档和源码。

全局 Policy 和项目规则决定 Agent 应如何工作。已安装运行时决定当前 CLI 实际支持什么。upstream 是经过审查的证据，不是动态导入的最高优先级指令源。

### 全局 Policy 与本地 Reference

`global-policy.md` 是跨 Agent Policy 的唯一逻辑维护源。应将它部署到各 Agent 的全局规则文件，但不能让部署副本变成独立维护的分叉。

全局 Policy 有意不包含机器专属路径。每次部署到全局 `AGENTS.md` 时，都必须添加指向 `SPEC_KIT_REFERENCE.md` 的机器专属绝对路径；不能要求 Agent 扫描任意目录，也不能假设当前项目就是本仓库。

`SPEC_KIT_REFERENCE.md` 是离线操作参考，不是最高 Policy，也不应变成完整 upstream 文档的复制品。

### 软件工程工作原则

对于实质性软件工程工作，先识别真实项目根目录，读取项目规则，并在修改前理解已有 brownfield 系统。如果存在 `.specify/`，继续已有 Spec Kit 状态，不要例行重新初始化。如果不存在，只有在确实需要进行实质性项目变更时才初始化。

Agent-neutral 的概念生命周期是：

`constitution → specify → clarify → plan → checklist → tasks → analyze → implement → validate → converge`

将 `clarify`、`checklist` 和 `analyze` 作为由风险和歧义驱动的质量门，而不是机械仪式。`converge` 是完成门：发现遗漏时追加任务，然后重复 `implement`、`validate` 和 `converge`。测试通过或原始任务列表耗尽本身并不足以代表完成。

对于实质性 bug，在适当情况下使用专门的 `bug` extension。全局 CLI 与项目生成的 integration 是两个独立层。已有项目应优先使用受支持的 integration/extension 升级生命周期；不能假设全局 CLI 安装会提供全局 Agent Skills，也不要手工把 bundled Skills 复制到全局目录。

### upstream 审查与 baseline

`UPSTREAM_BASELINE` 表示最近一个已经完成语义影响审查的 upstream commit，不表示 upstream 最新 commit。维护时依次读取 baseline、fetch、比较 commit/文件、检查相关 diff、分类影响、更新本地文档、验证，最后推进 baseline。

影响分类为：

- `NONE`：不改变本地操作知识或 Policy；
- `REFERENCE`：操作事实发生变化，只更新 Reference；
- `POLICY`：方法论、生命周期、完成语义或权威模型发生变化，因此审查全局 Policy。

不能仅因为存在 upstream commit 就修改或部署 `AGENTS.md`。路径优先级只是审查辅助，必须与 commit message、diff 语义和 release notes 结合。检测阶段是确定性的；语义判断和 Policy 更新需要人工审查。

### 监测与自动化边界

第一阶段的自动化是：

`git fetch → baseline comparison → commit/file report → GitHub Issue notification`

支持每周 schedule 和 `workflow_dispatch`。禁止自动 merge upstream，也禁止自动 merge 或部署 Policy 变化。未来可以增加 Agent-assisted review 和自动 PR，但治理 Policy 的 PR 仍需人工审查。

### 运行时注意事项

`specify integration list` 和 `specify integration status` 是 project-aware 命令，可能要求当前项目存在 `.specify/`。在 Spec Kit 项目之外，应使用 `specify --help` 或 `specify integration --help`，不要仅为了发现命令而初始化项目。

生成的 Agent integration 产物可能从 command layout 迁移到 Skills layout。应以当前项目的 integration status、managed-file metadata 和已安装 CLI 为权威；不能从旧项目或其他 Agent 的目录布局推断当前行为。
