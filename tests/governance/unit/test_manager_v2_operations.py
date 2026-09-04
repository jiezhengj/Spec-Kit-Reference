"""Focused contracts for v2 migration and native companion plans."""

from __future__ import annotations

import base64
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "governance/manager"))
import speckit_governance as manager


class ManagerV2OperationTests(unittest.TestCase):
    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")

    def v1_target(self, root: Path, package_version: str = "1.3.0") -> None:
        config = json.loads((ROOT / "governance/project/PROJECT_CONFIG.default.json").read_text(encoding="utf-8"))
        config["schema_version"] = 1
        config.pop("workflow_governance", None)
        config["quality_gates"]["clarify"] = "risk-triggered"
        config["quality_gates"]["checklist"] = "risk-triggered"
        self.write_json(root / "docs/spec-kit/PROJECT_CONFIG.json", config)
        self.write_json(root / "docs/spec-kit/MANIFEST.json", {
            "schema_version": 1,
            "governance_package_version": package_version,
            "policy_version": package_version,
            "reference_version": "2026.08.28",
            "manager_version": package_version,
            "source": {"repository": "test", "revision": "1" * 40, "release": f"v{package_version}", "reviewed_upstream_revision": "2" * 40},
            "specify_compatibility": {"minimum_version": "1.0.4", "tested_version": "1.0.4", "maximum_version_exclusive": None, "approved_install_ref": "2" * 40},
            "paths": {}, "content_sha256": {}, "project_owned_files": [],
            "portable_anchor": {"path": "AGENTS.md", "marker_start": manager.START_MARKER, "marker_end": manager.END_MARKER},
        })

    def test_v2_migration_rejects_non_bridge_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.v1_target(root, "1.2.0")
            with self.assertRaises(manager.GovernanceError) as raised:
                manager.governance_v2_upgrade_mutations(root, {"source_root": str(ROOT), "source_revision": "3" * 40}, "plan-id")
            self.assertEqual(raised.exception.status, "MIGRATION_REQUIRED")

    def test_v2_migration_builds_hash_bound_record_and_preserves_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.v1_target(root)
            sidecar = root / "docs/spec-kit/features/demo/DISCOVERY.md"
            sidecar.parent.mkdir(parents=True)
            sidecar.write_text("user evidence\n", encoding="utf-8")
            snapshot = {"source_root": str(ROOT), "source_revision": "3" * 40}
            mutations, record_rel = manager.governance_v2_upgrade_mutations(root, snapshot, "plan-id")
            by_path = {item["path"]: item for item in mutations}
            config = json.loads(base64.b64decode(by_path["docs/spec-kit/PROJECT_CONFIG.json"]["content_b64"]))
            record = json.loads(base64.b64decode(by_path[record_rel]["content_b64"]))
            manifest = json.loads(base64.b64decode(by_path["docs/spec-kit/MANIFEST.json"]["content_b64"]))
            self.assertEqual(config["schema_version"], 2)
            self.assertEqual(record["plan_id"], "plan-id")
            self.assertRegex(record["plan_binding_sha256"], r"^[0-9a-f]{64}$")
            self.assertIn("docs/spec-kit/features", record["preserved_subtrees"])
            self.assertEqual(manifest["companion"]["extension"], "governance-discovery")
            self.assertEqual(manifest["specify_compatibility"]["minimum_version"], "1.0.4")
            self.assertEqual(manifest["specify_compatibility"]["tested_version"], "1.0.4")
            self.assertEqual(sidecar.read_text(encoding="utf-8"), "user evidence\n")
            self.assertNotIn("docs/spec-kit/features/demo/DISCOVERY.md", by_path)

    def test_companion_plan_uses_independent_104_argv(self) -> None:
        snapshot = {"source_root": str(ROOT), "tree_sha256": "4" * 64}
        with mock.patch.object(manager, "require_companion_cli_contract"), mock.patch.object(
            manager, "companion_allowed_prefixes", return_value=[".specify/", ".agents/skills/"]
        ):
            install = manager.companion_external_mutations(Path("/tmp/project"), snapshot, True)
            remove = manager.companion_external_mutations(Path("/tmp/project"), snapshot, False)
        self.assertEqual([item["argv"][1:3] for item in install], [["extension", "add"], ["preset", "add"], ["workflow", "add"]])
        self.assertEqual(install[1]["argv"][1:4], ["preset", "add", "--dev"])
        self.assertEqual(install[1]["argv"][-2:], ["--priority", "5"])
        self.assertEqual([item["argv"][1:3] for item in remove], [["workflow", "remove"], ["preset", "remove"], ["extension", "remove"]])
        self.assertEqual(remove[-1]["argv"][-1], "--force")
        self.assertTrue(all(item["allowed_path_prefixes"] == [".specify/", ".agents/skills/"] for item in install + remove))

    def test_v2_reference_sync_repairs_cli_compatibility_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.v1_target(root, "2.0.0")
            manifest_path = root / "docs/spec-kit/MANIFEST.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["specify_compatibility"]["tested_version"] = "0.16.6"
            self.write_json(manifest_path, manifest)
            mutations = manager.governance_update_mutations(root, ROOT)
            by_path = {item["path"]: item for item in mutations}
            updated = json.loads(base64.b64decode(by_path["docs/spec-kit/MANIFEST.json"]["content_b64"]))
            self.assertEqual(updated["specify_compatibility"]["minimum_version"], "1.0.4")
            self.assertEqual(updated["specify_compatibility"]["tested_version"], "1.0.4")


if __name__ == "__main__":
    unittest.main()
