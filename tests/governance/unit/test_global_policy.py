from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PLACEHOLDER = "<ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>"


class GlobalPolicyTemplateTests(unittest.TestCase):
    def test_canonical_source_filename_is_uppercase(self) -> None:
        self.assertTrue((ROOT / "GLOBAL_POLICY.md").is_file())
        self.assertFalse((ROOT / "global-policy.md").exists())

    def test_template_has_title_sections_and_placeholder(self) -> None:
        text = (ROOT / "GLOBAL_POLICY.md").read_text(encoding="utf-8")
        self.assertTrue(text.endswith("\n"))
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("<!-- SPEC-KIT-GLOBAL-POLICY:START version="))
        self.assertEqual(lines[1], "")
        self.assertEqual(lines[2], "# Spec Kit Global Policy")
        self.assertEqual(lines[-2], "")
        self.assertEqual(lines[-1], "<!-- SPEC-KIT-GLOBAL-POLICY:END -->")
        self.assertEqual(sum(line.startswith("# ") for line in lines), 1)
        self.assertEqual(sum(line.startswith("## ") for line in lines), 5)
        self.assertEqual(text.count(PLACEHOLDER), 1)
        self.assertIn("SPEC_KIT_GOVERNANCE_SOURCE: " + PLACEHOLDER, text)
        self.assertLessEqual(sum(bool(line.strip()) for line in lines), 40)

    def test_deployment_protocol_exists(self) -> None:
        protocol = ROOT / "docs/GLOBAL_POLICY_DEPLOYMENT.md"
        self.assertTrue(protocol.is_file())
        text = protocol.read_text(encoding="utf-8")
        for required in ("os.link", "no-clobber", "deploy-journal", "outside the markers", "zero writes"):
            self.assertIn(required, text)

    def test_runtime_ignore_marker_is_exact(self) -> None:
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("# SPEC-KIT-GOVERNANCE-RUNTIME:START\n/.spec-kit-governance/\n# SPEC-KIT-GOVERNANCE-RUNTIME:END", text)


if __name__ == "__main__":
    unittest.main()
