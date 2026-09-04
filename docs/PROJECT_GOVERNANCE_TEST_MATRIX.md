# Required Test Matrix

Tests must cover schema validation, canonical plan hashes, path safety, markers, atomic writes, external scope, missing/obsolete/untested CLI versions, identity conflicts, exact keys, native installed/not installed/unwritable states, partial installation, default denial of generic, generic attestation, multi-install conflict, default change rollback, Loader/Materialized delivery, upgrades, rollbacks, and capability inventory equivalence.

The ownership boundary must have a regression test: manager-owned mutations to `.specify/**`, `specs/**`, or native Agent-generated files are rejected, while supported upstream CLI operations remain representable as external mutations. Conversation-approval tests must prove that “方案可以” advances artifact alignment but never authorizes direct code edits before the upstream specification, plan, and tasks are aligned. Runtime-independence tests must prove that the local package does not require a global Policy or central Reference directory.

The optional update-reminder path must prove that `plan-install-update-reminder` works with only an installed CLI, an existing `.specify/` project, and an explicit existing context anchor; it must append only its own managed block, preserve upstream Spec Kit files and existing anchor content, delegate detection to `specify self check`, and never authorize an automatic `specify self upgrade`.

# Governed workflow and review evidence

The strict v2 workflow must prove that a substantive request begins with
Discovery, that product and safety decisions cannot be silently defaulted, and
that a non-interactive run pauses at every required human review. Missing,
stale, superseded, self-signed, malformed, absolute-path, traversal-path, or
symlink-escaping review evidence must block the next phase. An approved review
must bind the artifact type and every declared artifact hash; changing an
artifact must invalidate approval.

Task readiness tests must reject each missing required task-package field,
duplicate IDs, unknown traceability, dependency cycles, directory-only target
paths, unverifiable validation commands, and empty expected results. They must
warn on multiple independently observable results and require
contract-first decomposition for producer/consumer work across modules. The
validator must be read-only: all feature-artifact hashes before and after a
run must match.

Cold-start review tests must use only an isolated selected task package and
repository checkout, with no prior conversation. A substantive reviewer
question, missing prerequisite, or unavailable referenced artifact must fail
the readiness gate. Unfilled project workflow slots must safely skip; filled
slots must preserve declared outputs for their successor.

# Bridge and strict-release migration

The `1.3.0` bridge must preserve v1 behavior and may only generate a v2 plan;
it must not enable strict gates, write v2 config, install the companion, or
change feature behavior. Its plan must contain a complete backup inventory,
rollback journal, source and input hashes, and a preserved
`docs/spec-kit/features/**` subtree declaration.

The `2.0.0` path must reject direct v1 manager overwrite and require a verified
bridge migration record. Upgrade and rollback fixtures must prove that business
files, `.specify/**`, `specs/**`, native Agent-generated files, user-owned
anchor bytes outside managed blocks, and feature-sidecar evidence remain
byte-identical. Missing current CLI capabilities must return
`COMPANION_CAPABILITY_UNAVAILABLE`; an incomplete restoration must return
`RECOVERY_REQUIRED`.

# Release artifact contract

Build each release twice from identical inputs and require byte-identical ZIPs
and index payloads. The portable ZIP must include all project governance
documents, manager, schemas including the v2 review/task/migration schemas,
release metadata, and the companion source. The extension ZIP must include the
same manager bytes, companion source, and extension metadata. Validator tests
must reject an altered archive, content-hash map, generated source metadata,
required companion file, shared manager, bridge/strict compatibility metadata,
or noncanonical ZIP entry.

# Central Reference update matrix

The central Reference update path must prove that a clean source with the same target manifest revision returns `UP_TO_DATE`, a newer ancestor source returns `UPDATE_AVAILABLE` with changed paths, a dirty or missing source returns `CENTRAL_SOURCE_UNVERIFIED`, and a missing target manifest returns `TARGET_NOT_BOOTSTRAPPED`. The session contract must prove that no loaded global Policy or no central source means silent skip without directory scanning.

The approved upgrade path must prove that `plan-upgrade --source <source>` updates only `docs/spec-kit/**`, `tools/spec-kit-governance/governance.py`, and the separately managed governance-loader and Reference-update-check blocks in the context anchor; it must produce no external CLI mutation and leave `.specify/**`, `specs/**`, native Agent files, and business files byte-identical. A post-sync handoff test must prove that Spec Kit artifact alignment remains an upstream workflow decision rather than a manager mutation.

# Native Blocker Acceptance

Configure unwritable, permission-denied, and sandbox fixtures separately for the native init target, integration target, managed-file repair, context anchor, and anchor parent directory. Every fixture must return `NATIVE_INSTALL_BLOCKED`, produce no generic integration, other key, active binding, or `READY` state, and prove that existing artifacts and user work were not deleted.

# Upstream Regression

Preserve the checker's baseline SHA validation, official remote validation, non-ancestor blocking, `--no-fetch`, exit codes `0/1/2`, POSIX wrapper, PowerShell wrapper, and CI notify-only, no-write behavior.
