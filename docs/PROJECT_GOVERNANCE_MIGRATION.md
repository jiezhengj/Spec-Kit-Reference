# Version migration

`NONE` does not publish a governance package; `REFERENCE` bumps the patch version; a compatible `POLICY` change bumps the minor version; an incompatible change to a fixed path, schema, manager contract, adapter contract, marker, or hash contract bumps the major version.

An upgrade must first check the fixed central release index, generate `plan-upgrade`, review the Policy, Reference, manager, adapter, manifest, and capability inventory, and then apply the plan. The project-owned `LOCAL_OVERRIDES.md`, `PROJECT_CONFIG.json`, and `ADAPTERS.json` are not overwritten by the central package. An upgrade must not modify `.specify/**`, `specs/**`, or native Agent-generated integration files; those remain under upstream CLI or project ownership.

The central Reference and global Policy are maintenance inputs, not runtime prerequisites. A target project remains operational with its committed `docs/spec-kit/**` package, local manager, runtime state, and managed loader, even when the maintainer's central Reference directory or global Policy is unavailable.

# Rollback

A rollback first generates `plan-rollback`, lists the target version and managed files, verifies that upstream- and user-owned files are not in the target set, and is then executed by `apply-plan`. It must not uninstall an integration, delete user work, or restore unplanned files by default. Return `RECOVERY_REQUIRED` when the recovery journal is incomplete.
