# Release compatibility

V1 supports the Python standard library manager, project governance package,
and the installed Spec Kit CLI only when the release manifest records a tested
CLI version and immutable install reference. The current repository is a
source checkout; a `latest.json` release index is created only by the release
builder after artifact hashes and deterministic output have been validated.

The package is compatible with target projects that have the installed
`specify` CLI, an existing Spec Kit `.specify/` project state, and the committed
local governance additions. A personal global Policy and the maintainer's
central Reference directory are not runtime dependencies. The package must not
rewrite `.specify/**`, `specs/**`, or native Agent-generated integration files;
supported upstream CLI commands remain the executor for those artifacts.

The optional `plan-install-update-reminder` operation is narrower than the
full package: it requires only an existing `.specify/` project, the installed
CLI, and an explicit existing context anchor. It appends only its separate
managed reminder block and does not install `docs/spec-kit/**` or copy the
manager into the target project.
