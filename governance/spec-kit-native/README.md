# Component source and supported installation

This directory is the versioned source for the Spec Kit-native part of the governance package. It is not a target project's `.specify/` directory and must never be copied there by hand.

The companion has three independently installable components:

- `extensions/discovery` provides Discovery, readiness, cold-start-review, and validation commands.
- `presets/tiny-model-tasks` wraps the upstream `speckit.tasks` command with the tiny-model task contract.
- `workflows/governed-sdd` provides the gated lifecycle orchestration.

For Spec Kit 1.0.4, the Reference manager must install the components individually through their native CLI primitives, in this order:

```text
specify extension add governance/spec-kit-native/extensions/discovery --dev
specify preset add --dev governance/spec-kit-native/presets/tiny-model-tasks --priority 5
specify workflow add governance/spec-kit-native/workflows/governed-sdd --dev
```

Those commands are examples for a reviewed manager-generated operation plan. They are not authorization to mutate a target project directly.

# Bundle compatibility boundary

`bundle.yml` follows the current Spec Kit 1.0 bundle-manifest schema and can be structurally validated and reproducibly built. The 1.0.4 bundle installer does not consume a component reference's relative `source` field: it resolves extensions, presets, and workflows only from the CLI core pack, an installed component, or a configured catalog. Consequently, a built archive is a distributable provenance artifact, not a self-installing bundle on 1.0.4.

The manager must fail closed with `COMPANION_CAPABILITY_UNAVAILABLE` if a future CLI changes this contract incompatibly. It must not claim that `specify bundle install` installed these relative sources until an upstream release supports that operation and the compatibility baseline is updated.

# Ownership and runtime boundary

The extension commands create and read only `docs/spec-kit/features/<feature-id>/` governance evidence plus existing upstream artifacts read-only. The preset asks the upstream tasks command to author `tasks.md`; it does not patch the upstream-generated skill. The workflow dispatches installed commands and pauses at human gates; it does not create an approval ledger event. Approval evidence remains a manager-mediated, hash-bound user action.

# Slot boundary

Spec Kit 1.0.4 has workflow overlays but no declared `slot` step type. The workflow therefore exposes stable, named anchor gates (`slot-security`, `slot-design`, `slot-localization`, and `slot-release`) that a project overlay can replace or surround using the upstream overlay mechanism. The contract for those anchors is in [slots/README.md](slots/README.md). An unfilled anchor is intentionally a human gate, not an automatic skip: governance must never silently bypass a required project review.

# Validation

Run these read-only checks from this repository:

```text
specify bundle validate --path governance/spec-kit-native --offline
specify bundle build --path governance/spec-kit-native --output /private/tmp/spec-kit-native-build
specify workflow run governance/spec-kit-native/workflows/governed-sdd/workflow.yml --help
```

The first command validates the manifest shape. Offline reference resolution may report warnings because the companion is intentionally not pre-bundled into the CLI. The workflow file is also validated through the CLI's workflow install/run path in an isolated initialized project during release tests.
