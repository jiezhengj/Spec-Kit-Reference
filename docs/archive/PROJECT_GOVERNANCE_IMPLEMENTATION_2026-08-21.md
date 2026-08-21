# Archive status

This dated file is the implementation snapshot used for the 2026-08-21
governance rollout. It is retained for audit and reproducibility, not as a
live project runtime dependency. Future implementation work must use the
current `governance/` source, schemas, manager, and ongoing maintenance
documents; a later rollout may supersede or remove this snapshot after its
review record is preserved.

# Document Purpose

This document guides the implementing Agent in modifying the `SpecKitReference` repository to establish a Spec Kit project governance system that does not presuppose a list of Agent products, can be committed with each project, works offline, and can connect future Agents on demand.

This document is an implementation specification, not a background discussion. Even without the previous session, personal global rules, or knowledge of this repository's design history, the implementing Agent must be able to complete the implementation using only this document, the current repository state, and the currently installed `specify` CLI.

The normative terms in this document define implementation behavior using only “must” and “must not”:

- “Must” means a completion condition that cannot be omitted.
- “Must not” means a prohibited action.
- The implementing Agent must not choose an architecture based on wording such as “recommended,” “normally,” “optional,” or “as appropriate.”
- Every behavior that project maintainers are allowed to choose must correspond to a field with a fixed enumeration value in `docs/spec-kit/PROJECT_CONFIG.json`.
- Any deviation not explicitly permitted by the `PROJECT_CONFIG.json` schema is considered unimplemented, not a reasonable variant.

# Implementation Goals

The final implementation must satisfy all of the following simultaneously:

1. Shorten `GLOBAL_POLICY.md` into a stable global Bootstrap.
2. Commit the complete Spec Kit Policy and operational Reference to business projects as a project governance package.
3. Do not hard-code Codex, Claude, Gemini, Trae, or any other fixed Agent set into the project governance architecture.
4. When an Agent actually enters a project for the first time, that Agent or its host declares its identity, and the governance manager resolves the correct native integration based on the current `specify` runtime.
5. Install known but uninstalled integrations on demand rather than pre-installing every possible integration.
6. Provide deterministic handling for supported, unsupported, unidentified, CLI-missing, catalog-unavailable, integration-conflict, and other cases.
7. Project collaborators must still be able to read the complete project governance knowledge without personal global rules or a central Reference directory.
8. The maintainer's global Reference may discover candidate updates to the project governance package, but must not silently change project behavior.
9. All installation, upgrade, and managed-file writes must be plannable, reviewable, verifiable, and reversible.
10. The project governance package must not forge or manually copy the Skills, Commands, events, or other managed artifacts of native Spec Kit integrations.

# Fixed Implementation Decisions

The following decisions are fixed; the implementing Agent must not replace them with other “equivalent solutions”:

1. The root `GLOBAL_POLICY.md` is the sole global deployment template; the two-step design of “Policy source plus a separately appended locator at deployment time” no longer exists.
2. `GLOBAL_POLICY.md` must contain fixed START/END markers and exactly one local-machine path placeholder.
3. Global-rule deployment must be performed by a person selecting the target Agent product's real global rules file, manually filling in the placeholder, and copying the managed block as a whole; project code and governance tools must not automatically guess or write to the global rules file.
4. The directories, file names, schemas, and manager command names of the central repository and business projects are fixed by this document and must not be renamed independently. A future path migration must bump the governance package major version and provide a migrator.
5. The project must commit a root `AGENTS.md` as a generic Loader; no fixed multi-brand rules-file set may be pre-generated.
6. The project must commit `PROJECT_CONFIG.json`. Machine behavior is determined by this file; `LOCAL_OVERRIDES.md` stores only human-readable supplementary rules.
7. V1 does not automatically parse `context-anchor-hints.json`, nor infer a context anchor from official documentation, directory names, or product names. An anchor may come only from an existing active binding or a project-relative path explicitly provided by the user for the current onboarding plan.
8. V1 does not automatically determine the integration key from the product display name. Only a key explicitly provided by the user or host, or a key from an existing active binding in `ADAPTERS.json`, may enter the mutation plan.
9. The core manager must use the Python 3 standard library and the file is fixed at `tools/spec-kit-governance/governance.py`.
10. V1 deliverables are fixed as a deterministic portable release ZIP and a Spec Kit extension archive; V1 is not complete based on a CLI bundle and does not implement a bundle branch.
11. All mutations must use the fixed two-phase plan/apply protocol and require the current user to authorize the exact `plan_id`.
12. The Manager must not implement a generic `--force` parameter. The sole permitted external `--force` is the initial `specify init --here --force` on a non-empty brownfield project; it must appear in a dedicated initialization plan, after per-file backups and target-inventory review and authorization of the exact `plan_id` by the current user. All other init, install, use, switch, upgrade, render, and rollback operations must not contain `--force`.
13. The project default integration is fixed to the pinned strategy; ordinary Agent onboarding must not change it.
14. Context delivery is fixed to Loader by default. Materialized may be used only when there is existing evidence of a failed fresh-session Loader and the user explicitly requests it.
15. Generic transition is prohibited by default; it may be executed only when project configuration permits it, the current CLI has no native integration, compatibility evidence is complete, and the user approves the exact plan.
16. The CLI installation source is fixed to one 40-character Git commit SHA in `MANIFEST.json`; V1 does not let the implementing Agent choose among Git, PyPI, or floating `main`.
17. Central-update version rules are fixed: `NONE` publishes no project package; `REFERENCE` bumps patch; a compatible `POLICY` bumps minor; any incompatibility in the schema, manager contract, adapter schema, or fixed paths bumps major.
18. Existing capabilities must be migrated item by item through the “capability conservation gate”; no old capability without a mapping and acceptance test may be deleted, weakened, or claimed as migrated.

# Core Conclusion

The project does not need to pre-enroll every Agent that might be used. The correct model is:

`Project stores an Agent-neutral governance package → current Agent declares identity on first use → resolve a native integration supported by the current CLI → install on demand → generate and verify that Agent's project governance entry point → commit the adapter record`

After one project-level adaptation for a given Agent, subsequent collaborators directly reuse the committed integration and adapter and do not repeat the initial enrollment.

However, one technical boundary must be accepted: the current `specify` CLI does not know “who is calling me,” and different Agents have no unified project rules file, Skills directory, Commands format, or invocation protocol. Therefore, “resolve on first use without pre-enrollment” can be implemented, but “any completely unknown Agent can be automatically compatible with zero knowledge and zero configuration” cannot be promised.

A completely unknown Agent must satisfy at least one of the following three conditions:

1. The current CLI already provides a native integration for that Agent.
2. The Agent is compatible with the validated `generic` Commands contract, and the user or project policy explicitly approves degraded mode.
3. A true native integration is developed, reviewed, and released for that Agent.

If the product identity, rules entry point, Skills or Commands directory, file format, parameter placeholders, and invocation semantics are all unknown, the manager must stop and must not guess.

# Assumptions That Must Be Abandoned

Implementation must not depend on the following assumptions:

- The current Agent is necessarily Codex, Claude, or Gemini.
- `AGENTS.md` is a universal standard that every Agent reads.
- The Agent whose CLI is installed on the machine is the Agent for the current session.
- The Agent shown as available by `specify check` is the current caller.
- The default integration in `.specify/integration.json` is the Agent for the current session.
- The presence of `.claude/`, `.agents/`, or `.trae/` in the project proves the current Agent identity.
- Products with similar names can be automatically mapped to the same integration.
- `generic` can always substitute when a native integration cannot be found.
- Once multiple integrations coexist, every Agent automatically receives the same extension, preset, and event capabilities.
- `specify integration use <key>` is a personal setting that can be switched without side effects in every session.

# Current Runtime Verification Baseline

At the time this document was drafted, the following was installed on the local machine:

```text
specify 0.16.6.dev0
```

The following was verified during drafting:

- `specify check` can list multiple Agents known to the current CLI.
- Trae has a built-in integration with key `trae`.
- Trae's Spec Kit Skills are located at `.trae/skills/speckit-*/SKILL.md`.
- CodeBuddy has a built-in integration with key `codebuddy`.
- The current built-in registry has no literal `WorkBuddy`.
- WorkBuddy must not be automatically identified as CodeBuddy because their names are similar.
- `specify integration status --json` can read the health status of the project's current integration.
- In the current version, `specify integration list`, `search`, and `info` require the project to already contain `.specify/`.
- Catalog search may depend on the network or cache.
- If `--integration` is omitted during current non-interactive initialization, Copilot is selected by default rather than the current Agent being identified.
- `generic` is a Markdown Commands adapter, not a universal adapter layer for arbitrary Agents.
- `generic` currently does not declare multi-install safe.
- `integration use <key>` modifies the project's sole default integration and affects default-sensitive artifacts.
- A non-default integration may have core Spec Kit Skills or Commands, but extensions, presets, events, and some shared templates may still be related to the default integration.

The above is only a verification snapshot. The implementing Agent must rerun current runtime discovery and must not treat the version snapshot as a permanent fact.

Before implementation begins, run at least:

```bash
specify version
specify --help
specify check
specify init --help
specify integration --help
specify integration list --help
specify integration status --help
specify integration install --help
specify integration use --help
specify integration switch --help
specify integration scaffold --help
specify extension --help
specify extension add --help
specify extension update --help
specify bundle --help
specify bundle build --help
specify bundle install --help
```

If the current CLI differs from this document, the current project state, current integration, and current CLI are the operational authority; record the difference in the design documents, compatibility records, and tests. Do not silently guess commands from the old document.

# Overall Architecture

The final architecture consists of five layers:

| Layer | Function | Depends on a specific Agent |
|---|---|---:|
| Global Bootstrap | Discovers the project governance package, establishes basic boundaries, and discovers central updates | No |
| Project governance package | Complete Policy, Reference, operating protocol, version, and project-specific exceptions | No |
| Project governance manager | Resolves the Agent, generates plans, writes the adapter, validates, and upgrades | No |
| Agent Adapter | Delivers the project governance entry point to the Agent actually in use | Yes, generated on demand |
| Spec Kit Integration | Provides native Skills, Commands, and related artifacts for the current Agent | Yes, managed by the CLI |

The following responsibility boundaries must be maintained:

1. Policy determines “how work should be done.”
2. The current CLI determines “which commands and integrations are supported now.”
3. The project governance package determines the governance baseline jointly accepted by the team.
4. The Adapter determines how a given Agent reads the project governance package.
5. The Integration determines how a given Agent invokes Spec Kit.
6. The governance manager must not fabricate native Agent Skills, Commands, events, or presets.
7. Spec Kit integrations are not responsible for maintaining the complete project Policy.
8. The central Reference may provide candidate updates only; it may not bypass project review.
9. The current user’s personal global rules may not override the shared governance baseline already committed to the project.

# Authority Order

The authority order for governance policy must be:

1. The user’s current explicit instructions.
2. Higher-priority runtime or security rules.
3. All applicable project-local rules, including the native Agent anchor, root or subdirectory Agent rules, README, architecture, compliance and security rules, and `LOCAL_OVERRIDES.md`.
4. The project-committed `POLICY.md`.
5. The user’s personal global Bootstrap.
6. The project `REFERENCE.md`.
7. The central Reference on the personal machine.
8. Upstream documentation and source code.

The authority order for runtime operational facts must be:

1. The current project `.specify/` state.
2. The currently installed integration and its manifest.
3. The currently installed `specify` CLI.
4. The project-committed `REFERENCE.md`.
5. The personal central Reference.
6. Upstream documentation and source code.

When the personal central Reference discovers content newer than the project, it may generate only a candidate upgrade description. Until the project merges an upgrade PR, the committed governance package remains the shared baseline.

# Capability Conservation Gate

This refactor changes only how governance knowledge is maintained, distributed, deployed, and updated; it must not weaken any engineering governance capability that already exists. Before implementation begins, `governance/capability-baseline.json` must be established, and every legacy capability must be mapped to a new destination through schemas and tests.

## Capability Baseline Sources

The implementation Agent must read and register, section by section:

- `GLOBAL_POLICY.md`
- `SPEC_KIT_REFERENCE.md`
- The full `README.md`, including Chinese and English global deployment, Durable design decisions, checker, wrapper, exit codes, and platform behavior
- `AGENTS.md`
- `UPSTREAM_BASELINE`
- `docs/UPSTREAM_UPDATE_POLICY.md`
- `docs/CHANGE_IMPACT.md`
- `docs/HISTORY.md`
- `scripts/check_upstream.py`
- `scripts/check-upstream.sh`
- `scripts/check-upstream.ps1`
- `.github/workflows/check-spec-kit-upstream.yml`
- The current CLI’s `version`, `--help`, and integration behavior

Registration must not be based on headings alone. Every rule containing the semantics of “must,” “must not,” “priority,” “completion condition,” “authority order,” or “failure handling” must have an independent capability ID.

## Fixed Capability Categories

Each capability may use only the following disposition:

```text
PRESERVE
MOVE
REPLACE
```

- `PRESERVE`: The semantics and scope remain unchanged; only equivalent formatting or wording cleanup is allowed.
- `MOVE`: The semantics remain unchanged, but the capability is migrated from the old file to a specific new file.
- `REPLACE`: The legacy capability is replaced by a specific new protocol. The replacement rationale, evidence of user approval, target capability ID, and regression tests must be recorded.

V1 has no `REMOVE` disposition. The implementation Agent must not delete any legacy rule and claim that it is “covered by the overall architecture.” If deletion is truly required, implementation must stop, the user’s explicit approval for the specific capability ID must be obtained, and this implementation document and the schema must be modified first.

## Capability Record Structure

Every record must contain:

```json
{
  "id": "CAP-NATIVE-INTEGRATION-NO-DOWNGRADE",
  "source": {
    "file": "GLOBAL_POLICY.md",
    "section": "Agent-neutral integration",
    "source_sha256": "<sha256>"
  },
  "requirement": "When a native integration exists for the concrete Agent, an unwritable target or permission failure is a blocker and must not fall back to generic.",
  "disposition": "PRESERVE",
  "targets": [
    "GLOBAL_POLICY.md",
    "governance/project/POLICY.md",
    "governance/project/OPERATING_PROTOCOL.md"
  ],
  "tests": [
    "test_native_target_unwritable_is_blocker",
    "test_native_install_failure_never_proposes_generic",
    "test_completion_rejected_without_native_managed_files"
  ],
  "approval": null
}
```

