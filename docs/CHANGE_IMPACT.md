# Upstream impact assessment

## Review range

Baseline:

`abfc66b670c81b9758f1f47f18f7fea0f48686cf`

Reviewed through:

`fa19e1c68b6daec5cab3309913cf5ecf6553075d`

## Date

2026-08-21

## Classification

REFERENCE

## Relevant upstream changes

Reviewed commit `fa19e1c68b6daec5cab3309913cf5ecf6553075d` fixes the Qoder CLI migration from `.qoder/commands/*.md` to `.qoder/skills/<name>/SKILL.md`, updates invocation style, and retires legacy flat extension commands after replacement Skills are present.

## Impact on SPEC_KIT_REFERENCE.md

The local reference now explicitly states that generated integration artifacts can migrate between command and Skills layouts and that current project integration status and managed-file metadata are authoritative. No Qoder-specific command is required because the local reference intentionally remains Agent-neutral.

## Impact on AGENTS.md

The repository maintenance policy is intentionally independent of dynamically fetched upstream instructions. No upstream content has been promoted to governance authority.

## Runtime compatibility

Installed/expected CLI:

`specify` version was verified as `0.16.6.dev0`; `specify integration --help` succeeds. In this governance repository, `specify integration list` and `specify integration status` correctly report that no `.specify/` project exists. The earlier `uv trampoline` failure was resolved by registering Python314 on PATH.

Potential version mismatch:

The upstream reviewed commit, local reference, and installed CLI may differ and must be recorded separately when verified. Project-level integration behavior still needs to be checked from a real Spec Kit project root.

## Changes made

- [x] Created the repository governance and reference documents.
- [x] Added deterministic upstream detection.
- [x] Added scheduled and manual notification workflow.
- [x] Complete the current upstream semantic review.
- [x] Record the current reviewed upstream SHA.
- [x] Record the installed `specify` CLI version, if available.

## Conclusion

The Qoder integration change is classified as `REFERENCE`: it changes generated artifact layout for one integration but does not change the local Agent governance lifecycle. The baseline has advanced to the reviewed commit after repository validation. The current CLI is operational; project-level integration behavior remains to be checked from a real Spec Kit project root.

## Local policy amendment

Date:

`2026-08-21`

Classification:

`POLICY`

Trigger:

The DriversLicense migration review found that choosing `generic` because the Codex Skills target was not writable produced a valid Agent-neutral project but did not satisfy the requirement to expose Codex Spec Kit Skills.

Decision:

When a concrete Agent is in scope, its native Spec Kit integration is mandatory. Permission, sandbox, or unwritable-path failures are blockers and must not trigger a silent downgrade to `generic`. A migration cannot be marked complete or pushed as complete until the native integration and its managed files are verified. `generic` remains available only for an explicitly Agent-neutral request.

Affected documents:

- `GLOBAL_POLICY.md`
- `SPEC_KIT_REFERENCE.md`

Validation:

The rule was added to the single logical Policy source and the corresponding operational reference. Existing upstream baseline data was not changed.
