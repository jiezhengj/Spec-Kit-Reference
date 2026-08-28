# Required Test Matrix

Tests must cover schema validation, canonical plan hashes, path safety, markers, atomic writes, external scope, missing/obsolete/untested CLI versions, identity conflicts, exact keys, native installed/not installed/unwritable states, partial installation, default denial of generic, generic attestation, multi-install conflict, default change rollback, Loader/Materialized delivery, upgrades, rollbacks, and capability inventory equivalence.

The ownership boundary must have a regression test: manager-owned mutations to `.specify/**`, `specs/**`, or native Agent-generated files are rejected, while supported upstream CLI operations remain representable as external mutations. Conversation-approval tests must prove that “方案可以” advances artifact alignment but never authorizes direct code edits before the upstream specification, plan, and tasks are aligned. Runtime-independence tests must prove that the local package does not require a global Policy or central Reference directory.

The optional update-reminder path must prove that `plan-install-update-reminder` works with only an installed CLI, an existing `.specify/` project, and an explicit existing context anchor; it must append only its own managed block, preserve upstream Spec Kit files and existing anchor content, delegate detection to `specify self check`, and never authorize an automatic `specify self upgrade`.

# Central Reference update matrix

The central Reference update path must prove that a clean source with the same target manifest revision returns `UP_TO_DATE`, a newer ancestor source returns `UPDATE_AVAILABLE` with changed paths, a dirty or missing source returns `CENTRAL_SOURCE_UNVERIFIED`, and a missing target manifest returns `TARGET_NOT_BOOTSTRAPPED`. The session contract must prove that no loaded global Policy or no central source means silent skip without directory scanning.

The approved upgrade path must prove that `plan-upgrade --source <source>` updates only `docs/spec-kit/**`, `tools/spec-kit-governance/governance.py`, and the separately managed governance-loader and Reference-update-check blocks in the context anchor; it must produce no external CLI mutation and leave `.specify/**`, `specs/**`, native Agent files, and business files byte-identical. A post-sync handoff test must prove that Spec Kit artifact alignment remains an upstream workflow decision rather than a manager mutation.

# Native Blocker Acceptance

Configure unwritable, permission-denied, and sandbox fixtures separately for the native init target, integration target, managed-file repair, context anchor, and anchor parent directory. Every fixture must return `NATIVE_INSTALL_BLOCKED`, produce no generic integration, other key, active binding, or `READY` state, and prove that existing artifacts and user work were not deleted.

# Upstream Regression

Preserve the checker's baseline SHA validation, official remote validation, non-ancestor blocking, `--no-fetch`, exit codes `0/1/2`, POSIX wrapper, PowerShell wrapper, and CI notify-only, no-write behavior.
