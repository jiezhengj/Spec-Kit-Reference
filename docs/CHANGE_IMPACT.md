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

## Local policy amendment — substantive task entry

Date:

`2026-08-28`

Classification:

`POLICY`

Trigger:

In Spec Kit projects, an Agent could interpret conversational approval such as “方案可以” as immediate permission to edit application code, even when the approved direction was not represented in the current specification, plan, and tasks.

Decision:

Conversational approval advances the direction into the upstream Spec Kit artifact workflow; it does not authorize direct code edits before artifact alignment. Discussion-only work remains non-mutating. The Reference package remains a governance guide and manager for its own additions, not a second Spec Kit executor. The upstream CLI continues to own `.specify/**`, `specs/**`, and native Agent-generated integration files. `analyze`, `validate`, and `converge` are required before substantive completion.

A manager ownership guard rejects direct local mutations outside `docs/spec-kit/**`, `tools/spec-kit-governance/governance.py`, `.spec-kit-governance/**`, and the managed loader or Reference-update-check blocks in the explicit context anchor. Global Policy and the central Reference are not target-project runtime prerequisites for offline work.

Affected documents:

- `GLOBAL_POLICY.md`
- `SPEC_KIT_REFERENCE.md`
- `governance/project/START_HERE.md`
- `governance/project/POLICY.md`
- `governance/project/OPERATING_PROTOCOL.md`
- `governance/project/REFERENCE.md`
- `governance/manager/speckit_governance.py`

Validation:

The `1.1.0` release metadata, portable package, extension package, manager ownership regression, conversation-approval contract, schema validation, `pytest`, `unittest`, and compile checks passed. This local policy amendment did not advance the upstream baseline; the following section records the separate upstream review.

## Local capability addition — 2026-08-28

### Classification

`POLICY`

### Decision

Added a source-gated, session-scoped central Reference update check. It runs only when the current Agent has loaded the global Policy and that Policy exposes a readable `SPEC_KIT_GOVERNANCE_SOURCE` path. Without the global Policy or central source, normal target-project work skips the check silently and does not scan arbitrary directories.

### Synchronization boundary

After a verified update is reported and the user explicitly approves an exact plan, synchronization updates only the target governance package, local manager, and the managed Reference-update block in the selected context anchor. It does not edit `.specify/**`, `specs/**`, native Agent-generated files, or business code. The upstream Spec Kit workflow independently decides whether specification, plan, tasks, or other Spec artifacts require alignment.

### Release

This policy-affecting capability is published as governance package `1.2.0` with `policy_version` `1.2.0`. The existing CLI-only `plan-install-update-reminder` remains available as a separate lightweight path.

## Local capability addition — 2026-08-28

### Classification

`REFERENCE`

### Decision

Added the optional `plan-install-update-reminder` operation for an already Spec Kit project that has an installed `specify` CLI and an existing explicit context anchor but does not install the full `docs/spec-kit/**` governance package. The operation appends only a separate managed reminder block. The Agent is instructed to call upstream `specify self check` once per session and to request approval before `specify self upgrade`.

### Boundary verification

The operation does not create or copy the project governance package, does not copy the manager into the target project, and does not modify `.specify/**`, `specs/**`, or native Agent-generated integration files. No global Policy or central Reference directory is required at runtime. The reminder is informational; an offline or timed-out update check is non-blocking.

### Release

This compatible Reference capability is published as governance package `1.1.1`; `policy_version` remains `1.1.0`. The portable and extension artifacts remain subject to the existing plan/apply, checksum, and explicit approval protocols.

## Upstream review — 2026-08-28

### Review range

Baseline:

`fa19e1c68b6daec5cab3309913cf5ecf6553075d`

Reviewed through:

`5aa8bea7823dcd056f111f847bf2d576bad3f0a5`

### Classification

`REFERENCE`

### Relevant upstream changes

The range includes the Spec Kit `1.0.1` release and subsequent `1.0.2.dev0` development changes. The relevant operational changes are the existing-project adoption guide, the distinction between Spec Kit project-file maintenance and feature-artifact evolution, the `.specify/feature.json` active-feature selector, Python support for workflow init scripts, and additional validation hardening for bundles, presets, events, and catalog inputs. Community catalog content and dependency-only changes do not alter this repository's governance contract.

### Local impact

The local central and project References now record that the active feature is selected by `.specify/feature.json` or `SPECIFY_FEATURE_DIRECTORY`, not by the Git branch; existing-project initialization uses the upstream `specify init --here --force --integration <key>` command under the existing reviewable-baseline and manager-scope protections; and workflow init script choices include `sh`, `ps`, and `py` where the installed CLI exposes them. No upstream-produced artifact is copied, replaced, or edited by this repository.

The upstream quickstart documents both a shorter lifecycle and a full lifecycle with optional quality gates. This repository keeps its independently approved local policy requiring `analyze`, `validate`, and `converge` before substantive completion. The upstream range is therefore `REFERENCE`, not a local Policy replacement.

### Runtime compatibility

The installed local CLI is `specify 1.0.2.dev0`, matching the reviewed upstream source version `1.0.2.dev0`. Runtime behavior must continue to be checked against the installed CLI and project state; the release manifest records the reviewed upstream revision separately.

### Conclusion

The range is reviewed and the local Reference updates are complete. No global Policy change is justified by these upstream commits. After repository validation, advance `UPSTREAM_BASELINE` to `5aa8bea7823dcd056f111f847bf2d576bad3f0a5` as the last maintenance mutation.