## Capability Domains That Must Be Conserved

At least the following capability domains must be registered; “at least” means that the implementation Agent must also register other existing rules discovered by scanning, not that these domains are optional:

1. Prefer Spec Kit for substantive engineering work.
2. Avoid meaningless process for lightweight tasks.
3. Identify the actual project root.
4. Understand the brownfield system.
5. Protect the user’s existing work.
6. Resume an existing `.specify/` state instead of reinitializing it.
7. After protecting existing work, support a controlled first initialization for a non-empty brownfield project.
8. Agent-neutral invocation; do not hard-code one command syntax.
9. Prefer the current Agent’s native integration.
10. When a native integration target is unwritable, permission is insufficient, a sandbox blocks it, or installation fails, block the operation and never downgrade to generic.
11. `generic` must not masquerade as native Skills or Commands support.
12. Perform the multi-install safety check before installing an integration.
13. Preserve the authority order of the current project, integration, CLI, Reference, and upstream.
14. The `constitution → specify → clarify → plan → checklist → tasks → analyze → implement → validate → converge` lifecycle.
15. The quality-gate semantics of Clarify, checklist, and analyze.
16. Keep the specification, plan, tasks, and implementation synchronized.
17. Bug reproduction, remediation, and validation.
18. The validation and convergence completion gate.
19. Layered upgrades for the CLI, integration, extension, and Skills.
20. Do not mistake global CLI installation for installation of project Agent Skills.
21. Never hide failed checks or unresolved blockers at completion.
22. The central upstream baseline, `NONE`, `REFERENCE`, and `POLICY` classifications, and human review.
23. Do not merge upstream history or automatically deploy Policy changes.
24. Advance `UPSTREAM_BASELINE` only after evidence review, document updates, and validation are complete.
25. Stop and require human review when the baseline is not an ancestor of current upstream, history has been rewritten, or the official remote does not match.
26. Use the official upstream remote only for fetch, log, diff, and evidence; do not replace this repository or merge upstream history.
27. A `REFERENCE` change updates only the runtime Reference; do not also modify Policy when methodology has not changed.
28. Keep the checker read-only; it must not modify Policy, Reference, baseline, or the worktree. Conserve the existing meanings of exit codes `0`, `1`, and `2` individually.
29. Keep POSIX and PowerShell wrapper behavior equivalent.
30. Scheduled and manual CI only detects, classifies, and creates notifications or issues; it must not automatically merge, deploy, or advance the baseline.
31. Map the existing single source of truth, path validation, and deployment locator behavior to the new single-template marker protocol with `REPLACE`, and record approval evidence from the user in this session.

## Fixed Regression Gate for No Downgrade from Native Integration

The following scenario must be a release-blocking test:

1. The current Agent identity and native integration key are explicit.
2. The current CLI confirms that the native integration exists.
3. The target Skills or Commands path is unwritable, or CLI installation returns a permission failure.
4. The Resolver must return `NATIVE_INSTALL_BLOCKED`.
5. The operation plan must not contain `generic`, another Agent key, `--force`, or a “migration complete” conclusion.
6. The final state must not be higher than blocked.
7. After the user fixes permissions or provides a writable checkout, the same native key must be used again.
8. The blocker may be cleared only after `specify integration status --json` and managed-file validation succeed.

This rule must be retained in both the global template and the project `POLICY.md`, because the global Bootstrap must protect first initialization before the project governance package is installed, while the project Policy protects collaborators’ subsequent operations.

## Runtime Artifact Conservation

Governance package migration must not automatically delete, uninstall, switch, rebuild, or downgrade any existing:

- default integration
- additional integrations
- integration manifests
- extensions
- presets
- workflows
- event configuration
- shared infrastructure
- `.specify/memory/constitution.md`
- existing feature artifacts under `specs/`
- native Agent Skills or Commands

The runtime inventory must be recorded before migration and compared item by item afterward. Any reduction in artifacts, a state changing from healthy to warning/error, a capability degrading from `READY` to `READY_WITH_LIMITATIONS`, or native Skills becoming invisible must block completion unless there is a `REPLACE` capability record explicitly approved by the user.

## Capability Conservation Acceptance

The release build must fail on any of the following conditions:

- A legacy rule has no capability ID.
- A capability has no target.
- A capability has no test.
- `REPLACE` has no evidence of user approval.
- The target Policy lacks the no-downgrade-from-native-integration rule.
- The runtime inventory comparison shows an unapproved reduction.
- The project has only `generic`, but the current Agent’s native integration actually exists.
- The Adapter claims `READY`, but capability verification is incomplete.

# Target Structure of the Central Governance Repository

After implementation, the current repository must have the following fixed structure:

```text
GLOBAL_POLICY.md
SPEC_KIT_REFERENCE.md
UPSTREAM_BASELINE
README.md

governance/
  project/
    POLICY.md
    START_HERE.md
    OPERATING_PROTOCOL.md
    AGENT_ONBOARDING.md
    LOCAL_OVERRIDES.template.md
    PROJECT_CONFIG.default.json

  resolver/
    resolver-contract.md

  manager/
    speckit_governance.py
    bootstrap_updater.py

  schemas/
    governance-manifest.schema.json
    project-config.schema.json
    adapters.schema.json
    resolution-result.schema.json
    operation-plan.schema.json
    capability-baseline.schema.json

  capability-baseline.json

  extension/
    speckit-governance/
      extension.yml
      commands/
      scripts/
        python/
          bootstrap_governance.py
      templates/

  release/
    COMPATIBILITY.md
    CHANGELOG.md
    latest.json

scripts/
  build_governance_release.py
  validate_governance_release.py

tests/
  governance/
    unit/
    integration/
    fixtures/
    e2e/

docs/
  GLOBAL_POLICY_DEPLOYMENT.md
  archive/
    PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md
  PROJECT_GOVERNANCE_OPERATIONS.md
  PROJECT_GOVERNANCE_SECURITY.md
  PROJECT_GOVERNANCE_MIGRATION.md
  PROJECT_GOVERNANCE_TEST_MATRIX.md
```

The directory and file names are the V1 fixed protocol; they must not be tweaked, renamed, or duplicated in a parallel implementation. If a fixed path must be migrated in the future, the major version must be bumped and a migrator, migration documentation, and rollback tests must be provided. Two Policy sources requiring independent manual maintenance must not be created at the same time.

The central `governance/manager/speckit_governance.py` is the manager’s sole source file. The Release builder must copy it byte-for-byte to the project path `tools/spec-kit-governance/governance.py`; only the filename may differ, with no template substitution or second hand-written implementation. Build validation must assert that their normalized content SHA-256 values are identical. The project file is updated only through a release upgrade and must not be written back to the central source.

# Requirements for Restructuring `GLOBAL_POLICY.md`

The current `GLOBAL_POLICY.md` contains stable principles, CLI operations, the complete lifecycle, and upgrade rules. After implementation, it must become the sole global deployment template that can be copied directly. Deployers must no longer be asked to “copy the Policy and append a locator separately.”

The template must satisfy the following:

1. UTF-8 and LF.
2. The first line must be the fixed START marker.
3. The last non-empty content must be the fixed END marker.
4. START and END must each appear exactly once.
5. The local path placeholder must appear exactly once.
6. The placeholder must be on the `SPEC_KIT_GOVERNANCE_SOURCE` line.
7. It must not contain a global file path for any Agent product.
8. It must not contain a second machine path, `~`, an environment-variable reference, or platform guessing.
9. It must not exceed 40 non-empty lines.

For the initial V1 implementation, the body of `GLOBAL_POLICY.md` must be implemented according to the following template. Later POLICY impact reviews may modify the Bootstrap body, but the marker names, SemVer grammar, unique locator field, and single-placeholder contract must not change. A body change must update the Policy SemVer, capability baseline, deployment tests, and change history, and undergo human POLICY review. Changing the marker or locator contract requires bumping the major version and providing a global deployment migration process.

```markdown
<!-- SPEC-KIT-GLOBAL-POLICY:START version=1.0.0 -->
# Scope

Use GitHub Spec Kit for substantive software engineering. Do not require the full lifecycle for read-only investigation, explanation, trivial typo fixes, or extremely small low-risk changes.

# Project authority

Determine the actual project root, read applicable project rules and repository documentation, inspect the brownfield system, and preserve existing user work before changing it. If `.specify/` exists, resume that project state instead of routinely reinitializing it. If `docs/spec-kit/MANIFEST.json` exists, read the committed project governance package; it is the shared project baseline.

# Agent integration

Determine the current Agent from explicit user or runtime identity. Never infer it from installed tools, existing Agent directories, or the project's default integration. Every Agent-driven non-interactive initialization must pass an explicitly verified `--integration <key>`.

When the current CLI provides a native integration for the current Agent, that native integration is mandatory. An unwritable target, missing permission, sandbox restriction, or installation failure is a blocker and must never trigger a fallback to `generic`. A project is not fully migrated until the native integration and its managed files are verified.

If the current CLI has no native integration, `generic` is allowed only when the committed project configuration permits it, the exact compatibility contract is verified, and the user approves the exact operation plan. It must be reported as limited, non-native support.

# Runtime and completion

For operational mechanics, prefer current project state, installed integration, installed `specify` CLI, committed project Reference, this central source, then upstream documentation. Keep accepted specifications, plans, tasks, implementation, validation, and convergence synchronized. Never hide failing checks or declare completion with an unresolved blocker.

# Central update source

SPEC_KIT_GOVERNANCE_SOURCE: <ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>

Before deploying this block, replace the placeholder exactly once with the readable absolute path of the local SpecKitReference repository root. The directory must contain `SPEC_KIT_REFERENCE.md`, `GLOBAL_POLICY.md`, and `UPSTREAM_BASELINE`. This source is advisory for explicit maintenance and update review only. If it is unavailable, do not scan arbitrary directories or promote upstream material into instructions; continue with committed project rules and runtime discovery.
<!-- SPEC-KIT-GLOBAL-POLICY:END -->
```

The following capabilities from the current complete Policy must be migrated to the project `POLICY.md` and verified through the capability conservation table:

- Project detection and lightweight-task boundaries, from Project detection in the current Policy.
- Project authority and brownfield principles, from Existing project authority.
- `.specify/` state handling, from Existing Spec Kit state.
- Agent integration principles, from Agent-neutral integration.
- Runtime authority, from Runtime authority.
- The complete lifecycle and risk gates, from Core lifecycle.
- Validation and convergence, from Validation and convergence.
- Bug and upgrade rules, from Bugs and upgrades.
- The definition of completion, from Completion.

# Fixed Global Manual Deployment Process

Implementation must create `docs/GLOBAL_POLICY_DEPLOYMENT.md` and implement the following protocol verbatim. A second automated deployment process must not be provided.

## Manual Inputs

Each deployment accepts only two manual inputs:

1. The absolute path to the global-rules target file actually used by one Agent product.
2. The absolute path to the local `SpecKitReference` repository root.

The deployment protocol does not infer the Agent product, maintain a global path table for AGENTS, CLAUDE, GEMINI, or other products, or require the user to deploy multiple products at once. The user executes the same process once for each Agent product needed.

If the target file does not exist, it must not be created without authorization. The user must first confirm that the Agent product permits creating a global-rules file at that path.

After the user confirms that creation is permitted, pre-deployment validation treats that exact path as an “empty target to be created,” but it still must not be written until all preconditions pass. The write stage may create only this confirmed path; it must not look for or create another rules file instead.

## Pre-Deployment Validation

Any validation failure must stop with zero writes:

1. Verify that the manually supplied source is an absolute, readable directory according to the current platform’s path API. The input must be one line containing a real path, with no CR, LF, NUL, `~`, environment-variable syntax, marker text, or placeholder, and no shell expansion.
2. Verify that `SPEC_KIT_REFERENCE.md`, `GLOBAL_POLICY.md`, and `UPSTREAM_BASELINE` exist and are readable in the source.
3. The sole template is fixed as `<source>/GLOBAL_POLICY.md`; no second template may be obtained from the current working directory, another checkout, or session text.
4. Read the template and verify UTF-8, LF-only line endings, exactly one trailing LF, and no BOM.
5. The START marker must match the entire line `^<!-- SPEC-KIT-GLOBAL-POLICY:START version=(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*) -->$` and occur exactly once.
6. The END marker must equal the entire line `<!-- SPEC-KIT-GLOBAL-POLICY:END -->`, occur exactly once, and follow START. Any line containing `SPEC-KIT-GLOBAL-POLICY:` that does not match the grammar above causes validation to fail.
7. Verify that `<ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>` occurs exactly once and only on the unique `SPEC_KIT_GOVERNANCE_SOURCE:` line.
8. When reading an existing target, verify that it is BOM-free UTF-8; do not normalize line endings outside the markers. A confirmed target to be created, or an existing target with no markers, has first-deployment status; one valid marker pair in the correct order has update status; any missing marker, duplicate, reversed order, or malformed marker stops the process.

The content inside the markers is a wholly managed artifact and may not be customized locally. During updates, do not attempt to identify or merge manual changes inside the markers; unconditionally replace them with the new rendered block. The deployment documentation must require users to put custom rules they need to retain outside the markers.

## Sole Rendering Transformation

Rendering obtains the complete marker span from the verified `<source>/GLOBAL_POLICY.md` and performs exactly one literal replacement:

```text
<ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>
```

Replace it with the verified absolute source path.

After replacement, verify again that:

- There are zero placeholders.
- Each marker still occurs exactly once.
- The `SPEC_KIT_GOVERNANCE_SOURCE` value exactly matches the input.
- The source directory remains readable and contains the three required files.
- The rendered block uses UTF-8 and LF and ends with one LF.

## First Deployment

For a target to be created or an empty file, the candidate bytes are fixed as the complete rendered block.

An existing non-empty target with no markers must preserve its original bytes in full. If the last byte is LF, append one LF and then the rendered block; if the last byte is not LF, append two LFs and then the rendered block. The target’s original bytes must not be rewritten; newly inserted bytes always use LF even when the original content uses CRLF.

## Update Deployment

If the target already has one valid marker pair, the replacement span starts at the `<` of the START marker, ends at the `>` of the END marker, and includes the one line-ending sequence immediately following END: two bytes when CRLF is present, one byte for LF alone, and no extension when there is no line ending. The candidate is fixed as `prefix bytes + rendered block + suffix bytes`. Prefix and suffix must be preserved byte-for-byte. An update is not a merge; the managed block always follows the source template.

