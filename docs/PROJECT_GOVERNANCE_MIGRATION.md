# Version migration

`NONE` does not publish a governance package; `REFERENCE` bumps the patch version; a compatible `POLICY` change bumps the minor version; an incompatible change to a fixed path, schema, manager contract, adapter contract, marker, or hash contract bumps the major version.

An upgrade must first check the clean central Reference checkout, compare its Git revision with the target manifest, generate `plan-upgrade --source <central-or-staged-source>`, review the Policy, Reference, manager, separately managed governance-loader and Reference-update-check context-anchor blocks, adapter, manifest, and capability inventory, and then apply the plan. The project-owned `LOCAL_OVERRIDES.md`, `PROJECT_CONFIG.json`, and `ADAPTERS.json` are not overwritten by the central package. An upgrade must not modify `.specify/**`, `specs/**`, or native Agent-generated integration files; those remain under upstream CLI or project ownership.

The session check is enabled only when the current Agent has actually loaded the global Policy and its `SPEC_KIT_GOVERNANCE_SOURCE` locator resolves to the central checkout. If either is absent or unverifiable, normal project work proceeds without a Reference update notice and without scanning arbitrary directories. After the governance layer is synchronized, the upstream Spec Kit workflow independently decides whether specifications, plans, tasks, or other Spec Kit artifacts require alignment.

The central Reference and global Policy are maintenance inputs, not runtime prerequisites. A target project remains operational with its committed `docs/spec-kit/**` package, local manager, runtime state, and managed governance-loader/Reference-update-check blocks, even when the maintainer's central Reference directory or global Policy is unavailable.

Central Reference update detection is deliberately conditional: the current Agent must have actually loaded the global Policy and that Policy must provide the explicit central source locator. Without either, the target continues from its committed local snapshot and receives no Reference update notice. When a clean central source is newer, the Agent reports the candidate and waits for explicit approval before synchronizing only the governance and context layer. The upstream Spec Kit workflow then decides whether any specification, plan, tasks, or other upstream artifacts require changes.

# Rollback

A rollback first generates `plan-rollback`, lists the target version and managed files, verifies that upstream- and user-owned files are not in the target set, and is then executed by `apply-plan`. It must not uninstall an integration, delete user work, or restore unplanned files by default. Return `RECOVERY_REQUIRED` when the recovery journal is incomplete.
