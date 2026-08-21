# Scope

This document is the sole manual deployment protocol for `GLOBAL_POLICY.md`. It does not discover, create, or select the global rules file of any Agent product; the deployer must first provide the absolute path of the target file and the absolute path of the local governance repository root.

# Manual Inputs

Each deployment accepts only:

1. The absolute path of the global rules file actually loaded by the current Agent product.
2. The absolute path of the local `SpecKitReference` repository root.

If the target does not exist, a human must first confirm that the product permits creating a file at that exact path. After confirmation, treat it as a target to be created; no write may occur until all pre-deployment validation passes.

# Pre-deployment Validation

Any failure must stop the operation with zero writes:

1. source is an absolute, readable directory as determined by the current platform's path API; the input is a single-line literal path containing no CR, LF, NUL, `~`, environment-variable syntax, marker text, or placeholder, and no shell expansion is performed.
2. `SPEC_KIT_REFERENCE.md`, `GLOBAL_POLICY.md`, and `UPSTREAM_BASELINE` exist and are readable within source.
3. The sole template is `<source>/GLOBAL_POLICY.md`; the template must not be obtained from another checkout, the current working directory, or session text.
5. `GLOBAL_POLICY.md` has exactly one H1 title, `# Spec Kit Global Policy`, and its policy sections are H2 headings; the source is wrapped in the `<!-- SPEC-KIT-GLOBAL-POLICY:START version=X.Y.Z -->` and `<!-- SPEC-KIT-GLOBAL-POLICY:END -->` markers.
6. `<ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>` occurs exactly once and only on the sole `SPEC_KIT_GOVERNANCE_SOURCE:` line.
7. The template uses the fixed START line `<!-- SPEC-KIT-GLOBAL-POLICY:START version=X.Y.Z -->` and END line `<!-- SPEC-KIT-GLOBAL-POLICY:END -->`, where `X.Y.Z` is a non-negative SemVer; each generated line occurs exactly once and START precedes END.
8. Any target line containing `SPEC-KIT-GLOBAL-POLICY:` that does not match the generated marker grammar causes validation to fail.
9. A nonexistent target, an empty target, a target without markers, and a target with one valid and unique marker pair enter the create, initial append, or update branch, respectively; a missing, duplicate, reversed, or malformed marker stops the operation.

The managed marker block is generated as a whole. Updates do not perform a three-way merge or determine whether the block contains manual edits; the new rendered block replaces the old block unconditionally. Custom rules that must be preserved must be placed outside the markers.

# Sole Rendering Procedure

Read the complete source template and perform exactly one literal replacement:

```text
<ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>
```

Replace it with the validated absolute source path. After replacement, validation must confirm: zero placeholders remain, the marker grammar is valid, the source value is exactly identical to the input, and the rendered block is UTF-8/LF and ends with exactly one LF.

# Initial Deployment and Updates

For a target to be created or an empty file, the candidate is the complete rendered block.

For a nonempty target without markers, preserve all original bytes: if the final byte of the original file is LF, append one LF; otherwise append two LFs; then append the rendered block. Newly inserted bytes always use LF, and the original content is not normalized.

For an update, the candidate is fixed as:

```text
prefix bytes + rendered block + suffix bytes
```

The replacement span begins at the `<` of the START marker and ends at the `>` of the END marker, and includes one immediately adjacent newline sequence after END (two bytes for CRLF, one byte for LF, or none if absent). Preserve prefix and suffix byte for byte.

# Backup, Publication, and Recovery

1. Read UTC in the format `YYYYMMDDTHHMMSSZ`. The backup path is fixed as `<target>.spec-kit-global-policy.backup.<UTC>`; stop if it already exists, and do not overwrite it.
2. For an existing target, copy all bytes and permissions to the backup and reread its hash. For a target to be created, record `target_previously_absent = true` and do not create an empty backup.
3. In the target directory, use exclusive-create to create `<target>.spec-kit-global-policy.deploy-journal.<UTC>.json`, recording the pre-state, candidate hash, backup, and the `prepared` phase.
4. Safely create a temporary file in the same directory, write the candidate, flush/fsync it, and reread it for validation.
5. For an existing target, use an atomic replace on the same file system.
6. For a target to be created, call `os.link(candidate, target, follow_symlinks=False)` with the fsynced candidate; this no-clobber atomic publish corresponds to `link(2)` on POSIX and `CreateHardLinkW` on Windows. If the platform or file system does not support it, return `GLOBAL_DEPLOY_ATOMIC_CREATE_UNSUPPORTED`, keep the target absent, and do not write directly to the final target.
7. After publication, set the journal to `published` and fsync it, then reread the final target to validate the marker, placeholder, source, and hash.
8. If validation fails for an existing target, restore atomically from the backup and reread the hash. If validation fails for a target that was to be created, deletion is permitted only when the target hash equals the journal candidate hash; if the hashes differ, stop and recover manually.
9. Crash recovery first reads the journal: if the phase is `prepared` and the target is absent, delete the candidate; if the target hash equals the candidate hash, treat publication as complete and continue validation; if the hashes differ, stop. Apply the same determination in the `published` phase. Do not begin a new deployment until the journal has converged.
10. After successful validation, delete the candidate, set the journal to `verified`, and fsync it; retain the journal and backup until validation through an actual Agent load is complete.

Finally, the deployer creates a new session in the target Agent product and confirms that the global rules location was loaded. If either text validation or actual-session validation fails, deployment success must not be reported.

# Subsequent Updates

After the central `GLOBAL_POLICY.md` passes POLICY review and a new version is released, repeat the same update process. Do not manually synchronize individual sections within the old block. After the source directory moves, a human must provide the new absolute path again; do not scan the disk for an alternative directory.
