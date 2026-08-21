# Maintenance history

## 2026-08-21 — Documentation normalization

- Rewrote `README.md` around the current portable governance package, manager, release, deployment, and validation workflow.
- Translated every Markdown document under `docs/` to English while preserving commands, paths, hashes, statuses, and normative constraints.

## 2026-08-21 — Portable project governance implementation

- Added the Agent-neutral project governance package templates, schemas, capability baseline, resolver contract, and release metadata.
- Added the portable governance manager with explicit plan/apply authorization, native-integration blocker semantics, explicit generic transition attestation, fresh-session binding activation, upgrade/rollback planning, and atomic manager writes with recovery evidence.
- Added deterministic portable and extension release builders/validators and a 68-test governance contract suite covering the preserved upstream checker, CI, wrapper, policy, integration, lifecycle, deployment, and isolated-init rehearsal capabilities.
- Renamed the root policy source to `GLOBAL_POLICY.md`, added explicit documentation-language rationale, and kept the dated implementation snapshot as a non-portable maintenance artifact.
- Moved the one-time implementation contract to `docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md` so the live `docs/` directory contains only ongoing maintenance documents.

## 2026-08-21 — Native Agent integration requirement

- Added a hard requirement to use the native Spec Kit integration whenever a concrete Agent, such as Codex, is in scope.
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