## Writing and Post-Validation

1. Read the current UTC time in the fixed format `YYYYMMDDTHHMMSSZ`. The backup path is fixed as `<absolute target path>.spec-kit-global-policy.backup.<UTC time>`; if it already exists, stop without overwriting the old backup.
2. Copy the complete bytes and file permissions of an existing target to the backup, then reread and verify that the backup hash matches the original target. Do not create an empty backup for a target to be created; the audit record must state `target_previously_absent = true`.
3. Use the operating system’s secure exclusive-create API to create a temporary file in the target file’s directory; do not use a predictable fixed temporary filename.
4. The temporary file inherits the existing target’s permissions. A target to be created uses the current user’s default secure file permissions.
5. Write the candidate content and flush it; perform fsync when supported by the platform.
6. Reread the candidate file and perform all marker, placeholder, source, and outside-marker byte validations.
7. Before writing the mutation, use exclusive-create to establish `<target>.spec-kit-global-policy.deploy-journal.<UTC time>.json`, recording the target pre-state, candidate path and hash, backup path, and phase `prepared`; flush/fsync after writing. If a same-name or unparseable old journal exists, stop and recover first; do not begin a new deployment.
8. Install the candidate for an existing target using an atomic replace on the same filesystem. A target to be created must use no-clobber atomic publish: call Python `os.link(candidate, target, follow_symlinks=False)` on a flushed/fsynced candidate in the same directory; the POSIX equivalent is `link(2)`, and the Windows equivalent is `CreateHardLinkW`. The operation must fail atomically when the target exists and must make the complete candidate bytes appear directly on success. If the filesystem or platform does not support hard-link no-clobber semantics, return `GLOBAL_DEPLOY_ATOMIC_CREATE_UNSUPPORTED` and keep the target absent; do not fall back to writing the final target directly.
9. After a successful publish, update the journal phase to `published` and fsync it; reread the final target and verify its hash, markers, and source. If an existing target fails, perform one atomic recovery using the backup, then reread and verify the recovery hash. If validation of a target to be created fails, delete the target only when its hash equals the candidate hash in the journal; stop and recover manually when the hashes differ.
10. Crash recovery must read the journal first: when the phase is `prepared` and the target is absent, delete the candidate with the same identity and finish; when the target exists and its hash equals the candidate hash, treat it as a complete publish and continue post-validation; stop when the target hash differs. Apply the same hash determination for phase `published`. Do not start a new deployment until the journal has converged.
11. After successful validation, delete the candidate, update the journal to `verified`, and fsync it; fsync the parent directory when supported. Retain the journal and timestamped backup until the user completes real Agent loading validation.
12. The user opens a new session in the target Agent product and manually confirms that the global-rules location was actually loaded.
13. Report deployment complete only after both text validation and real Agent loading validation succeed.

When permissions, temporary-file handling, backup, atomic replacement, or post-validation fails, the original target must be preserved or restored. If recovery validation fails, report the exact target and backup paths and enter manual recovery; do not continue deployment or report success.

## Subsequent Updates

After the central `GLOBAL_POLICY.md` version changes, the user reruns the same “update deployment” process. Do not manually synchronize the old block section by section.

After the Source directory is moved, the user must rerun the update process with the new absolute path. The tool must not scan the disk to find the new location.

# Central Reference and Project Reference

The root `SPEC_KIT_REFERENCE.md` remains the central review Reference.

The following fixed portable-content marker must be added to it:

```markdown
<!-- PROJECT-PORTABLE-REFERENCE:START version=1 -->

[Runtime discovery, integrations, lifecycle, upgrades, and authority order applicable to any project]

<!-- PROJECT-PORTABLE-REFERENCE:END -->
```

When building the project governance package, copy only the content inside the markers.

For every portable fact in the capability baseline sourced from the current `SPEC_KIT_REFERENCE.md`, the target must point to a specific capability ID inside the central portable marker, and the built project’s `REFERENCE.md`, `POLICY.md`, or `OPERATING_PROTOCOL.md` must be verified to contain that semantics. It must not merely be registered as a source and then migrated into free text outside build-test coverage.

The following centrally maintained information must not be copied into the body of a business project Reference:

- The current maintainer’s local machine path.
- Remote operation instructions for this governance repository.
- The central GitHub Action maintenance process.
- The central `UPSTREAM_BASELINE` file path.
- CLI detection results from the current machine.
- The central worktree status.
- Personal environment diagnostics.

The source commit of the project Reference, the upstream commit reviewed centrally, the generation time, and the version are written to `MANIFEST.json`; they must not be mixed into the Reference body.

The portable block must contain all of the following, along with other portable runtime knowledge discovered by the capability-baseline scan:

- Runtime discovery commands.
- The meaning of `.specify/`.
- The separation between the CLI and Agent integrations.
- The concepts of integration install, status, and upgrade.
- The applicable boundaries of integration use, switch, self check, self upgrade, and extension update.
- A warning that Skills and Commands layouts may change.
- The principle of preferring native integrations.
- A warning that the default integration may differ from the current Agent identity.
- Non-interactive init must explicitly pass `--integration`.
- The capability limitations of `generic`.
- Do not treat an ordinary `init --force` as an upgrade or repair method.
- The verified limitations of Bug workflow extensions and project-aware discovery.
- The lifecycle and convergence.
- Runtime authority order.

# Structure After Installation in a Business Project

Every business project with an installed governance package must commit:

```text
AGENTS.md
.gitignore

docs/spec-kit/
  START_HERE.md
  POLICY.md
  REFERENCE.md
  OPERATING_PROTOCOL.md
  AGENT_ONBOARDING.md
  LOCAL_OVERRIDES.md
  PROJECT_CONFIG.json
  MANIFEST.json
  ADAPTERS.json

tools/spec-kit-governance/
  governance.py
  VERSION

.specify/
  ...

.spec-kit-governance/   # local runtime state, ignored and not committed
  plans/
  backups/
  staging/

<native context anchor for each onboarded Agent>
<native Skills or Commands for each installed Agent integration>
```

Requirements:

- `AGENTS.md` is a general best-effort entry point and does not mean that every Agent will read it.
- Generate a native context anchor only for an Agent that has actually been used and verified.
- Do not pre-generate fixed collections such as `CLAUDE.md`, `GEMINI.md`, or `.trae/`.
- The project does not maintain a list of Agents that might be used in the future.
- `ADAPTERS.json` records only Agents that have actually been onboarded and verified.
- `PROJECT_CONFIG.json` stores the sole machine-readable project decision.
- `tools/spec-kit-governance/` must run directly without depending on a particular default integration.
- Reading project governance must not depend on the central Reference’s absolute path.
- `specify` continues to manage Skills, Commands, and manifests in `.specify/`.
- The root `.gitignore` must contain the ignore rule inside a separate block `# SPEC-KIT-GOVERNANCE-RUNTIME:START`, `/.spec-kit-governance/`, `# SPEC-KIT-GOVERNANCE-RUNTIME:END`; content outside the markers must be preserved byte-for-byte. The project must not commit this runtime state.

# Project Governance File Responsibilities

## `START_HERE.md`

This is the first entry point for an Agent without background context and must use short sentences and explicit steps:

1. Confirm the actual project root.
2. Read `POLICY.md`.
3. Read `PROJECT_CONFIG.json`.
4. Read `LOCAL_OVERRIDES.md`.
5. Read `REFERENCE.md` whenever CLI, integration, extension, init, upgrade, rollback, or recovery is involved.
6. Check `.specify/`.
7. Check whether the Agent's adapter is registered.
8. Do not treat the project's default integration as the current Agent identity.
9. Do not omit `--integration` for non-interactive initialization.
10. Execute the first-onboarding protocol when the current Agent is not registered.
11. For every governance update, plan first, then review, then apply.

## `POLICY.md`

It must include all of the following:

- Scope of applicability.
- Project-root identification.
- Brownfield inspection requirements.
- Protection of user work.
- Handling of an existing `.specify/`.
- Dynamic Agent resolution.
- Native integration priority.
- When any of the current Agent's native integration, init target, managed Skills or Commands, or context anchor cannot be completed because of unwritability, permissions, sandbox, repair, or installation failure, it must return `NATIVE_INSTALL_BLOCKED`; it must not use generic or another key and must not report completion.
- Unsafe multi-install handling.
- Default integration handling.
- The complete lifecycle.
- Quality gates explicitly enabled by `PROJECT_CONFIG.json.quality_gates`.
- Bug workflow.
- Synchronization between specification and implementation.
- Testing and validation.
- The convergence completion gate.
- The authority order for CLI, integration, and Reference.
- Governance-package upgrades and the boundary for central updates.
- Failure, blocking, and rollback principles.

The body must not hard-code a particular set of Agents as the default or required supported set.

## `REFERENCE.md`

Only portable runtime knowledge belongs here:

- `specify version`
- `specify --help`
- `specify integration --help`
- Meaning of `.specify/`
- Integration lifecycle
- Separation of Skills or Commands from the global CLI
- Upgrade relationship among the CLI, integration, extension, and bundle
- Lifecycle concepts
- Runtime authority
- `generic` limitations
- Explicit integration requirement for non-interactive initialization

## `OPERATING_PROTOCOL.md`

All execution branches must be written as executable steps:

- New project.
- Existing Spec Kit project.
- CLI missing.
- Current Agent registered.
- Current Agent unregistered but supported by the CLI.
- Current Agent unsupported by the CLI.
- Safe multi-integration.
- Unsafe multi-integration.
- Default integration differs from the current Agent.
- Context anchor unknown.
- Native integration, init target, managed files, or context anchor unwritable, permission-denied, sandbox-blocked, or partially failed during installation. This branch must always: preserve and inventory existing state; return `NATIVE_INSTALL_BLOCKED`; request permission or a writable checkout; after repair, regenerate the plan with the same claimed key; never fall back to generic.
- No network.
- Policy or Reference hash conflict.
- Central candidate update.
- Rollback.

## `AGENT_ONBOARDING.md`

Describe only identity resolution, integration installation, context-anchor delivery, verification, and registration when an Agent first enters the project; do not repeat the daily lifecycle.

## `LOCAL_OVERRIDES.md`

This file is owned by the project maintainers and is never overwritten by central updates.

This file records only human-readable explanations of project governance:

- Business reasons for each `PROJECT_CONFIG.json` field.
- Project testing, compliance, and security requirements.
- Project-specific quality gates and completion conditions.

The Manager must not parse this Markdown file to determine machine behavior.

## `PROJECT_CONFIG.json`

This file is owned by the project maintainers and is never overwritten by central upgrades. It must pass `project-config.schema.json` validation. The initial V1 content is fixed as follows:

```json
{
  "schema_version": 1,
  "default_integration": {
    "policy": "pinned",
    "key": null,
    "allow_change": false
  },
  "onboarding": {
    "requires_current_user_approval": true,
    "allow_unsafe_multi_install": false
  },
  "generic": {
    "policy": "deny",
    "maximum_bindings": 1
  },
  "catalogs": {
    "allowed_sources": []
  },
  "context": {
    "default_delivery_mode": "loader",
    "allow_materialized_after_loader_failure": true
  },
  "upgrade": {
    "review_mode": "pull-request-required"
  },
  "quality_gates": {
    "clarify": "risk-triggered",
    "checklist": "risk-triggered",
    "analyze": "risk-triggered",
    "validate": "required",
    "converge": "required"
  }
}
```

In the central template, `default_integration.key` is fixed to JSON `null`, meaning that the Agent-neutral bootstrap is not yet bound to a specific Agent. When there is no `.specify/` and no active binding, `null` is a valid `pre-init-governance` state; the governance package must not invent an integration key to pass validation. When the first `plan-init` succeeds, the explicitly user-approved actual key must be written in the same transaction. A project with an existing `.specify/` or active binding must have a non-empty key; only then may schema/`verify` reject `null`.

The only fields that project maintainers may modify through a separate PR are:

- `default_integration.key`
- `default_integration.allow_change`
- `generic.policy`; the enum permits only `deny` or `explicit-approval-required`
- The enums declared by the schema in `quality_gates`

In V1, `onboarding.requires_current_user_approval` and `onboarding.allow_unsafe_multi_install` must remain `true` and `false`, respectively; the schema must reject other values. In V1, `generic.maximum_bindings` must be `1`. In V1, `catalogs.allowed_sources` must be an empty array; any remote community catalog is for human discovery only and cannot be an installation source. In V1, `upgrade.review_mode` must be `pull-request-required`, and the schema must reject other values. Opening installation sources or local direct-upgrade mode in the future requires bumping the schema and package version and defining immutable refs, artifact hashes, approval, and trust rules.

`risk-triggered` is not discretionary. Every substantive engineering operation plan must contain the following structure:

```json
{
  "ambiguity_open": false,
  "cross_cutting_component_count": 1,
  "public_contract_change": false,
  "data_migration": false,
  "security_impact": false,
  "compliance_impact": false,
  "irreversible_operation": false,
  "artifact_conflict": false,
  "unknown_bug_cause": false,
  "evidence": ["<project-relative-evidence-path>"]
}
```

The Manager must calculate `cross_cutting_component_count` from target paths; the plan author must declare each remaining boolean, and approval of the exact plan must cover them. The gate formulas are fixed:

- `clarify_required = ambiguity_open or artifact_conflict or unknown_bug_cause`
- `checklist_required = public_contract_change or data_migration or security_impact or compliance_impact or irreversible_operation`
- `analyze_required = cross_cutting_component_count >= 2 or artifact_conflict or public_contract_change or data_migration or security_impact or compliance_impact`

If any required gate lacks its corresponding artifact, the Manager must block implementation or completion; if the plan lacks risk assessment or evidence, schema validation fails.

## `MANIFEST.json`

Maintained by the governance manager; arbitrary manual modification is not allowed.

## `ADAPTERS.json`

Records only Agents that have actually onboarded; it must not be prefilled with a product list.

# `MANIFEST.json` Specification

The following structure must be used and strictly validated by `governance-manifest.schema.json`:

