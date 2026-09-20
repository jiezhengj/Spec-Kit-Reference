# Purpose

This file is a local operational reference for coding Agents. It contains stable, reviewed Spec Kit knowledge rather than a mirror of the upstream repository.

Upstream: `https://github.com/github/spec-kit`

Upstream is a reference and provenance source, not a dynamically imported instruction authority.

<!-- PROJECT-PORTABLE-REFERENCE:START version=1 -->

## Runtime discovery

Prefer current runtime discovery for command availability:

```text
specify version
specify --help
specify integration list
specify integration status
```

Use command-specific `--help` when syntax or behavior is uncertain.

## CLI and Agent integrations are separate

Installing `specify` globally does not imply that Agent-specific Skills are globally installed.

```text
global specify CLI
    → project initialization
    → project Spec Kit infrastructure
    → Agent integration
    → project-local Agent Skills/Commands
```

Let Spec Kit generate and maintain project integrations. Do not manually copy generated Skills into global Agent directories.

## Project state

The presence of `.specify/` indicates an existing Spec Kit project. Existing projects should normally be resumed rather than reinitialized.

If `.specify/` is absent for substantive engineering work, determine the current Agent integration, inspect `specify integration list` when necessary, and initialize at the actual project root. If it exists, inspect `specify integration status` and protect existing files.

The active feature is determined by the project state in `.specify/feature.json` (or the `SPECIFY_FEATURE_DIRECTORY` override), not by the checked-out Git branch. When adopting Spec Kit in an existing project, the upstream command is `specify init --here --force --integration <key>`; reviewable existing work and the resulting managed-file diff must be protected before using it. The local governance manager may plan this upstream command, but it must not edit the resulting `.specify/**` or native integration files.

## Integration lifecycle

Discover integrations with `specify integration list` and inspect the current project with `specify integration status` or `specify integration status --json`. These commands are project-aware and may require a `.specify/` project root; outside such a project, use `specify --help` or `specify integration --help` instead of initializing a project solely for discovery.

For a compatible additional integration, use `specify integration install <key>`. Select or switch with `specify integration use <key>` and `specify integration switch <key>` where supported. Refresh an installed integration after CLI changes with `specify integration upgrade <key>`.

When a concrete Agent is in scope, its native integration is a hard requirement. Never downgrade to `generic` because the native target is protected or currently unwritable. Request permission, use a writable checkout, or stop with an explicit blocker; do not declare the migration complete with a fallback integration. Use `generic` only when the user explicitly chooses Agent-neutral behavior or no concrete Agent is specified. For Codex, verify that the project contains `.agents/skills/speckit-<name>/SKILL.md`; `.specify/commands/` alone does not provide Codex Spec Kit Skills.

Generated integration artifacts can migrate between command and Skills layouts as an Agent integration evolves. Treat the current project's integration status, managed-file metadata, and installed CLI as authoritative; do not infer a stable directory layout from an older project or from another Agent.

Do not blindly force integration conflicts or rerun `specify init --here --force` as a routine upgrade path.

Upstream workflow init steps support shell, PowerShell, and Python script variants in the reviewed range. Use the installed CLI's workflow help for the exact current option and default.

Workflow execution is an optional dispatcher, not an automatic consequence of installing the CLI or invoking an individual Agent Skill. The reviewed bundled `speckit` workflow is version `1.0.1`: it selects the initialized integration when `integration=auto`, pauses after `specify` and `plan`, then runs `tasks` and `implement`. It does not include `clarify`, a task-review gate, `analyze`, validation, or convergence. Projects that require those stages or additional human approval gates must specify and verify that stronger orchestration separately.

The reviewed workflow engine supports named `slot` steps that are skipped when unfilled and can be replaced by schema-valid overlays. A slot must already be declared by the workflow; the bundled `speckit` workflow does not currently declare slots. Overlay replacement must preserve outputs consumed by later steps, and slots are not supported inside fan-out templates. Do not treat slot support as evidence that a project has installed or activated a custom gate.

