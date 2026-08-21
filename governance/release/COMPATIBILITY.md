# Release compatibility

V1 supports the Python standard library manager, project governance package,
and the installed Spec Kit CLI only when the release manifest records a tested
CLI version and immutable install reference. The current repository is a
source checkout; a `latest.json` release index is created only by the release
builder after artifact hashes and deterministic output have been validated.