```json
{
  "schema_version": 1,
  "governance_package_version": "1.0.0",
  "policy_version": "1.0.0",
  "reference_version": "2026.08.21",
  "manager_version": "1.0.0",
  "source": {
    "repository": "https://github.com/jiezhengj/Spec-Kit-Reference",
    "revision": "<immutable-full-commit-sha>",
    "release": "<immutable-release-tag>",
    "reviewed_upstream_revision": "<full-upstream-sha>"
  },
  "specify_compatibility": {
    "minimum_version": "<minimum-version>",
    "tested_version": "<tested-version>",
    "maximum_version_exclusive": null,
    "approved_install_ref": "<40-character-git-commit-sha>"
  },
  "paths": {
    "start_here": "docs/spec-kit/START_HERE.md",
    "policy": "docs/spec-kit/POLICY.md",
    "reference": "docs/spec-kit/REFERENCE.md",
    "operating_protocol": "docs/spec-kit/OPERATING_PROTOCOL.md",
    "onboarding": "docs/spec-kit/AGENT_ONBOARDING.md",
    "local_overrides": "docs/spec-kit/LOCAL_OVERRIDES.md",
    "project_config": "docs/spec-kit/PROJECT_CONFIG.json",
    "adapters": "docs/spec-kit/ADAPTERS.json",
    "manager": "tools/spec-kit-governance/governance.py"
  },
  "content_sha256": {
    "docs/spec-kit/START_HERE.md": "<sha256>",
    "docs/spec-kit/POLICY.md": "<sha256>",
    "docs/spec-kit/REFERENCE.md": "<sha256>",
    "docs/spec-kit/OPERATING_PROTOCOL.md": "<sha256>",
    "docs/spec-kit/AGENT_ONBOARDING.md": "<sha256>",
    "tools/spec-kit-governance/governance.py": "<sha256>"
  },
  "project_owned_files": [
    "docs/spec-kit/LOCAL_OVERRIDES.md",
    "docs/spec-kit/PROJECT_CONFIG.json",
    "docs/spec-kit/ADAPTERS.json"
  ],
  "portable_anchor": {
    "path": "AGENTS.md",
    "marker_start": "<!-- PROJECT SPEC-KIT GOVERNANCE START -->",
    "marker_end": "<!-- PROJECT SPEC-KIT GOVERNANCE END -->"
  }
}
```

Constraints:

1. `source.revision` must be a full SHA.
2. Floating identifiers such as `main` and `latest` are not permitted as reproducible installation sources.
3. All hashes use normalized UTF-8, LF bytes.
4. Do not record usernames, user directories, tokens, temporary directories, or local absolute paths.
5. Stop when the schema is incompatible.
6. `LOCAL_OVERRIDES.md` is not part of the central overwrite set.
7. During a project upgrade, the manager itself must also verify its hash.
8. The manifest may be updated only after the operation plan passes validation.
9. `approved_install_ref` must match `^[0-9a-f]{40}$`.
10. A release artifact must contain no `<...>` placeholders. The builder must fill every field with real versions, SHAs, and hashes before release.
11. The fixed meaning of `maximum_version_exclusive: null` is “no additional hard upper bound declared”; a CLI above `tested_version` still returns `CLI_VERSION_UNTESTED`, may run only read-only doctor/resolve, and all apply operations must wait for compatibility validation or a new release.

CLI compatibility fields do not use SemVer. The V1 accepted version grammar is fixed as `^([0-9]+)\.([0-9]+)\.([0-9]+)(?:(\.dev|a|b|rc)([0-9]+))?$`. Compare the three integers first, then stages in `.dev < a < b < rc < final` order, and finally the stage number; the final stage number is fixed at 0. Any other format returns `CLI_VERSION_UNPARSEABLE`; the implementing Agent must not introduce `packaging`, npm semver, or a self-selected parser.

The determination order is fixed: below `minimum_version` returns `CLI_INCOMPATIBLE`; above `tested_version` returns `CLI_VERSION_UNTESTED`; when `maximum_version_exclusive` is non-null and the current version is greater than or equal to it, also return `CLI_VERSION_UNTESTED`; all other versions may proceed according to the manifest. The governance package, Policy, and manager versions continue to use strict SemVer and must not be mixed with the CLI grammar.

# `ADAPTERS.json` Specification

Initial state:

```json
{
  "schema_version": 1,
  "anchors": [
    {
      "id": "root-agents",
      "path": "AGENTS.md",
      "format": "markdown",
      "delivery_mode": "loader",
      "marker_start": "<!-- PROJECT SPEC-KIT GOVERNANCE START -->",
      "marker_end": "<!-- PROJECT SPEC-KIT GOVERNANCE END -->",
      "managed_content_sha256": "<sha256>",
      "status": "rendered",
      "managed": true
    }
  ],
  "bindings": []
}
```

Physical anchors and Agent bindings must be recorded separately. A physical path may have only one anchor record; multiple Agents may reference the same `anchor_id`.

After an Agent completes first onboarding, add the following to `bindings`:

```json
{
  "runtime_id": "vendor.product",
  "display_name": "Product Name",
  "integration_key": "product-key",
  "integration_mode": "native",
  "status_evidence_sha256": "<sha256-of-normalized-integration-status-json>",
  "default_integration_changed": false,
  "anchor_ids": ["root-agents"],
  "capabilities": {
    "core_workflow": "verified",
    "extensions": "not-verified",
    "presets": "not-verified",
    "events": "not-verified"
  },
  "verification": {
    "status": "active",
    "specify_version": "<version>",
    "product_version": "<version-or-unknown>",
    "verified_at": "<RFC3339>",
    "method": "fresh-session-loader",
    "evidence": "docs/spec-kit/evidence/<immutable-evidence-file>"
  }
}
```

Anchor status permits only:

```text
rendered
stale
blocked
```

Binding status permits only:

```text
provisional
active
deprecated
blocked
```

`rendered` only means that the managed block of the physical anchor has been generated; it does not prove that any Agent has been verified. A binding may be marked `active` only after a fresh session verifies that the Agent loaded the context anchor and can use the declared Spec Kit workflow.

Fixed enums:

- `integration_mode` permits only `native` or `explicit-generic-transition`.
- `capabilities.*` permits only `verified`, `not-verified`, `not-applicable`, or `blocked`.
- `verification.method` permits only `fresh-session-loader` or `fresh-session-materialized`.
- `verification.evidence` must be a project-relative immutable evidence file or an immutable PR URL.
- A binding must not directly own a file path; it may only reference `anchor_ids`.
- Multiple bindings must not separately claim ownership of the same physical marker.

# Dynamic Agent Identity Protocol

The governance manager cannot identify the current Agent from nothing.

Priority of current-Agent identity declarations:

1. The integration key explicitly provided by the user in the current request.
2. The runtime ID and integration key explicitly provided by the Agent host through runtime metadata.
3. `SPEC_KIT_CURRENT_AGENT_ID` and `SPEC_KIT_CURRENT_INTEGRATION_KEY` explicitly passed by the host.
4. The Agent's explicit declaration of its own runtime ID and integration key.
5. When the user provides only a product name, it may be used only to display candidates and cannot produce a mutation plan.

`ADAPTERS.json` is not an identity source. Only after obtaining the current runtime ID may the manager query for an active binding with the same runtime ID. The current Agent identity must not be inferred because the project has only one binding.

If any two declaration sources provide different runtime IDs or integration keys, return `IDENTITY_CONFLICT`; do not choose a higher-priority value and continue mutation. The user must provide one unambiguous value again.

Do not use the following to determine the current Agent:

- A CLI present on PATH.
- A product shown as available by `specify check`.
- `.agents/`, `.claude/`, `.trae/`, or similar directories in the project.
- The default integration in `.specify/integration.json`.
- The Git author or file creator.
- Fuzzy string similarity.
- Another product with a similar name.

When identity is unknown, mutation must stop and the following prompt must be shown:

```text
Please provide the current Agent's runtime ID and its integration key in Spec Kit.
I will not infer them from installed tools, existing directories, or similar product names.
```

`SPECKIT_INTEGRATION_DEFAULT` must not be used as the current Agent identity. It affects only the default for initialization without arguments.

# Agent Resolution State Definitions

The governance manager must return only one of the following states:

| State | Meaning |
|---|---|
| `CLI_MISSING` | `specify` is not installed |
| `CLI_INCOMPATIBLE` | CLI is outside the manifest compatibility range |
| `CLI_VERSION_UNTESTED` | CLI is above the tested version; only Policy, Reference, doctor, and resolve-agent are allowed; plan/apply are not allowed |
| `CLI_VERSION_UNPARSEABLE` | CLI version does not conform to the V1 restricted version grammar; only Policy and Reference may be read |
| `IDENTITY_UNKNOWN` | Current Agent identity cannot be determined |
| `IDENTITY_CONFLICT` | Two declaration sources provide conflicting identity or key |
| `KEY_REQUIRED` | Product name is known, but no exact integration key usable for mutation is available |
| `PROJECT_NOT_INITIALIZED` | Agent is known, but the project has no `.specify/` |
| `EXACT_NATIVE_INSTALLED` | Native integration is installed and healthy |
| `NATIVE_CANDIDATE_NOT_INSTALLED` | User or host provided a candidate key, but installation and status verification have not succeeded |
| `NATIVE_CANDIDATE_INSTALLED_UNVERIFIED` | Candidate key is installed and healthy, but its match to the current runtime ID has not been proved |
| `NATIVE_CANDIDATE_REJECTED` | Current CLI rejected the candidate key |
| `NATIVE_INSTALL_BLOCKED` | Native integration is blocked by permissions, an unwritable target, sandbox, or an installation error |
| `AMBIGUOUS` | Multiple candidates exist |
| `CATALOG_UNAVAILABLE` | The sole determination depends on a catalog, but the catalog is unavailable |
| `CONTEXT_ANCHOR_UNKNOWN` | No active anchor exists and the user provided no project-relative anchor |
| `ANCHOR_FORMAT_UNSUPPORTED` | Anchor is not Markdown or plain text supported by V1; plan/apply is prohibited |
| `UNSUPPORTED_GENERIC_COMPATIBLE` | No native integration exists, but compatibility with generic has been verified |
| `UNSUPPORTED_INCOMPATIBLE` | No native integration exists and generic is incompatible or unknown |
| `INTEGRATION_CONFLICT` | Safe multi-install is not possible |
| `DEFAULT_CHANGE_FORBIDDEN` | Project config has not enabled the one-time default-change window |
| `CENTRAL_SOURCE_UNVERIFIED` | Central release index, Git revision, worktree, or artifact hash is inconsistent |
| `STATE_BROKEN` | Current Spec Kit state is damaged |
| `RECOVERY_REQUIRED` | A failed operation leaves paths whose provenance or safe recovery cannot be proved; human handling is required |
| `READY_WITH_LIMITATIONS` | Core workflow is available, but default-sensitive capabilities are unverified |
| `READY` | Capabilities within the declared scope have been verified |

Ambiguous results must not be forcibly converted into an integration key.

# Dynamic Integration Resolution Algorithm

## Phase One: Read-Only Preflight

The governance manager must:

1. Determine the Git project root.
2. Read all applicable project rules.
3. Check worktree status and protect existing user work.
4. Check `.specify/`.
5. Check the project governance package and manifest.
6. Read and validate `PROJECT_CONFIG.json`.
7. Check whether `specify` is on PATH.
8. Run `specify version`, `specify --help`, and `specify integration --help`.
9. Do not initialize a real project to obtain catalog information.
10. Do not write files.

## Phase Two: Determine Current Agent Identity

Collect identity according to the “Dynamic Agent Identity Protocol.”

If identity is unknown, return `IDENTITY_UNKNOWN`.

If only a product name is available and there is no exact key, return `KEY_REQUIRED`.

If the user, host, or Agent provides an integration key, mark that value only as `claimed_key`. Successful CLI installation and healthy `specify integration status --json` prove only that the key can be installed, not that it matches the current runtime ID. It may be marked `EXACT_NATIVE_INSTALLED` only when an active binding already exists or a new fresh-session runtime-to-key verification has completed.

When `claimed_key == "generic"`, immediately enter the Explicit Generic Transition eligibility validator; do not return any `NATIVE_*` state or enter the native-install branch.

## Phase Three: Existing `.specify/` Project

Run:

```bash
specify integration status --json
```

Requirements:

1. `specify integration status --json` is the only integration CLI output that V1 permits direct machine parsing.
2. Return `STATE_BROKEN` when JSON cannot be parsed, status reports a blocking finding, or the existing manifest is unhealthy.
3. If the claimed key appears in `installed_integrations` and its manifest check has no missing, modified, or invalid files: return `EXACT_NATIVE_INSTALLED` when an active binding with the same runtime ID and key exists; otherwise return `NATIVE_CANDIDATE_INSTALLED_UNVERIFIED`.
4. If the candidate key is not installed, return `NATIVE_CANDIDATE_NOT_INSTALLED` and allow an installation plan containing only that key.
5. The V1 manager does not parse Rich human output from `integration list`, `search`, or `info`, import the private `specify_cli` Python API, or create a temporary Spec Kit project to query the registry.
6. The original text of `integration list`, `search`, `info`, Reference, and catalog output may be attached to a plan for human review only; it cannot independently produce a verified key.

## Phase Four: Project Without `.specify/`

Outside a project, the current CLI cannot reliably provide a machine-readable integration registry. V1 permits only the user, host, or current Agent to explicitly provide an exact integration key. A human may inspect `specify check`, CLI help, and registry material before entering the key, but the manager does not parse this human output or run interactive init instead of a key declaration.

When only a product name, Reference, web page, or catalog text is available without an exact key, return `KEY_REQUIRED`. The Manager must not infer a key from documents or web pages.

Do not initialize a real project to query a catalog.

Do not execute:

```bash
specify init --here --non-interactive
```

because the current CLI defaults to Copilot.

The approved initialization plan must execute:

```bash
specify init --here --non-interactive --integration <explicitly-approved-key>
```

For a non-empty brownfield project, controlled `--force` initialization is the only external force branch permitted by V1. Before execution:

1. Confirm the actual project root.
2. Check Git status.
3. Protect existing uncommitted work.
4. Generate rehearsal candidate paths, the minimum allowed prefixes for external mutation, and a risk list.
5. For all existing files under each allowed prefix, create a path inventory, byte-level backup, mode, and SHA-256 at `.spec-kit-governance/backups/<plan-id>/`.
6. Add the root `.spec-kit-governance/` to the managed rules in the project's `.gitignore`.
7. Obtain the current user's explicit authorization for the exact `plan_id` and complete command.
8. Only then execute `specify init --here --force --non-interactive --integration <explicitly-approved-key>`.
9. If init fails, inspect partial artifacts and restore from the file-level backups in the plan; do not reset, stash, checkout, or delete files not in the plan.

