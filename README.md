# 中文说明

Spec-Kit-Reference 是经过审查的 GitHub Spec Kit 兼容性与治理层。它把持续变化的上游项目转化为稳定的本地 Policy、运行时 Reference，以及可随业务项目提交的治理包。本仓库不是 github/spec-kit 的 fork、镜像或 submodule；`origin` 是本仓库，`upstream` 只用于 fetch、diff 和影响审查，绝不合并上游历史。

## 核心文件

- `AGENTS.md`：本仓库维护规则。
- `GLOBAL_POLICY.md`：唯一可部署、与 Agent 无关的全局 Policy 模板。
- `SPEC_KIT_REFERENCE.md`：经过审查的运行事实和运行时发现指南。
- `UPSTREAM_BASELINE`：最近一次完成语义影响审查的上游提交。
- `governance/`：生成业务项目可移植治理包、schema、resolver 和 manager 的源目录。
- `docs/`：持续维护文档；一次性实施快照位于 `docs/archive/`，不会复制进业务项目。

## 项目治理要点

实质性工程工作应先确定项目根目录、读取项目本地规则、检查 `.specify/` 并理解 brownfield 状态。未治理项目通过已审查 operation plan 安装 `docs/spec-kit/`，再用显式 runtime ID 和准确 integration key 接入当前 Agent。存在 native integration 时必须使用 native；不可写、权限、sandbox、修复或 CLI 安装失败都是 blocker，不得静默降级为 `generic`。

项目包不会预先登记 Codex、Claude、Gemini、Trae、Workbuddy 或其他固定品牌。未知 Agent 不猜测映射；只有显式 runtime 声明或已验证 binding 才能建立身份。只有显示名称而没有准确 key 时返回 `KEY_REQUIRED`。

## 全局 Policy 部署

人工选择实际使用的 Agent 产品全局规则文件，把 `GLOBAL_POLICY.md` 中的 `SPEC_KIT_GOVERNANCE_SOURCE` 占位符替换为本仓库绝对路径，生成临时副本，然后只复制 marker 区块；区块外内容必须保留。不得猜测全局规则位置、另行追加 locator，也不得把个人路径永久写回已提交模板。精确协议见 [`docs/GLOBAL_POLICY_DEPLOYMENT.md`](docs/GLOBAL_POLICY_DEPLOYMENT.md)；普通项目工作不需要读取该协议。

## 本地验证与真实项目验证

~~~bash
python3 -m unittest discover -s tests -p 'test*.py'
python3 -m compileall -q governance scripts tests
git diff --check
~~~

本地测试全绿不代表真实 Agent 已加载 context anchor 或已生成正确的 native managed files；跨 Agent、跨平台推广前仍需使用真实项目、真实 CLI、真实 Agent 会话和目标平台权限进行受控验证。

下方英文部分提供完整操作说明；`docs/` 下的维护文档统一使用英文，以便跨 Agent 协作时只有一份规范文本。

# Purpose

