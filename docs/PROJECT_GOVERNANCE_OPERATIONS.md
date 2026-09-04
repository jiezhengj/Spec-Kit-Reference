# Operational entry point

The fixed public entry point for Reference-owned governance changes is `tools/spec-kit-governance/governance.py`. Its read-only commands are `doctor`, `resolve-agent`, `verify`, and `check-update`; every manager mutation must first generate an operation plan and then be executed with `apply-plan --approve-plan-id <id> --approve-plan-sha256 <hash>`.

The manager is not a second Spec Kit executor. The upstream `specify` CLI owns `.specify/**`, `specs/**`, and native Agent-generated integration files. The manager may invoke supported upstream CLI commands as an opaque external step, but its own file mutations are restricted to `docs/spec-kit/**`, `tools/spec-kit-governance/governance.py`, `.spec-kit-governance/**`, and the separately managed loader and Reference-update-check blocks in the explicitly selected context anchor.

# Central Reference update handoff

When the current Agent has actually loaded the global Policy and its `SPEC_KIT_GOVERNANCE_SOURCE` locator points to a clean central Reference checkout, the manager may run `check-update --source <central-source>` once before the first substantive task in a new session. The check is read-only. If the global Policy or source locator is absent, unavailable, dirty, or unverifiable, normal project work skips it silently and never searches arbitrary directories.

`UP_TO_DATE` produces no notice. `UPDATE_AVAILABLE` is an informational prompt only. After explicit approval, stage the source and generate `plan-upgrade --source <staged-source>`. The plan may update the committed governance package, the project manager, and the separately managed governance-loader and Reference-update-check blocks in the context anchor. It must not update `.specify/**`, `specs/**`, native Agent files, or business code. Once the governance layer is current, upstream Spec Kit decides whether its specification, plan, or task artifacts need alignment.

# Standard sequence

First confirm the project root, read `docs/spec-kit/START_HERE.md`, and inspect `.specify/` and `specify integration status --json`. For a new project, run `plan-governance-bootstrap` first, then run `plan-init`/`plan-onboard` with explicit `--runtime-id`, `--integration-key`, and `--context-anchor` values; onboarding the current Agent must first pass the native resolver. Install an Extension separately with `plan-extension-install`; it must not be an implicit side effect of bootstrap. A successfully installed CLI integration remains provisional; fresh-session evidence must be provided when running `plan-activate-binding`, or `READY` must not be reported.

If an exact integration key, a context anchor, a writable native target, or compatibility with the current CLI version is unavailable, the manager must stop; it must neither guess the product nor switch to generic.

For an existing `.specify/` project that does not carry `docs/spec-kit/**`, the optional `plan-install-update-reminder` operation is the lightweight reminder path. It requires an existing exact context anchor and installed CLI, appends only the separate managed reminder block, and leaves `.specify/**`, `specs/**`, and native integration files untouched. The block delegates update detection to upstream `specify self check`; it does not auto-upgrade.

# Daily feature workflow

After a substantive discussion, approval such as “方案可以” authorizes advancing the direction into the upstream Spec Kit workflow. It does not authorize direct application-code edits. Inspect the current feature specification, plan, and tasks; update them with the upstream Spec Kit commands when they are missing or inconsistent, then run the required `analyze`, implement only the resulting tasks, validate, and converge. Discussion-only work remains non-mutating. If scope, assumptions, risks, or affected components change during implementation, pause and update the upstream artifacts before continuing.

`verify` proves only the Reference-owned governance package. It is not feature-completion evidence.

# Governed SDD workflow

For a project configured with `workflow_governance.mode` of
`governed-sdd-required`, a request such as “按 Spec 制定方案” begins with
Discovery rather than an immediate specification draft. Record the objective,
users, scenarios, data, boundaries, risks, acceptance evidence, known facts,
open questions, and provisional assumptions. Product, safety, privacy, and
release decisions remain questions for the user when they materially affect the
feature; reasonable implementation defaults are not approval evidence.

The governed sequence is:

```text
discovery → review-discovery → specify → clarify-loop → review-spec
→ plan → review-plan-bundle → checklist → tasks → audit-task-readiness
→ cold-start-review → review-task-package → analyze
→ remediation-gate-if-needed → implement → validate → converge
→ completion-review
```

At every review gate, stop in `PAUSED` and present the artifact type, current
hashes, decisions, assumptions, open risks, and requested disposition. Only an
explicit human approval bound to the displayed artifact type and hashes opens
the next transition. An Agent checklist, a generated test result, or an
approval of another artifact cannot substitute for that evidence. A rejection
returns work to the artifact's revision stage; a changed artifact invalidates
the earlier approval.

Before implementation, generate a self-contained task package for each task:
goal, traceability, necessary context, prerequisite state, allowed and
prohibited changes, target files and symbols, interfaces and invariants,
concrete implementation steps, failure behavior, validation command, expected
result, completion evidence, and escalation condition. Run the read-only
readiness audit and required cold-start review. A package that needs material
context from the original conversation is not ready for a small isolated model.

# V1 to v2 execution

Strict governed SDD is available only after the project has completed the
`1.3.0` bridge and an approved v2 migration plan. The bridge may plan but must
not activate strict gates. The v2 plan requires companion capability discovery
and exact upstream CLI argv in its operation plan. If a required workflow,
preset, extension, or validator cannot be resolved, return
`COMPANION_CAPABILITY_UNAVAILABLE`; do not silently run the legacy path while
claiming governed completion.

# Failure handling

An unwritable Native target, or a permission, sandbox, repair, or installation failure, uniformly returns `NATIVE_INSTALL_BLOCKED`; an unknown identity returns `IDENTITY_UNKNOWN` or `KEY_REQUIRED`; plan-input drift, scope escape, or incomplete recovery returns `RECOVERY_REQUIRED`. On failure, retain the plan, backup, journal, and changed-file inventory; V1 performs no automatic cleanup.