`plan-init` must run one rehearsal outside the real project, in a temporary directory, using the same CLI version, integration key, and init argv. The rehearsal is only for obtaining candidate generated paths, file types, and content hashes; it must not be used to query current Agent identity. The Manager must merge rehearsal results item by item with existing paths in the real project and generate candidate create/modify/conflict lists and minimum allowed prefixes; a rehearsal must not disguise external mutation as exact manager file mutation.

Before `apply-plan` executes init, it must save the complete path inventory of the real project and the original bytes and hashes of every expected modify target. After execution it must compare the actual additions and modifications:

- When the actual set is within allowed prefixes and satisfies postconditions, save the exact changed-file inventory and continue status, managed-file, and capability verification.
- If a modification is outside a prefix or a postcondition is not satisfied, immediately enter failure recovery. Restore all old files in the scope snapshot; only files proved by the pre-apply inventory to have been absent, newly created by this init, and within allowed prefixes may be deleted.
- Files whose provenance or safe recovery cannot be proved must not be deleted; return `RECOVERY_REQUIRED`, list the exact paths, and block completion.

# On-Demand Onboarding Protocol

The project does not pre-onboard every Agent. Perform an on-demand binding only when a new Agent actually enters the project for the first time.

## Native Integration Already Installed

1. Run `specify integration status --json`.
2. Use the status JSON to verify that the corresponding manifest was checked.
3. Verify that missing, modified, and invalid managed files are all empty. If repair of native managed files for the current runtime fails because of unwritability, permissions, or sandbox, return `NATIVE_INSTALL_BLOCKED`; return `STATE_BROKEN` only for other damage unrelated to the current binding.
4. Check `ADAPTERS.json`.
5. If the adapter is active, use it directly.
6. If the adapter does not exist, enter the context-anchor onboarding flow.
7. Do not change the default integration.

## Native Integration Not Yet Installed

1. Obtain the integration key from an explicit declaration by the user, host, or current Agent.
2. Compute `desired_installed_set = existing_installed_set - explicitly_planned_removals + candidate`.
3. Check the manifest health of every installed integration. If no stable JSON source exists for the uninstalled candidate's multi-install-safe metadata, the plan field must contain `candidate_multi_install_safety = "deferred_to_cli"`; do not infer safety from Rich text.
4. Generate an installation operation plan without `--force`, leaving the CLI's built-in safety gate to decide whether the candidate can coexist.
5. Require current-user authorization for the exact `plan_id`. Project configuration must not bypass this requirement.
6. Execute:

   ```bash
   specify integration install <key>
   ```

7. Do not add `--force`.
8. Run again:

   ```bash
   specify integration status --json
   ```

9. After healthy status, the state is `NATIVE_CANDIDATE_INSTALLED_UNVERIFIED`; enter context-anchor and fresh-session runtime-to-key verification. Do not return `EXACT_NATIVE_INSTALLED` early.
10. If the CLI rejects it for multi-install safety, return `INTEGRATION_CONFLICT`. If installation fails because the target is unwritable, permissions, sandbox, or another error, return `NATIVE_INSTALL_BLOCKED`; do not generate a generic plan or substitute another Agent key.
11. Commit the new integration artifacts and adapter together.

## Unsafe Multi-Install

Do not install automatically.

V1 permits only the following choices:

1. Keep the current integration.
2. Generate a separate replacement plan authorized by the current user. The plan must list the exact uninstall or switch argv actually supported by the CLI, every integration artifact expected to be deleted, the corresponding capability `REPLACE` record, recovery steps, and the expected final installed set; do not generate it if any item is missing.
3. Stop and wait for a safe native integration.

V1 does not support an unsafe multi-install exception and does not generate `integration install --force`. Do not assume `switch` automatically clears all other non-default integrations; the operation plan must list the expected final set and verify it with status JSON after apply.

# Default Integration Handling

The project may have only one default integration.

The governance manager must not treat the default integration as the current Agent identity or switch it automatically whenever a collaborator enters the project.

The project `PROJECT_CONFIG.json` must record `default_integration.policy = "pinned"`, the current actual key, and `allow_change = false`.

If the current Agent's integration is installed but is not the default:

- Installed core Spec Kit Skills or Commands verified by status are available capabilities.
- The project governance package and adapter are unaffected.
- The completeness of extensions, presets, events, and shared templates must be verified separately.
- The state is `READY_WITH_LIMITATIONS` until verified.
- Do not claim complete feature parity.

If the team needs to change the project default integration:

1. Through a separate PR, first change only `PROJECT_CONFIG.json.default_integration.allow_change` from `false` to `true` and record the target key; this PR does not execute CLI mutation.
2. `plan-default-change` may be generated only when `allow_change == true`; otherwise return `DEFAULT_CHANGE_FORBIDDEN`.
3. Verify that the target key is installed and the manifest is healthy, and record the old default, `.specify/integration.json`, init options, shared infrastructure, extensions, presets, events, and an inventory of all installed integrations.
4. The plan first executes `specify integration use <target-key>` and immediately verifies with `specify integration status --json` that the actual default changed.
5. Only after step 4 succeeds may the manager atomically update `PROJECT_CONFIG.json.default_integration.key` and the relevant adapter capability, and restore `allow_change` to `false` in the same apply.
6. Reverify shared infrastructure, extensions, presets, events, and every installed integration. Events are an independent capability; do not claim that `integration use` automatically migrates events.
7. If any verification or file update after step 4 fails, restore project files and execute `specify integration use <old-key>`; verify status again. Recovery failure returns `RECOVERY_REQUIRED`.

# Context Anchor Resolution Protocol

The project governance package is not automatically read by every Agent.

Context-anchor resolution priority:

1. The active binding for that runtime ID in `ADAPTERS.json`.
2. The path explicitly provided by the user in `plan-onboard --context-anchor <project-relative-path>`.
3. If neither exists, return `CONTEXT_ANCHOR_UNKNOWN`.

V1 does not carry or automatically resolve `context-anchor-hints.json`, read `agent-context` defaults to write files automatically, infer a rules file from Skills or Commands directories, or automatically choose a path from official documentation. The implementing Agent may show these materials to the user for human judgment, but only a project-relative path supplied by the user may enter an operation plan.

The context-anchor path must:

- Be project-relative.
- Contain no `..`.
- Not be absolute.
- Not escape the project root through a symlink.
- Be a plain-text file or a safe target that does not yet exist.
- Match the current Agent's official or verified behavior.

The onboarding plan must perform a write preflight for the anchor and its parent directory and include `anchor_compatibility_evidence`. Evidence may be only a project-relative immutable file or an immutable official URL with a content hash. If evidence is missing, return `CONTEXT_ANCHOR_UNKNOWN`; if the format is unsupported, return `ANCHOR_FORMAT_UNSUPPORTED`; if the anchor required by a native Agent fails because of unwritability, permissions, or sandbox, return `NATIVE_INSTALL_BLOCKED` and do not fall back to Materialized, generic, or another path.

The V1 renderer supports only ordinary UTF-8 Markdown or plain-text anchors. JSON, YAML, TOML, databases, or proprietary rules containers return `ANCHOR_FORMAT_UNSUPPORTED`; do not write Markdown markers into them.

# Loader and Materialized Delivery Modes

## Loader Mode

In V1, `PROJECT_CONFIG.json.context.default_delivery_mode` is fixed to `loader`. An ordinary onboarding plan may generate only Loader.

Only a short managed block is written into the context anchor:

```markdown
<!-- PROJECT SPEC-KIT GOVERNANCE START -->

This repository uses the committed project-local Spec Kit governance package.

Before substantive engineering work, read in order:

1. `docs/spec-kit/START_HERE.md`
2. `docs/spec-kit/POLICY.md`
3. `docs/spec-kit/LOCAL_OVERRIDES.md`
4. `docs/spec-kit/REFERENCE.md` when operational details are uncertain
5. `docs/spec-kit/OPERATING_PROTOCOL.md` before initialization, onboarding, upgrade, or recovery

The committed project package is the team baseline. Do not replace it with
personal global rules or a machine-local Reference. Do not infer the current
Agent from the project's default integration.

<!-- PROJECT SPEC-KIT GOVERNANCE END -->
```

It must be verified that the Agent will:

1. Read the context anchor.
2. Continue reading the project governance files as required by Loader.
3. Follow the Policy.

Only after verification passes may the adapter be marked `active`.

## Materialized Mode

Materialized may be explicitly requested only through `plan-onboard --delivery-mode materialized --loader-failure-evidence <project-relative-evidence>`. The evidence must come from a fresh-session Loader test that follows the real Agent verification protocol but failed to read `POLICY.md`. Without this evidence, the manager must reject the Materialized plan.

The managed block must contain:

1. Loader.
2. A complete copy of `POLICY.md`.
3. A copy of `LOCAL_OVERRIDES.md`.
4. Policy version.
5. Policy SHA-256.
6. Generator version.

Even in Materialized mode, `POLICY.md` remains the sole logical source. Complete text in any Agent-specific file may be generated only by the renderer and must not be maintained independently by hand.

After `POLICY.md` or `LOCAL_OVERRIDES.md` changes, every Materialized anchor must be marked stale and rendered again; a Loader anchor is updated only when the Loader protocol itself changes.

# Role of Root `AGENTS.md`

The governance package must maintain a minimal Loader in the root `AGENTS.md` as a general best-effort entry point.

However, the following must be explicit:

- It is not a universal file read by every Agent.
- It cannot replace the actual Agent's native context anchor.
- It does not mean that the project supports only Codex.
- It is merely an open, discoverable project-level Bootstrap.

If the project already has an `AGENTS.md`, modify only the content inside the governance markers; project rules outside the markers must be preserved verbatim.

# Handling Unsupported Agents

## Exclude Name Misclassification

Fuzzy matching must not be used to select a product automatically.

For example:

- Trae currently has a native `trae` integration.
- CodeBuddy currently has a native `codebuddy` integration.
- WorkBuddy must not be mapped automatically to CodeBuddy merely because their names are similar.

## No Native Integration

The following must be output:

```text
The current CLI does not provide a verified native integration for this Agent.

Please provide:
1. Product name and version;
2. The project rules file it reads;
3. The Commands or Skills directory it reads;
4. Supported file formats;
5. Command invocation syntax;
6. Parameter placeholder conventions.
```

After outputting this information, the Resolver must stop and must not choose a subsequent branch itself. It may enter one of the following independent branches corresponding to the request only after the user makes a new explicit request.

## Native Adapter Path

For this case, the Resolver returns only `UNSUPPORTED_INCOMPATIBLE` and the required-information checklist; it must not run the scaffold automatically. The following independent work may be performed only after the user separately and explicitly requests an engineering task to “develop a native integration for this Agent”:

1. Develop a genuine Spec Kit integration for the product.
2. Use the integration scaffold supported by the current CLI as the development starting point.
3. Implement the correct Skills or Commands format, directory, invocation semantics, event configuration, and tests.
4. Enter the reviewed release process.
5. Install it using a CLI version that includes the integration.
6. Re-run project onboarding.

Entries discovered in the current catalog are not necessarily directly installable. The implementation must not assume that a community integration can already be installed by the current CLI.

## Explicit Generic Transition

`PROJECT_CONFIG.json.generic.policy` defaults to `deny`. A generic plan may be generated only when that value has already been changed to `explicit-approval-required` through an independent project change and all of the following conditions have been verified:

1. A `native_absence_attestation` exists for the current runtime ID and exact CLI version; the manager must not claim on its own that no native integration exists.
2. The target Agent supports Markdown command files in the project.
3. The exact Commands directory is known.
4. The parameter placeholders and invocation semantics are known to be compatible.
5. The target directory is inside the project.
6. The current user approves the exact `plan_id`.
7. The manifest explicitly records that this is not natively supported.
8. Multi-install conflicts have been handled.

`native_absence_attestation` must be written to the operation plan with the following fixed structure:

```json
{
  "runtime_id": "vendor.product",
  "specify_version": "<exact-observed-version>",
  "catalog_evidence": "docs/spec-kit/evidence/<immutable-evidence-file>",
  "catalog_evidence_sha256": "<sha256>",
  "reviewed_at": "<RFC3339>",
  "reviewed_by_current_operator": true,
  "conclusion": "no-native-integration-found-for-runtime"
}
```

The evidence file must preserve the current-version `specify check`, applicable human output from `integration list/search/info` or immutable official registry evidence, and an explanation of how a person reached the conclusion from the runtime ID. The attestation is valid only for exactly matching `runtime_id` and `specify_version`; it must be reviewed again when the CLI version changes. Return `UNSUPPORTED_INCOMPATIBLE` when there is no attestation, the evidence hash does not match, or the conclusion is not unique.

Example:

```bash
specify integration install generic \
  --integration-options="--commands-dir .example-agent/commands"
```

Do not add `--force`.

V1 permits at most one generic binding per project, and a generic transition may run only when the installed integration set is empty. If any integration is already installed in the project, return `INTEGRATION_CONFLICT` and stop; V1 does not implement branches for migration, uninstall, switch, or replacement with generic. Do not delete the manifest or artifacts directly to manufacture an empty set.

A generic binding always uses `integration_mode = "explicit-generic-transition"` and must never be marked native. Until all declared capabilities have completed fresh-session verification, it may only be `READY_WITH_LIMITATIONS`.

The project `POLICY.md` must contain the following fixed paragraph:

> When the current CLI provides a native integration for an Agent, the native integration must be used; do not downgrade to generic because of permissions, an unwritable path, convenience, or conflict avoidance. Generic may be used only with explicit user or project-policy approval when the current CLI has no native integration and the target Agent has been verified compatible with the generic Commands directory, Markdown format, parameters, and invocation semantics. Stop when verification is impossible.

Persist the generic transition only in the corresponding binding's `generic_transition` field in `ADAPTERS.json`; `MANIFEST.json` does not carry project-specific generic decisions. The structure is fixed as follows:

```json
{
  "native_absence_attestation_sha256": "<sha256>",
  "native_absence_evidence": "docs/spec-kit/evidence/<immutable-evidence-file>",
  "attested_specify_version": "<exact-version>",
  "native_integration_available_at_approval": false,
  "limitations_acknowledged": true,
  "commands_dir": ".example-agent/commands",
  "format": "markdown",
  "compatibility_verified": true
}
```

