"""Release-blocking checks for the bridge and strict governance artifacts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "scripts/build_governance_release.py"
VALIDATE = ROOT / "scripts/validate_governance_release.py"


class GovernedReleaseContractTests(unittest.TestCase):
    def run_builder(self, output: Path, version: str = "2.0.0") -> dict:
        result = subprocess.run(
            [sys.executable, str(BUILD), "--version", version, "--output-dir", str(output)],
            cwd=ROOT,
            check=True,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return json.loads(result.stdout)

    def validate(self, index: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATE), str(index)],
            cwd=ROOT,
            check=check,
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_release_notes_define_bridge_before_strict_upgrade(self) -> None:
        compatibility = (ROOT / "governance/release/COMPATIBILITY.md").read_text(encoding="utf-8")
        changelog = (ROOT / "governance/release/CHANGELOG.md").read_text(encoding="utf-8")
        migration = (ROOT / "docs/PROJECT_GOVERNANCE_MIGRATION.md").read_text(encoding="utf-8")
        for text in (compatibility, changelog, migration):
            self.assertIn("1.3.0", text)
            self.assertIn("2.0.0", text)
            self.assertIn("MIGRATION_REQUIRED", text)
        self.assertLess(compatibility.index("1.3.0"), compatibility.index("2.0.0"))
        self.assertIn("docs/spec-kit/features/**", compatibility)
        self.assertIn("COMPANION_CAPABILITY_UNAVAILABLE", compatibility)

    def test_strict_release_is_deterministic_and_contains_governed_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first_root = Path(directory) / "first"
            second_root = Path(directory) / "second"
            first = self.run_builder(first_root)
            second = self.run_builder(second_root)
            self.assertEqual(first["version"], "2.0.0")
            self.assertEqual(first["portable_artifact"]["sha256"], second["portable_artifact"]["sha256"])
            self.assertEqual(first["extension_artifact"]["sha256"], second["extension_artifact"]["sha256"])
            self.assertEqual(
                (first_root / "latest.json").read_bytes(),
                (second_root / "latest.json").read_bytes(),
            )
            validated = self.validate(first_root / "latest.json")
            self.assertIn("OK", validated.stdout)

            portable = first_root / first["portable_artifact"]["path"]
            extension = first_root / first["extension_artifact"]["path"]
            with zipfile.ZipFile(portable) as portable_zip, zipfile.ZipFile(extension) as extension_zip:
                portable_names = portable_zip.namelist()
                extension_names = extension_zip.namelist()
                required_portable = {
                    "governance/spec-kit-native/bundle.yml",
                    "governance/spec-kit-native/presets/tiny-model-tasks/preset.yml",
                    "governance/spec-kit-native/workflows/governed-sdd/workflow.yml",
                    "governance/schemas/artifact-review.schema.json",
                    "governance/schemas/task-readiness-report.schema.json",
                    "governance/schemas/cold-start-review.schema.json",
                    "governance/schemas/workflow-governance.schema.json",
                    "governance/schemas/project-config-migration-record.schema.json",
                }
                self.assertTrue(required_portable.issubset(portable_names))
                self.assertIn("governance/spec-kit-native/bundle.yml", extension_names)
                metadata = json.loads(portable_zip.read("governance/release/SOURCE_METADATA.json"))
                self.assertEqual(metadata["schema_version"], 2)
                self.assertEqual(metadata["compatibility"]["release_line"], "strict")
                self.assertEqual(metadata["compatibility"]["project_config_schema_version"], 2)
                self.assertTrue(metadata["compatibility"]["requires_bridge_migration"])
                shared = "governance/manager/speckit_governance.py"
                self.assertEqual(portable_zip.read(shared), extension_zip.read(shared))
                self.assertIn(b'version: 2.0.0', extension_zip.read("extension.yml"))
                self.assertIn(b'GOVERNANCE_PACKAGE_VERSION = "2.0.0"', portable_zip.read(shared))

    def test_bridge_release_contains_migration_tools_but_no_strict_policy_or_companion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "bridge"
            manifest = self.run_builder(output, "1.3.0")
            self.validate(output / "latest.json")
            with zipfile.ZipFile(output / manifest["portable_artifact"]["path"]) as portable_zip:
                names = portable_zip.namelist()
                metadata = json.loads(portable_zip.read("governance/release/SOURCE_METADATA.json"))
                self.assertEqual(metadata["compatibility"]["release_line"], "bridge")
                self.assertIn("governance/manager/speckit_governance.py", names)
                self.assertIn("governance/schemas/project-config-migration-record.schema.json", names)
                self.assertIn("governance/project/PROJECT_CONFIG.default.json", names)
                bridge_config = json.loads(portable_zip.read("governance/project/PROJECT_CONFIG.default.json"))
                self.assertEqual(bridge_config["schema_version"], 1)
                self.assertNotIn("workflow_governance", bridge_config)
                self.assertFalse(any(name.startswith("governance/spec-kit-native/") for name in names))
                manager = portable_zip.read("governance/manager/speckit_governance.py")
                self.assertIn(b'GOVERNANCE_PACKAGE_VERSION = "1.3.0"', manager)
                self.assertIn(b'POLICY_VERSION = "1.2.0"', manager)
                self.assertIn(b'MANAGER_VERSION = "1.3.0"', manager)
            with zipfile.ZipFile(output / manifest["extension_artifact"]["path"]) as extension_zip:
                self.assertIn(b'version: 1.3.0', extension_zip.read("extension.yml"))

    def test_validator_rejects_an_altered_release_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "release"
            manifest = self.run_builder(output)
            artifact = output / manifest["portable_artifact"]["path"]
            data = artifact.read_bytes()
            artifact.write_bytes(data + b"tampered")
            result = self.validate(output / "latest.json", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("checksum mismatch", result.stderr)

    def test_release_builder_rejects_non_semantic_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(BUILD), "--version", "2.0", "--output-dir", directory],
                cwd=ROOT,
                check=False,
                text=True,
                encoding="utf-8",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("semantic version", result.stderr)


if __name__ == "__main__":
    unittest.main()
