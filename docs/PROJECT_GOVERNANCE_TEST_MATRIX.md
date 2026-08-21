# Required Test Matrix

Tests must cover schema validation, canonical plan hashes, path safety, markers, atomic writes, external scope, missing/obsolete/untested CLI versions, identity conflicts, exact keys, native installed/not installed/unwritable states, partial installation, default denial of generic, generic attestation, multi-install conflict, default change rollback, Loader/Materialized delivery, upgrades, rollbacks, and capability inventory equivalence.

# Native Blocker Acceptance

Configure unwritable, permission-denied, and sandbox fixtures separately for the native init target, integration target, managed-file repair, context anchor, and anchor parent directory. Every fixture must return `NATIVE_INSTALL_BLOCKED`, produce no generic integration, other key, active binding, or `READY` state, and prove that existing artifacts and user work were not deleted.

# Upstream Regression

Preserve the checker's baseline SHA validation, official remote validation, non-ancestor blocking, `--no-fetch`, exit codes `0/1/2`, POSIX wrapper, PowerShell wrapper, and CI notify-only, no-write behavior.