The binding with `integration_mode = "explicit-generic-transition"` must contain this object; a native binding must not contain it. The evidence path and hash in the binding must exactly match the operation-plan attestation. When the CLI version changes, mark the binding stale; do not promote it to `READY` before a new attestation.

# Handling a Missing CLI

Run first:

```bash
specify version
```

When it is missing:

1. The project Policy and Reference may still be read.
2. Do not claim that a native integration has been verified.
3. Do not install silently.
4. Read `approved_install_ref` from `MANIFEST.json`.
5. Output installation advice.
6. Wait for user authorization.
7. After installation, run `specify version` and the compatibility checks again.

V1 permits only the 40-character Git commit SHA pinned by the manifest:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@<40-character-approved-commit-sha>
```

Do not put Markdown link syntax in executable commands.

Do not use an unpinned Git `main`, a tag, automatic PyPI selection, or a second installation source. If other sources must be supported in the future, add an `install_source.type` schema, bump the package version, and add compatibility and upgrade tests; the implementation Agent must not choose one independently in V1.

# Project Governance Manager Command Contract

Implement core logic with the Python standard library. POSIX shell and PowerShell may serve only as thin wrappers.

The Manager must implement, and may use only, the following public subcommand names:

```text
governance.py doctor
governance.py resolve-agent
governance.py plan-governance-bootstrap
governance.py plan-init
governance.py plan-onboard
governance.py plan-extension-install
governance.py plan-default-change
governance.py apply-plan
governance.py render
governance.py verify
governance.py check-update
governance.py plan-upgrade
governance.py plan-rollback
governance.py plan-activate-binding
```

`apply-plan` is the sole entry point for all mutations. Do not implement `apply-upgrade`, `apply-rollback`, or direct-write commands that bypass the operation plan.

Before the first installation, the same-version `governance.py` in the artifact staging directory is the only permitted temporary entry point; it must follow the same schema, plan/apply, backup, and verification protocols. After the first apply succeeds, `tools/spec-kit-governance/governance.py` inside the project becomes the subsequent entry point.

## `plan-governance-bootstrap`

This command installs only the Agent-neutral project governance package: `docs/spec-kit/`, the root `AGENTS.md` Loader, project config, manifest, and project manager. It must not install an Agent integration, create an Agent binding, or require the current Agent to have a native integration.

When `.specify/` already exists, read the real default key into `PROJECT_CONFIG.json`. When `.specify/` does not exist, retain `default_integration.key = null` and mark the project state `pre-init-governance`; when `plan-init` subsequently succeeds, the actual default key must be filled in during the same apply. `verify` rejects null only when `.specify/` already exists.

## `plan-extension-install`

This command is available only after the project has a healthy `.specify/`. It must write `specify extension add <verified-staged-extension-directory>` into the plan as an external CLI mutation, declaring the minimum permitted write path prefixes, the pre-execution scope snapshot, postconditions, and the recovery protocol. Do not install an extension without authorization for the exact plan.

## `doctor`

Read-only checks:

- Project root.
- Git status.
- Governance-package paths.
- Schema.
- Hashes.
- `.specify/`.
- CLI version.
- Integration status.
- Adapter markers.
- Symlink and path risks.
- Leakage of personal absolute paths.

## `resolve-agent`

Inputs:

```text
--runtime-id
--display-name
--integration-key
--json
```

The runtime ID is required. An integration key is also required when generating a mutation plan; when only a display name is supplied, return `KEY_REQUIRED`.

This command outputs only the resolution result and does not write to the project.

## Operation Plan Contract

Every plan subcommand must generate immutable canonical JSON conforming to `operation-plan.schema.json`, with these fixed fields:

- `schema_version`
- `plan_id`
- `operation_type`
- `created_at`
- `expires_at`, fixed at 30 minutes after creation
- `project_root_fingerprint`
- `git_head`
- `git_status_porcelain_sha256`
- `manifest_sha256`
- `project_config_sha256`
- `adapters_sha256`
- `local_overrides_sha256`
- `integration_status_sha256`
- `specify_version`
- Relative path and SHA-256 for each input file
- Current Agent runtime ID and declaration source
- `claimed_integration_key`
- `required_native_key`, which must equal the claimed key during native onboarding
- `native_fallback_prohibited`, fixed to `true` during native onboarding
- `native_target_paths` and per-item `write_preflight`
- `on_native_write_failure`, fixed to `NATIVE_INSTALL_BLOCKED`
- A context anchor, when required by the operation
- `anchor_compatibility_evidence`, containing a project-relative evidence file or immutable official URL, content hash, and review conclusion
- `manager_file_mutations`
- `external_cli_mutations`
- Whether the default integration changes
- Whether network access is required
- Required user-authorization text
- Risks and recovery steps
- `plan_sha256`

Each item in `manager_file_mutations` must contain an action, exact project-relative path, old hash, expected new hash, mode, and rollback bytes reference. Because the Manager generates the content itself, this type of mutation must not use a path prefix in place of an exact path.

`external_cli_mutations` is used for CLI operations without a stable dry-run, such as `specify init`, `integration install/use/switch`, and `extension add`. Each item must contain:

- Exact argv array; shell strings must not be stored.
- Exact working directory.
- CLI version.
- The minimum set of `allowed_path_prefixes`.
- The full path, file type, mode, and content-hash snapshot before execution for each allowed prefix.
- Expected status postconditions and managed-file postconditions.
- The exact path of the changed-file inventory generated after execution.
- Failure-recovery protocol.

An external mutation need not fabricate expected hashes for every new file before execution. It must fully back up every existing file within the allowed scope and record files created during execution. If actual changes escape the allowed prefixes after execution, stop immediately and recover from the journal; return `RECOVERY_REQUIRED` when safe recovery is impossible.

The fixed `plan_sha256` algorithm is: first remove the top-level `plan_sha256` field, encode the remaining object as UTF-8 JSON with keys sorted in ascending Unicode code-point order, fixed `,` and `:` separators, no extra whitespace, and NaN and Infinity forbidden, then calculate SHA-256. After writing back `plan_sha256`, do not include that field in its own hash again.

Plan files are always written to `.spec-kit-governance/plans/<plan-id>.json`. File-level backups are always written to `.spec-kit-governance/backups/<plan-id>/`. State directories must not be committed to Git and must not be placed in `.specify/`, to avoid fabricating Spec Kit project state before init.

V1 does not implement automatic cleanup. Plans, changed-file inventories, merge material, backups, staging journals, and failure evidence are retained permanently until the user explicitly cleans them by plan ID in an independent maintenance task. The Manager does not provide `clean-runtime-artifacts` and must not silently delete by age. All logs and plans must pass this document's sensitive-information filter before being written.

## `apply-plan`

The invocation syntax is fixed:

```bash
python3 tools/spec-kit-governance/governance.py apply-plan \
  --plan .spec-kit-governance/plans/<plan-id>.json \
  --approve-plan-id <plan-id> \
  --approve-plan-sha256 <plan-sha256>
