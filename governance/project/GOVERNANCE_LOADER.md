<!-- PROJECT-SPEC-KIT-GOVERNANCE:START -->

# Spec Kit Governance

This repository uses the committed project-local Spec Kit governance package.

Read `docs/spec-kit/START_HERE.md` before substantive engineering work.

At entry to an existing Spec Kit project, run `tools/spec-kit-governance/governance.py check-capabilities`. If `specify`, the active integration, `assess`, or `bug` is missing, ask the user whether to install the missing capability through the native CLI. If the user declines, return `HANDOFF_TO_AGENT` and let the current Agent continue without applying Reference governance to that capability.

A conversational approval such as `the plan is acceptable` advances a direction into the upstream Spec Kit workflow; it does not authorize direct application-code edits before the current Spec Kit artifacts are aligned.

The governance package does not edit `.specify/**`, `specs/**`, or native Agent-generated integration files.

Do not replace the project baseline with personal global rules or a local Reference.

<!-- PROJECT-SPEC-KIT-GOVERNANCE:END -->
