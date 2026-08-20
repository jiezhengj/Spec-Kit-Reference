# Maintenance history

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
