"""Focused tests for the new project-local Spec Kit updater."""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from unittest.mock import patch

from scripts import spec_kit_component_updater as updater


NOW = datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)


class FakeRunner:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.captures: list[tuple[str, ...]] = []
        self.interactions: list[tuple[str, ...]] = []
        self.capture_results: dict[tuple[str, ...], updater.CommandResult] = {}
        self.interactive_result = updater.CommandResult(1, "network error")
        self.on_interactive = None

    def capture(self, *args: str) -> updater.CommandResult:
        self.captures.append(args)
        result = self.capture_results.get(args, updater.CommandResult(1, "unexpected command"))
        return result() if callable(result) else result

    def interactive(self, *args: str) -> updater.CommandResult:
        self.interactions.append(args)
        if self.on_interactive:
            self.on_interactive(args)
        return self.interactive_result


class VersionTests(unittest.TestCase):
    def test_numeric_versions_compare_by_components(self) -> None:
        self.assertEqual(updater.parse_version("1.0.12"), (1, 0, 12, 0))
        self.assertGreater(updater.parse_version("1.0.12"), updater.parse_version("1.0.9"))
        self.assertIsNone(updater.parse_version("1.0.12rc1"))

    def test_integration_release_proxy_is_fail_closed(self) -> None:
        self.assertEqual(updater.classify_integration_version("1.0.12", "1.0.12"), "current")
        self.assertEqual(updater.classify_integration_version("1.0.12", "1.0.11"), "outdated")
        self.assertEqual(updater.classify_integration_version("1.0.12", "1.0.13"), "future-manifest")
        self.assertEqual(updater.classify_integration_version("1.0.12", "dev"), "unknown")

    def test_self_check_result_parsing(self) -> None:
        self.assertEqual(
            updater.parse_self_check("Up to date: 1.0.12"),
            ("up-to-date", "1.0.12"),
        )
        self.assertEqual(
            updater.parse_self_check("Update available: 1.0.12 → 1.0.13"),
            ("update-available", "1.0.13"),
        )
        self.assertIsNone(updater.parse_self_check("network unavailable"))


class CatalogParsingTests(unittest.TestCase):
    def test_extension_catalog_parser_preserves_source_and_permission(self) -> None:
        output = (
            "Active Extension Catalogs:\n"
            "  official (priority 1)\n"
            "     URL: \n"
            "https://example.test/extensions/catalog.\n"
            "json\n"
            "     Install: install allowed\n"
        )
        parsed = updater.parse_extension_catalogs(output)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0].name, "official")
        self.assertTrue(parsed[0].install_allowed)
        self.assertEqual(parsed[0].url, "https://example.test/extensions/catalog.json")

    def test_workflow_catalog_parser_requires_one_unambiguous_id(self) -> None:
        output = (
            "Workflow Catalog Sources:\n"
            "  [0] default \ufffd\ufffd install allowed\n"
            "      https://raw.githubusercontent.com/github/spec-kit/main/workflows/catalog.\n"
            "json\n"
        )
        parsed = updater.parse_workflow_catalogs(output)
        self.assertEqual(parsed[0].name, "default")
        self.assertEqual(parsed[0].url, updater.OFFICIAL_WORKFLOW_CATALOG)
        search = "Workflows (1):\n  Spec Kit (speckit) v1.0.2\n"
        self.assertEqual(updater.parse_workflow_search_version(search, "speckit"), "1.0.2")
        duplicate = search + "  Other Spec Kit (speckit) v1.0.3\n"
        self.assertIsNone(updater.parse_workflow_search_version(duplicate, "speckit"))

    def test_custom_catalog_override_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            reason = updater.official_catalog_override_reason(
                root,
                kind="workflow",
                environment={"SPECKIT_WORKFLOW_CATALOG_URL": "https://untrusted.test/catalog.json"},
                user_home=root / "home",
            )
            self.assertIn("non-default catalog", reason or "")
            config = root / ".specify" / "workflow-catalogs.yml"
            config.parent.mkdir()
            config.write_text("catalogs: []\n", encoding="utf-8")
            reason = updater.official_catalog_override_reason(
                root,
                kind="workflow",
                environment={},
                user_home=root / "home",
            )
            self.assertIn("custom catalog configuration", reason or "")


