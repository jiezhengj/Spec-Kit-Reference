from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class UpstreamCheckerContractTests(unittest.TestCase):
    def test_checker_keeps_read_only_and_exit_contract(self) -> None:
        source = (ROOT / "scripts/check_upstream.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        self.assertIn("--no-fetch", source)
        self.assertIn("return 0", source)
        self.assertIn("return 2", source)
        self.assertIn("sys.exit(1)", source)
        self.assertNotIn("write_text", source)
        self.assertNotIn("unlink", source)
        self.assertIsNotNone(tree)


if __name__ == "__main__":
    unittest.main()
