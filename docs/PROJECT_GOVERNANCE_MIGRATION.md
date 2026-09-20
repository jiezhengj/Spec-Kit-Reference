# Release-line selection

`NONE` does not publish a governance package; `REFERENCE` bumps the patch
version; a compatible `POLICY` change bumps the minor version; an incompatible
change to a fixed path, schema, manager contract, adapter contract, marker, or
hash contract bumps the major version.

The current package uses the adaptive v2 profile as its default. A project
upgrade preserves user-owned evidence and automatically migrates the former
mandatory companion defaults to `upstream-adaptive`; no legacy-strict profile
is retained.

The historical `1.3.0` bridge and `2.0.0` release artifacts remain readable
for package and rollback compatibility. `MIGRATION_REQUIRED` describes an
unconverted v1 artifact boundary only; it is not a runtime workflow profile
and does not justify retaining a legacy-strict project mode.

# Routine v1 update

For a compatible update, first check the clean central Reference checkout,
compare its Git revision with the target manifest, generate and automatically
apply `auto-upgrade --source <central-or-staged-source>`. The exact plan still
reviews the Policy, Reference, manager, separately managed governance-loader
and Reference-update-check context-anchor blocks, adapter, manifest, project
profile, and capability inventory. The project-owned
`LOCAL_OVERRIDES.md`, `PROJECT_CONFIG.json`, and `ADAPTERS.json` are not
overwritten by the central package. An upgrade must not modify `.specify/**`,
`specs/**`, or native Agent-generated integration files; those remain under
upstream CLI or project ownership.

# V1 to v2 migration

The bridge manager must first generate a read-only inventory and atomic
`plan-upgrade-governance-v2`. The plan must bind its source revision, input
hashes, migration-record hash, exact manager mutations, external upstream CLI
argv, backup locations, and rollback journal. It must name
`docs/spec-kit/features/**` as a preserved project-local subtree and must not
rewrite its contents.

The exact plan validates the v2 config conversion, workflow-governance
settings, companion capability discovery, context-anchor managed blocks,
feature-review evidence path, rollback journal, and any required upstream
workflow/preset/extension installation. Any changed input, source, feature
artifact hash, or CLI capability invalidates the plan.

Applying a v2 plan may write only Reference-owned governance additions and
explicitly scoped upstream CLI outputs. It must never directly write
`.specify/**`, `specs/**`, native Agent-generated files, business files, or
user-owned anchor content outside managed blocks. The manager must return
`COMPANION_CAPABILITY_UNAVAILABLE` when the current CLI cannot install or
resolve the companion primitives; it may not mark a weaker workflow ready.

The central Reference session check is enabled only when the current Agent has actually loaded the global Policy and its `SPEC_KIT_GOVERNANCE_SOURCE` locator resolves to the central checkout. If either is absent or unverifiable, normal project work proceeds without a Reference update notice and without scanning arbitrary directories. This does not disable the independent upstream Spec Kit update protocol: whenever `.specify/` exists, the Agent checks the installed CLI at most once per new session and handles approved CLI upgrades plus no-force installed-component refreshes according to the current CLI contracts. After the governance layer is synchronized, the upstream Spec Kit workflow independently decides whether specifications, plans, tasks, or other Spec Kit artifacts require alignment.

The central Reference and global Policy are maintenance inputs, not runtime prerequisites. A target project remains operational with its committed `docs/spec-kit/**` package, local manager, runtime state, and managed governance-loader/Reference-update-check blocks, even when the maintainer's central Reference directory or global Policy is unavailable.

Central Reference update detection is deliberately conditional: the current Agent must have actually loaded the global Policy and that Policy must provide the explicit central source locator. Without either, the target continues from its committed local snapshot and receives no Reference update notice. When a clean central source is newer, the Agent automatically synchronizes only the governance and context layer through the exact generated plan. The upstream Spec Kit workflow then decides whether any specification, plan, tasks, or other upstream artifacts require changes.

# Rollback

A rollback first generates `plan-rollback` or
`plan-rollback-governance-v2`, lists the target version and managed files,
verifies that upstream- and user-owned files are not in the target set, and is
then executed by `apply-plan`. v2 rollback restores v1 governance only through
the bridge journal. It retains review ledgers and other feature-sidecar evidence
as read-only history. It must not uninstall an integration, delete user work,
delete `.specify/**`, delete `specs/**`, or restore unplanned files by default.
Return `RECOVERY_REQUIRED` when the recovery journal is incomplete.
