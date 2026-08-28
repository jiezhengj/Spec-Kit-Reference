<!-- SPEC-KIT-GLOBAL-POLICY:START version=1.2.0 -->

# Spec Kit Global Policy

## Scope

Use GitHub Spec Kit for substantive software engineering. Do not require the full lifecycle for read-only investigation, explanation, trivial typo fixes, or extremely small low-risk changes.

## Project authority

Determine the actual project root, read all applicable project-local rules, inspect the brownfield system, and preserve existing user work before changing it. If `.specify/` exists, resume that project state instead of routinely reinitializing it. If `docs/spec-kit/MANIFEST.json` exists, read the committed project governance package; it is the shared project baseline.

If the project already has the runtime-selected project context anchor, that file is project-owned instruction content. The Spec Kit governance loader may be appended to or updated inside that file only through the reviewed manager plan; every byte outside the managed loader region must remain unchanged. Never replace, delete, reorder, normalize, or overwrite the anchor. If no anchor exists, create only the exact project-relative path supplied and evidence-validated by the current Agent runtime or the user; never guess a filename.

During first-time Spec Kit initialization, the current Agent must ask the user which BCP-47 language tag to use for new or substantially rewritten project documentation. Pass that exact user selection to the manager and persist it in the project configuration and managed context-anchor loader. Do not infer the language from locale, Agent product, existing documents, or a default.

## Agent integration

Determine the current Agent from an explicit user, host, or Agent runtime declaration. Never infer it from installed tools, existing directories, or the project's default integration. Every non-interactive initialization must pass an explicitly approved `--integration <key>`.

When the current CLI provides a native integration for the current Agent, that native integration is mandatory. An unwritable target, missing permission, sandbox restriction, managed-file repair failure, or installation failure is a blocker and must never trigger a fallback to `generic`. A project is not fully migrated until the native integration and its managed files are verified.

If the current CLI has no native integration, `generic` is allowed only when the committed project configuration permits it, a current-version human-reviewed native-absence attestation and exact compatibility contract exist, the installed integration set is empty, and the user approves the exact operation plan. It must be reported as limited, non-native support.

## Runtime and completion

For operational mechanics, prefer current project state, installed integration, installed `specify` CLI, committed project Reference, this central source, then upstream documentation. Keep accepted specifications, plans, tasks, implementation, validation, and convergence synchronized. Never hide failing checks or declare completion with an unresolved blocker.

For substantive work, approval of a conversational proposal such as “方案可以” authorizes advancing the direction into the upstream Spec Kit workflow; it does not authorize direct application-code edits before the current specification, plan, and tasks are aligned. The Reference package must not directly edit `.specify/**`, `specs/**`, or native Agent-generated files. The central Reference and a globally deployed Policy are maintenance conveniences, not target-project runtime prerequisites.

## Central update source

SPEC_KIT_GOVERNANCE_SOURCE: <ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>

Before deploying this source, replace the placeholder exactly once with the readable absolute path of the local SpecKitReference repository root. The directory must contain `SPEC_KIT_REFERENCE.md`, `GLOBAL_POLICY.md`, and `UPSTREAM_BASELINE`. When this Policy is actually loaded, and `.specify/` plus the committed project governance package exist, the Agent may run the central manager's read-only `check-update --source <path>` once before the first substantive task in a new session. If the Policy, source, or verification is unavailable, skip silently; never scan arbitrary directories or treat an unverified source as an update. A verified update is informational and requires an exact reviewed plan and explicit approval before synchronization.

<!-- SPEC-KIT-GLOBAL-POLICY:END -->
