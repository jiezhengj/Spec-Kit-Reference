# Frozen v1 project snapshot

`project/` is the byte-preserved project template from the last committed v1 governance baseline immediately before the 2.0.0 policy implementation. The 1.3.0 release builder maps these files to `governance/project/` inside the bridge archive.

The snapshot exists so an installed v1 manager can apply a normal reviewed `plan-upgrade` without receiving v2 policy or configuration early. Do not edit it to track the current strict template. Changes require a bridge-compatibility review and regression coverage proving schema v1 and the absence of `workflow_governance`.
