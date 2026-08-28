# Purpose

Spec-Kit-Reference is a reviewed compatibility and governance layer for [GitHub Spec Kit](https://github.com/github/spec-kit). It converts a moving upstream project into stable local Policy, runtime reference material, and a portable governance package that can be committed with a business project.

This repository is not a fork, mirror, or submodule of `github/spec-kit`. `origin` is this governance repository; `upstream` is the official Spec Kit repository and is used only for fetch, diff, and impact review. Never merge upstream history into this repository.

# 用途

Spec-Kit-Reference 是经过审查的 [GitHub Spec Kit](https://github.com/github/spec-kit) 兼容性与治理层。它将持续变化的上游项目转化为稳定的本地 Policy、运行时参考资料，以及可随业务项目一同提交的可移植治理包。

本仓库不是 `github/spec-kit` 的 fork、镜像或 submodule。`origin` 是本治理仓库；`upstream` 是官方 Spec Kit 仓库，仅用于 fetch、diff 和影响审查。绝不得把上游历史合并到本仓库。

# Repository layout

The repository has three distinct layers.

## Central policy and reference

- [AGENTS.md](AGENTS.md) contains maintenance rules for this repository.
- [GLOBAL_POLICY.md](GLOBAL_POLICY.md) is the single deployable, Agent-neutral global Policy template.
- [SPEC_KIT_REFERENCE.md](SPEC_KIT_REFERENCE.md) records reviewed operational facts and runtime discovery guidance.
- [UPSTREAM_BASELINE](UPSTREAM_BASELINE) records the latest upstream commit whose semantic impact has been reviewed.

## Portable project governance

The `governance/` tree is the source for the package committed into a business project. A project receives a self-contained `docs/spec-kit/` package and a project-local `tools/spec-kit-governance/governance.py` manager. It is a collaborator's offline baseline and does not depend on a maintainer's global rules or local Reference directory.

The package is deliberately Agent-neutral. During onboarding, a concrete Agent supplies its runtime identity, exact Spec Kit integration key, and project context anchor. The package never pre-registers a fixed list of Agent brands.

## Central implementation and maintenance material

The `docs/` directory contains central English implementation, deployment, migration, operations, security, test, upstream-review, and history documents. They are maintenance contracts and are not copied into business projects; only the portable package under `docs/spec-kit/` is copied.

# 仓库结构

本仓库由三个彼此分离的层组成。

## 中央 Policy 与 Reference

- [AGENTS.md](AGENTS.md) 包含本仓库的维护规则。
- [GLOBAL_POLICY.md](GLOBAL_POLICY.md) 是唯一可部署、与 Agent 无关的全局 Policy 模板。
- [SPEC_KIT_REFERENCE.md](SPEC_KIT_REFERENCE.md) 记录已审查的运行事实和运行时发现指南。
- [UPSTREAM_BASELINE](UPSTREAM_BASELINE) 记录最近一次已完成语义影响审查的上游提交。

## 可移植项目治理

`governance/` 目录树是要提交到业务项目中的治理包源代码。项目会获得自包含的 `docs/spec-kit/` 包，以及项目本地的 `tools/spec-kit-governance/governance.py` manager。它是协作者的离线基线，不依赖维护者的全局规则或本地 Reference 目录。

该包刻意保持 Agent-neutral。onboarding 时，具体 Agent 提供其 runtime identity、精确的 Spec Kit integration key 和项目 context anchor。该包绝不预先登记固定的 Agent 品牌列表。

## 中央实施与维护材料

`docs/` 目录包含中央维护所用的英文实施、部署、迁移、运维、安全、测试、上游审查和历史文档。它们是维护契约，不会复制到业务项目；只有 `docs/spec-kit/` 下的可移植包会被复制。

# Prerequisites

Repository maintenance requires Git and Python 3. The `specify` CLI is needed for runtime discovery and real-project validation. The installed CLI and current project state are authoritative; do not assume that its version matches the reviewed Reference.

If the CLI is missing, an Agent must request authorization before installation. The approved V1 form is pinned to the immutable upstream commit recorded in the release manifest:

~~~bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@<approved-40-character-commit-sha>
~~~

Do not silently install the CLI, use a floating `main` branch, or treat a global CLI installation as proof that Agent-specific project Skills exist.

# 前置条件

维护仓库需要 Git 和 Python 3。运行时发现和真实项目验证需要 `specify` CLI。已安装的 CLI 和当前项目状态是权威；不得假定其版本与经审查的 Reference 一致。

如果 CLI 缺失，Agent 必须先请求授权，才能安装。获准的 V1 形式固定到 release manifest 中记录的不可变上游提交：

~~~bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@<approved-40-character-commit-sha>
~~~

不得静默安装 CLI，不得使用浮动的 `main` 分支，也不得把全局 CLI 安装视为 Agent 专属项目 Skills 已存在的证明。

# Runtime authority

When sources disagree, operational mechanics use this order:

1. Current project Spec Kit state and project-local rules.
2. Installed project integration and its managed-file metadata.
3. Installed `specify` CLI.
4. Committed project `docs/spec-kit/REFERENCE.md`.
5. This repository's `SPEC_KIT_REFERENCE.md`.
6. Upstream documentation and source as reviewed evidence.

Upstream content is never dynamically imported as a higher-priority instruction source. Explicit user instructions, higher-priority runtime rules, and applicable project-local rules always take precedence.

# 运行时权威顺序

当来源之间冲突时，运行机制按以下顺序确定：

1. 当前项目的 Spec Kit 状态和项目本地规则。
2. 已安装的项目 integration 及其 managed-file metadata。
3. 已安装的 `specify` CLI。
4. 已提交的项目 `docs/spec-kit/REFERENCE.md`。
5. 本仓库的 `SPEC_KIT_REFERENCE.md`。
6. 作为已审查证据的上游文档和源代码。

上游内容绝不会被动态导入为更高优先级的指令来源。明确的用户指令、更高优先级的运行时规则和适用的项目本地规则始终优先。

# Global Policy deployment

[GLOBAL_POLICY.md](GLOBAL_POLICY.md) is the only global Policy template. It is a Markdown document with one H1 title and H2 policy sections, wrapped in `<!-- SPEC-KIT-GLOBAL-POLICY:START version=1.1.0 -->` and `<!-- SPEC-KIT-GLOBAL-POLICY:END -->`. The deployment renderer fills this deployment-time locator:

~~~text
SPEC_KIT_GOVERNANCE_SOURCE: <ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>
~~~

For each Agent product actually in use: identify its real global rule file, render a temporary copy of `GLOBAL_POLICY.md` with this repository's absolute path, copy the rendered marker block into that rule file, preserve all content outside the block, and verify in a fresh session.

Do not permanently write a personal absolute path into the committed source template. Do not guess rule locations, append a second locator, or deploy the deployment protocol itself as global Policy. The exact marker grammar, backup, no-clobber, atomic replacement, recovery, and fresh-session verification procedure is in [docs/GLOBAL_POLICY_DEPLOYMENT.md](docs/GLOBAL_POLICY_DEPLOYMENT.md); it is needed for a global deployment or audit, not normal project work.

# 全局 Policy 部署

[GLOBAL_POLICY.md](GLOBAL_POLICY.md) 是唯一的全局 Policy 模板。它是包含一个 H1 标题和 H2 Policy 章节的 Markdown 文档，由 `<!-- SPEC-KIT-GLOBAL-POLICY:START version=1.1.0 -->` 与 `<!-- SPEC-KIT-GLOBAL-POLICY:END -->` 包裹。部署 renderer 填写以下仅在部署时使用的 locator：

~~~text
SPEC_KIT_GOVERNANCE_SOURCE: <ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>
~~~

对于每个实际在用的 Agent 产品：确认其真正的全局规则文件；用本仓库绝对路径渲染 `GLOBAL_POLICY.md` 的临时副本；把渲染后的 marker block 复制进该规则文件；保留 block 外的所有内容；并在新的会话中验证。

不得把个人绝对路径永久写入已提交的源模板。不得猜测规则位置、追加第二个 locator，或把部署协议本身部署为全局 Policy。精确的 marker grammar、备份、no-clobber、原子替换、恢复和新会话验证流程见 [docs/GLOBAL_POLICY_DEPLOYMENT.md](docs/GLOBAL_POLICY_DEPLOYMENT.md)；它用于全局部署或审计，不用于普通项目工作。

# Project governance workflow

For substantive work in a business project:

1. Find the actual project root.
2. Read applicable project-local rules and inspect the brownfield system.
3. Check for `.specify/`; resume existing Spec Kit state when it exists.
4. If the project is not governed, install the portable package into `docs/spec-kit/` through a reviewed operation plan.
5. Resolve the current Agent with an explicit runtime ID and exact integration key.
6. Install or repair the native integration through a reviewed plan.
7. Write the project context anchor and carry compatibility evidence.
8. Verify the integration in a fresh Agent session.
9. Activate the binding only after verification evidence is approved.

Every mutation uses a two-stage plan/apply protocol. Approve the exact plan ID and hash before `apply-plan`. Native integration failure is a blocker: an unwritable target, permission error, sandbox restriction, repair failure, or CLI installation failure must never silently become `generic`.

This plan/apply rule governs mutations owned by this Reference package. It does not replace the upstream Spec Kit feature workflow. After a substantive discussion, approval such as “方案可以”, “按这个来”, “没问题”, or “就这么改” authorizes the Agent to align the direction with the current upstream specification, plan, and tasks; it does not authorize direct application-code edits that skip that alignment. Discussion-only work does not edit application files. If the direction is already aligned, the Agent may continue from the appropriate upstream handoff; if scope, assumptions, risks, or affected components change, it must update the upstream artifacts before continuing.

If the project already has the runtime-selected project context anchor, it is project-owned instruction content. The governance loader may only be appended or updated inside its managed region through the reviewed manager plan; every byte outside that region must remain byte-identical. The manager may create only the exact anchor path supplied and evidence-validated by the current Agent runtime or user; it never guesses a filename.

Before first-time `plan-init`, the current Agent asks the user for the BCP-47 language tag for new or substantially rewritten project documentation. It passes that exact value as `--documentation-language <tag>`, and the manager persists it in `PROJECT_CONFIG.json` and the selected context-anchor loader. The language is never inferred from locale, Agent product, existing documents, or a default.

The conceptual Spec Kit lifecycle is:

~~~text
constitution → specify → clarify → plan → checklist → tasks → analyze
→ implement → validate → converge
~~~

Clarify and checklist are risk-driven. Analyze, validate, and converge are required before substantive completion; passing tests or exhausting an initial task list is insufficient when artifacts and implementation disagree.

# 项目治理工作流

业务项目中的实质性工作按以下步骤进行：

1. 找到实际的项目根目录。
2. 阅读适用的项目本地规则并检查 brownfield 系统。
3. 检查 `.specify/`；若其存在，则恢复既有 Spec Kit 状态。
4. 若项目尚未受治理，通过已审查的 operation plan 将可移植包安装到 `docs/spec-kit/`。
5. 使用显式 runtime ID 与精确 integration key 解析当前 Agent。
6. 通过已审查的 plan 安装或修复 native integration。
7. 写入项目 context anchor 并携带 compatibility evidence。
8. 在新的 Agent 会话中验证 integration。
9. 仅在验证证据获准后才激活 binding。

每项变更都使用两阶段的 plan/apply 协议。`apply-plan` 前必须批准精确的 plan ID 和 hash。native integration 失败是 blocker：不可写 target、权限错误、sandbox 限制、修复失败或 CLI 安装失败，绝不得静默变成 `generic`。

这条 plan/apply 规则只治理本 Reference 包拥有的变更，不替代上游 Spec Kit 的功能工作流。实质性讨论后，用户说“方案可以”“按这个来”“没问题”或“就这么改”，只表示批准把方向推进到上游 specification、plan 和 tasks 的对齐；不表示允许跳过对齐直接修改业务代码。仅讨论选项时不得修改业务文件；若方向已对齐，可从相应的上游交接点继续；若范围、假设、风险或受影响组件发生变化，必须先更新上游 artifacts。

如果项目已经有运行时选定的项目上下文锚点文件，它属于项目拥有的规则内容。治理 loader 只能通过已审查的 manager plan 追加或更新其受管区块；区块之外的每个字节都必须保持完全一致。manager 只能创建当前 Agent 运行时或用户明确提供并完成证据校验的精确路径，绝不猜测文件名。

首次执行 `plan-init` 前，当前 Agent 必须询问用户：新建或实质性重写的项目文档使用哪个 BCP-47 语言标签。它必须把该值作为 `--documentation-language <tag>` 原样传给 manager，由 manager 写入 `PROJECT_CONFIG.json` 和选定的上下文锚点 loader。语言不得从地区设置、Agent 产品、现有文档或默认值推断。

概念上的 Spec Kit 生命周期为：

~~~text
constitution → specify → clarify → plan → checklist → tasks → analyze
→ implement → validate → converge
~~~

Clarify 和 checklist 由风险驱动。Analyze、validate 和 converge 是实质性工作完成前的必需 gate；当 artifacts 与 implementation 不一致时，仅测试通过或耗尽初始任务列表都不足以完成工作。

# Agent-neutral integration rules

The resolver never infers the current Agent from a product name, installed binary, default integration, directory name, Rich catalog output, or similar brand. Only an explicit runtime declaration or existing verified binding establishes identity.

- A display name without an exact integration key returns `KEY_REQUIRED`.
- A native integration available for the current Agent is mandatory.
- An installed integration remains provisional until a fresh session verifies the runtime-to-key binding, anchor, Loader, and managed files.
- `generic` is not a permission fallback. It is allowed only after explicit native-absence evidence, compatibility evidence, project configuration approval, an empty installed integration set, and exact plan approval.
- Generic support must be reported as limited and non-native.
- Unknown or unsupported Agents stop with an explicit status; they are not guessed or silently mapped to another product.

For a concrete Agent, the integration key and generated layout come from the installed CLI. Do not hard-code Codex, Claude, Gemini, Trae, Workbuddy, or any other fixed product list into the project package.

# Agent-neutral integration 规则

resolver 绝不从产品名称、已安装 binary、默认 integration、目录名称、Rich catalog 输出或相似品牌推断当前 Agent。只有显式 runtime declaration 或既有的已验证 binding 才能建立 identity。

- 没有精确 integration key 的 display name 返回 `KEY_REQUIRED`。
- 对当前 Agent 可用的 native integration 是强制要求。
- 已安装 integration 在新的会话验证 runtime-to-key binding、anchor、Loader 和 managed files 之前始终只是 provisional。
- `generic` 不是权限 fallback。只有取得明确的 native-absence evidence、compatibility evidence、项目配置批准、空的已安装 integration set 及精确 plan 批准后，才允许使用它。
- Generic support 必须报告为 limited 和 non-native。
- 未知或不支持的 Agent 以明确 status 停止；不得猜测或静默映射到其他产品。

对于具体 Agent，integration key 和生成布局来自已安装 CLI。不得在项目包中硬编码 Codex、Claude、Gemini、Trae、Workbuddy 或任何其他固定产品列表。

# Manager commands

The portable manager is the single project mutation entrypoint:

~~~text
tools/spec-kit-governance/governance.py doctor
tools/spec-kit-governance/governance.py resolve-agent
tools/spec-kit-governance/governance.py plan-governance-bootstrap
tools/spec-kit-governance/governance.py plan-init
tools/spec-kit-governance/governance.py plan-onboard
tools/spec-kit-governance/governance.py plan-extension-install
tools/spec-kit-governance/governance.py plan-default-change
tools/spec-kit-governance/governance.py plan-upgrade
tools/spec-kit-governance/governance.py plan-rollback
tools/spec-kit-governance/governance.py plan-activate-binding
tools/spec-kit-governance/governance.py apply-plan
tools/spec-kit-governance/governance.py render
tools/spec-kit-governance/governance.py verify
tools/spec-kit-governance/governance.py check-update
~~~

`apply-plan` is the only mutation entrypoint for Reference-owned governance changes. Plans record project and Git snapshots, CLI and integration state, exact file mutations, external CLI scope, recovery steps, and a canonical SHA-256 plan hash. Runtime plans, backups, journals, and failure evidence live under `.spec-kit-governance/` and are ignored by Git. The upstream `specify` CLI remains the executor for upstream Spec Kit artifacts and feature workflow.

`plan-governance-bootstrap` requires the exact runtime-selected `--context-anchor <project-relative-path>`. `plan-init` additionally requires `--runtime-id <id>`, `--integration-key <key>`, and the user's explicit `--documentation-language <BCP-47-tag>`; it records the language in project configuration and the selected anchor. For native external operations, pass runtime-reported targets as repeated `--allowed-path-prefix <project-relative-prefix>` values. The manager never guesses Agent filenames or generated Skills/Commands directories. Non-empty brownfield initialization may use `--force` only in the dedicated, rehearsal-backed init plan. No other operation may use `--force`.

# Manager 命令

可移植 manager 是唯一的项目变更入口：

~~~text
tools/spec-kit-governance/governance.py doctor
tools/spec-kit-governance/governance.py resolve-agent
tools/spec-kit-governance/governance.py plan-governance-bootstrap
tools/spec-kit-governance/governance.py plan-init
tools/spec-kit-governance/governance.py plan-onboard
tools/spec-kit-governance/governance.py plan-extension-install
tools/spec-kit-governance/governance.py plan-default-change
tools/spec-kit-governance/governance.py plan-upgrade
tools/spec-kit-governance/governance.py plan-rollback
tools/spec-kit-governance/governance.py plan-activate-binding
tools/spec-kit-governance/governance.py apply-plan
tools/spec-kit-governance/governance.py render
tools/spec-kit-governance/governance.py verify
tools/spec-kit-governance/governance.py check-update
~~~

`apply-plan` 是 Reference 自有治理变更的唯一入口。Plan 记录项目和 Git snapshots、CLI 与 integration 状态、精确文件变更、外部 CLI scope、恢复步骤，以及 canonical SHA-256 plan hash。运行时 plan、备份、journals 和 failure evidence 位于 `.spec-kit-governance/` 下，且被 Git 忽略。上游 Spec Kit artifacts 和功能工作流仍由上游 `specify` CLI 执行。

`plan-governance-bootstrap` 必须接收运行时选定的精确 `--context-anchor <项目相对路径>`。`plan-init` 还必须接收 `--runtime-id <id>`、`--integration-key <key>` 和用户明确选择的 `--documentation-language <BCP-47-tag>`；manager 会把语言写入项目配置和选定的 anchor。对于 native 外部操作，必须把运行时报告的 target 作为可重复的 `--allowed-path-prefix <项目相对前缀>` 传入。manager 绝不猜测 Agent 文件名或生成的 Skills/Commands 目录。非空 brownfield 初始化仅可在专用且经过 rehearsal-backed 的 init plan 中使用 `--force`。其他操作都不得使用 `--force`。

# Portable releases

The release builder creates two deterministic artifacts: a portable governance ZIP for staging and project bootstrap, and a Spec Kit extension archive for extension installation.

Build and validate a release from the repository root:

~~~bash
python3 scripts/build_governance_release.py \
  --version 1.1.0 \
  --output-dir /tmp/speckit-governance-release

python3 scripts/validate_governance_release.py \
  /tmp/speckit-governance-release/latest.json
~~~

The builder records source revision, worktree status, reviewed upstream revision, artifact hashes, and per-file content hashes. It rejects a missing canonical `GLOBAL_POLICY.md` or a legacy `global-policy.md`. The validator checks deterministic ZIP ordering, payload hashes, required files, and shared portable/extension content.

A release must be reviewed before broad rollout. The current source checkout may be dirty while work is in progress; `check-update` accepts only a clean Git source whose HEAD and artifacts match the release provenance.

# 可移植发布

release builder 创建两个确定性 artifacts：一个用于 staging 和项目 bootstrap 的可移植治理 ZIP，以及一个用于 extension 安装的 Spec Kit extension archive。

从仓库根目录构建和验证发布：

~~~bash
python3 scripts/build_governance_release.py \
  --version 1.1.0 \
  --output-dir /tmp/speckit-governance-release

python3 scripts/validate_governance_release.py \
  /tmp/speckit-governance-release/latest.json
~~~

builder 记录 source revision、worktree status、已审查的 upstream revision、artifact hashes 和逐文件 content hashes。它拒绝缺失 canonical `GLOBAL_POLICY.md` 或仍存在 legacy `global-policy.md` 的情况。validator 检查确定性的 ZIP 排序、payload hashes、required files 以及共享的 portable/extension content。

release 在广泛 rollout 前必须经审查。工作进行中当前 source checkout 可以 dirty；`check-update` 只接受 HEAD 与 artifacts 匹配 release provenance 的 clean Git source。

# Upstream maintenance

Configure the official remote as follows:

~~~bash
git remote add upstream https://github.com/github/spec-kit.git
~~~

Use the platform wrapper to inspect changes:

~~~bash
python3 scripts/check_upstream.py
sh scripts/check-upstream.sh
~~~

On Windows PowerShell:

~~~powershell
.\scripts\check-upstream.ps1
~~~

The checker compares `UPSTREAM_BASELINE` with `upstream/main` and never edits Policy, Reference, documentation, or the baseline. Exit `0` means no unreviewed upstream commits, exit `2` means unreviewed upstream commits exist, and exit `1` means the check could not complete.

Use `--no-fetch` only when the existing `upstream/main` ref is the evidence to review. For every detected range: read the baseline; fetch and compare commits and changed paths; inspect complete relevant files and diffs; classify impact as `NONE`, `REFERENCE`, or `POLICY`; update only justified local documents; record the result in `docs/CHANGE_IMPACT.md` and `docs/HISTORY.md`; validate; then advance `UPSTREAM_BASELINE` last.

`POLICY` changes require human review before merge or deployment. Never merge upstream history or automatically deploy upstream prose.

# 上游维护

按如下方式配置官方 remote：

~~~bash
git remote add upstream https://github.com/github/spec-kit.git
~~~

使用平台 wrapper 检查变更：

~~~bash
python3 scripts/check_upstream.py
sh scripts/check-upstream.sh
~~~

在 Windows PowerShell 中：

~~~powershell
.\scripts\check-upstream.ps1
~~~

checker 将 `UPSTREAM_BASELINE` 与 `upstream/main` 比较，且绝不编辑 Policy、Reference、文档或 baseline。Exit `0` 表示没有未经审查的上游 commits，exit `2` 表示存在未经审查的上游 commits，exit `1` 表示检查未能完成。

只有当现有 `upstream/main` ref 就是要审查的证据时才使用 `--no-fetch`。对每个检测到的 range：阅读 baseline；fetch 并比较 commits 和 changed paths；检查完整的相关 files 和 diffs；将影响分类为 `NONE`、`REFERENCE` 或 `POLICY`；只更新有依据的本地文档；在 `docs/CHANGE_IMPACT.md` 和 `docs/HISTORY.md` 中记录结果；验证；最后才推进 `UPSTREAM_BASELINE`。

`POLICY` 变更必须在 merge 或部署前经人工审查。绝不得合并上游历史或自动部署上游 prose。

# Validation

Run the local contract suite from the repository root:

~~~bash
python3 -m unittest discover -s tests -p 'test*.py'
python3 -m compileall -q governance scripts tests
git diff --check
~~~

The tests cover the preserved upstream checker and CI behavior, canonical policy markers, path safety, plan hashing, dirty-worktree protection, native no-downgrade behavior, generic attestation, onboarding evidence, isolated init rehearsal, external CLI scope, release contracts, and capability-baseline hashes.

Real-project validation is a separate gate. It must use an actual project, actual CLI, actual Agent session, and target-platform permissions. A green local suite does not prove that a real Agent loaded its context anchor or correctly created native managed files.

# 验证

从仓库根目录运行本地契约套件：

~~~bash
python3 -m unittest discover -s tests -p 'test*.py'
python3 -m compileall -q governance scripts tests
git diff --check
~~~

测试覆盖保留的 upstream checker 与 CI 行为、canonical policy markers、路径安全、plan hashing、dirty-worktree 保护、native 不降级行为、generic attestation、onboarding evidence、隔离的 init rehearsal、外部 CLI scope、release contracts 和 capability-baseline hashes。

真实项目验证是独立 gate。它必须使用实际项目、实际 CLI、实际 Agent 会话和目标平台权限。本地套件全绿并不能证明真实 Agent 已加载 context anchor，或其 native managed files 已被正确创建。

# Documentation map

- [docs/GLOBAL_POLICY_DEPLOYMENT.md](docs/GLOBAL_POLICY_DEPLOYMENT.md): global template deployment and recovery protocol.
- [docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md](docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md): dated implementation record covering architecture, schemas, states, commands, and completion definition.
- [docs/PROJECT_GOVERNANCE_MIGRATION.md](docs/PROJECT_GOVERNANCE_MIGRATION.md): package upgrade, rollback, and migration rules.
- [docs/PROJECT_GOVERNANCE_OPERATIONS.md](docs/PROJECT_GOVERNANCE_OPERATIONS.md): operational procedures for implementation Agents.
- [docs/PROJECT_GOVERNANCE_SECURITY.md](docs/PROJECT_GOVERNANCE_SECURITY.md): path, CLI, log, and recovery security boundaries.
- [docs/PROJECT_GOVERNANCE_TEST_MATRIX.md](docs/PROJECT_GOVERNANCE_TEST_MATRIX.md): release-blocking validation matrix.
- [docs/UPSTREAM_UPDATE_POLICY.md](docs/UPSTREAM_UPDATE_POLICY.md): upstream review and automation boundary.
- [docs/CHANGE_IMPACT.md](docs/CHANGE_IMPACT.md): latest reviewed impact assessment.
- [docs/HISTORY.md](docs/HISTORY.md): maintenance history.

The dated implementation record is retained under `docs/archive/` as the implementation snapshot and audit trail for this rollout. It is not a project runtime dependency and must not be copied into business projects.

# 文档地图

- [docs/GLOBAL_POLICY_DEPLOYMENT.md](docs/GLOBAL_POLICY_DEPLOYMENT.md)：全局模板部署与恢复协议。
- [docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md](docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md)：带日期的实施记录，涵盖架构、schema、状态、命令和完成定义。
- [docs/PROJECT_GOVERNANCE_MIGRATION.md](docs/PROJECT_GOVERNANCE_MIGRATION.md)：包升级、回滚和迁移规则。
- [docs/PROJECT_GOVERNANCE_OPERATIONS.md](docs/PROJECT_GOVERNANCE_OPERATIONS.md)：供实施 Agent 使用的操作流程。
- [docs/PROJECT_GOVERNANCE_SECURITY.md](docs/PROJECT_GOVERNANCE_SECURITY.md)：路径、CLI、日志和恢复的安全边界。
- [docs/PROJECT_GOVERNANCE_TEST_MATRIX.md](docs/PROJECT_GOVERNANCE_TEST_MATRIX.md)：阻断发布的验证矩阵。
- [docs/UPSTREAM_UPDATE_POLICY.md](docs/UPSTREAM_UPDATE_POLICY.md)：上游审查与自动化边界。
- [docs/CHANGE_IMPACT.md](docs/CHANGE_IMPACT.md)：最近一次已审查的影响评估。
- [docs/HISTORY.md](docs/HISTORY.md)：维护历史。

带日期的实施记录保留在 `docs/archive/` 下，作为本次 rollout 的 implementation snapshot 和 audit trail。它不是项目运行时依赖，且不得复制进业务项目。

# Contribution boundaries

Preserve user changes and never reset or overwrite unrelated work. Do not merge `upstream/main`, vendor the upstream repository without explicit need, manually copy generated Agent Skills into global directories, or make Policy changes without human review.

When changing a schema, fixed path, enum, or manager contract incompatibly, bump the governance package major version and provide a migration path, rollback test, and release-note entry.

# 贡献边界

保留用户变更，绝不得 reset 或覆盖无关工作。不得合并 `upstream/main`，不得在没有明确需要时 vendor 上游仓库，不得手动复制生成的 Agent Skills 到全局目录，也不得在未经人工审查时变更 Policy。

当不兼容地变更 schema、固定路径、enum 或 manager contract 时，必须提升 governance package 的 major version，并提供 migration path、rollback test 和 release-note entry。

# Current status

The central implementation, portable package, schemas, manager, release builder, deployment protocol, capability baseline, and local regression suite are present. Controlled real-project validation is still required before a cross-Agent and cross-platform rollout is called final.

# 当前状态

中央实施、可移植包、schema、manager、release builder、部署协议、capability baseline 和本地回归套件均已具备。在跨 Agent、跨平台 rollout 被认定为最终完成之前，仍需要进行受控的真实项目验证。