```

On Windows, use `python` or `py -3` with the same argv. Approval parameters prove only that the operator explicitly confirmed this exact plan; they are not OS identity authentication, and documentation must not claim to verify a natural person's identity.

Re-verify before execution:

- The project root has not changed.
- Input-file hashes have not changed.
- Git status has no changes beyond those in the plan.
- The CLI version remains compatible.
- Integration status has not changed.
- The operation plan has not expired.
- The two approval parameters supplied by the caller exactly match the plan.
- `plan_id`, canonical JSON hash, and the current user's approval value exactly match.
- The mutation target set exactly matches the plan.

Stop on any mismatch.

## `render`

Process only anchors in `ADAPTERS.json.anchors` with `managed = true` and status `rendered` or `stale`. An explicit onboarding plan may have 0 marker pairs before writing and must have exactly 1 pair afterward; render, upgrade, and rollback must each have exactly 1 pair before and after writing. More than 1 pair before writing always blocks; upgrade must not treat a missing marker as onboarding and repair it automatically.

## `verify`

It must check every file in `MANIFEST.json.content_sha256`, `PROJECT_CONFIG.json`, `LOCAL_OVERRIDES.md`, `ADAPTERS.json`, integration status, hashes, path safety, the capability baseline, and capability declarations.

## Updates and Rollbacks

Updates and rollbacks must strictly use the corresponding plan subcommand and the sole `apply-plan` two-stage process.

# Standard Resolution JSON

Example:

```json
{
  "schema_version": 1,
  "status": "NATIVE_CANDIDATE_NOT_INSTALLED",
  "project_root": "<validated-project-root>",
  "identity": {
    "runtime_id": "vendor.product",
    "display_name": "Product Name",
    "source": "runtime-declared"
  },
  "integration": {
    "key": "product-key",
    "mode": "native",
    "installed": false,
    "default": false,
    "multi_install_safe": true
  },
  "context": {
    "anchor": null,
    "anchor_source": null
  },
  "required_action": "provide-context-anchor-and-approve-onboarding-plan",
  "warnings": ["CONTEXT_ANCHOR_UNKNOWN"],
  "next_safe_step": "Provide an exact project-relative context anchor, then run plan-onboard"
}
```

Do not write the following content to diagnostic JSON or logs:

- Tokens.
- The complete environment-variable list.
- The user's home directory.
- Private URL queries.
- Secrets.
- Absolute paths unrelated to the diagnosis.

# Extension, Release Archive, and Portable Manager

V1 must build both deterministic release artifacts; it must not choose between them:

1. `speckit-governance-<version>-portable.zip`: contains the project governance-package template, schema, portable manager, bootstrap updater, LICENSE, manifest, and checksum.
2. `speckit-governance-<version>-extension.zip`: contains same-version extension source, payload, provenance, and bootstrap entry conforming to the currently verified Spec Kit extension directory format. Before installation, it must be extracted into a verified staging directory and that directory passed to the current CLI; do not assume that the CLI can install a ZIP file directly.

V1 does not implement a Spec Kit bundle and does not make bundle build or bundle install a release, installation, or acceptance condition. A future bundle must be added as an independent compatibility feature and must not replace the portable ZIP, extension archive, or in-project manager.

## Fixed Responsibilities

- `governance.py` is the sole managed write logic. The first bootstrap uses the same file in artifact staging; after success, use `tools/spec-kit-governance/governance.py` in the project.
- The extension source does not directly rewrite governance files; however, `specify extension add` is an external CLI mutation and must go through `plan-extension-install`; it must not be called read-only delivery.
- The extension bootstrap is fixed at `scripts/python/bootstrap_governance.py`. It may only verify the artifact, call the portable manager to generate a plan, and show the plan to the user; it must not bypass `apply-plan`.
- Adapter materialization must be performed by the in-project portable manager.
- A non-default Agent must not be switched to the project default merely to read the governance package.
- The governance extension must not copy, rewrite, or fabricate Spec Kit native Skills, Commands, events, presets, or shared infrastructure.
- Successful extension installation does not mean successful project governance-package installation; bootstrap plan, `apply-plan`, `verify`, and capability-conservation acceptance must still be completed.

## Fixed First Bootstrap Order

1. Obtain the portable ZIP from an approved immutable source and verify the release manifest and SHA-256.
2. Extract it to `.spec-kit-governance/staging/<plan-id>/artifact/`; do not touch governance target files or `.specify/` in this step.
3. Run the verified `governance.py plan-governance-bootstrap` from staging.
4. After the user authorizes with the fixed approval parameters, run the same `governance.py apply-plan` from staging.
5. After success, run the in-project `governance.py verify`. This proves only that the Agent-neutral governance package is installed; it does not prove onboarding of any Agent.
6. When the current Agent needs to perform project engineering work, separately run dynamic identity resolution and `plan-onboard`. If native integration or anchor writing fails, enter `NATIVE_INSTALL_BLOCKED`, while the already committed shared governance package remains readable.

## Fixed Extension Installation Order

1. The project must already have a healthy `.specify/` and an installed governance package.
2. Obtain the extension ZIP, verify the release manifest and SHA-256, and extract it to `.spec-kit-governance/staging/<plan-id>/extension/`.
3. Verify that the extension source's `extension.yml`, payload version, and content hash match the portable release.
4. Run `plan-extension-install`, writing `specify extension add <staged-extension-directory>` and its external-mutation scope into the plan.
5. Run `apply-plan` after the user authorizes the exact plan.
6. Verify integration status, extension lifecycle, default-sensitive artifacts, and capability inventory.

The project must not install an extension automatically merely because of the first bootstrap. Generate `plan-extension-install` only when the user explicitly requests extension capabilities or submitted project rules require that extension; this user choice does not change the implementation architecture.

## Manager Self-Update

The running `governance.py` must not overwrite itself. An upgrade artifact must include a separate `bootstrap_updater.py`; the upgrade plan always writes the new manager and all managed files to `.spec-kit-governance/staging/<plan-id>/`. The updater file must be outside the replacement set; on Windows, the old manager must exit before the updater starts.

Multi-file upgrades are not one atomic transaction and must implement a recoverable journal:

1. After staging is complete, verify all new-file hashes, schema, and compatibility once.
2. For each target, record old existence, bytes, mode, hash, and backup path.
3. In canonical path order, perform a same-directory temporary-file plus atomic replace for each file, fsyncing the journal after every step.
4. After all replacements, run the new manager's post-verify.
5. If any step fails, recover in reverse journal order and re-read to verify old hashes.
6. Return the old-version healthy state only after all recovery succeeds; on recovery failure return `RECOVERY_REQUIRED`, retain staging, backup, and journal, and do not continue running mutations.

The updater executes only operation plans generated and verified by the old manager and reuses the same replacement-primitive module from the release; it must not have different path, hash, backup, or recovery algorithms.

## `agent-context` Boundary

An existing healthy `agent-context` extension may continue maintaining its own current-plan prompt. The governance system must not automatically install, delete, upgrade, or reconfigure it; must not treat its generated short prompt as the complete Policy; and must not reuse its markers. Before and after an upgrade, verify that its existing registration state and managed artifacts have not changed outside the plan.

# Release and Upgrade Strategy

Use SemVer for versions:

- `NONE`: Do not release a project governance-package version; update only the central review record and baseline.
- `REFERENCE`: bump patch.
- Backward-compatible `POLICY`: bump minor.
- Any incompatibility in fixed paths, schema, Manager commands or parameters, operation-plan contract, adapter schema, marker contract, or hash contract: bump major and provide a migrator and rollback tests.

The central release must contain:

- Immutable release tag.
- Complete source commit.
- Reviewed upstream commit.
- Portable ZIP.
- Extension archive.
- SHA-256 for both artifacts.
- Manifest.
- Changelog.
- Compatibility.
- Migration note.
- Rollback version.

Both ZIPs must be built by `scripts/build_governance_release.py` using the Python standard-library `zipfile`. Sort input paths in ascending UTF-8 code-point order; do not write explicit directory entries; fix timestamps to `(1980, 1, 1, 0, 0, 0)`; fix ordinary-file Unix mode to `0644` and declared-executable Python or shell entry points to `0755`; set `create_system = 3`; fix compression to `ZIP_DEFLATED` with `compresslevel = 9`; do not write host extended attributes, Finder, NTFS, xattr, or absolute paths. Two consecutive builds from the same Git revision must be byte-identical or the release fails.

The Extension ZIP is not a direct installation input. The compatibility manifest must record the fixed `extension_install_argv = ["specify", "extension", "add", "<verified-staged-extension-directory>"]`. The release test must extract the artifact and use the current tested CLI in an isolated Spec Kit project to actually execute the installation plan against that directory. If the current CLI does not accept that directory format, do not release the extension artifact and do not claim compatibility merely because ZIP construction succeeded.

Project upgrade process:

1. Run `governance.py verify`.
2. Run `governance.py check-update`.
3. Check the immutable version and checksum.
4. Create a separate upgrade branch and PR; do not upgrade the default-branch workspace directly.
5. Run `plan-upgrade`.
6. Review the Policy, Reference, manager, adapter, and manifest diff.
7. Resolve three-way conflicts.
8. Obtain human approval.
9. After the user authorizes the exact `plan_id`, run `apply-plan`.
10. Run `verify` again.
11. Run `specify integration status --json`.
12. Run project-relevant tests.
13. After merge, the new version becomes the team's shared baseline.

Save a capability inventory separately before and after the upgrade, and compare integrations, default key, extensions, presets, events, shared infrastructure, constitution, specs, Skills, Commands, adapters, and governance files item by item. Except for changes explicitly listed in the upgrade plan and approved by the user, the two inventories must be equivalent. If there is any additional deletion, downgrade, invalidation, or default change, the upgrade fails and rolls back.

The central locator may only report updates and must not apply them automatically.

`check-update` accepts only an explicit `--source <absolute-SpecKitReference-root>` and does not scan the environment or disk. The calling Agent may read the locator from its loaded personal global Bootstrap and pass it explicitly; without a source, report only “central update source not configured.” The sole index path is fixed at `<source>/governance/release/latest.json`; its schema must contain version, immutable source commit, relative portable-artifact path and SHA-256, relative extension-artifact path and SHA-256, compatibility, and reviewed upstream commit.

The Manager must verify that the source is a Git checkout, HEAD equals the index's source commit, the worktree is clean for the index and both artifacts, and artifact hashes match. If any condition fails, return `CENTRAL_SOURCE_UNVERIFIED`, show diagnostics only, and do not generate an upgrade plan. Version selection uses only the unique release in the index; do not scan tags, select a `latest` directory, or read uncommitted worktree templates.

# Write and Conflict Protection

All writes must satisfy the following requirements:

1. The target is inside the verified project root.
2. Reject absolute-path escapes.
3. Reject `..`.
4. Reject symlink escapes.
5. Reject writes to directories or non-regular files.
6. An explicit onboarding write may have 0 marker pairs before the write and must have 1 pair afterward; render, upgrade, and rollback must have 1 pair both before and after the write; stop before any write if more than 1 pair exists.
7. Markers must not be nested, reversed, or duplicated.
8. The old hash inside the markers must match the manifest.
9. Preserve content outside the markers exactly.
10. Never overwrite `LOCAL_OVERRIDES.md`.
11. When Policy or Reference has been modified locally, generate the fixed per-file `base/`, `local/`, and `target/` materials plus `MERGE_INSTRUCTIONS.md` under `.spec-kit-governance/plans/<plan-id>/merge/`, then stop; the manager must not automatically choose either side of the conflict.
12. Use a temporary file in the same directory and an atomic rename.
13. Leave the original file unchanged after failure.
14. Repeated apply operations must be idempotent.
15. The manager must not provide a general-purpose `--force`. Only `plan-init` that passes every prerequisite gate in the "Dynamic Integration Resolution Algorithm" may place `specify init --here --force` in argv; schema validation must fail if `--force` appears in any other operation.
16. Do not execute arbitrary shell strings provided by project files.
17. Do not automatically install unknown catalog content.
18. Do not automatically write user-global configuration.
19. Do not automatically modify Git remotes.
20. Do not automatically commit or push.

# Cross-Platform Requirements

The core logic must have exactly one implementation and use only the Python 3 standard library. POSIX shell, PowerShell, batch, or Agent command files may only locate the Python interpreter and forward the original argv; they must not duplicate parsing, write, hash, plan, or upgrade logic.

The following must be supported:

| Platform or environment | Entry point or behavior |
|---|---|
| macOS | `python3` |
| Linux | `python3` |
| Windows | `python`, then try `py -3` after failure |
| No network | Use the committed governance package; online updates are prohibited |
| No `uv` | Output installation guidance only |
| No `specify` | Output installation guidance only |
| Old CLI | Output a compatibility error; do not upgrade automatically |
| CLI version is higher than `tested_version`, or a non-null upper bound exists and the version is greater than or equal to `maximum_version_exclusive` | Allow Policy and Reference reads and purely read-only diagnostics; reject generation or application of mutation plans and return `CLI_VERSION_UNTESTED` |
| CLI version does not conform to the restricted V1 grammar | Allow Policy and Reference reads only; return `CLI_VERSION_UNPARSEABLE` |

The implementation must not depend on:

- GNU-specific commands.
- macOS-specific arguments.
- Shell `eval`.
- Logic supported only by Bash as the sole implementation.
- Commands assembled by concatenating unescaped user input.
- Any particular Agent product directory as universal truth.

The rules in the repository's `.gitattributes` must be preserved:

```gitattributes
* text=auto eol=lf
*.bat text eol=crlf
*.cmd text eol=crlf
```

# Test Requirements

## Unit Tests

At minimum, cover:

1. Missing fields in each of the manifest, project config, adapter, capability baseline, and operation plan.
2. Unknown schema versions and unknown enum values.
3. Invalid SemVer, 40-character Git SHA, and SHA-256 values.
4. LF and CRLF hash normalization.
5. Exact identity match, unknown identity, conflicting identity, and display name only.
6. Similar names belonging to different products.
7. Missing, outdated, above-tested-limit, and invalid-output CLI cases.
8. Integration status error.
9. Native integration installed.
10. Native integration not installed.
11. A native integration exists but its target Skills or Commands directory is not writable; the result must be `NATIVE_INSTALL_BLOCKED`, and the plan must not contain generic, another key, or a completion status.
12. After permissions are repaired, only the original integration key may continue, and the previously failed plan must not be reused.
13. Generic compatible, incompatible, and configuration-default rejection cases.
14. When the current CLI has a native integration, generic must be rejected even if generic is compatible.
15. Multi-install unsafe.
16. Missing, duplicate, nested, reversed, and manually modified markers.
17. Symlink escape and path traversal.
18. Read-only files and atomic-write failure.
19. Idempotent repeated apply.
20. Preservation of `LOCAL_OVERRIDES.md`.
21. Checksum mismatch.
22. An expired plan, or changes to Git, input hashes, CLI, or integration status after plan generation.
23. The default integration incorrectly treated as the current Agent.
24. Multiple Agent CLIs simultaneously present on PATH.
25. A catalog result exists but is not installable by the current CLI registry.
26. No network, but a built-in integration can be confirmed.
27. Reject Materialized when Loader failure evidence is absent.
28. Reject an attempt by the running manager to overwrite itself.
29. Release failure when a Capability record lacks disposition, target, or test.
30. Upgrade failure when capability inventory contains an unplanned deletion, degradation, invalidation, or default change.
31. Backup, authorization, and rollback for controlled brownfield init; schema failure when `--force` appears in a non-init operation.
32. Global-template markers, unique placeholder, manual rendering, and byte-for-byte preservation outside the markers.
33. Return `NATIVE_INSTALL_BLOCKED` when the native init target is not writable, without generating generic or another key.
34. Return `NATIVE_INSTALL_BLOCKED` when a user-provided native context anchor or its parent directory is not writable.
35. When native install leaves partial artifacts but status is unhealthy, do not return `READY` or create an active binding.
36. `claimed_key = "generic"` must enter the generic validator and must not enter a `NATIVE_*` branch.
37. Block when generic attestation is missing, the CLI version changes, or the evidence hash does not match.
38. Byte-for-byte candidate results for a global target that is absent, empty, lacks a final newline, uses LF, uses CRLF, has a valid older SemVer marker, or has an END marker without a final newline.
39. Stop with zero overwrites for every case in which the global source is not the template in the supplied directory itself, has malformed markers, has duplicate placeholders, has a BOM, is not UTF-8, is missing the source file, or encounters a competing target creation.
40. Hard-link no-clobber publication for an absent global target, blocking on unsupported filesystems, and crash-journal recovery for both `prepared` and `published` phases.

## CLI Integration Tests

All tests must run in separate temporary Git repositories:

1. A new project without `.specify/`.
2. An existing healthy `.specify/`.
3. Native installed and default.
4. Native installed but not default.
5. Native not installed and safe to coexist.
6. Native not installed and unsafe to coexist.
7. A Skills-based integration.
8. A Markdown Commands-based integration.
9. An integration whose Commands or Skills artifacts use TOML/YAML but whose evidence-verified context anchor is Markdown or plain text; a fixture that has only a TOML/YAML rules container and no supported anchor must return `ANCHOR_FORMAT_UNSUPPORTED` and must not become active.
10. Use the `skills_integration_key` explicitly supplied at test runtime. Test pre-validation must prove that the key uses Skills, differs from `primary_integration_key`, and is multi-install-safe; the test records the key and evidence and does not encode it as an architecture constant.
11. Simulate an unknown Agent absent from the registry whose name resembles an existing integration.
12. Simulate a false match between similar names.
13. Missing CLI.
14. Catalog offline.
15. Local Extension installation.
16. Untrusted remote source.
17. Dry-run and apply diff agreement.
18. Integration status verification.
19. Adapter Loader mode.
20. Adapter Materialized mode.
21. Rollback.
22. No additional diff on the second run.
23. A test omitting integration from non-interactive init must prove that the governance manager refuses to generate that command.
24. Ordinary Agent onboarding must not change the default integration.
25. Three fixtures—an unwritable native integration target path, permission denial, and sandbox blocking—must all return `NATIVE_INSTALL_BLOCKED` and must not create generic artifacts.
26. All pre-existing extension, preset, event, shared infrastructure, spec, Skill, and Command inventory must remain unchanged before and after a native integration installation failure.
27. Capability inventory must be equivalent before and after a governance upgrade; only changes individually approved in the operation plan are permitted.
28. Installing an Extension archive must not directly modify the business project; bootstrap generates a plan only.
29. The portable ZIP and Extension archive must have identical version, manifest, and content hashes for the same payload.
30. Successful manager self-update and rollback after replacement failure.
31. Initial and update deployment of the central global Policy, malformed markers, an unreplaced placeholder, and an invalid Reference path.

Test selection must be based on capability type. The test operator must explicitly fill in `primary_integration_key`, `secondary_safe_integration_key`, `skills_integration_key`, and `commands_integration_key` for the current run in `tests/governance/runtime-selection.json`; the file belongs only to test-run evidence and not to the project's support list. The harness must use evidence from the current CLI to verify that every key satisfies its corresponding capability selector, and must stop on verification failure rather than choosing a similar brand. The test report must record the actual keys, CLI version, and status evidence.

The fixed structure of this file is:

```json
{
  "schema_version": 1,
  "specify_version": "<observed-version>",
  "primary_integration_key": "<verified-key>",
  "secondary_safe_integration_key": "<verified-key>",
  "skills_integration_key": "<verified-key>",
  "commands_integration_key": "<verified-key>",
  "evidence": {
    "integration_status_json_sha256": "<sha256>",
    "manual_registry_review": "<project-relative-evidence-file>"
  }
}
```

`runtime-selection.json` must be placed in the test temporary directory or `.gitignore` and must not be published with the governance release. When automated tests use a controlled fake CLI fixture, all four keys must use the fixture's own capability metadata; for real CLI tests, the operator must fill them in explicitly, and the manager must not parse Rich tables to populate them.

If the current test environment cannot satisfy any required capability selector, return `TEST_ENVIRONMENT_INSUFFICIENT` and fail the release build. Do not skip it, substitute a "similar product," or reduce the acceptance scope; the test operator must move to a CLI/runtime environment that satisfies the requirement.

## Real-Agent Verification

Every active adapter must perform the following:

1. Use a fresh checkout or clean worktree.
2. Start a new session in the corresponding Agent.
3. The test harness places a one-time random probe token in a managed test copy of `POLICY.md` and records its hash; the user prompt must not contain the token, Policy text, governance file paths, or Loader content.
4. The fixed prompt asks only: "Report the version of this project's governance Policy, verify the probe token, report the current runtime ID and current Spec Kit integration key, and list the project-governance entry points you will use. Do not modify files."
5. Through the Loader, the Agent must read `START_HERE.md` and `POLICY.md` from the native context anchor and return exactly the same probe token, Policy version, runtime ID, and integration key.
6. The returned runtime ID must exactly match the claimed identity, and the integration key must exactly match the installed candidate; only then may a runtime-to-key verified binding be established and `EXACT_NATIVE_INSTALLED` be allowed.
7. Verify that its native Spec Kit Command or Skill is discoverable.
8. Run the fixed, read-only minimal workflow: list the available Spec Kit workflow names and the current project's `.specify` status without creating or modifying files.
9. Save the session export; if export is unavailable, save a continuous sequence of screenshots. Write the SHA-256 of the evidence file, screenshots, or export, along with the product version, CLI version, prompt hash, and result hash, to an immutable evidence record.
10. Verify that Skills, Commands, extensions, presets, events, and project-governance entry points that existed before onboarding remain discoverable.
11. Remove the probe token from the test copy, then render and verify again; the probe must not enter a release or the default branch.
12. Update the binding to active.

An adapter that cannot be automatically verified must remain provisional.

# Rollback Requirements

Governance-package rollback must not uninstall or reset a native integration by default.

Before every successful upgrade, the manager must:

1. Verify the current manifest and hashes.
2. Preserve the immutable identifier of the previously verified governance-package version.
3. Generate a pre-upgrade audit record.
4. Plan first, then apply.
5. Preserve the complete pre-upgrade capability inventory.

Rollback procedure:

1. Run `plan-rollback --to <verified-version>`.
2. Review which managed files will be restored.
3. Confirm that `LOCAL_OVERRIDES.md` is not in the target list.
4. After the user approves the exact `plan_id`, run `apply-plan`.
5. Run `governance.py verify`.
6. Run `specify integration status --json`.
7. Compare against the capability inventory recorded for the rollback target version; rollback must not delete later user work or Agent integration artifacts.
8. Record the reason, version, impact, and follow-up in the PR or commit description.

If Policy, Reference, or markers have been modified manually and locally, automatic rollback is prohibited; generate three-way merge materials and stop.

# Implementation Phases

## Phase 0: Protect Current Work

The current repository already contains uncommitted changes. The implementation Agent must:

1. Read `git status`.
2. Read the complete diff.
3. Treat existing changes as user work.
4. Do not reset, overwrite through checkout, or restore user deletions.
5. Phase 0 generates only a read-only audit of `git status`, tracked and untracked paths, and the diff; it must not stash, commit, reset, checkout, or copy the entire repository. Recoverable file-level backups may be created only in a user-approved operation plan, for exact manager-mutation targets or within the allowed scope of an external mutation.
6. Do not advance `UPSTREAM_BASELINE` unless a formal upstream impact review is completed at the same time.

## Phase 1: Freeze the Capability Baseline

1. Read all current specifications and runtime state according to "Capability Baseline Sources."
2. Create `governance/capability-baseline.json` and its schema.
3. For each capability, specify `PRESERVE`, `MOVE`, or `REPLACE`, its new target, and its release-blocking test.
4. Record an inventory of current integrations, default, extensions, presets, events, shared infrastructure, constitution, specs, Skills, Commands, and project-governance entry points.
5. Have a human review the baseline; do not enter Phase 2 while any capability remains unmapped.

## Phase 2: Establish Schemas and the Test Framework

Create these first:

- Governance manifest schema.
- Adapter schema.
- Project config schema.
- Capability baseline schema.
- Resolution result schema.
- Operation plan schema.
- Path-safety tests.
- Marker tests.
- Hash-normalization tests.
- Native no-downgrade blocking tests.
- Capability-inventory equivalence tests.

Do not implement automatic upgrade writes before the schemas are stable.

## Phase 3: Implement the Global Template and Manual Deployment Protocol

1. Reduce `GLOBAL_POLICY.md` according to the fixed template in this document.
2. Create `docs/GLOBAL_POLICY_DEPLOYMENT.md`, implementing verbatim the requirements for manual input, prerequisite validation, the sole replacement, backup, atomic write, and postcondition validation.
3. Update the Chinese and English deployment instructions in README so that they reference only this fixed procedure.
4. Implement static template-validation tests: one marker pair, one placeholder, a line-count limit, and no personal absolute paths.
5. Do not write any personal global rules file; leave actual deployment to the manual procedure in Phase 12.

## Phase 4: Split Policy

1. Reduce `GLOBAL_POLICY.md`.
2. Create the project `POLICY.md`.
3. Preserve the semantics of existing rules.
4. Add dynamic Agent resolution.
5. Correct the controlled-exception rules for generic.
6. Add default-integration restrictions.
7. Review that no lifecycle, validation, or convergence capability has been lost.
8. Associate every old Policy capability with its new target and test in the capability baseline.

## Phase 5: Generate the Portable Reference

1. Add portable markers to the central Reference.
2. Implement deterministic extraction.
3. Exclude central-maintenance metadata.
4. Write provenance into the manifest.
5. Verify that the project Reference contains no personal absolute path.

## Phase 6: Implement Project Config and the Read-Only Resolver

Complete these first:

- `PROJECT_CONFIG.json` defaults and schema
- `doctor`
- `resolve-agent`
- JSON output
- all error states
- no file writes

Do not implement apply before the Resolver passes its tests.

## Phase 7: Implement Planning and Safe Writes

1. `plan-governance-bootstrap`。
2. `plan-init`。
3. `plan-onboard`。
4. `plan-extension-install`。
5. `plan-default-change`。
6. Canonical operation-plan JSON and non-self-referential `plan_sha256`.
7. Two contracts: manager file mutation and external CLI mutation.
8. Marker renderer.
9. Atomic single-file writes, external scope snapshots, and journals.
10. Hash checks.
11. `apply-plan` with fixed approved argv.
12. Idempotency.
13. Three-way conflict materials and stop status.
14. Dedicated prerequisite gates and rollback for controlled brownfield `--force` init.

## Phase 8: Implement the Adapter Lifecycle

1. Portable `AGENTS.md` Loader.
2. Active binding or a user-explicit context anchor; do not implement automatic candidate resolution.
3. Loader mode.
4. Materialized mode.
5. Provisional and active verification.
6. Capability records.

## Phase 9: Package the Two Fixed Release Artifacts

1. Implement the portable ZIP builder.
2. Create the Extension archive according to the current CLI format.
3. Implement `scripts/python/bootstrap_governance.py` inside the Extension.
4. The Extension only verifies and delivers the payload, then invokes the manager to generate a plan.
5. Implement a separate `bootstrap_updater.py` and staged self-update.
6. Build two immutable artifacts and the SHA-256 of each.
7. Verify that the two artifacts have identical payload version, manifest, and content hashes.
8. Verify local, offline, and failure-rollback behavior.
9. Do not implement a bundle and do not automatically trust a community catalog.

## Phase 10: Implement Upgrade and Rollback

1. `check-update`
2. `plan-upgrade`
3. Upgrade through the sole `apply-plan`
4. Three-way conflict handling
5. `plan-rollback`
6. Rollback through the sole `apply-plan`
7. Release provenance
8. Read-only discovery through the central locator
9. Capability-inventory equivalence gate before and after upgrade

## Phase 11: Real-World Pilot

The test harness must select the following by capability selector:

- One primary Agent integration.
- One non-default integration that is safe to coexist.
- One current runtime integration that is Skills-based and not the primary brand.
- One completely unknown simulated Agent.
- One generic-compatible fixture.
- One generic-incompatible fixture.
- One fixture with an unwritable native integration target.

For every selection, record the actual key and runtime evidence in the report; do not turn the pilot product set into a project support list.

## Phase 12: Release Acceptance and Manual Deployment of the Global Policy

1. Run all schema, unit, CLI integration, real-Agent, capability-conservation, and rollback tests.
2. Confirm that every item in the capability baseline has a new target and a passing release-blocking test.
3. Build the two fixed release artifacts and verify their checksums.
4. Confirm that verification of the project governance package, Resolver, adapters, upgrade, and rollback is complete.
5. For each actual Agent product, the user manually selects its real global rules file.
6. The user fills in the single absolute-path placeholder for the central repository.
7. Install or replace the marker block for each target according to `docs/GLOBAL_POLICY_DEPLOYMENT.md`.
8. Manually confirm in a new session of every product that the global Bootstrap is loaded.
9. Failure to deploy one target must not affect other successfully deployed targets; preserve the old file for the failed target and repair it separately.

# Documentation Formatting Requirements

Markdown documents generated or modified by the implementation must follow this repository's rules:

1. Do not place a global placeholder title duplicating the filename at the top of the body.
2. Use H1 directly for top-level business sections in the body.
3. Use H2 and H3 for subsections.
4. Preserve a complete blank line above and below every heading.
5. Do not automatically append unrelated "Further Reading" or "Related Notes" sections.
6. Do not use Markdown horizontal rules.
7. Governance Markdown generated by V1 must not use Frontmatter; the body must not contain `---` on a line by itself.

# Final Acceptance Checklist

Implementation is complete only when every item below is satisfied:

- [ ] The global Policy has been shortened and contains no fixed set of Agent brands.
- [ ] Root `GLOBAL_POLICY.md` is the sole global deployment template, with exactly one marker pair and one placeholder for the absolute path of the central repository.
- [ ] `docs/GLOBAL_POLICY_DEPLOYMENT.md` fixes the process for manually selecting the target, filling in the path, initial installation, update, backup, atomic replacement, and new-session verification.
- [ ] A previously absent global target is published atomically only through hard-link no-clobber; stop if unsupported, and verify crash recovery through the journal.
- [ ] Tools do not guess, create, or write any personal global rules file.
- [ ] The project governance package contains the complete Policy, Reference, operating protocol, and first-time onboarding protocol.
- [ ] The project commits and validates `PROJECT_CONFIG.json` against the fixed schema.
- [ ] A verified Agent can still work without the central Reference or personal global rules.
- [ ] The project does not pregenerate a fixed combination of `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.
- [ ] Root `AGENTS.md` serves only as a generic best-effort entry point.
- [ ] New Agents use on-demand onboarding rather than preinstalling every integration.
- [ ] The Resolver does not treat Agent tools installed on the machine as the current identity.
- [ ] The Resolver does not treat the default integration as the current identity.
- [ ] Non-interactive init always passes `--integration <key>` explicitly.
- [ ] The system does not guess when identity is unknown, multiple candidates exist, or the catalog is unavailable.
- [ ] Products with similar names are not automatically mapped to each other.
- [ ] When the current CLI has a native integration, the system does not downgrade to generic.
- [ ] When the native integration target is unwritable, permissions are insufficient, the sandbox blocks access, or installation fails, the result is `NATIVE_INSTALL_BLOCKED`; no generic, other integration key, or "complete" result is produced.
- [ ] Project `POLICY.md` and `OPERATING_PROTOCOL.md` both contain the fixed blocker branches for native init, install, managed-file repair, and an unwritable context anchor.
- [ ] All four failure tests—native init target, integration target, anchor parent directory, and partial install—assert `NATIVE_INSTALL_BLOCKED`, no fallback, no active binding, and no `READY`.
- [ ] After permissions are repaired, only the same native integration key continues, and a new plan is generated.
- [ ] When no native integration exists, generic may be used only after explicit compatibility validation and authorization.
- [ ] The system does not automatically use `--force` when multi-install is unsafe.
- [ ] The system does not automatically switch the default integration for every session.
- [ ] Capability limitations of a non-default integration are recorded accurately.
- [ ] An Adapter is marked active only after real fresh-session verification.
- [ ] Both Loader and Materialized modes pass testing.
- [ ] Materialized is allowed only with evidence of Loader fresh-session failure.
- [ ] User content outside markers is preserved completely.
- [ ] `LOCAL_OVERRIDES.md` is never overwritten by a central update.
- [ ] All project files contain no personal absolute path.
- [ ] Every release uses an immutable version and checksum.
- [ ] Every release contains both a portable ZIP and Extension archive, and the two have identical payload version, manifest, and content hashes.
- [ ] V1 has no bundle branch; all ordinary writes use the sole manager logic, and the self-update updater executes only a plan approved by the old manager and the shared replacement primitive.
- [ ] CLI installation, integration installation, and governance upgrade all plan first, receive authorization second, and apply third.
- [ ] The central Reference may only discover candidate updates and cannot silently overwrite the project.
- [ ] macOS, Linux, and Windows PowerShell tests pass.
- [ ] No-network, no-CLI, and old-CLI scenarios all have safe outcomes.
- [ ] Rollback does not delete user work and does not uninstall an integration by default.
- [ ] `governance/capability-baseline.json` covers every old capability; each has `PRESERVE`, `MOVE`, or an approved `REPLACE`, a new target, and a release-blocking test.
- [ ] Before and after upgrade, the inventory of integrations, default, extensions, presets, events, shared infrastructure, constitution, specs, Skills, Commands, adapters, and governance files has no unplanned degradation.
- [ ] Any unmapped capability, unplanned deletion, degradation, invalidation, or default change blocks release.
- [ ] Existing uncommitted changes in the current repository are protected.
- [ ] The existing upstream maintenance and `NONE`, `REFERENCE`, and `POLICY` classification mechanism has not been weakened.
- [ ] Advancing the baseline last, non-ancestor blocking, checker exit codes `0/1/2`, read-only behavior, POSIX/PowerShell wrappers, and notify-only/no-write CI each have an independent capability ID and regression test.
- [ ] All documentation follows this repository's Markdown heading and blank-line rules.
- [ ] No Markdown horizontal rule is used.

