# Validator adapter contract

The native companion does not implement a second lifecycle engine. Its validator boundary is the project-local Reference manager's read-only commands:

- `audit-feature-readiness --feature-dir docs/spec-kit/features/<feature-id>`;
- `check-artifact-approval --feature-dir docs/spec-kit/features/<feature-id> --artifact-type <type>`;
- `verify-task-package --feature-dir docs/spec-kit/features/<feature-id>`;
- `check-companion-status`.

The commands must be implemented by the governance manager before any project enables `governed-sdd-required`. Until then, the companion commands must report `COMPANION_CAPABILITY_UNAVAILABLE` and stop before `speckit.implement`.

Validators may read upstream-owned files and write only their Reference-owned report paths. They must never write `.specify/**`, `specs/**`, or native Agent-generated files, and a successful audit must never be converted into a user approval event.
