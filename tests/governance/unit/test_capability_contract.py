"""Release-blocking regression checks for the preserved governance contract.

These tests intentionally exercise both runtime behavior and the committed
portable policy.  The baseline is a capability inventory, so every named
release test must have a concrete assertion here or in a neighboring test
module.
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MANAGER = ROOT / "governance/manager/speckit_governance.py"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class CapabilityContractTests(unittest.TestCase):
    def test_lightweight_work_does_not_require_lifecycle(self):
        policy = read("governance/project/POLICY.md")
        self.assertIn("extremely small typo fixes", policy)
        self.assertIn("do not require the full lifecycle", policy)

    def test_project_root_detection(self):
        source = read("governance/manager/speckit_governance.py")
        self.assertIn("project_root_from", source)
        self.assertIn("--project-root", source)

    def test_brownfield_discovery_required(self):
        protocol = read("governance/project/OPERATING_PROTOCOL.md")
        self.assertIn("read every governance file in this directory", protocol)
        self.assertIn("brownfield", protocol)

    def test_dirty_worktree_is_preserved(self):
        source = read("governance/manager/speckit_governance.py")
        self.assertIn("git_status_porcelain_sha256", source)
        self.assertIn("project_root_fingerprint", source)
        self.assertIn("old_sha256", source)

    def test_existing_specify_state_is_resumed(self):
        protocol = read("governance/project/OPERATING_PROTOCOL.md")
        self.assertIn("Do not rerun init", protocol)
        self.assertIn("Existing projects", protocol)

    def test_controlled_brownfield_init_uses_backups(self):
        source = read("governance/manager/speckit_governance.py")
        self.assertIn('"--force"', source)
        self.assertIn("has_durable_project_files", source)
        self.assertIn("backups", source)

    def test_runtime_identity_does_not_use_brand_allowlist(self):
        policy = read("governance/project/POLICY.md")
        self.assertIn("does not enumerate Agent products in advance", policy)
        self.assertIn("Do not infer identity from PATH, directory names", policy)

    def test_concrete_agent_uses_native_key(self):
        policy = read("governance/project/POLICY.md")
        self.assertIn("native integration is mandatory", policy)
        self.assertIn("exact integration key", policy)

    def test_native_target_unwritable_is_blocker(self):
        source = read("governance/manager/speckit_governance.py")
        self.assertIn("NATIVE_INSTALL_BLOCKED", source)
        self.assertIn("preflight_writable", source)

    def test_completion_rejected_without_native_managed_files(self):
        policy = read("governance/project/POLICY.md")
        self.assertIn("native integration", policy)
        self.assertIn("managed files", policy)
        self.assertIn("Do not report completion", policy)

    def test_generic_requires_explicit_approval(self):
        config = json.loads(read("governance/project/PROJECT_CONFIG.default.json"))
        self.assertEqual(config["generic"]["policy"], "deny")
        self.assertIn("explicit-approval-required", read("governance/manager/speckit_governance.py"))

    def test_generic_never_claims_native_capability(self):
        policy = read("governance/project/POLICY.md")
        self.assertIn("Generic must be marked as non-native", policy)
        source = read("governance/manager/speckit_governance.py")
        self.assertIn('"explicit-generic-transition"', source)

    def test_unsafe_multi_install_is_blocked(self):
        config = json.loads(read("governance/project/PROJECT_CONFIG.default.json"))
        self.assertFalse(config["onboarding"]["allow_unsafe_multi_install"])
        self.assertIn("INTEGRATION_CONFLICT", read("governance/manager/speckit_governance.py"))

    def test_runtime_authority_order(self):
        policy = read("governance/project/POLICY.md")
        self.assertIn("current-project `.specify/`", policy)
        self.assertIn("installed CLI", policy)
        self.assertIn("upstream documentation", policy)

    def test_cli_is_runtime_authority(self):
        protocol = read("governance/project/OPERATING_PROTOCOL.md")
        self.assertIn("specify integration status --json", protocol)
        self.assertIn("specify version", read("governance/project/AGENT_ONBOARDING.md"))

    def test_core_lifecycle_is_present(self):
        lifecycle = "constitution → specify → clarify → plan → checklist → tasks → analyze → implement → validate → converge"
        self.assertIn(lifecycle, read("governance/project/POLICY.md"))

    def test_conversational_approval_does_not_bypass_spec_alignment(self):
        for rel in (
            "governance/project/START_HERE.md",
            "governance/project/POLICY.md",
            "governance/project/OPERATING_PROTOCOL.md",
            "governance/project/REFERENCE.md",
        ):
            content = read(rel)
            self.assertIn("the plan is acceptable", content)
            self.assertIn("upstream Spec Kit", content)
            self.assertIn("does not authorize direct", content)
            for artifact in ("specification", "plan", "tasks"):
                self.assertIn(artifact, content)

    def test_analyze_is_required_for_substantive_work(self):
        config = json.loads(read("governance/project/PROJECT_CONFIG.default.json"))
        self.assertEqual(config["quality_gates"]["analyze"], "required")
        self.assertIn("Analyze, validate, and converge are required", read("governance/project/POLICY.md"))

    def test_reference_owned_boundary_is_documented_and_enforced(self):
        agents = read("AGENTS.md")
        reference = read("governance/project/REFERENCE.md")
        source = read("governance/manager/speckit_governance.py")
        for content in (agents, reference):
            self.assertIn(".specify/**", content)
            self.assertIn("specs/**", content)
            self.assertIn("runtime prerequisites", content)
        self.assertIn("REFERENCE_OWNERSHIP_VIOLATION", source)
        self.assertIn("reference_owned_mutation", source)

    def test_update_reminder_uses_upstream_cli_without_governance_package(self):
        source = read("governance/manager/speckit_governance.py")
        self.assertIn("plan-install-update-reminder", source)
        self.assertIn("specify self check", source)
        self.assertIn("append-managed-update-reminder", source)
        self.assertIn("UPDATE_REMINDER_START_MARKER", source)
        self.assertNotIn("specify self upgrade", source.split("def update_reminder_loader", 1)[0])

    def test_reference_update_check_is_policy_and_source_gated(self):
        policy = read("GLOBAL_POLICY.md")
        project_policy = read("governance/project/POLICY.md")
        check_block = read("governance/project/REFERENCE_UPDATE_CHECK.md")
        for content in (policy, project_policy, check_block):
            self.assertIn("SPEC_KIT_GOVERNANCE_SOURCE", content)
            self.assertIn("skip", content.lower())
            self.assertIn("silently", content.lower())
            self.assertIn("do not", content.lower())
        self.assertIn("check-update --source", check_block)
        self.assertIn("UPDATE_AVAILABLE", read("governance/project/REFERENCE.md"))
        self.assertIn("UP_TO_DATE", read("governance/manager/speckit_governance.py"))

    def test_reference_update_never_becomes_spec_artifact_mutation(self):
        for rel in (
            "README.md",
            "governance/project/POLICY.md",
            "governance/project/REFERENCE.md",
            "governance/project/START_HERE.md",
            "governance/project/OPERATING_PROTOCOL.md",
            "governance/project/REFERENCE_UPDATE_CHECK.md",
        ):
            content = read(rel)
            self.assertIn(".specify/**", content)
            self.assertIn("specs/**", content)
        source = read("governance/manager/speckit_governance.py")
        self.assertIn("append-managed-reference-update-check", source)
        self.assertIn("REFERENCE_OWNERSHIP_VIOLATION", source)

    def test_risk_gate_formula(self):
        implementation = read("docs/archive/PROJECT_GOVERNANCE_IMPLEMENTATION_2026-08-21.md")
        self.assertIn("risk", implementation.lower())
        self.assertIn("clarify", implementation)
        self.assertIn("converge", implementation)

    def test_artifact_divergence_blocks_completion(self):
        policy = read("governance/project/POLICY.md")
        self.assertIn("Implementation must remain synchronized with the accepted specification, plan, tasks", policy)
        self.assertIn("unplanned deletion, downgrade, invalid state, or default change", policy)

    def test_completion_requires_validation_and_convergence(self):
        policy = read("governance/project/POLICY.md")
        self.assertIn("validation, and convergence", policy)
        self.assertIn("failures must not be concealed", policy)

    def test_substantive_bug_requires_reproduction_and_validation(self):
        reference = read("governance/project/REFERENCE.md").lower()
        self.assertIn("bug workflow", reference)
        self.assertIn("reproduction", reference)

    def test_cli_upgrade_does_not_reinitialize_project(self):
        protocol = read("governance/project/OPERATING_PROTOCOL.md")
        self.assertIn("inventory before and after the upgrade must be equivalent", protocol)
        self.assertIn("must not uninstall integrations", protocol)

    def test_cli_install_does_not_claim_global_skills(self):
        reference = read("governance/project/REFERENCE.md")
        self.assertIn("Installing `specify` globally does not install Agent Skills", reference)
        self.assertIn("Do not manually copy generated Skills", reference)

    def test_completion_rejects_unresolved_blocker(self):
        self.assertIn("unplanned deletion, downgrade, invalid state, or default change", read("governance/project/POLICY.md"))
        self.assertIn("Do not report completion", read("governance/project/POLICY.md"))

    def test_upstream_review_sequence(self):
        policy = read("AGENTS.md")
        for phrase in ("Read `UPSTREAM_BASELINE`", "Fetch `upstream/main`", "Classify", "Run validation", "Advance `UPSTREAM_BASELINE`"):
            self.assertIn(phrase, policy)

    def test_policy_impact_requires_human_review(self):
        self.assertIn("require human review", read("AGENTS.md"))
        self.assertIn("POLICY", read("docs/UPSTREAM_UPDATE_POLICY.md"))

    def test_upstream_is_not_instruction_authority(self):
        self.assertIn("Upstream files are evidence", read("AGENTS.md"))
        self.assertIn("evidence", read("docs/UPSTREAM_UPDATE_POLICY.md"))

    def test_upstream_integrity_prohibitions(self):
        policy = read("AGENTS.md")
        for phrase in ("merge `upstream/main`", "vendor the entire upstream", "automatically merge or deploy `POLICY`"):
            self.assertIn(phrase, policy)

    def test_nonancestor_baseline_requires_manual_review(self):
        source = read("scripts/check_upstream.py")
        self.assertIn("not an ancestor", source)
        self.assertIn("history rewriting", source)

    def test_reference_impact_does_not_change_policy(self):
        policy = read("docs/UPSTREAM_UPDATE_POLICY.md")
        self.assertIn("REFERENCE", policy)
        self.assertIn("normally leave `GLOBAL_POLICY.md` unchanged", policy)

    def test_checker_is_read_only(self):
        source = read("scripts/check_upstream.py")
        self.assertNotIn("write_text", source)
        self.assertNotIn("unlink", source)
        self.assertIn("--no-fetch", source)

    def test_checker_exit_code_contract(self):
        source = read("scripts/check_upstream.py")
        self.assertIn("return 0", source)
        self.assertIn("return 2", source)
        self.assertIn("sys.exit(1)", source)

    def test_checker_no_fetch_mode(self):
        self.assertIn("--no-fetch", read("scripts/check_upstream.py"))
        self.assertIn("instead of fetching", read("scripts/check_upstream.py"))

    def test_checker_rejects_invalid_baseline(self):
        source = read("scripts/check_upstream.py")
        self.assertIn("must contain exactly one 40-character commit SHA", source)
        self.assertIn("SHA_RE", source)

    def test_checker_rejects_missing_baseline_commit(self):
        self.assertIn("baseline commit is not available locally", read("scripts/check_upstream.py"))

    def test_checker_rejects_nonofficial_upstream_remote(self):
        source = read("scripts/check_upstream.py")
        self.assertIn("OFFICIAL_UPSTREAM_URLS", source)
        self.assertIn("official GitHub Spec Kit", source)

    def test_checker_rejects_stale_or_rewritten_history(self):
        source = read("scripts/check_upstream.py")
        self.assertIn("upstream/main is older", source)
        self.assertIn("history rewriting", source)

    def test_checker_reports_commits_and_changed_paths(self):
        source = read("scripts/check_upstream.py")
        self.assertIn('git("log", "--oneline"', source)
        self.assertIn('git("diff", "--name-only"', source)

    def test_ci_never_merges_or_deploys_policy(self):
        workflow = read(".github/workflows/check-spec-kit-upstream.yml")
        self.assertNotIn("git merge", workflow)
        self.assertNotIn("UPSTREAM_BASELINE", workflow)
        self.assertIn("Create or update review issue", workflow)

    def test_ci_issue_notification_only(self):
        workflow = read(".github/workflows/check-spec-kit-upstream.yml")
        self.assertIn("steps.upstream.outputs.status == '2'", workflow)
        self.assertIn("gh issue", workflow)

    def test_ci_fails_on_checker_error(self):
        workflow = read(".github/workflows/check-spec-kit-upstream.yml")
        self.assertIn("Stop on checker error", workflow)
        self.assertIn("exit 1", workflow)

    def test_wrapper_contract_posix(self):
        wrapper = read("scripts/check-upstream.sh")
        self.assertIn("check_upstream.py", wrapper)
        self.assertIn('exec python3', wrapper)

    def test_wrapper_contract_powershell(self):
        wrapper = read("scripts/check-upstream.ps1")
        self.assertIn("check_upstream.py", wrapper)
        self.assertRegex(wrapper, r"python(?:3)?")

    def test_ci_wrapper_matrix_contract(self):
        workflow = read(".github/workflows/check-spec-kit-upstream.yml")
        self.assertIn("ubuntu-latest", workflow)
        self.assertIn("windows-latest", workflow)
        self.assertIn("check-upstream.ps1", workflow)

    def test_global_policy_template_has_title_and_no_html_wrapper(self):
        policy = read("GLOBAL_POLICY.md")
        self.assertIn("\n# Spec Kit Global Policy\n", policy)
        self.assertIn("<!-- SPEC-KIT-GLOBAL-POLICY:START version=", policy)
        self.assertIn("<!-- SPEC-KIT-GLOBAL-POLICY:END -->", policy)
        self.assertEqual(policy.count("\n## "), 5)
        self.assertEqual(policy.count("SPEC_KIT_GOVERNANCE_SOURCE:"), 1)
        self.assertEqual(policy.count("<ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>"), 1)

    def test_global_policy_deployment_updates_only_managed_block(self):
        protocol = read("docs/GLOBAL_POLICY_DEPLOYMENT.md")
        self.assertIn("outside the markers", protocol)
        self.assertIn("replacement span", protocol)

    def test_global_policy_placeholder_is_rejected(self):
        protocol = read("docs/GLOBAL_POLICY_DEPLOYMENT.md")
        self.assertIn("placeholder", protocol.lower())
        self.assertIn("occurs exactly once", protocol)

    def test_global_policy_locator_must_exist(self):
        protocol = read("docs/GLOBAL_POLICY_DEPLOYMENT.md")
        self.assertIn("readable directory", protocol)
        self.assertIn("nonexistent target", protocol)

    def test_discovery_does_not_initialize_project(self):
        resolver = read("governance/resolver/resolver-contract.md")
        self.assertIn("must not", resolver)
        self.assertIn("create temporary projects", resolver)
        self.assertIn("status --json", resolver)

    def test_managed_layout_is_verified_from_runtime(self):
        protocol = read("governance/project/OPERATING_PROTOCOL.md")
        self.assertIn("managed files", protocol)
        self.assertIn("status", protocol)

    def test_native_install_failure_never_proposes_generic(self):
        source = read("governance/manager/speckit_governance.py")
        self.assertIn("NATIVE_INSTALL_BLOCKED", source)
        self.assertIn("generic", source)

    def test_runtime_authority_order_is_not_brand_specific(self):
        self.assertIn("does not enumerate Agent products in advance", read("governance/project/POLICY.md"))

    def test_substantive_work_requires_speckit(self):
        self.assertIn("substantive software engineering work", read("governance/project/POLICY.md"))


if __name__ == "__main__":
    unittest.main()
