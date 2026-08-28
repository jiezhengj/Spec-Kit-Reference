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

## CLI upgrade

```text
specify self check
specify self upgrade
specify integration status
specify integration upgrade <key>
specify extension update
```

The actual installed CLI and project integration are authoritative if this reference differs from runtime behavior.

## Agentic SDD

The canonical conceptual lifecycle is:

```text
constitution → specify → clarify → plan → checklist → tasks → analyze → implement → validate → converge
```

`clarify` and `checklist` are quality gates selected according to ambiguity, risk, and complexity. `analyze`, `validate`, and `converge` are required before substantive completion. Invocation syntax depends on the current Agent integration.

The upstream quickstart documents both a shorter path and a full path with optional quality gates. This project's committed governance policy intentionally strengthens the completion contract: `analyze`, `validate`, and `converge` remain required before substantive completion.

Convergence checks implementation completeness against accepted feature artifacts. If it finds missing work, it may append tasks; then repeat `implement`, validation, and `converge` until complete.

## Ownership and runtime independence

The upstream Spec Kit CLI owns `.specify/**`, `specs/**`, and native Agent integration files. This Reference may inspect them and invoke supported CLI commands, but it must not directly edit or replace them. Its target-project additions are the committed `docs/spec-kit/**` package, the local governance manager, `.spec-kit-governance/**` runtime state, and the managed loader block in the explicitly selected context anchor.

A conversational approval such as “方案可以” advances a direction into the upstream Spec Kit workflow; it does not authorize direct code edits before the specification, plan, and tasks are aligned. The central Reference and global Policy are not runtime prerequisites for a target project whose local governance package and loader are present.

## Bug workflow

The bundled bug extension may be installed with `specify extension add bug`. Use the integration-specific workflow exposed by the project, and verify the reproduction and remediation.

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

Reviewed upstream commit: `github/spec-kit @ 5aa8bea7823dcd056f111f847bf2d576bad3f0a5`.

Reference last reviewed: `2026-08-28`.

Verified local CLI: `specify 1.0.2.dev0`; `specify integration --help` succeeds. In this governance repository, `integration list` and `integration status` correctly report that no `.specify/` project exists.

The integration commands should be rechecked from an actual Spec Kit project root when project-level runtime verification is needed.

The most recent semantic review and the locally verified CLI version are recorded in `docs/CHANGE_IMPACT.md`. These values may differ from the latest upstream commit and from the currently available runtime.
