# Resolver contract

The resolver uses only the Python standard library and the current project's runtime. The only permitted integration CLI machine-readable output is `specify integration status --json`; it must not parse Rich list/search/info output, import private APIs, scan the filesystem, or create temporary projects to query the registry.

Identity-claim precedence is: the current user's key, host runtime metadata, an explicit environment variable, and the Agent's self-declaration. Any conflict returns `IDENTITY_CONFLICT`; a display name without a key returns `KEY_REQUIRED`. Installation health does not prove a runtime match; only fresh-session binding verification yields `EXACT_NATIVE_INSTALLED`.
