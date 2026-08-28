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
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=check,
            env=env,
        )

    def test_bootstrap_plan_apply_is_self_describing(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            result = self.run_manager(
                project, "plan-governance-bootstrap", "--source", str(ROOT),
                "--context-anchor", "runtime/project-rules.txt",
            )
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
            self.assertEqual(manifest["portable_anchor"]["path"], "runtime/project-rules.txt")
            self.assertTrue((project / "runtime/project-rules.txt").is_file())
            loader = (project / "runtime/project-rules.txt").read_text(encoding="utf-8")
            self.assertIn("方案可以", loader)
            self.assertIn(".specify/**", loader)
            self.assertIn("does not authorize direct", loader)
            verified = json.loads(self.run_manager(project, "verify").stdout)
            self.assertEqual(verified["status"], "READY")

    def test_bootstrap_preserves_existing_managed_loader_and_user_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            anchor = project / ".unlisted-agent/rules.txt"
            anchor.parent.mkdir()
            existing = b"# project rules\n\n" + manager.marker_loader().encode("utf-8")
            anchor.write_bytes(existing)
            bootstrap = json.loads(self.run_manager(
                project, "plan-governance-bootstrap", "--source", str(ROOT),
                "--context-anchor", ".unlisted-agent/rules.txt",
            ).stdout)
            self.run_manager(project, "apply-plan", "--plan", bootstrap["path"], "--approve-plan-id", bootstrap["plan_id"], "--approve-plan-sha256", bootstrap["plan_sha256"])
            self.assertEqual(anchor.read_bytes(), existing)

    def test_bootstrap_only_appends_to_existing_unmanaged_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            anchor = project / "vendor/context.rules"
            anchor.parent.mkdir()
            existing = b"# Project-owned rules\n\nKeep this exact text and byte order."
            anchor.write_bytes(existing)
            bootstrap = json.loads(self.run_manager(
                project, "plan-governance-bootstrap", "--source", str(ROOT),
                "--context-anchor", "vendor/context.rules",
            ).stdout)
            self.run_manager(project, "apply-plan", "--plan", bootstrap["path"], "--approve-plan-id", bootstrap["plan_id"], "--approve-plan-sha256", bootstrap["plan_sha256"])
            result = anchor.read_bytes()
            self.assertTrue(result.startswith(existing))
            self.assertEqual(result.count(manager.START_MARKER.encode("utf-8")), 1)
            self.assertEqual(result.count(manager.END_MARKER.encode("utf-8")), 1)

    def test_update_reminder_requires_only_specify_project_and_preserves_upstream_files(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            (project / ".specify").mkdir()
            (project / ".specify/feature.json").write_text('{"feature":"demo"}\n', encoding="utf-8")
            (project / "specs").mkdir()
            (project / "specs/demo.md").write_text("upstream spec\n", encoding="utf-8")
            anchor = project / ".agent/context.md"
            anchor.parent.mkdir()
            original_anchor = b"# Agent rules\n\nKeep these bytes exactly.\n"
            anchor.write_bytes(original_anchor)
            fake_bin = project / "bin"
            self.create_fake_specify(
                fake_bin,
                "import json\n"
                "import sys\n"
                "args = sys.argv[1:]\n"
                "if not args or args[0] in ('--version', 'version'):\n"
                "    print('1.0.0')\n"
                "    sys.exit(0)\n"
                "if len(args) >= 2 and args[0] == 'integration' and args[1] == 'status':\n"
                "    print(json.dumps({'installed_integrations': [], 'default_integration': None}))\n"
                "    sys.exit(0)\n"
                "sys.exit(0)\n",
            )
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
            before_spec = (project / ".specify/feature.json").read_bytes()
            before_specs = (project / "specs/demo.md").read_bytes()
            result = self.run_manager(
                project,
                "plan-install-update-reminder",
                "--context-anchor", ".agent/context.md",
                check=False,
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            plan_info = json.loads(result.stdout)
            plan = json.loads(Path(plan_info["path"]).read_text(encoding="utf-8"))
            self.assertEqual([item["path"] for item in plan["manager_file_mutations"]], [".agent/context.md"])
            self.assertEqual(plan["manager_file_mutations"][0]["action"], "append-managed-update-reminder")
            self.assertEqual(plan["external_cli_mutations"], [])
            self.assertIsNone(plan["manifest_sha256"])
            self.assertFalse((project / "docs/spec-kit").exists())
            self.assertFalse((project / "tools").exists())
            applied = self.run_manager(
                project,
                "apply-plan",
                "--plan", plan_info["path"],
                "--approve-plan-id", plan_info["plan_id"],
                "--approve-plan-sha256", plan_info["plan_sha256"],
                env=env,
            )
            self.assertEqual(json.loads(applied.stdout)["status"], "applied")
            self.assertEqual((project / ".specify/feature.json").read_bytes(), before_spec)
            self.assertEqual((project / "specs/demo.md").read_bytes(), before_specs)
            self.assertTrue(anchor.read_bytes().startswith(original_anchor))
            reminder = anchor.read_text(encoding="utf-8")
            self.assertEqual(reminder.count(manager.UPDATE_REMINDER_START_MARKER), 1)
            self.assertEqual(reminder.count(manager.UPDATE_REMINDER_END_MARKER), 1)
            self.assertIn("specify self check", reminder)
            self.assertIn("specify self upgrade", reminder)
            self.assertNotIn(manager.START_MARKER, reminder)

    def test_update_reminder_upsert_preserves_existing_governance_loader(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            anchor = project / "rules/context.md"
            anchor.parent.mkdir(parents=True)
            original = b"# User rules\r\n\r\n" + manager.marker_loader().encode("utf-8") + b"\r\nTail stays exact."
            anchor.write_bytes(original)
            reminder = manager.update_reminder_loader().encode("utf-8")
            updated = manager.append_update_reminder(original, reminder)
            self.assertTrue(updated.startswith(b"# User rules\r\n\r\n"))
            self.assertTrue(updated.startswith(original))
            self.assertIn(manager.START_MARKER.encode("utf-8"), updated)
            self.assertEqual(updated.count(manager.UPDATE_REMINDER_START_MARKER.encode("utf-8")), 1)
            self.assertEqual(manager.append_update_reminder(updated, reminder), updated)

    def test_any_declared_anchor_rejects_replace_or_create_mutations(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            anchor = project / "custom-agent.instructions"
            anchor.write_text("project rules\n", encoding="utf-8")
            for action in ("create", "replace"):
                with self.assertRaises(manager.GovernanceError) as raised:
                    manager.file_mutation(
                        project, "custom-agent.instructions", b"replacement\n", action,
                        protected_anchor=True,
                    )
                self.assertEqual(raised.exception.status, "PROJECT_RULES_PROTECTED")

    def test_bootstrap_requires_runtime_or_user_supplied_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            result = self.run_manager(project, "plan-governance-bootstrap", "--source", str(ROOT), check=False)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stderr)["status"], "CONTEXT_ANCHOR_UNKNOWN")

    def test_runtime_supplied_anchor_is_supported_without_product_catalog(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            env = os.environ.copy()
            env["SPEC_KIT_CONTEXT_ANCHOR"] = ".unknown-runtime/project.instructions"
            result = self.run_manager(project, "plan-governance-bootstrap", "--source", str(ROOT), env=env)
            plan = json.loads(Path(json.loads(result.stdout)["path"]).read_text())
            anchor_mutation = next(item for item in plan["manager_file_mutations"] if item.get("protected_anchor"))
            self.assertEqual(anchor_mutation["path"], ".unknown-runtime/project.instructions")
            self.assertEqual(anchor_mutation["action"], "append-managed-loader")

    def test_plan_validation_protects_declared_anchor_without_filename_knowledge(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            mutation = manager.file_mutation(project, "vendor/rules.conf", b"replacement\n")
            plan = manager.make_plan(
                project, "plan-governance-bootstrap", [mutation],
                context_anchor="vendor/rules.conf",
            )
            with self.assertRaises(manager.GovernanceError) as raised:
                manager.validate_plan_shape(plan)
            self.assertEqual(raised.exception.status, "PROJECT_RULES_PROTECTED")

    def test_manager_rejects_upstream_owned_mutations(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            for protected_path in (
                ".specify/templates/spec-template.md",
                ".specify/memory/constitution.md",
                "specs/demo/plan.md",
                ".claude/commands/specify.md",
            ):
                mutation = manager.file_mutation(project, protected_path, b"must not be manager-owned\n")
                plan = manager.make_plan(
                    project,
                    "plan-governance-bootstrap",
                    [mutation],
                    context_anchor="runtime/project-rules.txt",
                )
                with self.assertRaises(manager.GovernanceError) as raised:
                    manager.validate_plan_shape(plan)
                self.assertEqual(raised.exception.status, "REFERENCE_OWNERSHIP_VIOLATION")

    def test_update_reminder_cannot_treat_spec_ownership_as_context_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            mutation = manager.file_mutation(
                project,
                ".specify/context.md",
                manager.update_reminder_loader().encode("utf-8"),
                "append-managed-update-reminder",
                protected_anchor=True,
            )
            plan = manager.make_plan(
                project,
                "plan-install-update-reminder",
                [mutation],
                context_anchor=".specify/context.md",
            )
            with self.assertRaises(manager.GovernanceError) as raised:
                manager.validate_plan_shape(plan)
            self.assertEqual(raised.exception.status, "REFERENCE_OWNERSHIP_VIOLATION")

    def test_explicit_and_runtime_anchor_conflict_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            env = os.environ.copy()
            env["SPEC_KIT_CONTEXT_ANCHOR"] = "runtime/rules.txt"
            result = self.run_manager(
                project, "plan-governance-bootstrap", "--source", str(ROOT),
                "--context-anchor", "user/rules.txt", check=False, env=env,
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stderr)["status"], "IDENTITY_CONFLICT")

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

    def create_fake_specify(self, bin_dir: Path, py_body: str) -> None:
        bin_dir.mkdir(parents=True, exist_ok=True)
        py_script = bin_dir / "fake_specify.py"
        py_script.write_text(py_body, encoding="utf-8")
        sh_script = bin_dir / "specify"
        sh_script.write_text(f"#!/bin/sh\nexec \"{sys.executable}\" \"{py_script}\" \"$@\"\n", encoding="utf-8")
        sh_script.chmod(0o755)
        if os.name == "nt":
            cmd_script = bin_dir / "specify.cmd"
            cmd_script.write_text(f'@"{sys.executable}" "{py_script}" %*\n', encoding="utf-8")
            bat_script = bin_dir / "specify.bat"
            bat_script.write_text(f'@"{sys.executable}" "{py_script}" %*\n', encoding="utf-8")

    def test_native_cli_failure_is_a_blocker_not_generic(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / ".specify").mkdir()
            fake_bin = project / "bin"
            self.create_fake_specify(fake_bin, "import sys\nsys.exit(7)\n")
            old_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{fake_bin}{os.pathsep}{old_path}"
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
            bootstrap = json.loads(self.run_manager(
                project, "plan-governance-bootstrap", "--source", str(ROOT),
                "--context-anchor", "project.runtime-rules",
            ).stdout)
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
            py_body = (
                "import sys\n"
                "from pathlib import Path\n\n"
                "args = sys.argv[1:]\n"
                "if not args or args[0] in ('--version', 'version'):\n"
                "    print('0.16.6.dev0')\n"
                "    sys.exit(0)\n"
                "if args[0] == 'init':\n"
                "    p = Path('.specify')\n"
                "    p.mkdir(parents=True, exist_ok=True)\n"
                "    (p / 'state.txt').write_text('initialized\\n', encoding='utf-8')\n"
                "    sys.exit(0)\n"
                "if len(args) >= 2 and args[0] == 'integration' and args[1] == 'status':\n"
                "    print('{\"installed_integrations\":[{\"key\":\"native-key\"}],\"default_integration\":{\"key\":\"native-key\"}}')\n"
                "    sys.exit(0)\n"
                "sys.exit(0)\n"
            )
            self.create_fake_specify(fake_bin, py_body)
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
            anchor_path = project / ".workbuddy/context.md"
            anchor_path.parent.mkdir()
            original_anchor = b"# Workbuddy project rules\n\nPreserve these bytes exactly.\n"
            anchor_path.write_bytes(original_anchor)
            bootstrap = json.loads(self.run_manager(
                project, "plan-governance-bootstrap", "--source", str(ROOT),
                "--context-anchor", ".workbuddy/context.md", env=env,
            ).stdout)
            self.run_manager(
                project, "apply-plan", "--plan", bootstrap["path"],
                "--approve-plan-id", bootstrap["plan_id"],
                "--approve-plan-sha256", bootstrap["plan_sha256"], env=env,
            )
            result = self.run_manager(
                project, "plan-init",
                "--runtime-id", "workbuddy.runtime",
                "--integration-key", "native-key",
                "--context-anchor", ".workbuddy/context.md",
                "--documentation-language", "mi-NZ",
                "--force",
                env=env,
            )
            info = json.loads(result.stdout)
            plan = json.loads(Path(info["path"]).read_text())
            self.assertEqual(plan["rehearsal"]["argv"][-1], "native-key")
            self.assertIn(".specify/state.txt", plan["rehearsal"]["changed_files"])
            self.assertEqual(plan["documentation_language"], "mi-NZ")
            anchor_mutation = next(
                item for item in plan["manager_file_mutations"]
                if item["path"] == ".workbuddy/context.md"
            )
            self.assertTrue(anchor_mutation["protected_anchor"])
            self.assertIn(
                "Project documentation language: `mi-NZ`.",
                base64.b64decode(anchor_mutation["content_b64"]).decode("utf-8"),
            )
            self.assertFalse((project / ".specify").exists())
            applied = self.run_manager(
                project, "apply-plan", "--plan", info["path"],
                "--approve-plan-id", info["plan_id"],
                "--approve-plan-sha256", info["plan_sha256"], check=False, env=env,
            )
            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertEqual(json.loads(applied.stdout)["status"], "applied")
            config = json.loads((project / "docs/spec-kit/PROJECT_CONFIG.json").read_text())
            self.assertEqual(config["documentation"]["language_tag"], "mi-NZ")
            self.assertEqual(config["documentation"]["selection_source"], "explicit-user-selection")
            manifest = json.loads((project / "docs/spec-kit/MANIFEST.json").read_text())
            self.assertEqual(
                manifest["content_sha256"]["docs/spec-kit/PROJECT_CONFIG.json"],
                manager.sha256_file(project / "docs/spec-kit/PROJECT_CONFIG.json"),
            )
            self.assertTrue(anchor_path.read_bytes().startswith(original_anchor))
            anchor = anchor_path.read_text()
            self.assertIn("Project documentation language: `mi-NZ`.", anchor)
            self.assertFalse((project / "AGENTS.md").exists())
            for child in fake_bin.iterdir():
                child.unlink()
            fake_bin.rmdir()

    def test_plan_init_requires_user_selected_documentation_language(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            fake_bin = project / "bin"
            py_body = (
                "import sys\n"
                "args = sys.argv[1:]\n"
                "if not args or args[0] in ('--version', 'version'):\n"
                "    print('0.16.6.dev0')\n"
                "sys.exit(0)\n"
            )
            self.create_fake_specify(fake_bin, py_body)
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
            common = (
                "plan-init", "--runtime-id", "unlisted.runtime",
                "--integration-key", "native-key", "--context-anchor", "rules/context.md",
            )
            missing = self.run_manager(project, *common, check=False, env=env)
            self.assertEqual(json.loads(missing.stderr)["status"], "DOCUMENTATION_LANGUAGE_REQUIRED")
            invalid = self.run_manager(
                project, *common, "--documentation-language", "not a language", check=False, env=env,
            )
            self.assertEqual(json.loads(invalid.stderr)["status"], "DOCUMENTATION_LANGUAGE_INVALID")
            no_runtime = self.run_manager(
                project, "plan-init", "--integration-key", "native-key",
                "--context-anchor", "rules/context.md",
                "--documentation-language", "en", check=False, env=env,
            )
            self.assertEqual(json.loads(no_runtime.stderr)["status"], "IDENTITY_UNKNOWN")
            no_anchor = self.run_manager(
                project, "plan-init", "--runtime-id", "unlisted.runtime",
                "--integration-key", "native-key",
                "--documentation-language", "en", check=False, env=env,
            )
            self.assertEqual(json.loads(no_anchor.stderr)["status"], "CONTEXT_ANCHOR_UNKNOWN")

    def test_generic_transition_requires_attestation_and_stays_non_native(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            bootstrap = json.loads(self.run_manager(
                project, "plan-governance-bootstrap", "--source", str(ROOT),
                "--context-anchor", "project.runtime-rules",
            ).stdout)
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
                "specify_version": "0.16.6",
                "catalog_evidence": "docs/spec-kit/evidence/catalog.txt",
                "catalog_evidence_sha256": hashlib.sha256(catalog.read_bytes()).hexdigest(),
                "reviewed_by_current_operator": True,
                "conclusion": "no-native-integration-found-for-runtime",
            }) + "\n")
            anchor_evidence = evidence_dir / "anchor.json"
            anchor_evidence.write_text(json.dumps({
                "anchor_path": ".unknown-runtime/project.instructions",
                "format": "markdown",
                "review_conclusion": "markdown loader anchor reviewed",
            }) + "\n")
            fake_bin = project / "bin"
            py_body = (
                "import sys\n"
                "from pathlib import Path\n\n"
                "args = sys.argv[1:]\n"
                "if not args or args[0] in ('--version', 'version'):\n"
                "    print('0.16.6')\n"
                "    sys.exit(0)\n"
                "if len(args) >= 2 and args[0] == 'integration' and args[1] == 'status':\n"
                "    print('{\"installed_integrations\":[]}')\n"
                "    sys.exit(0)\n"
                "if len(args) >= 2 and args[0] == 'integration' and args[1] == 'install':\n"
                "    p = Path('.example-commands')\n"
                "    p.mkdir(parents=True, exist_ok=True)\n"
                "    (p / 'workflow.md').write_text('command\\n', encoding='utf-8')\n"
                "    sys.exit(0)\n"
                "sys.exit(0)\n"
            )
            self.create_fake_specify(fake_bin, py_body)
            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
            result = self.run_manager(
                project,
                "plan-onboard",
                "--runtime-id", "vendor.unknown",
                "--integration-key", "generic",
                "--attestation", "docs/spec-kit/evidence/no-native.json",
                "--commands-dir", ".example-commands",
                "--context-anchor", ".unknown-runtime/project.instructions",
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
