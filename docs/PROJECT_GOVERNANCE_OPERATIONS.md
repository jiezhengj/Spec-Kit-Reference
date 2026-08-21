# Operational entry point

The fixed public entry point for the project governance package is `tools/spec-kit-governance/governance.py`. The read-only commands are `doctor`, `resolve-agent`, `verify`, and `check-update`; every mutation must first generate an operation plan and then be executed with `apply-plan --approve-plan-id <id> --approve-plan-sha256 <hash>`.

# Standard sequence

First confirm the project root, read `docs/spec-kit/START_HERE.md`, and inspect `.specify/` and `specify integration status --json`. For a new project, run `plan-governance-bootstrap` first, then run `plan-init`/`plan-onboard` with explicit `--runtime-id`, `--integration-key`, and `--context-anchor` values; onboarding the current Agent must first pass the native resolver. Install an Extension separately with `plan-extension-install`; it must not be an implicit side effect of bootstrap. A successfully installed CLI integration remains provisional; fresh-session evidence must be provided when running `plan-activate-binding`, or `READY` must not be reported.

If an exact integration key, a context anchor, a writable native target, or compatibility with the current CLI version is unavailable, the manager must stop; it must neither guess the product nor switch to generic.

# Failure handling

An unwritable Native target, or a permission, sandbox, repair, or installation failure, uniformly returns `NATIVE_INSTALL_BLOCKED`; an unknown identity returns `IDENTITY_UNKNOWN` or `KEY_REQUIRED`; plan-input drift, scope escape, or incomplete recovery returns `RECOVERY_REQUIRED`. On failure, retain the plan, backup, journal, and changed-file inventory; V1 performs no automatic cleanup.