Spec-Kit-Reference is a reviewed compatibility and governance layer for
[GitHub Spec Kit](https://github.com/github/spec-kit). It converts a moving
upstream project into stable local policy, operational reference material, and
a portable project governance package for coding Agents.

This repository is not a fork, mirror, or submodule of github/spec-kit.
Never merge the upstream history into this repository.

- origin is this governance repository.
- upstream is the official Spec Kit repository and is used for fetch, diff,
  and impact review only.

# Repository layout

The repository has three distinct layers.

## Central policy and reference

- [AGENTS.md](AGENTS.md) contains maintenance rules for this repository.
- [GLOBAL_POLICY.md](GLOBAL_POLICY.md) is the single deployable, Agent-neutral
  global Policy template.
- [SPEC_KIT_REFERENCE.md](SPEC_KIT_REFERENCE.md) records reviewed operational
  facts and runtime discovery guidance.
- [UPSTREAM_BASELINE](UPSTREAM_BASELINE) records the latest upstream commit
  whose semantic impact has been reviewed.

## Portable project governance

The governance/ tree is the source for the package committed into a business
project. A project receives a self-contained docs/spec-kit/ package and a
project-local tools/spec-kit-governance/governance.py manager. The package is
the collaborator's offline baseline; it does not depend on a maintainer's
global rules or local Reference directory.

The package is deliberately Agent-neutral. A concrete Agent supplies its own
runtime identity, exact Spec Kit integration key, and project context anchor
during onboarding. The package never pre-registers a fixed list of Agent
brands.

## Central implementation and maintenance material

The docs/ directory contains the English implementation, deployment,
migration, operations, security, test, upstream-review, and history documents.
These documents are central maintenance contracts. They are not copied into
business projects; only the portable package under docs/spec-kit/ is.

# Prerequisites

For repository maintenance, use Git and Python 3. The specify CLI is needed
for runtime discovery and real-project validation. The installed CLI and the
current project state are authoritative for behavior; this repository never
assumes that the installed version matches the reviewed Reference.

If the CLI is missing, an Agent must ask for authorization before installing
it. The approved V1 install form is pinned to an immutable upstream commit
recorded by the release manifest:

~~~bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@<approved-40-character-commit-sha>
~~~

Do not silently install the CLI, use a floating main branch, or treat a
global CLI installation as proof that Agent-specific project Skills exist.

# Runtime authority

When sources disagree, use this order for operational mechanics:

1. Current project Spec Kit state and project-local rules.
2. The installed project integration and its managed-file metadata.
3. The installed specify CLI.
4. The committed project docs/spec-kit/REFERENCE.md.
5. This repository's SPEC_KIT_REFERENCE.md.
6. Upstream documentation and source as reviewed evidence.

Upstream content is never dynamically imported as a higher-priority
instruction source. Explicit user instructions, higher-priority runtime rules,
and applicable project-local rules always take precedence.

# Global Policy deployment

[GLOBAL_POLICY.md](GLOBAL_POLICY.md) is the only global Policy template. It
contains one managed marker block and one deployment-time locator:

~~~text
SPEC_KIT_GOVERNANCE_SOURCE: <ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>
~~~

For each Agent product you actually use:

1. Identify that product's real global rule file yourself.
2. Render a temporary copy of GLOBAL_POLICY.md by replacing the placeholder
   with the absolute path of this repository.
3. Copy the rendered marker block into the selected global rule file.
4. Preserve all content outside the marker block.
5. Verify the Agent in a fresh session.

Do not permanently write a personal absolute path into the committed source
template. Do not guess global rule locations, append a second locator, or
deploy the deployment protocol itself as global Policy.

The exact marker grammar, backup, no-clobber, atomic replacement, recovery, and
fresh-session verification protocol is documented in
[docs/GLOBAL_POLICY_DEPLOYMENT.md](docs/GLOBAL_POLICY_DEPLOYMENT.md). That
document is needed when performing or auditing a global deployment; normal
project work does not need to read it.

# Project governance workflow

When substantive work is required in a business project:

1. Find the actual project root.
2. Read applicable project-local rules and inspect the brownfield system.
3. Check for .specify/ and resume existing Spec Kit state when it exists.
4. If the project is not yet governed, install the portable package into
   docs/spec-kit/ through a reviewed operation plan.
5. Resolve the current Agent using an explicit runtime ID and exact integration
   key.
6. Install or repair the native integration through a reviewed plan.
7. Write the project context anchor and carry compatibility evidence.
8. Verify the integration in a fresh Agent session.
9. Activate the binding only after the verification evidence is approved.

All mutations use a two-stage plan/apply protocol. The exact plan ID and hash
must be approved before apply-plan runs. Native integration failure is a
blocker: an unwritable target, permission error, sandbox restriction, repair
failure, or CLI installation failure must never silently become generic.

The conceptual Spec Kit lifecycle is:

~~~text
constitution → specify → clarify → plan → checklist → tasks → analyze
→ implement → validate → converge
~~~

The quality gates are risk-driven. Converge is the completion gate; passing
tests or exhausting an initial task list is not sufficient when artifacts and
implementation disagree.

# Agent-neutral integration rules

The resolver does not infer the current Agent from a product name, installed
binary, default integration, directory name, Rich catalog output, or a similar
brand. Only an explicit runtime declaration or an existing verified binding
may establish identity.

- A display name without an exact integration key returns KEY_REQUIRED.
- A native integration available for the current Agent is mandatory.
- An installed integration is provisional until a fresh session verifies the
  runtime-to-key binding, anchor, Loader, and managed files.
- Generic is not a permission fallback. It is allowed only after explicit
  native-absence evidence, compatibility evidence, project configuration
  approval, an empty installed integration set, and exact plan approval.
- Generic support must be reported as limited and non-native.
- Unknown or unsupported Agents stop with an explicit status; they are not
  guessed or silently mapped to another product.

For a concrete Agent, the integration key and generated layout come from the
installed CLI. Do not hard-code Codex, Claude, Gemini, Trae, Workbuddy, or any
other fixed product list into the project package.

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

Apply-plan is the only mutation entrypoint. Plans record project and Git
snapshots, CLI and integration state, exact file mutations, external CLI
scope, recovery steps, and a canonical SHA-256 plan hash. Runtime plans,
backups, journals, and failure evidence live under .spec-kit-governance/ and
are ignored by Git.

Plan-init always uses an explicit --integration key. Non-empty brownfield
initialization may use --force only inside the dedicated, rehearsal-backed
init plan. No other operation may use --force.

# Portable releases

The release builder creates two deterministic artifacts:

- a portable governance ZIP for staging and project bootstrap;
- a Spec Kit extension archive for extension installation.

Build and validate a release from the repository root:

~~~bash
python3 scripts/build_governance_release.py \
  --version 1.0.0 \
  --output-dir /tmp/speckit-governance-release

python3 scripts/validate_governance_release.py \
  /tmp/speckit-governance-release/latest.json
~~~

The builder records source revision, worktree status, reviewed upstream
revision, artifact hashes, and per-file content hashes. It rejects a missing
canonical GLOBAL_POLICY.md or a legacy global-policy.md. The validator
checks deterministic ZIP ordering, payload hashes, required files, and shared
portable/extension content.

A release must be reviewed before it is used for a broad rollout. The current
source checkout may be dirty while work is in progress; check-update accepts
only a clean Git source whose HEAD and artifacts match the release provenance.

# Upstream maintenance

The official remote should be configured as:

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

The checker compares UPSTREAM_BASELINE with upstream/main and never edits
Policy, Reference, documentation, or the baseline.

- Exit 0: no unreviewed upstream commits.
- Exit 2: unreviewed upstream commits exist.
- Exit 1: the check could not complete.

Use --no-fetch only when the existing upstream/main ref is the evidence you
intend to review. For every detected range:

1. read the baseline;
2. fetch and compare commits and changed paths;
3. inspect complete relevant files and diffs;
4. classify the impact as NONE, REFERENCE, or POLICY;
5. update only justified local documents;
6. record the result in docs/CHANGE_IMPACT.md and docs/HISTORY.md;
7. validate the repository;
8. advance UPSTREAM_BASELINE last.

POLICY changes require human review before merge or deployment. Never merge
upstream history or automatically deploy upstream prose.

# Validation

Run the local contract suite from the repository root:

~~~bash
python3 -m unittest discover -s tests -p 'test*.py'
python3 -m compileall -q governance scripts tests
git diff --check
~~~

The tests cover the preserved upstream checker and CI behavior, canonical
policy markers, path safety, plan hashing, dirty-worktree protection, native
no-downgrade behavior, generic attestation, onboarding evidence, isolated init
rehearsal, external CLI scope, release contracts, and capability-baseline
hashes.

Real-project validation remains a separate gate. It must use an actual project,
actual CLI, actual Agent session, and the target platform permissions. A green
local suite does not prove that a real Agent loaded its context anchor or that
its native managed files were created correctly.

# Documentation map

- [docs/GLOBAL_POLICY_DEPLOYMENT.md](docs/GLOBAL_POLICY_DEPLOYMENT.md): global
  template deployment and recovery protocol.
- [docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md](docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md):
  dated implementation record covering architecture, schemas, states, commands, and completion definition.
- [docs/PROJECT_GOVERNANCE_MIGRATION.md](docs/PROJECT_GOVERNANCE_MIGRATION.md):
  package upgrade, rollback, and migration rules.
- [docs/PROJECT_GOVERNANCE_OPERATIONS.md](docs/PROJECT_GOVERNANCE_OPERATIONS.md):
  operational procedures for implementation Agents.
- [docs/PROJECT_GOVERNANCE_SECURITY.md](docs/PROJECT_GOVERNANCE_SECURITY.md):
  path, CLI, log, and recovery security boundaries.
- [docs/PROJECT_GOVERNANCE_TEST_MATRIX.md](docs/PROJECT_GOVERNANCE_TEST_MATRIX.md):
  release-blocking validation matrix.
- [docs/UPSTREAM_UPDATE_POLICY.md](docs/UPSTREAM_UPDATE_POLICY.md): upstream
  review and automation boundary.
- [docs/CHANGE_IMPACT.md](docs/CHANGE_IMPACT.md): latest reviewed impact
  assessment.
- [docs/HISTORY.md](docs/HISTORY.md): maintenance history.

The dated implementation record is retained under `docs/archive/` as the
implementation snapshot and audit trail for this rollout. It is not a project
runtime dependency and must not be copied into business projects.

# Contribution boundaries

Preserve user changes and never reset or overwrite unrelated work. Do not
merge upstream/main, vendor the upstream repository without an explicit
need, manually copy generated Agent Skills into global directories, or make
Policy changes without human review.

When changing a schema, fixed path, enum, or manager contract incompatibly,
bump the governance package major version and provide a migration path,
rollback test, and release-note entry.

# Current status

The central implementation, portable package, schemas, manager, release
builder, deployment protocol, capability baseline, and local regression suite
are present. Controlled real-project validation is still required before a
cross-Agent and cross-platform rollout is called final.
