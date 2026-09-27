# Maintenance history

## 2026-09-27 — Compatible governance release 2.1.0

- Bumped the compatible v2 package, Policy, manager, and extension to `2.1.0` so existing `2.0.0` projects can detect the update.
- Recorded the full macOS and Windows central Reference paths and pinned governed non-interactive initialization to Python scripts.
- Added regression coverage for the dual-host locator, release metadata, and `--script py` in both manager rehearsal and actual invocation.

## 2026-09-27 — Reference source repository scope gate

- Added an early source-repository boundary to `AGENTS.md` and `GLOBAL_POLICY.md` so Reference maintenance does not trigger target-project Feature routing or `.specify/` initialization.
- Limited the exception to a checkout containing both `SPEC_KIT_REFERENCE.md` and `UPSTREAM_BASELINE`; downstream product work remains governed by the portable Policy.
- Recorded scoped upstream impact without advancing the baseline because the full range was not reviewed.

## 2026-09-27 — Platform-independent Python project initialization

- Required Reference-governed non-interactive initialization to pass `--script py`, removing host-dependent PowerShell/shell selection.
- Updated `plan-init` rehearsal and actual invocation together and synchronized the central and project policy/reference documents.
- Recorded the scoped upstream evidence without advancing the baseline because the full intervening history was not reviewed.

## 2026-09-21 — Reference-independent upstream update maintenance

- Made the Spec Kit upstream update check activate for every existing `.specify/` project, whether or not a central Reference or `docs/spec-kit/**` package is present.
- Limited the user approval gate to a reported CLI upgrade; supported refreshes of installed integrations, extensions, and workflows are automatic and never add `--force`.
- Preserved the central Reference check as a separate source-gated maintenance operation.

## 2026-09-21 — Task-scoped high-assurance routing

- Added an explicit high-risk Feature route question between task-scoped `governed-sdd` and the adaptive full upstream path.
- Clarified that both routes use upstream Spec Kit and that a task-scoped choice never changes the project default configuration.
- Clarified that the companion is selected, installed, or verified only for the route that requires it; ordinary adaptive work remains non-blocking when it is absent.
- Added regression coverage for the routing contract and preserved the default `upstream-adaptive` profile.

## 2026-09-21 — Adaptive routing, automatic Reference upgrades, and official extensions

- Replaced the mandatory governed default with the adaptive upstream profile; the former `governed-sdd-required` configuration is migrated automatically and no legacy-strict profile is retained.
- Added version-neutral CLI contract probing and removed exact Specify release gating.
- Added `check-capabilities`, official `assess`/`bug` capability detection, consented native extension installation, and `HANDOFF_TO_AGENT` behavior after refusal.
- Added hash-bound `auto-upgrade` for Reference-owned synchronization without a project-owner approval prompt while preserving the `.specify/**`, `specs/**`, native integration, and business-code ownership boundary.

## 2026-09-04 — Governed discovery and executable task contracts

- Added mandatory structured Discovery for substantive Spec intent, with explicit exit criteria for blocking questions, high-impact assumptions, scope, primary journeys, and user-approved snapshots.
- Added hash-bound human review ledgers for Discovery, specification, plan bundle, task package, and remediation; Agent self-review cannot create approval and changed artifacts make approval stale.
- Added tiny-model task-package readiness and cold-start validation so implementation work can be handed to an executor without the originating conversation.
- Added the `governed-sdd` companion workflow, discovery extension, tiny-model preset, and manager checks while preserving upstream ownership of `.specify/**`, `specs/**`, and native Agent-generated artifacts.
- Defined the reviewed `1.3.0` bridge and `2.0.0` strict migration, rollback, manifest-v2, and project-local feature-sidecar preservation contracts.

## 2026-09-04 — Upstream baseline review

- Reviewed `5aa8bea7823dcd056f111f847bf2d576bad3f0a5` through `df6b3187022ce986759bd854467e8a4bb56bb0f4` after fetching `upstream/main`.
- Classified the range as `REFERENCE`: workflow slots, bundled workflow `1.0.1`, stricter artifact prerequisites, `FEATURE_DIR` script output, new integrations, and runtime hardening were reviewed without promoting upstream content into local Policy.
- Documented that the bundled workflow gates only specification and planning and does not automatically provide clarification, task review, analysis, validation, or convergence.
- The earlier baseline review recorded `specify 1.0.4` for its workflow, preset, and extension command surfaces; current CLI versions remain runtime evidence rather than a package compatibility pin.
- Advanced the baseline only after the Reference update and repository validation completed.

## 2026-08-28 — Central Reference update handoff

- Added a source-gated, session-scoped read-only check for a newer central Reference when the loaded global Policy provides the explicit source locator.
- Made missing Policy, missing central source, dirty source, and unverifiable source silent and non-blocking during normal target-project work.
- Extended the approved governance upgrade path to update the target governance package, manager, and managed context-anchor Reference check block only.
- Preserved the upstream ownership boundary: `.specify/**`, `specs/**`, native Agent files, specification, plan, and tasks remain outside the Reference synchronizer.
- Published the policy-affecting governance package update as `1.2.0`.

## 2026-08-28 — Optional CLI update reminder

