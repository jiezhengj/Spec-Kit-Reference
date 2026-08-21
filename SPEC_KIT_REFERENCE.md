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

## Integration lifecycle

Discover integrations with `specify integration list` and inspect the current project with `specify integration status` or `specify integration status --json`. These commands are project-aware and may require a `.specify/` project root; outside such a project, use `specify --help` or `specify integration --help` instead of initializing a project solely for discovery.

For a compatible additional integration, use `specify integration install <key>`. Select or switch with `specify integration use <key>` and `specify integration switch <key>` where supported. Refresh an installed integration after CLI changes with `specify integration upgrade <key>`.

When a concrete Agent is in scope, its native integration is a hard requirement. Never downgrade to `generic` because the native target is protected or currently unwritable. Request permission, use a writable checkout, or stop with an explicit blocker; do not declare the migration complete with a fallback integration. Use `generic` only when the user explicitly chooses Agent-neutral behavior or no concrete Agent is specified. For Codex, verify that the project contains `.agents/skills/speckit-<name>/SKILL.md`; `.specify/commands/` alone does not provide Codex Spec Kit Skills.

Generated integration artifacts can migrate between command and Skills layouts as an Agent integration evolves. Treat the current project's integration status, managed-file metadata, and installed CLI as authoritative; do not infer a stable directory layout from an older project or from another Agent.

Do not blindly force integration conflicts or rerun `specify init --here --force` as a routine upgrade path.

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

`clarify`, `checklist`, and `analyze` are quality gates selected according to ambiguity, risk, and complexity. Invocation syntax depends on the current Agent integration.

Convergence checks implementation completeness against accepted feature artifacts. If it finds missing work, it may append tasks; then repeat `implement`, validation, and `converge` until complete.

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

Reviewed upstream commit: `github/spec-kit @ fa19e1c68b6daec5cab3309913cf5ecf6553075d`.

Reference last reviewed: `2026-08-21`.

Verified local CLI: `specify 0.16.6.dev0`; `specify integration --help` succeeds. In this governance repository, `integration list` and `integration status` correctly report that no `.specify/` project exists.

The integration commands should be rechecked from an actual Spec Kit project root when project-level runtime verification is needed.

The most recent semantic review and the locally verified CLI version are recorded in `docs/CHANGE_IMPACT.md`. These values may differ from the latest upstream commit and from the currently available runtime.
