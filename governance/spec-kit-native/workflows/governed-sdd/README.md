# Governed workflow

`governed-sdd` is a new workflow ID. It does not replace the upstream bundled `speckit` workflow.

It intentionally pauses at every human gate in non-interactive execution. To resume a paused run, the user must first review the named artifact, use the governance manager to append the matching hash-bound ledger event, and then supply the relevant `review_*` input as `approve`. Supplying an input only resolves the workflow gate; it is not approval evidence by itself.

The workflow dispatches `speckit.governance-discovery.*` commands supplied by the companion extension and `speckit.tasks` supplied by the tiny-model preset. The extension and preset must therefore be installed and registered for the active native integration before this workflow is run.

# Revision behavior

The installed Spec Kit CLI may pause or abort at gates, but the Reference manager does not assume a particular release's routing grammar. A rejection therefore remains an explicit workflow outcome. The operator corrects the artifact using the relevant upstream command, and the manager rejects stale hashes when high-assurance review evidence is in use.
