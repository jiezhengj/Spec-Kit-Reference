<!-- PROJECT-SPEC-KIT-REFERENCE-UPDATE-CHECK:START version=1 -->

# Spec Kit Reference update check

This check is active only when the current Agent has loaded the global Spec Kit Policy and that Policy provides a readable `SPEC_KIT_GOVERNANCE_SOURCE` absolute path.

When `.specify/` and the committed project governance package are present, run the local governance manager's read-only `check-update --source <central-reference-path>` once before the first substantive task in a new Agent session. If the Policy or source locator is absent, skip this check silently; do not scan the computer for a Reference directory.

If a verified Reference update is available, tell the user and wait for explicit approval before staging and applying a `plan-upgrade`. The sync may update only Reference-owned governance files and this managed block; it must never edit `.specify/**`, `specs/**`, native Agent files, or business code. After the governance sync, let the upstream Spec Kit workflow decide whether any specification, plan, or task artifacts need updating.

A missing source, unclean source, invalid verification, offline check, or timeout is non-blocking in normal project work and must not be presented as an available update.

<!-- PROJECT-SPEC-KIT-REFERENCE-UPDATE-CHECK:END -->
