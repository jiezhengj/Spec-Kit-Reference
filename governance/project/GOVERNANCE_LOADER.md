<!-- PROJECT-SPEC-KIT-GOVERNANCE:START -->

# Spec Kit Governance

This repository uses the committed project-local Spec Kit governance package.

Read `docs/spec-kit/START_HERE.md` before substantive engineering work.

At entry to an existing Spec Kit project, run `tools/spec-kit-governance/governance.py check-capabilities`. If `specify`, the active integration, `assess`, or `bug` is missing, ask the user whether to install the missing capability through the native CLI. If the user declines, return `HANDOFF_TO_AGENT` and let the current Agent continue without applying Reference governance to that capability.

Whenever `.specify/` exists, independently of the central Reference or `GLOBAL_POLICY.md`, perform the upstream Spec Kit update check at most once per new Agent session before the first substantive action. Run the currently installed CLI's read-only `specify self check`; do not assume an exact version or installation source. Ask the user before `specify self upgrade` only when a newer CLI is reported. Regardless of whether that CLI upgrade is approved, declined, or not needed, inspect the current integration, installed extensions, and installed workflows using the CLI's actual help/status/list contracts and automatically run supported refresh commands such as `specify integration upgrade <active-key>`, `specify extension update`, and `specify workflow update` when components can be refreshed. If the CLI has no freshness field, a supported no-force update command may be run and its no-update result is sufficient. Do not install missing components, assume presets are covered, invent flags, or add `--force`. If refresh is blocked by modified managed files, a requested `--force`, an unsafe scope, or another irreversible choice, stop and ask the user with the exact reason and paths.

A conversational approval such as `the plan is acceptable` advances a direction into the upstream Spec Kit workflow; it does not authorize direct application-code edits before the current Spec Kit artifacts are aligned.

The governance package does not edit `.specify/**`, `specs/**`, or native Agent-generated integration files.

Do not replace the project baseline with personal global rules or a local Reference.

<!-- PROJECT-SPEC-KIT-GOVERNANCE:END -->