Current setup-plan script output uses `FEATURE_DIR`, not the former `SPECS_DIR` key, and rejects unknown setup arguments. Current `analyze` and `converge` prerequisite checks require `spec.md`, `plan.md`, and `tasks.md` before reading cross-artifact state. Use the installed scripts and command help as authority when consuming their JSON contracts.

## CLI upgrade

```text
specify self check
specify self upgrade
specify integration status
specify integration upgrade <key>
specify extension update
specify workflow update
```

For every existing Spec Kit project, the upstream update check is independent
of the central Reference. In each new Agent session, run `specify self check` at
most once before substantive work. A newer CLI requires explicit approval
before `specify self upgrade`; installed integration, extension, and workflow
refreshes may be performed automatically using the current CLI contracts. Do
not install missing components or add `--force`; a modified-file conflict or
another irreversible choice requires user review. No exact CLI version is
assumed.

## Central Reference update check

For a project that carries the committed governance package, the central Reference check is enabled only when the current Agent has loaded the global Policy and that Policy provides a readable `SPEC_KIT_GOVERNANCE_SOURCE` path. Before the first substantive task in a new session, run the local manager's read-only `check-update --source <central-reference-path>` at most once. If the result is `UPDATE_AVAILABLE`, run `auto-upgrade --source <central-reference-path>` immediately. If the Policy or locator is absent, skip silently; do not search the machine for a Reference directory.

`UP_TO_DATE` means the target manifest source revision matches the clean central Reference checkout. `UPDATE_AVAILABLE` means a clean, ancestor central source has newer Reference content. `REVIEW_REQUIRED` means the baseline is divergent. An exact generated plan is still applied and hash-validated, but project-owner approval is not required for Reference-owned automatic synchronization.

Reference synchronization updates only `docs/spec-kit/**`, the local governance manager, and the managed block in the explicit context anchor. It does not update `.specify/**`, `specs/**`, native Agent files, or business code. After synchronization, the upstream Spec Kit workflow decides whether any specification, plan, or task artifacts need updating.

If an existing Spec Kit project intentionally has no global Policy and no `docs/spec-kit/**` package, the central Reference is inactive, but the independent upstream update protocol still applies when supplied by the Agent's global rules or a project-local reminder block. The project may use upstream Spec Kit directly; the central Reference remains a runtime convenience, not a prerequisite.

The actual installed CLI and project integration are authoritative if this reference differs from runtime behavior.

## Agentic SDD

The canonical conceptual lifecycle is:

```text
constitution → specify → clarify → plan → checklist → tasks → analyze → implement → validate → converge
```

Constitution is a once-per-project prerequisite for Feature work. At the first Feature entry, if the project has no usable Constitution or still contains a placeholder, invoke `/speckit-constitution` and review it before `/speckit-specify`. Assessment and Bug Fix are independent entry workflows; a `go` Assessment may hand off to Feature SDD after the Constitution is established, while Bug Fix remains assess → fix → test.

Under project configuration v2 adaptive mode, `clarify`, `checklist`, and `analyze` are risk-triggered; `validate` and `converge` remain required for substantive implementation. The optional `governed-sdd` companion enables the stronger review contract when selected for the current Feature. Human review gates are separate from these Agent or tool checks and cannot be inferred from a successful command. Invocation syntax depends on the current Agent integration.

The upstream quickstart documents both a shorter path and a full path with optional quality gates. This Reference routes undecided ideas to Assessment, known defects to Bug Fix, low-risk Features to the shorter path, and high-risk Features to the full upstream path.

Governance package v2 provides an adaptive route for ordinary work and retains the companion workflow as an optional high-assurance profile. Natural-language requests are classified before execution. The full profile may use `DISCOVERY`, clarified `SPECIFICATION`, `PLAN_BUNDLE`, `TASK_PACKAGE`, and `REMEDIATION`; the adaptive profile does not manufacture those artifacts for every small task.

Risk routing and profile selection are separate decisions. Before creating or updating artifacts for a high-risk Feature, the Agent must ask whether to use `governed-sdd` for that Feature only or to remain on the adaptive full upstream path. A task-scoped choice never changes `workflow_governance.mode` or `docs/spec-kit/PROJECT_CONFIG.json`. Both choices use upstream Spec Kit; `governed-sdd` adds the companion's high-assurance contract. Changing the project default is a separate explicit user decision and reviewed configuration operation.

