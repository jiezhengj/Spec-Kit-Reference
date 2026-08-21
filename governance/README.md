# Data contracts

`governance/` is the central portable source for the project governance package. Every JSON file uses UTF-8, LF, and JSON Schema Draft 2020-12.

## Fixed files

- `project/PROJECT_CONFIG.default.json` is the only initial template for the `docs/spec-kit/PROJECT_CONFIG.json` committed by a new project.
- `capability-baseline.json` is the pre-implementation capability-conservation inventory; it is not runtime configuration and must not be overwritten by a project installer.
- `schemas/` defines the V1 contracts for the governance manifest, project configuration, adapter registry, resolution result, operation plan, and capability baseline.

The central repository also retains detailed implementation contracts and acceptance materials:

- `docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md`: a snapshot of the complete architecture, state, commands, and completion definition for this implementation.
- `docs/PROJECT_GOVERNANCE_MIGRATION.md`: rules for upgrades, rollbacks, and project migration.
- `docs/PROJECT_GOVERNANCE_OPERATIONS.md`: the operating manual for implementation Agents.
- `docs/PROJECT_GOVERNANCE_SECURITY.md`: security boundaries for paths, external CLIs, logs, and recovery.
- `docs/PROJECT_GOVERNANCE_TEST_MATRIX.md`: the release-blocking test matrix.

These documents belong to the implementation and review layer of the central governance repository and are not copied into a business project's governance package. The dated implementation snapshot is for this rollout's audit and is not a long-term runtime dependency; business projects carry only the portable runtime files in `docs/spec-kit/`.

## Validation order

1. Validate `PROJECT_CONFIG.default.json` against `project-config.schema.json` first.
2. Validate `capability-baseline.json` against `capability-baseline.schema.json` next.
3. Before the manager generates or reads any other governance JSON, it must validate it against the schema with the same name; stop for an unknown schema version or enum.

## Maintenance boundary

Central upgrades must not overwrite project-owned `LOCAL_OVERRIDES.md`, `PROJECT_CONFIG.json`, or `ADAPTERS.json`. Any incompatible change to a schema, fixed path, or enum is a governance-package major change and must provide a migrator and rollback tests.
