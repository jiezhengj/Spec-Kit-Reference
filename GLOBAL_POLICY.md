# Spec Kit Global Policy

## Scope

Use GitHub Spec Kit for substantive software engineering. Do not require the full lifecycle for read-only investigation, explanation, trivial typo fixes, or extremely small low-risk changes.

## Project authority

Determine the actual project root, read all applicable project-local rules, inspect the brownfield system, and preserve existing user work before changing it. If `.specify/` exists, resume that project state instead of routinely reinitializing it. If `docs/spec-kit/MANIFEST.json` exists, read the committed project governance package; it is the shared project baseline.

If the project already has an `AGENTS.md`, it is project-owned instruction content. The Spec Kit governance loader may be appended to that file only through the reviewed manager plan; it must never replace, delete, reorder, normalize, or overwrite the existing bytes. If no `AGENTS.md` exists, the manager may create the loader file through the same reviewed plan.

## Agent integration

Determine the current Agent from an explicit user, host, or Agent runtime declaration. Never infer it from installed tools, existing directories, or the project's default integration. Every non-interactive initialization must pass an explicitly approved `--integration <key>`.

When the current CLI provides a native integration for the current Agent, that native integration is mandatory. An unwritable target, missing permission, sandbox restriction, managed-file repair failure, or installation failure is a blocker and must never trigger a fallback to `generic`. A project is not fully migrated until the native integration and its managed files are verified.

If the current CLI has no native integration, `generic` is allowed only when the committed project configuration permits it, a current-version human-reviewed native-absence attestation and exact compatibility contract exist, the installed integration set is empty, and the user approves the exact operation plan. It must be reported as limited, non-native support.

## Runtime and completion

For operational mechanics, prefer current project state, installed integration, installed `specify` CLI, committed project Reference, this central source, then upstream documentation. Keep accepted specifications, plans, tasks, implementation, validation, and convergence synchronized. Never hide failing checks or declare completion with an unresolved blocker.

## Central update source

SPEC_KIT_GOVERNANCE_SOURCE: <ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>

Before deploying this source, replace the placeholder exactly once with the readable absolute path of the local SpecKitReference repository root. The directory must contain `SPEC_KIT_REFERENCE.md`, `GLOBAL_POLICY.md`, and `UPSTREAM_BASELINE`. This source is advisory for explicit maintenance and update review only. If it is unavailable, do not scan arbitrary directories or promote upstream material into instructions; continue with committed project rules and runtime discovery.