class CacheTests(unittest.TestCase):
    def test_only_successful_results_are_cached_and_ttl_is_seven_days(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cache = updater.CacheStore(root, NOW)
            identity = {"cli_version": "1.0.12"}
            cache.record("cli-release", identity=identity, result="failed", detail="offline", remote_check=True)
            self.assertNotIn("cli-release", cache.data["components"])
            cache.record("cli-release", identity=identity, result="up-to-date", detail="1.0.12", remote_check=True)
            self.assertIsNotNone(cache.get_fresh("cli-release", identity))
            cache.save()
            expired = updater.CacheStore(root, NOW + timedelta(days=7))
            self.assertIsNone(expired.get_fresh("cli-release", identity))

    def test_session_gate_is_open_only_for_a_recent_successful_full_check(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            cache = updater.CacheStore(Path(temporary), NOW)
            self.assertFalse(cache.full_check_is_fresh())

            cache.set_full_check("success")
            self.assertTrue(cache.full_check_is_fresh())

            cache.now = NOW + timedelta(days=6, hours=23)
            self.assertTrue(cache.full_check_is_fresh())
            cache.now = NOW + timedelta(days=7)
            self.assertFalse(cache.full_check_is_fresh())

    def test_session_gate_retries_after_incomplete_or_interrupted_check(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            cache = updater.CacheStore(Path(temporary), NOW)
            cache.set_full_check("success")
            self.assertTrue(cache.full_check_is_fresh())

            cache.set_full_check("running")
            self.assertFalse(cache.full_check_is_fresh())
            cache.set_full_check("attention")
            self.assertFalse(cache.full_check_is_fresh())

    def test_session_gate_rejects_invalid_and_future_timestamps(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            cache = updater.CacheStore(Path(temporary), NOW)
            cache.data["last_full_check"] = {
                "status": "success",
                "checked_at_utc": "not-a-timestamp",
            }
            self.assertFalse(cache.full_check_is_fresh())

            cache.set_full_check("success")
            cache.now = NOW - timedelta(seconds=1)
            self.assertFalse(cache.full_check_is_fresh())


class CacheAndSessionGateTests(unittest.TestCase):
    def prepare_project(self, root: Path) -> None:
        registry = root / ".specify" / "workflows" / "workflow-registry.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(json.dumps({"workflows": {}}), encoding="utf-8")

    def make_runner(self, *, self_check: updater.CommandResult) -> FakeRunner:
        runner = FakeRunner(Path("."))
        runner.capture_results.update(
            {
                ("--version",): updater.CommandResult(0, "specify 1.0.12"),
                ("self", "check"): self_check,
                ("integration", "status", "--json"): updater.CommandResult(
                    0, json.dumps({"status": "ok", "installed_integrations": []})
                ),
                ("extension", "list", "--json"): updater.CommandResult(0, "[]"),
            }
        )
        return runner

    def test_successful_full_run_opens_the_seven_day_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.prepare_project(root)
            runner = self.make_runner(
                self_check=updater.CommandResult(0, "Up to date: 1.0.12")
            )
            check = updater.ComponentUpdater(root, runner=runner, now=NOW)
            with patch.object(updater.shutil, "which", return_value="specify"), patch.object(
                updater, "CommandRunner", return_value=runner
            ):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(check.run(), 0)
            self.assertTrue(check.cache.full_check_is_fresh())
            self.assertEqual(check.cache.data["last_full_check"]["status"], "success")
            persisted = updater.CacheStore(root, NOW)
            self.assertTrue(persisted.full_check_is_fresh())

    def test_incomplete_full_run_closes_a_previously_open_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.prepare_project(root)
            previous = updater.CacheStore(root, NOW)
            previous.set_full_check("success")
            previous.save()
            runner = self.make_runner(
                self_check=updater.CommandResult(1, "network error")
            )
            check = updater.ComponentUpdater(root, runner=runner, now=NOW)
            with patch.object(updater.shutil, "which", return_value="specify"), patch.object(
                updater, "CommandRunner", return_value=runner
            ):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(check.run(), 2)
            self.assertFalse(check.cache.full_check_is_fresh())
            self.assertEqual(check.cache.data["last_full_check"]["status"], "attention")
            persisted = updater.CacheStore(root, NOW)
            self.assertFalse(persisted.full_check_is_fresh())

    def test_cli_update_waiting_for_user_approval_still_opens_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.prepare_project(root)
            runner = self.make_runner(
                self_check=updater.CommandResult(
                    0, "Update available: 1.0.12 → 1.0.13"
                )
            )
            check = updater.ComponentUpdater(root, runner=runner, now=NOW)
            with patch.object(updater.shutil, "which", return_value="specify"), patch.object(
                updater, "CommandRunner", return_value=runner
            ):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(check.run(), 2)
            self.assertTrue(check.cache.full_check_is_fresh())
            self.assertEqual(check.cache.data["last_full_check"]["status"], "success")

    def test_cache_identity_change_invalidates_a_successful_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            cache = updater.CacheStore(Path(temporary), NOW)
            cache.record(
                "extension:assess",
                identity={"cli_version": "1.0.12", "local_version": "1.0.0"},
                result="up-to-date",
                detail="1.0.0",
                remote_check=True,
            )
            self.assertIsNone(
                cache.get_fresh(
                    "extension:assess",
                    {"cli_version": "1.0.12", "local_version": "1.0.1"},
                )
            )

    def test_documented_gitignore_rule_excludes_only_root_cache_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(
                "/.agent-state/spec_kit_component_update_cache.json\n",
                encoding="utf-8",
            )
            root_cache = root / ".agent-state" / "spec_kit_component_update_cache.json"
            root_cache.parent.mkdir()
            root_cache.write_text("{}\n", encoding="utf-8")
            ignored = subprocess.run(
                ["git", "check-ignore", "-q", ".agent-state/spec_kit_component_update_cache.json"],
                cwd=root,
                check=False,
            )
            self.assertEqual(ignored.returncode, 0)

            nested_cache = root / "nested" / ".agent-state" / "spec_kit_component_update_cache.json"
            nested_cache.parent.mkdir(parents=True)
            nested_cache.write_text("{}\n", encoding="utf-8")
            not_ignored = subprocess.run(
                ["git", "check-ignore", "-q", "nested/.agent-state/spec_kit_component_update_cache.json"],
                cwd=root,
                check=False,
            )
            self.assertEqual(not_ignored.returncode, 1)


class IntegrationUpdaterTests(unittest.TestCase):
    def test_rejects_unhealthy_integration_status(self) -> None:
        with self.assertRaises(ValueError):
            updater.parse_installed_integrations(
                json.dumps({"status": "error", "installed_integrations": ["claude-code"]})
            )

    def prepare_project(self, root: Path, version: str) -> Path:
        specify = root / ".specify"
        integration_dir = specify / "integrations"
        integration_dir.mkdir(parents=True)
        (specify / "integration.json").write_text(
            json.dumps({"installed_integrations": ["claude-code"]}), encoding="utf-8"
        )
        manifest = integration_dir / "claude-code.manifest.json"
        manifest.write_text(json.dumps({"integration": "claude-code", "version": version}), encoding="utf-8")
        return manifest

    def test_discovers_any_installed_integration_key_without_codex_assumption(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = self.prepare_project(root, "1.0.11")
            runner = FakeRunner(root)
            runner.capture_results[("integration", "status", "--json")] = updater.CommandResult(
                0, json.dumps({"status": "ok", "installed_integrations": ["claude-code"]})
            )

            def upgrade(args: tuple[str, ...]) -> None:
                self.assertEqual(args, ("integration", "upgrade", "claude-code", "--force"))
                manifest.write_text(json.dumps({"integration": "claude-code", "version": "1.0.12"}), encoding="utf-8")

            runner.interactive_result = updater.CommandResult(0, "upgraded")
            runner.on_interactive = upgrade
            check = updater.ComponentUpdater(root, runner=runner, now=NOW)
            with contextlib.redirect_stdout(io.StringIO()):
                check.check_integrations("1.0.12")
            self.assertEqual(runner.interactions, [("integration", "upgrade", "claude-code", "--force")])
            self.assertEqual(json.loads(manifest.read_text(encoding="utf-8"))["version"], "1.0.12")

    def test_current_integration_is_not_refreshed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.prepare_project(root, "1.0.12")
            runner = FakeRunner(root)
            runner.capture_results[("integration", "status", "--json")] = updater.CommandResult(
                0, json.dumps({"status": "ok", "installed_integrations": ["claude-code"]})
            )
            check = updater.ComponentUpdater(root, runner=runner, now=NOW)
            with contextlib.redirect_stdout(io.StringIO()):
                check.check_integrations("1.0.12")
            self.assertEqual(runner.interactions, [])


class FailedCheckTests(unittest.TestCase):
    def test_extension_failure_is_not_recorded_as_a_fresh_check(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".specify").mkdir()
            runner = FakeRunner(root)
            runner.capture_results[("extension", "list", "--json")] = updater.CommandResult(
                0,
                json.dumps([
                    {
                        "id": "assess",
                        "version": "1.0.0",
                        "source": {"kind": "catalog", "catalog": "official"},
                    }
                ]),
            )
            runner.capture_results[("extension", "catalog", "list")] = updater.CommandResult(
                0,
                "Active Extension Catalogs:\n"
                "  official (priority 1)\n"
                f"     URL: {updater.OFFICIAL_EXTENSION_CATALOG}\n"
                "     Install: install allowed\n",
            )
            runner.interactive_result = updater.CommandResult(1, "catalog unavailable")
            check = updater.ComponentUpdater(root, runner=runner, now=NOW, recheck=True)
            identity = {
                "cli_version": "1.0.12",
                "local_version": "1.0.0",
                "catalog_url": updater.OFFICIAL_EXTENSION_CATALOG,
            }
            check.cache.record(
                "extension:assess",
                identity=identity,
                result="up-to-date",
                detail="old successful result",
                remote_check=True,
            )
            check.cache.save()
            with patch.object(updater, "official_catalog_override_reason", return_value=None):
                with contextlib.redirect_stdout(io.StringIO()):
                    check.check_extensions("1.0.12")
            self.assertIsNone(check.cache.get_fresh(
                "extension:assess",
                {
                    **identity,
                },
            ))
            self.assertNotIn("extension:assess", check.cache.data["components"])


class ExtensionUpdaterTests(unittest.TestCase):
    def make_runner(self, root: Path, versions: list[str]) -> FakeRunner:
        runner = FakeRunner(root)
        records = iter(versions)

        def list_extensions() -> updater.CommandResult:
            version = next(records)
            return updater.CommandResult(
                0,
                json.dumps(
                    [
                        {
                            "id": "assess",
                            "version": version,
                            "source": {"kind": "local"},
                        }
                    ]
                ),
            )

        runner.capture_results[("extension", "list", "--json")] = list_extensions
        runner.capture_results[("extension", "catalog", "list")] = updater.CommandResult(
            0,
            "Active Extension Catalogs:\n"
            "  official (priority 1)\n"
            f"     URL: {updater.OFFICIAL_EXTENSION_CATALOG}\n"
            "     Install: install allowed\n",
        )
        return runner

    def test_up_to_date_extension_result_is_cached_and_reused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".specify").mkdir()
            runner = self.make_runner(root, ["1.0.0", "1.0.0"])
            runner.interactive_result = updater.CommandResult(
                0, "✓ assess: Up to date (v1.0.0)\nAll extensions are up to date!"
            )
            with patch.object(updater, "official_catalog_override_reason", return_value=None):
                first = updater.ComponentUpdater(root, runner=runner, now=NOW, recheck=True)
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    first.check_extensions("1.0.12")
                first.cache.save()
                self.assertEqual(first.cache.data["components"]["extension:assess"]["result"], "up-to-date")
                self.assertFalse(first.attention)
                self.assertFalse(first.incomplete)
                self.assertNotIn("来源未知", output.getvalue())

                second = updater.ComponentUpdater(root, runner=runner, now=NOW + timedelta(days=6))
                with contextlib.redirect_stdout(io.StringIO()):
                    second.check_extensions("1.0.12")
            self.assertEqual(runner.interactions, [("extension", "update", "assess")])

    def test_extension_update_is_cached_only_after_local_version_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".specify").mkdir()
            runner = self.make_runner(root, ["1.0.0", "1.0.1"])
            runner.interactive_result = updater.CommandResult(
                0, "Successfully updated 1 extension(s)"
            )
            with patch.object(updater, "official_catalog_override_reason", return_value=None):
                check = updater.ComponentUpdater(root, runner=runner, now=NOW, recheck=True)
                with contextlib.redirect_stdout(io.StringIO()):
                    check.check_extensions("1.0.12")
            entry = check.cache.data["components"]["extension:assess"]
            self.assertEqual(entry["result"], "updated")
            self.assertEqual(entry["identity"]["local_version"], "1.0.1")
            self.assertEqual(runner.interactions, [("extension", "update", "assess")])


class PromptTests(unittest.TestCase):
    def test_only_recognized_official_update_prompt_is_confirmed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runner = updater.CommandRunner(sys.executable, Path(temporary))
            with contextlib.redirect_stdout(io.StringIO()):
                result = runner.interactive(
                    "-c",
                    "import sys; print('Update these extensions? [y/N]: ', end='', flush=True); "
                    "print('ANSWER=' + sys.stdin.readline().strip())",
                )
            self.assertEqual(result.returncode, 0)
            self.assertIn("ANSWER=y", result.output)

    def test_unrecognized_confirmation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runner = updater.CommandRunner(sys.executable, Path(temporary))
            with contextlib.redirect_stdout(io.StringIO()):
                result = runner.interactive(
                    "-c",
                    "import sys; print('Overwrite project settings? [y/N]: ', end='', flush=True); "
                    "print('ANSWER=' + sys.stdin.readline().strip())",
                )
            self.assertEqual(result.returncode, 0)
            self.assertIn("ANSWER=n", result.output)


class CommandTimeoutTests(unittest.TestCase):
    def test_capture_terminates_a_timed_out_cli_command(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runner = updater.CommandRunner(
                sys.executable,
                Path(temporary),
                timeout_seconds=0.2,
            )
            with contextlib.redirect_stdout(io.StringIO()):
                result = runner.capture("-c", "import time; time.sleep(2)")
            self.assertEqual(result.returncode, 124)
            self.assertIn("已终止", result.output)

    def test_interactive_terminates_a_timed_out_cli_command(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            runner = updater.CommandRunner(
                sys.executable,
                Path(temporary),
                timeout_seconds=0.2,
            )
            with contextlib.redirect_stdout(io.StringIO()):
                result = runner.interactive("-c", "import time; time.sleep(2)")
            self.assertEqual(result.returncode, 124)
            self.assertIn("已终止", result.output)


class WorkflowUpdaterTests(unittest.TestCase):
    def test_successful_no_update_result_is_reused_for_seven_days(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflows_dir = root / ".specify" / "workflows"
            workflows_dir.mkdir(parents=True)
            registry_path = workflows_dir / "workflow-registry.json"
            registry_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "workflows": {
                            "speckit": {"version": "1.0.1", "source": "bundled"}
                        },
                    }
                ),
                encoding="utf-8",
            )
            runner = FakeRunner(root)
            runner.capture_results[("workflow", "catalog", "list")] = updater.CommandResult(
                0,
                "Workflow Catalog Sources:\n"
                "  [0] default — install allowed\n"
                f"      {updater.OFFICIAL_WORKFLOW_CATALOG}\n",
            )
            runner.capture_results[("workflow", "info", "speckit")] = updater.CommandResult(
                0, "Spec Kit (speckit)\n  Version:     1.0.1\n"
            )
            runner.capture_results[("workflow", "search", "speckit")] = updater.CommandResult(
                0, "Workflows (1):\n  Spec Kit (speckit) v1.0.1\n"
            )

            with patch.object(updater, "official_catalog_override_reason", return_value=None):
                first = updater.ComponentUpdater(root, runner=runner, now=NOW)
                with contextlib.redirect_stdout(io.StringIO()):
                    first.check_workflows("1.0.12")
                first.cache.save()
                self.assertIn("workflow:speckit", first.cache.data["components"])

                runner.captures.clear()
                second = updater.ComponentUpdater(
                    root,
                    runner=runner,
                    now=NOW + timedelta(days=6),
                )
                with contextlib.redirect_stdout(io.StringIO()):
                    second.check_workflows("1.0.12")
                self.assertNotIn(("workflow", "info", "speckit"), runner.captures)
                self.assertNotIn(("workflow", "search", "speckit"), runner.captures)

    def test_bundled_workflow_updates_only_after_official_catalog_is_newer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflows_dir = root / ".specify" / "workflows"
            workflows_dir.mkdir(parents=True)
            registry_path = workflows_dir / "workflow-registry.json"

            def write_registry(version: str, source: str = "bundled") -> None:
                registry_path.write_text(
                    json.dumps({"workflows": {"speckit": {"version": version, "source": source}}}),
                    encoding="utf-8",
                )

            write_registry("1.0.1")
            runner = FakeRunner(root)
            runner.capture_results[("workflow", "catalog", "list")] = updater.CommandResult(
                0,
                "  [0] default — install allowed\n"
                f"      {updater.OFFICIAL_WORKFLOW_CATALOG}\n",
            )
            info_versions = iter(("1.0.1", "1.0.2"))
            runner.capture_results[("workflow", "info", "speckit")] = lambda: updater.CommandResult(
                0, f"  Version:     {next(info_versions)}\n"
            )
            runner.capture_results[("workflow", "search", "speckit")] = updater.CommandResult(
                0, "  Spec Kit (speckit) v1.0.2\n"
            )
            runner.interactive_result = updater.CommandResult(0, "Workflow installed")
            runner.on_interactive = lambda args: write_registry("1.0.2", "catalog")

            with patch.object(updater, "official_catalog_override_reason", return_value=None):
                check = updater.ComponentUpdater(root, runner=runner, now=NOW)
                with contextlib.redirect_stdout(io.StringIO()):
                    check.check_workflows("1.0.12")
            self.assertEqual(runner.interactions, [("workflow", "add", "speckit")])
            entry = check.cache.data["components"]["workflow:speckit"]
            self.assertEqual(entry["result"], "updated")
            self.assertEqual(entry["identity"]["local_version"], "1.0.2")

    def test_catalog_workflow_uses_update_command_when_newer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workflows_dir = root / ".specify" / "workflows"
            workflows_dir.mkdir(parents=True)
            registry_path = workflows_dir / "workflow-registry.json"
            registry_path.write_text(
                json.dumps({"workflows": {"speckit": {"version": "1.0.1", "source": "catalog"}}}),
                encoding="utf-8",
            )
            runner = FakeRunner(root)
            runner.capture_results[("workflow", "catalog", "list")] = updater.CommandResult(
                0,
                "  [0] default — install allowed\n"
                f"      {updater.OFFICIAL_WORKFLOW_CATALOG}\n",
            )
            info_versions = iter(("1.0.1", "1.0.2"))
            runner.capture_results[("workflow", "info", "speckit")] = lambda: updater.CommandResult(
                0, f"  Version: {next(info_versions)}\n"
            )
            runner.capture_results[("workflow", "search", "speckit")] = updater.CommandResult(
                0, "  Spec Kit (speckit) v1.0.2\n"
            )
            runner.interactive_result = updater.CommandResult(0, "workflow update succeeded")

            with patch.object(updater, "official_catalog_override_reason", return_value=None):
                check = updater.ComponentUpdater(root, runner=runner, now=NOW, recheck=True)
                with contextlib.redirect_stdout(io.StringIO()):
                    check.check_workflows("1.0.12")
            self.assertEqual(runner.interactions, [("workflow", "update", "speckit")])
            self.assertEqual(check.cache.data["components"]["workflow:speckit"]["result"], "updated")


if __name__ == "__main__":
    unittest.main()
