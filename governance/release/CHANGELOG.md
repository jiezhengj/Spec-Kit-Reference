# Planned 2.0.0 release

## 2.0.0

- Introduces project-config schema v2 and the `workflow_governance` contract.
- Requires explicit Discovery, artifact-specific human review evidence, and
  hash-bound approval before each governed lifecycle transition.
- Adds self-contained tiny-model task packages, task-readiness validation, and
  cold-start review evidence.
- Adds the `governed-sdd` companion workflow, without replacing upstream
  bundled workflows or changing ownership of `.specify/**`, `specs/**`, or
  native Agent-generated files.
- Requires a verified `1.3.0` bridge migration record for v1 projects; direct
  v1-to-v2 overwrite is rejected as `MIGRATION_REQUIRED`.
- Preserves `docs/spec-kit/features/**` as project-local user evidence during
  central synchronization, migration, and rollback.

## 1.3.0 bridge

- Preserves the v1 portable governance behavior while adding read support for
  v2 migration contracts and a hash-bound v1-to-v2 migration planner.
- Adds complete backup inventory and rollback-journal requirements for the
  future major migration.
- Does not enable strict workflow gates, install the governed companion, or
  alter existing feature behavior.

# Released history

## 1.2.0

- Added source-gated, session-scoped central Reference update detection.
- Reference synchronization now updates the governance and Agent-context layer
  through the existing plan/apply workflow and never edits `.specify/**`,
  `specs/**`, or native Agent-generated files.
- Kept specification, plan, and task alignment as a separate upstream Spec Kit
  handoff after governance synchronization.

## 1.1.1

- Added an optional `plan-install-update-reminder` operation for existing
  Spec Kit projects that want a CLI update reminder without installing the
  full project governance package.
- Kept the reminder Reference-owned and limited to a separate managed context
  anchor block; update detection delegates to upstream `specify self check`.
- Preserved explicit approval for `specify self upgrade` and the ownership
  boundary for `.specify/**`, `specs/**`, and native Agent integration files.

## 1.1.0

- Strengthened the substantive-work entry rule so conversational approval enters
  the upstream Spec Kit artifact workflow instead of authorizing direct code
  edits.
- Made `analyze` a required completion gate and clarified that `validate` and
  `converge` are feature evidence, while governance `verify` remains package
  verification only.
- Added manager enforcement for the Reference ownership boundary and documented
  that global Policy and the central Reference are not target runtime prerequisites.

## 1.0.0

- Added the Agent-neutral project governance package, native no-downgrade
  onboarding gate, deterministic portable and extension artifacts, and the
  fixed global Policy deployment protocol.
