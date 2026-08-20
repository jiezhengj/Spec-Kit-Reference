# Update policy

`UPSTREAM_BASELINE` records the latest official Spec Kit commit whose semantic impact has been reviewed. It is not required to equal the latest upstream commit.

## Review procedure

1. Read `AGENTS.md` and the baseline.
2. Fetch `upstream/main`.
3. Compare the baseline with `upstream/main`.
4. Inspect commit messages, changed paths, diffs, and complete relevant files.
5. Consider path priority, release notes, commit intent, and diff semantics together.
6. Classify the result as `NONE`, `REFERENCE`, or `POLICY`.
7. Update local documents only when evidence requires it.
8. Record the assessment and history.
9. Validate the repository.
10. Advance the baseline last.

If the baseline is not an ancestor of `upstream/main`, treat the result as a manual review error or upstream history rewrite. Do not use a two-dot range as if it were a normal update; inspect the relevant commits and reset the reviewed baseline deliberately.

## High-priority paths

Pay particular attention to:

- `docs/reference/agentic-sdd*`
- `docs/reference/agentic-bugfix*`
- `docs/reference/integrations*`
- `integrations/**`
- `src/**/integrations/**`
- `templates/commands/**`
- `templates/**`
- `workflows/**`
- `core_pack/**`
- `docs/upgrade*`
- `pyproject.toml`
- `src/specify_cli/**`

These paths are a review aid, not an automatic allowlist or ignore list. A README, changelog, or release note can still contain a breaking change.

## Classifications

### NONE

No local operational knowledge or governance policy changes. Record the review and advance the baseline after validation.

### REFERENCE

Operational facts changed, such as CLI syntax, integrations, generated directories, upgrade commands, or extension behavior. Update `SPEC_KIT_REFERENCE.md` when justified; normally leave `global-policy.md` unchanged.

### POLICY

The methodology, lifecycle, completion semantics, integration architecture, or project-authority model changed in a way that may alter Agent behavior. Review and possibly update both `global-policy.md` and `SPEC_KIT_REFERENCE.md`. Human review is required before deployment or merge.

## Automation boundary

The checker and GitHub Action may detect and notify. They must not automatically edit or merge local policy. Semantic assessment is a review step, and baseline advancement happens only after that review is complete.
