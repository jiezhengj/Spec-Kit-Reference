# Security Boundaries

The governance manager accepts only project-relative paths and rejects absolute paths, `..`, symlink escapes, directories, special files, and shell strings. External CLI argv must be an array and must not pass through shell eval. Logs, plans, manifests, and diagnostics must not store tokens, secrets, complete environment variables, user home directories, private queries, or unrelated absolute paths.

# Write Safety

Manager mutations use temporary files in the target directory, flush/fsync, atomic replace, the old hash, and per-file backups. External CLI mutations use allowed path prefixes, a complete pre-execution snapshot, a post-execution changed-file inventory, and a journal; restore on scope escape or postcondition failure, and enter `RECOVERY_REQUIRED` when safe restoration is impossible.

# Native no-downgrade

Any unwritable native target, managed file repair, or context anchor, or any permission, sandbox, or installation failure affecting one, is a blocker. The system must not automatically switch to generic, another key, `--force`, or generate only `.specify/commands/` to falsely claim completion.
