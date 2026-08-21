import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class GovernanceSchemaContractTests(unittest.TestCase):
    def test_all_governance_json_is_valid_and_baseline_hashes_match(self):
        for path in (ROOT / "governance").rglob("*.json"):
            with self.subTest(path=path):
                json.loads(path.read_text(encoding="utf-8"))
        baseline = json.loads((ROOT / "governance/capability-baseline.json").read_text(encoding="utf-8"))
        for snapshot in baseline["source_snapshots"]:
            path = ROOT / snapshot["file"]
            self.assertTrue(path.is_file(), snapshot["file"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), snapshot["source_sha256"], snapshot["file"])

    def test_project_config_is_agent_neutral_and_fail_closed(self):
        config = json.loads((ROOT / "governance/project/PROJECT_CONFIG.default.json").read_text(encoding="utf-8"))
        self.assertEqual(config["default_integration"]["policy"], "pinned")
        self.assertIsNone(config["default_integration"]["key"])
        self.assertFalse(config["onboarding"]["allow_unsafe_multi_install"])
        self.assertEqual(config["generic"]["policy"], "deny")
        policy = (ROOT / "governance/project/POLICY.md").read_text(encoding="utf-8").lower()
        for product in ("codex", "claude", "gemini", "trae"):
            self.assertNotIn(product, policy)
        self.assertIn("不得因为方便、权限、路径或冲突降级 generic", policy)

    def test_every_capability_has_a_named_regression(self):
        baseline = json.loads((ROOT / "governance/capability-baseline.json").read_text(encoding="utf-8"))
        required = {name for item in baseline["capabilities"] for name in item.get("tests", [])}
        found = set()
        for path in (ROOT / "tests").rglob("*.py"):
            found.update(re.findall(r"\btest_[A-Za-z0-9_]+\b", path.read_text(encoding="utf-8")))
        self.assertEqual(required - found, set())


if __name__ == "__main__":
    unittest.main()
