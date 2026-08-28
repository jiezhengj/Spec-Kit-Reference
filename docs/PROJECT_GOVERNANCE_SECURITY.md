# Security Boundaries

The governance manager accepts only project-relative paths and rejects absolute paths, `..`, symlink escapes, directories, special files, and shell strings. External CLI argv must be an array and must not pass through shell eval. Logs, plans, manifests, and diagnostics must not store tokens, secrets, complete environment variables, user home directories, private queries, or unrelated absolute paths.

# Write Safety

Manager mutations use temporary files in the target directory, flush/fsync, atomic replace, the old hash, and per-file backups. External CLI mutations use allowed path prefixes, a complete pre-execution snapshot, a post-execution changed-file inventory, and a journal; restore on scope escape or postcondition failure, and enter `RECOVERY_REQUIRED` when safe restoration is impossible.

# Native no-downgrade

Any unwritable native target, managed file repair, or context anchor, or any permission, sandbox, or installation failure affecting one, is a blocker. The system must not automatically switch to generic, another key, `--force`, or generate only `.specify/commands/` to falsely claim completion.

# Ownership boundary

The manager rejects direct mutations to `.specify/**`, `specs/**`, and native Agent-generated integration files with `REFERENCE_OWNERSHIP_VIOLATION`. Those artifacts remain under project or upstream CLI ownership. Supported `specify` CLI calls may still be represented as scoped external operations; their output is inventoried and never silently treated as manager-owned content.

The optional update reminder is a separate managed block in the explicit context anchor. Its only runtime command is the upstream read-only `specify self check`; it must not invoke `specify self upgrade` without explicit user approval, and an offline check is non-blocking.

# Central Reference update security

Central Reference detection accepts only the explicitly loaded global Policy locator and a clean Git checkout; it never scans arbitrary directories, imports remote prose as instructions, or treats a dirty or unverifiable source as an available update. The check is read-only and session-gated. Synchronization requires an exact reviewed plan and explicit approval, and its protected-path check rejects `.specify/**`, `specs/**`, native Agent-generated files, and business files.

The synchronization plan updates only the governance and Agent-context layer. It does not infer that a changed Reference makes any specification, plan, or task stale. Those artifacts remain under the upstream Spec Kit workflow and must be reviewed there as a separate handoff.
