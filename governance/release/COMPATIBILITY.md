# Release compatibility contract

This document defines the compatibility obligations for a released governance
artifact. The release index is the machine-readable authority for an artifact's
version, immutable source revision, reviewed upstream revision, ZIP hashes, and
per-file hashes. A release is usable only after both the index and both ZIPs
pass `scripts/validate_governance_release.py`.

## Supported release lines

| Release line | Project config | Workflow behavior | Upgrade eligibility |
| --- | --- | --- | --- |
| `1.2.x` and earlier | v1 | Existing upstream Spec Kit lifecycle; no governed companion contract | May upgrade only to the `1.3.0` bridge first |
| `1.3.0` bridge | v1, with v2 migration planning support | Preserves existing behavior; never enables strict workflow gates | Required staging line before `2.0.0` |
| `2.0.0` | v2 | Governed SDD, explicit artifact reviews, tiny-model task readiness, and cold-start review | Only from a verified `1.3.0` bridge plan |

No manager may silently treat a v1 project as v2. A direct v1-to-v2 write, a
partially applied major migration, or an unverified bridge is
`MIGRATION_REQUIRED`; it is not a compatibility fallback.

## Bridge release: 1.3.0

`1.3.0` is a compatibility bridge, not the strict-governance release. It must
continue to read and write v1 manifests and `PROJECT_CONFIG.json` files exactly
as the v1 manager did. It may read v2 contracts solely to generate a
hash-bound, atomic v2 migration plan. It must not install the governed
workflow, write v2 configuration, add review records, or change a feature's
runtime behavior.

The bridge plan must inventory every candidate mutation, create a backup and
rollback journal, and declare `docs/spec-kit/features/**` as a preserved
project-local subtree. It must prove that business files, `.specify/**`,
`specs/**`, native Agent-generated files, existing local evidence, and user
rules outside managed blocks are byte-identical after bridge installation and
after a bridge rollback.

## Strict release: 2.0.0

`2.0.0` requires project-config schema v2 and a completed bridge-generated
migration record. It adds a companion source bundle and a Reference-owned
review-evidence sidecar. The companion uses upstream `specify` workflow,
preset, and extension primitives; it does not replace the upstream lifecycle
or grant the manager ownership of `.specify/**`, `specs/**`, or native Agent
files.

Before any companion install or v2 apply operation, the manager must discover
the installed CLI version and capabilities. Missing workflow, preset,
extension, or validator support returns `COMPANION_CAPABILITY_UNAVAILABLE`.
The manager must not substitute a weaker workflow or mark the project ready.

## Upgrade and rollback

Every upgrade starts with a read-only compatibility check and a reviewed
operation plan. The plan binds old hashes, source hashes, allowed manager
paths, external CLI argv, backups, and recovery actions. User approval binds
the exact plan ID and plan hash. A changed input invalidates that approval.

Rollback follows the journal created by the approved plan. Governance rollback
may restore the v1 portable policy, config, and manager only through the bridge
contract. It must retain v2 feature-sidecar evidence as read-only history and
must never delete user work, upstream Spec Kit artifacts, or native Agent
files. Incomplete journals or unsafe restoration return `RECOVERY_REQUIRED`.

## Runtime scope

The package remains compatible only with a target that has an installed
`specify` CLI, an existing Spec Kit project state when the operation requires
one, and the committed local governance additions. A personal global Policy and
the maintainer's central Reference directory are not target-project runtime
prerequisites. Central update detection remains source-gated and read-only.

The portable artifact carries generated
`governance/release/SOURCE_METADATA.json`. The metadata records the source
revision, release version, and reviewed upstream revision used to build the
artifact; it is evidence, not permission to bypass an upgrade plan.
