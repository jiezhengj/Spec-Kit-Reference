from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
START_RE = re.compile(r"^<!-- SPEC-KIT-GLOBAL-POLICY:START version=(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*) -->$")
END = "<!-- SPEC-KIT-GLOBAL-POLICY:END -->"
PLACEHOLDER = "<ABSOLUTE_PATH_TO_SPEC_KIT_REFERENCE_REPOSITORY>"


class GlobalPolicyTemplateTests(unittest.TestCase):
    def test_canonical_source_filename_is_uppercase(self) -> None:
        self.assertTrue((ROOT / "GLOBAL_POLICY.md").is_file())
        self.assertFalse((ROOT / "global-policy.md").exists())

    def test_template_has_exact_markers_and_placeholder(self) -> None:
        text = (ROOT / "GLOBAL_POLICY.md").read_text(encoding="utf-8")
        self.assertTrue(text.endswith("\n"))
        lines = text.splitlines()
        self.assertEqual(sum(bool(START_RE.fullmatch(line)) for line in lines), 1)
        self.assertEqual(lines.count(END), 1)
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