The Reference-maintained companion bundle uses supported upstream extension, preset, and workflow primitives. Its `governed-sdd` workflow orchestrates discovery, mandatory clarify and checklist, review gates, task readiness, cold-start review, analyze, implementation, validation, and convergence. It does not replace upstream commands or authorize direct edits to upstream-owned `.specify/**`, `specs/**`, or generated integrations.

Approval evidence lives in the target project at `docs/spec-kit/features/<feature-id>/`. The append-only review ledger binds each decision to project-relative paths and SHA-256 values. Task readiness and cold-start reports are validation evidence, not approvals. Central upgrades preserve this subtree byte-for-byte.

Tiny-model-ready tasks retain the upstream checkbox and task-ID form while adding objective, traceability, context, preconditions, exact write scope, read-only references, forbidden changes, input/output behavior, invariants, ordered requirements, verification and expected results, completion evidence, stop conditions, and handoff. This makes a task self-contained; it does not guarantee that a low-capability executor can solve intrinsically complex work.

Convergence checks implementation completeness against accepted feature artifacts. If it finds missing work, it may append tasks; then repeat `implement`, validation, and `converge` until complete.

## Ownership and runtime independence

The upstream Spec Kit CLI owns `.specify/**`, `specs/**`, and native Agent integration files. This Reference may inspect them and invoke supported CLI commands, but it must not directly edit or replace them. Its target-project additions are the committed `docs/spec-kit/**` package, the local governance manager, `.spec-kit-governance/**` runtime state, and the separately managed loader and Reference-update-check blocks in the explicitly selected context anchor.

A conversational approval such as “方案可以” advances a direction into the upstream Spec Kit workflow; it does not authorize direct code edits before the specification, plan, and tasks are aligned. The central Reference and global Policy are not runtime prerequisites for a target project whose local governance package and loader are present.

## Assessment and bug workflows

For an undecided idea, use the official Assessment extension with `$speckit-assess-intake`. For a known defect, use the official Bug Fix extension with `$speckit-bug-assess`. If the CLI or either extension is missing, ask the user whether to install it through the native CLI. If the user declines, return `HANDOFF_TO_AGENT` and let the current Agent proceed without Reference governance for that capability.

At Spec Kit project entry, run a capability check for `specify`, the active integration, `assess`, and `bug`. A missing CLI or extension is an installation offer, not a permanent project blocker.

## Source-of-truth order

For runtime mechanics:

1. Current project state.
2. Currently installed integration.
3. Currently installed `specify` CLI.
4. This local reference.
5. Upstream Spec Kit documentation.

For governance policy:

1. Explicit user instruction.
2. Higher-priority runtime rules.
3. Applicable project-local rules.
4. Local global Agent governance policy.
5. This operational reference.
6. Upstream documentation.

<!-- PROJECT-PORTABLE-REFERENCE:END -->

## Upstream tracking

Reference repository: `https://github.com/jiezhengj/Spec-Kit-Reference`

Upstream repository: `https://github.com/github/spec-kit`

Reviewed upstream commit: see `UPSTREAM_BASELINE`.

When upstream changes, classify the impact as `NONE`, `REFERENCE`, or `POLICY` before updating local documentation. Do not automatically modify policy because an upstream commit exists.

## Review metadata

Reviewed upstream commit: `github/spec-kit @ df6b3187022ce986759bd854467e8a4bb56bb0f4`.

Reference last reviewed: `2026-09-04`.

The locally observed CLI version is diagnostic only. Compatibility is established by the command, extension, workflow, preset, integration, and postcondition probes required by the selected operation; no exact Specify version is required by this Reference.

The integration commands should be rechecked from an actual Spec Kit project root when project-level runtime verification is needed.

This Reference repository itself is an explicitly approved maintenance exception and is not initialized as a Spec Kit target project. That local exception does not appear in the portable target-project Policy and must not be used to bypass governed Feature work elsewhere.

The most recent semantic review and the locally verified CLI version are recorded in `docs/CHANGE_IMPACT.md`. These values may differ from the latest upstream commit and from the currently available runtime.