- Added `plan-install-update-reminder` for already Spec Kit projects that want a CLI update reminder without global Policy or `docs/spec-kit/**`.
- Limited the target mutation to a separate managed block in the explicitly selected existing context anchor; the reminder delegates detection to upstream `specify self check`.
- Preserved explicit approval for `specify self upgrade` and kept `.specify/**`, `specs/**`, and native Agent integration files outside manager ownership.
- Published the compatible governance package update as `1.1.1`.

## 2026-08-28 — Upstream baseline review

- Reviewed `fa19e1c68b6daec5cab3309913cf5ecf6553075d` through `5aa8bea7823dcd056f111f847bf2d576bad3f0a5` after fetching `upstream/main`.
- Classified the range as `REFERENCE`: existing-project adoption guidance, active-feature state selection, workflow Python init scripts, and runtime validation hardening were reviewed; catalog-only changes had no local governance impact.
- Updated the central and project References with the justified runtime facts while preserving the independently approved local requirement for `analyze`, `validate`, and `converge`.
- Confirmed that no upstream-produced `.specify/`, `specs/`, or native Agent integration artifact is modified by this repository.
- Advanced `UPSTREAM_BASELINE` only after documentation and validation completed.

## 2026-08-28 — Substantive task entry and ownership boundary

- Made conversational approval such as “方案可以” an entry into upstream Spec Kit artifact alignment, not permission for direct application-code edits.
- Required the current specification, plan, and tasks to be aligned before implementation, with `analyze`, `validate`, and `converge` required before substantive completion.
- Kept the upstream CLI as the sole executor for `.specify/**`, `specs/**`, and native Agent-generated integration files; added manager rejection of out-of-bound local mutations.
- Documented that a target project needs its local governance additions and installed `specify`/Spec Kit state, but not a personal global Policy or central Reference directory at runtime.
- Published the compatible governance package update as `1.1.0` and left the unrelated upstream baseline review for a separate maintenance change.

## 2026-08-21 — Documentation normalization

- Rewrote `README.md` around the current portable governance package, manager, release, deployment, and validation workflow.
- Kept `README.md` as a complete English-and-Chinese mirror: every English section now has a corresponding Chinese section with the same commands, paths, statuses, and constraints.
- Standardized global and project-level governance markers with unified hyphen/colon delimiters: wrapped `GLOBAL_POLICY.md` with `SPEC-KIT-GLOBAL-POLICY` markers and updated the project anchor loader with `PROJECT-SPEC-KIT-GOVERNANCE` markers and an H1/H2 heading hierarchy.
- Made the runtime-selected project context anchor append-only for the governance loader and added regression coverage for byte-preserving injection and protected replace/create mutations.
- Added explicit user-selected BCP-47 documentation-language capture during `plan-init`, including managed-anchor injection and project configuration persistence.

## 2026-08-21 — Portable project governance implementation

- Added the Agent-neutral project governance package templates, schemas, capability baseline, resolver contract, and release metadata.
- Added the portable governance manager with explicit plan/apply authorization, native-integration blocker semantics, explicit generic transition attestation, fresh-session binding activation, upgrade/rollback planning, dynamic runtime-reported target scopes, and atomic manager writes with recovery evidence.
- Added deterministic portable and extension release builders/validators and a 76-test governance contract suite covering the preserved upstream checker, CI, wrapper, policy, integration, lifecycle, deployment, language-selection, anchor-protection, and isolated-init rehearsal capabilities.
- Renamed the root policy source to `GLOBAL_POLICY.md`, added explicit documentation-language rationale, and kept the dated implementation snapshot as a non-portable maintenance artifact.
- Moved the one-time implementation contract to `docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md` so the live `docs/` directory contains only ongoing maintenance documents.

## 2026-08-21 — Native Agent integration requirement

- Added a hard requirement to use the native Spec Kit integration whenever a concrete Agent is in scope.
- Defined permission, sandbox, and unwritable-path failures as blockers rather than reasons to downgrade to `generic`.
- Required verification of the Agent-specific generated layout and managed-file status before migration completion or push.

## 2026-08-20

Created the first governance-layer structure from the supplied implementation plan.

- Added Agent-neutral global policy and local operational reference.
- Added `origin` and `upstream` remote conventions.
- Added baseline-based deterministic upstream detection.
- Added scheduled and manual GitHub Actions notification.
- Reviewed upstream `abfc66b670c81b9758f1f47f18f7fea0f48686cf` and recorded it in `UPSTREAM_BASELINE`.
- Confirmed current upstream evidence for integrations, Agentic SDD, bug workflow, upgrades, and convergence.
- Verified local `specify` version `0.16.6.dev0`; recorded the integration subcommand trampoline failure for follow-up.

## 2026-08-21

Reviewed upstream `abfc66b670c81b9758f1f47f18f7fea0f48686cf` to `fa19e1c68b6daec5cab3309913cf5ecf6553075d`.

- Classified the Qoder CLI command-to-Skills migration as `REFERENCE`.
- Updated the local reference to warn that generated integration layouts can evolve.
- Added baseline ancestry protection and hardened the scheduled workflow against duplicate runs and unexpected checker exit codes.
- Re-verified the local CLI after the Python PATH repair and documented that integration discovery/status commands require a Spec Kit project root.
- Completed a post-implementation audit: documented first-time upstream remote setup and deployment-only Reference locators, aligned the lifecycle summary with the validation gate, and made stale offline refs distinguishable from invalid upstream history.
- Added official upstream URL validation, a Windows `py`-launcher fallback, and Ubuntu/Windows wrapper validation in CI.
