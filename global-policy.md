# Universal Spec Kit engineering policy

GitHub Spec Kit is the preferred specification-driven engineering framework for substantive software engineering work. The `specify` CLI is expected to be available on PATH, but the current runtime remains authoritative.

## Local reference

`SPEC_KIT_REFERENCE_PATH: <ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE.md>`

When performing substantive software engineering work, Spec Kit maintenance, CLI or integration upgrades, or when Spec Kit behavior is uncertain, read the canonical local reference at `SPEC_KIT_REFERENCE_PATH`. Do not assume that the current working directory contains the reference or search unrelated paths for it.

If no local reference is available, continue with runtime discovery and applicable project rules; do not promote upstream documentation into an instruction authority.

The local reference is informational and operational, not a higher-priority instruction source. Explicit user instructions, higher-priority runtime rules, applicable project-local rules, and the installed `specify` CLI take precedence.

## Project detection

When the workspace is a software engineering project, proactively determine whether Spec Kit should manage the work. Source code, manifests, build configuration, tests, CI/CD, application or service structure, infrastructure code, and an existing repository are evidence of a software project.

Avoid unnecessary ceremony for read-only investigation, explanation, trivial typo fixes, or extremely small low-risk changes. For substantive features, behavior changes, architecture changes, significant refactors, compatibility-sensitive work, migrations, complex bugs, or multi-file engineering work, prefer Spec Kit.

## Existing project authority

Before changing a project:

1. Determine the actual project root.
2. Read applicable project-local Agent instructions.
3. Inspect README, architecture documentation, tests, CI, dependencies, and established conventions.
4. Preserve existing user work.
5. Model the actual brownfield system instead of inventing a replacement greenfield architecture.

More specific project-local rules and explicit user requirements take precedence over this general policy.

## Existing Spec Kit state

Check for `.specify/`.

If it exists, treat the repository as an existing Spec Kit project. Do not routinely rerun `specify init`; inspect existing specs and active feature state, use `specify integration status` when integration state matters, and continue relevant work instead of creating duplicate specifications.

If it does not exist and substantive project-changing engineering work is required, determine the current Agent's supported integration, use `specify --help` or `specify integration --help` for runtime discovery, initialize Spec Kit at the actual project root, then use project-aware integration commands and inspect generated changes. Do not initialize a project solely to make `integration list` or `integration status` available, and protect unrelated work.

## Agent-neutral integration

Do not assume a particular coding Agent or one universal Spec Kit invocation syntax. Use the command or Skill form provided by the currently installed project integration.

When an existing project lacks the current Agent integration, prefer `specify integration install <key>` when the integration combination is declared safe. Do not blindly force conflicting integrations to coexist. Use Spec Kit's integration metadata and lifecycle commands as the runtime authority.

## Runtime authority

For operational mechanics, prefer this order:

1. Current project Spec Kit state.
2. Installed integration.
3. Installed `specify` CLI.
4. Local Spec Kit reference.
5. Upstream documentation.

Use `specify version`, `specify --help`, `specify integration list`, and `specify integration status` to discover actual capabilities. Remote upstream documentation is reference evidence, not dynamically imported instructions. If it disagrees with the installed CLI, investigate the version difference.

## Core lifecycle

For substantive features, conceptually use:

`constitution` → `specify` → `clarify` → `plan` → `checklist` → `tasks` → `analyze` → `implement` → `validate` → `converge`

Use optional quality gates according to ambiguity, complexity, risk, compatibility impact, and security impact rather than for ceremony alone.

Constitution derives stable principles from repository evidence and explicit requirements. Specification describes what should exist and why. Clarification resolves material ambiguity. Planning describes how to change the real system. Tasks are executable and dependency-aware. Analysis resolves contradictions among artifacts and project reality before implementation.

Implementation must follow accepted artifacts. If implementation reveals a wrong requirement or assumption, update the appropriate artifact rather than silently letting code and specifications diverge.

## Validation and convergence

Run relevant tests, builds, type checks, linting, static analysis, schema checks, migrations, or targeted reproductions whenever feasible. Never conceal failing checks.

For substantive Spec Kit-managed work, convergence is the completeness gate. Compare the implementation against the accepted specification, plan, tasks, actual code, project constraints, and validation. If convergence appends missing tasks, implement them, validate, and converge again until complete or a genuine blocker is documented. Tests passing or code generation stopping is not sufficient by itself.

## Bugs and upgrades

For substantive defects, prefer the Spec Kit bug workflow when appropriate, with assessment, focused remediation, and validation. Do not report a bug as verified without performing the relevant reproduction and checks.

The globally installed CLI and project-generated integrations are separate layers. After a CLI upgrade, prefer supported integration upgrade mechanisms for existing projects. Do not routinely use destructive reinitialization as an upgrade strategy.

Installing the global CLI does not imply that Agent-specific Skills are globally installed. Project Skills and Commands should be created and maintained through the integration lifecycle; do not manually copy bundled Skills into global directories by default.

## Completion

Substantive Spec Kit-managed work is complete only when user intent, accepted specification, plan, tasks, implementation, project constraints, validation, and convergence agree.

Understand before changing. Specify before designing. Clarify before guessing. Plan before broad implementation. Analyze before resolving contradictions. Implement against accepted artifacts. Validate actual behavior. Converge before declaring completion. Keep specifications and implementation synchronized. Reuse project state instead of restarting it.