# Current Implementation Status

The central repository implementation for this iteration is complete: the manager, schemas, portable project package, deterministic release, global Policy deployment contract, capability baseline, upgrade/rollback plan gates, native no-downgrade rules, Loader/Materialized evidence gates, external CLI scope checks, provenance checks, and local regression tests have all been implemented.

The following items explicitly remain real-project verification and must not be replaced by this repository's unit tests: whether a real Agent fresh session actually loads the anchor and Loader; whether the real native integration corresponding to the current Agent can write to the target environment and generate the expected managed files; the actual behavior of Materialized only after a real Loader fresh-session failure; and the macOS, Linux, Windows PowerShell, and no-permission/sandbox environment matrix. Before those verifications are complete, this repository may enter a controlled real-project pilot but must not claim final cross-Agent, cross-platform release completion.

# Definition of Implementation Completion

Completion may be declared only when user intent, global Bootstrap, project Policy, project Reference, dynamic Agent Resolver, Adapter lifecycle, native integration, version manifest, safe writes, upgrade, rollback, capability conservation, cross-platform testing, and real-Agent verification all agree.

Passing tests without the Adapter loading in a real session does not constitute completion.

Generating `.specify/` for a project when the current Agent has no native or explicitly approved compatible integration does not constitute completion.

When the current CLI has a native integration, using generic or another Agent integration because of an unwritable path, permissions, or sandbox issues—or generating only `.specify/commands/`—does not constitute completion.

If a governance rule, integration, extension, preset, event, Skill, Command, spec, or project entry point available in the old version has no explicit migration target and passing regression test in the new version, implementation is not complete.

Having a governance package while collaborators still depend on the maintainer's personal Reference path does not constitute completion.

Overwriting project Policy after discovering a central update but without project review does not constitute completion.

The most important implementation principle is:

> Do not preregister every Agent. The current Agent declares its identity on first entry; the governance manager resolves the native integration from the current runtime, then installs and verifies one adapter on demand. If a completely unknown product has no compatibility contract, stop explicitly instead of guessing.
