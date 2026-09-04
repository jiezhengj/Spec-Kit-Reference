# Stable overlay anchors

The following workflow step IDs are the only companion-defined extension anchors:

- `slot-security` follows `plan` and precedes plan-bundle review.
- `slot-design` follows `slot-security` and precedes plan-bundle review.
- `slot-localization` follows `slot-design` and precedes plan-bundle review.
- `slot-release` follows `converge` and precedes completion review.

Spec Kit 1.0.4 does not offer a native workflow `slot` type. Each anchor is therefore an explicit human gate. A project can use `specify workflow overlay add` to insert, replace, or surround a stable anchor using the upstream overlay grammar. The overlay must be project-owned and approved through the normal governance operation plan; it must not remove a mandatory gate or introduce a silent bypass.

# Overlay requirements

An overlay attached to `governed-sdd` must:

- use a unique, safe overlay ID;
- modify only its declared anchor or a new step inserted adjacent to that anchor;
- preserve a final gate that requires an explicit approve/reject decision;
- record the governing project configuration and evidence path in its gate message;
- avoid commands that mutate `.specify/**`, `specs/**`, or native Agent files outside supported upstream commands.

An unconfigured slot still requires a human decision that it is not applicable. It cannot automatically skip, because an automatic skip would weaken the governed workflow without reviewable evidence.
