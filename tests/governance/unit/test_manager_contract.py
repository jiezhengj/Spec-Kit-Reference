import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANAGER = ROOT / "governance/manager/speckit_governance.py"
sys.path.insert(0, str(ROOT / "governance/manager"))
import speckit_governance as manager


class ManagerContractTests(unittest.TestCase):
    def run_manager(self, project: Path, *args: str, check: bool = True, env=None):
        return subprocess.run(
            [sys.executable, str(MANAGER), "--project-root", str(project), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=check,
            env=env,
        )

    def test_bootstrap_plan_apply_is_self_describing(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            result = self.run_manager(project, "plan-governance-bootstrap", "--source", str(ROOT))
            plan_info = json.loads(result.stdout)
            plan = Path(plan_info["path"])
            applied = self.run_manager(
                project,
                "apply-plan",
                "--plan",
                str(plan),
                "--approve-plan-id",
                plan_info["plan_id"],
                "--approve-plan-sha256",
                plan_info["plan_sha256"],
            )
            self.assertEqual(json.loads(applied.stdout)["status"], "applied")
            manifest = json.loads((project / "docs/spec-kit/MANIFEST.json").read_text())
            self.assertIn("docs/spec-kit/ADAPTERS.json", manifest["content_sha256"])
            verified = json.loads(self.run_manager(project, "verify").stdout)
            self.assertEqual(verified["status"], "READY")

    def test_bootstrap_preserves_existing_managed_loader_and_user_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            existing = b"# project rules\n\n" + manager.marker_loader().encode("utf-8")
            (project / "AGENTS.md").write_bytes(existing)
            bootstrap = json.loads(self.run_manager(project, "plan-governance-bootstrap", "--source", str(ROOT)).stdout)
            self.run_manager(project, "apply-plan", "--plan", bootstrap["path"], "--approve-plan-id", bootstrap["plan_id"], "--approve-plan-sha256", bootstrap["plan_sha256"])
            self.assertEqual((project / "AGENTS.md").read_bytes(), existing)

    def test_unknown_identity_requires_exact_key_and_generic_is_not_native(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            missing_key = self.run_manager(
                project,
                "resolve-agent",
                "--runtime-id",
                "vendor.unknown.agent",
                "--display-name",
                "Unknown Agent",
                "--json",
            )
            self.assertEqual(json.loads(missing_key.stdout)["status"], "KEY_REQUIRED")
            generic = self.run_manager(
                project,
                "resolve-agent",
                "--runtime-id",
                "vendor.unknown.agent",
                "--integration-key",
                "generic",
                "--json",
            )
            response = json.loads(generic.stdout)
            self.assertEqual(response["status"], "UNSUPPORTED_INCOMPATIBLE")
            self.assertIsNone(response["integration"]["mode"])

    def test_native_cli_failure_is_a_blocker_not_generic(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / ".specify").mkdir()
            fake_bin = project / "bin"
            fake_bin.mkdir()
            fake = fake_bin / "specify"
            fake.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
            fake.chmod(0o755)
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{fake_bin}:{old_path}"
            try:
                plan = {
                    "plan_id": "native-failure-test",
                    "operation_type": "plan-onboard",
                    "required_native_key": "native-key",
                    "external_cli_mutations": [{"argv": ["specify", "integration", "install", "native-key"], "allowed_path_prefixes": [".specify/"]}],
                }
                with self.assertRaises(manager.GovernanceError) as raised:
                    manager.run_external_mutations(project, plan)
                self.assertEqual(raised.exception.status, "NATIVE_INSTALL_BLOCKED")
            finally:
                os.environ["PATH"] = old_path

    def test_conflicting_environment_identity_stops_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            old = os.environ.get("SPEC_KIT_CURRENT_AGENT_ID")
            os.environ["SPEC_KIT_CURRENT_AGENT_ID"] = "host.agent"
            try:
                result = self.run_manager(
                    project,
                    "resolve-agent",
                    "--runtime-id",
                    "user.agent",
                    "--integration-key",
                    "native-key",
                    "--json",
                    check=False,
                )
                self.assertEqual(json.loads(result.stderr)["status"], "IDENTITY_CONFLICT")
            finally:
                if old is None:
                    os.environ.pop("SPEC_KIT_CURRENT_AGENT_ID", None)
                else:
                    os.environ["SPEC_KIT_CURRENT_AGENT_ID"] = old

    def test_governance_upgrade_and_rollback_are_manager_operations(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            bootstrap = json.loads(self.run_manager(project, "plan-governance-bootstrap", "--source", str(ROOT)).stdout)
            self.run_manager(project, "apply-plan", "--plan", bootstrap["path"], "--approve-plan-id", bootstrap["plan_id"], "--approve-plan-sha256", bootstrap["plan_sha256"])
            upgrade = json.loads(self.run_manager(project, "plan-upgrade", "--source", str(ROOT)).stdout)
            plan = json.loads(Path(upgrade["path"]).read_text())
            self.assertEqual(plan["external_cli_mutations"], [])
            self.assertTrue(any(item["path"] == "tools/spec-kit-governance/governance.py" for item in plan["manager_file_mutations"]))
            rollback = json.loads(self.run_manager(project, "plan-rollback", "--source", str(ROOT), "--version", "1.0.0").stdout)
            rollback_plan = json.loads(Path(rollback["path"]).read_text())
            self.assertEqual(rollback_plan["external_cli_mutations"], [])

    def test_plan_init_records_isolated_rehearsal(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            fake_bin = Path(tempfile.mkdtemp(prefix="specify-fixture-bin-"))
            fake = fake_bin / "specify"
            fake.write_text(
                "#!/bin/sh\n"
                "if [ \"$1\" = \"--version\" ] || [ \"$1\" = \"version\" ]; then echo 0.16.6.dev0; exit 0; fi\n"
                "if [ \"$1\" = \"init\" ]; then mkdir -p .specify; printf '%s\\n' initialized > .specify/state.txt; exit 0; fi\n"
                "exit 0\n",
                encoding="utf-8",
            )
            fake.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}:{env['PATH']}"
            result = self.run_manager(project, "plan-init", "--integration-key", "native-key", env=env)
            info = json.loads(result.stdout)
            plan = json.loads(Path(info["path"]).read_text())
            self.assertEqual(plan["rehearsal"]["argv"][-1], "native-key")
            self.assertIn(".specify/state.txt", plan["rehearsal"]["changed_files"])
            self.assertFalse((project / ".specify").exists())
            for child in fake_bin.iterdir():
                child.unlink()
            fake_bin.rmdir()

    def test_generic_transition_requires_attestation_and_stays_non_native(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            bootstrap = json.loads(self.run_manager(project, "plan-governance-bootstrap", "--source", str(ROOT)).stdout)
            self.run_manager(project, "apply-plan", "--plan", bootstrap["path"], "--approve-plan-id", bootstrap["plan_id"], "--approve-plan-sha256", bootstrap["plan_sha256"])
            config_path = project / "docs/spec-kit/PROJECT_CONFIG.json"
            config = json.loads(config_path.read_text())
            config["generic"]["policy"] = "explicit-approval-required"
            config_path.write_text(json.dumps(config) + "\n")
            (project / ".specify").mkdir()
            evidence_dir = project / "docs/spec-kit/evidence"
            evidence_dir.mkdir()
            catalog = evidence_dir / "catalog.txt"
            catalog.write_text("no native integration\n")
            import hashlib
            attestation = evidence_dir / "no-native.json"
            attestation.write_text(json.dumps({
                "runtime_id": "vendor.unknown",
                "specify_version": "0.16.6.dev0",
                "catalog_evidence": "docs/spec-kit/evidence/catalog.txt",
                "catalog_evidence_sha256": hashlib.sha256(catalog.read_bytes()).hexdigest(),
                "reviewed_by_current_operator": True,
                "conclusion": "no-native-integration-found-for-runtime",
            }) + "\n")
            anchor_evidence = evidence_dir / "anchor.json"
            anchor_evidence.write_text(json.dumps({
                "anchor_path": "AGENTS.md",
                "format": "markdown",
                "review_conclusion": "markdown loader anchor reviewed",
            }) + "\n")
            fake_bin = project / "bin"
            fake_bin.mkdir()
            fake = fake_bin / "specify"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = \"--version\" ] || [ \"$1\" = \"version\" ]; then echo 0.16.6.dev0; elif [ \"$1\" = \"integration\" ] && [ \"$2\" = \"status\" ]; then printf '%s\\n' '{\"installed_integrations\":[]}'; elif [ \"$1\" = \"integration\" ] && [ \"$2\" = \"install\" ]; then mkdir -p .example-commands; echo command > .example-commands/workflow.md; fi\n", encoding="utf-8")
            fake.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}:{env['PATH']}"
            result = self.run_manager(
                project,
                "plan-onboard",
                "--runtime-id", "vendor.unknown",
                "--integration-key", "generic",
                "--attestation", "docs/spec-kit/evidence/no-native.json",
                "--commands-dir", ".example-commands",
                "--context-anchor", "AGENTS.md",
                "--anchor-evidence", "docs/spec-kit/evidence/anchor.json",
                check=False,
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            plan_info = json.loads(result.stdout)
            plan = json.loads(Path(plan_info["path"]).read_text())
            binding_mutation = next(item for item in plan["manager_file_mutations"] if item["path"] == "docs/spec-kit/ADAPTERS.json")
            self.assertIn("explicit-generic-transition", base64.b64decode(binding_mutation["content_b64"]).decode())
            applied = self.run_manager(project, "apply-plan", "--plan", plan_info["path"], "--approve-plan-id", plan_info["plan_id"], "--approve-plan-sha256", plan_info["plan_sha256"], env=env)
            self.assertEqual(json.loads(applied.stdout)["status"], "applied")
            fresh = project / "docs/spec-kit/evidence/fresh.json"
            fresh.write_text(json.dumps({"runtime_id": "vendor.unknown", "integration_key": "generic", "fresh_session": True, "loader_loaded": True, "managed_files_verified": True, "loader_failure": False}) + "\n")
            activation = self.run_manager(project, "plan-activate-binding", "--runtime-id", "vendor.unknown", "--integration-key", "generic", "--verification-evidence", "docs/spec-kit/evidence/fresh.json", env=env)
            activation_info = json.loads(activation.stdout)
            activation_plan = json.loads(Path(activation_info["path"]).read_text())
            self.run_manager(project, "apply-plan", "--plan", activation_info["path"], "--approve-plan-id", activation_info["plan_id"], "--approve-plan-sha256", activation_info["plan_sha256"], env=env)
            adapters = json.loads((project / "docs/spec-kit/ADAPTERS.json").read_text())
            self.assertEqual(adapters["bindings"][0]["verification"]["status"], "active")


if __name__ == "__main__":
    unittest.main()
