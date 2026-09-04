"""Behavioral fixtures for the v2 review and tiny-model readiness gates."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "governance/manager"))
import speckit_governance as manager


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class GovernedReadinessContractTests(unittest.TestCase):
    def write_json(self, path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")

    def make_v2_feature(self, root: Path) -> tuple[dict, dict]:
        config = json.loads((ROOT / "governance/project/PROJECT_CONFIG.default.json").read_text(encoding="utf-8"))
        self.write_json(root / "docs/spec-kit/PROJECT_CONFIG.json", config)
        feature = "demo"
        spec = root / "specs" / feature
        sidecar = root / "docs/spec-kit/features" / feature
        spec.mkdir(parents=True)
        sidecar.mkdir(parents=True)
        (sidecar / "DISCOVERY.md").write_text("Known facts and user decisions.\n", encoding="utf-8")
        (spec / "spec.md").write_text("# Acceptance\n\nThe feature has an observable result.\n", encoding="utf-8")
        (spec / "plan.md").write_text("# Implementation\n\nUse a bounded implementation.\n", encoding="utf-8")
        (spec / "tasks.md").write_text("- [ ] T001 Implement the bounded result in src/demo.py\n", encoding="utf-8")
        task = {
            "id": "T001",
            "objective": "Produce the bounded observable result.",
            "traceability": ["FR-001", "AC-001"],
            "context_summary": "This is the isolated implementation package for demo.",
            "preconditions": {"dependency_task_ids": []},
            "allowed_files": ["src/demo.py"],
            "read_only_references": ["specs/demo/spec.md", "specs/demo/plan.md"],
            "forbidden_changes": ["Do not change public configuration."],
            "inputs_outputs": "Input is a request; output is the bounded result.",
            "invariants_and_edge_cases": "Do not mutate unrelated state; handle empty input.",
            "implementation_steps": ["Add the bounded implementation.", "Keep public behavior stable."],
            "verification": [{"kind": "command", "command": "python3 -m unittest", "expected_result": "The relevant test passes."}],
            "completion_evidence": "Record the passing test output.",
            "stop_conditions": "Stop and ask for direction if the contract changes.",
            "handoff": "Report changed file and validation result.",
        }
        readiness = {
            "schema_version": 1,
            "feature_id": feature,
            "result": "READY",
            "generated_at": "2026-09-04T00:00:00Z",
            "artifact_paths": ["specs/demo/tasks.md"],
            "content_sha256": {"specs/demo/tasks.md": digest(spec / "tasks.md")},
            "tasks": [task],
        }
        self.write_json(sidecar / "TASK_READINESS.json", readiness)
        cold_start = {
            "schema_version": 1,
            "feature_id": feature,
            "result": "EXECUTABLE",
            "generated_at": "2026-09-04T00:00:00Z",
            "task_package_sha256": digest(sidecar / "TASK_READINESS.json"),
            "isolation": {
                "originating_conversation_provided": False,
                "repository_access": "read-only",
                "supplied_context": "declared-task-and-references-only",
            },
            "reviews": [{"task_id": "T001", "classification": "EXECUTABLE"}],
        }
        self.write_json(sidecar / "COLD_START_VALIDATION.json", cold_start)
        locations = manager.feature_locations(root, "specs/demo")
        event_id = 0
        events: list[dict] = []
        for artifact_type in ("DISCOVERY", "SPECIFICATION", "PLAN_BUNDLE", "TASK_PACKAGE"):
            paths = manager.event_artifact_paths(root, locations, artifact_type)
            hashes = {path: digest(root / path) for path in paths}
            event_id += 1
            request_id = f"review-{event_id}"
            events.append({
                "schema_version": 1, "event_id": request_id, "feature_id": feature,
                "artifact_type": artifact_type, "decision": "REVIEW_REQUESTED",
                "artifact_paths": paths, "content_sha256": hashes,
                "review_summary": "Human review requested.", "open_risks": [],
                "recorded_by": "Jane Reviewer", "recorded_at": "2026-09-04T00:00:00Z",
                "evidence": "review ticket", "supersedes_event_id": None,
            })
            event_id += 1
            events.append({
                "schema_version": 1, "event_id": f"review-{event_id}", "feature_id": feature,
                "artifact_type": artifact_type, "decision": "APPROVED",
                "artifact_paths": paths, "content_sha256": hashes,
                "review_summary": "Human review approved.", "open_risks": [],
                "recorded_by": "Jane Reviewer", "recorded_at": "2026-09-04T00:01:00Z",
                "evidence": "review ticket", "supersedes_event_id": None,
                "approved_by": "Jane Reviewer", "approved_at": "2026-09-04T00:01:00Z",
            })
        self.write_json(sidecar / "REVIEW_LEDGER.json", {"schema_version": 1, "feature_id": feature, "events": events})
        return locations, config

    def test_isolated_task_package_with_current_human_reviews_is_ready(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_v2_feature(root)
            result = manager.audit_feature_readiness(root, "specs/demo")
            self.assertEqual(result["status"], "READY")
            self.assertTrue(result["implement_allowed"])
            self.assertEqual(result["cold_start_validation"]["required_samples"], 1)

    def test_changed_reviewed_artifact_invalidates_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_v2_feature(root)
            (root / "specs/demo/spec.md").write_text("# Acceptance\n\nChanged after approval.\n", encoding="utf-8")
            result = manager.audit_feature_readiness(root, "specs/demo")
            specification = next(item for item in result["approvals"] if item["artifact_type"] == "SPECIFICATION")
            self.assertEqual(specification["status"], "STALE")
            self.assertFalse(result["implement_allowed"])

    def test_task_package_missing_a_contract_field_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            locations, _ = self.make_v2_feature(root)
            readiness_path = root / "docs/spec-kit/features/demo/TASK_READINESS.json"
            readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
            del readiness["tasks"][0]["stop_conditions"]
            self.write_json(readiness_path, readiness)
            result = manager.verify_task_package(root, locations)
            self.assertEqual(result["status"], "TASK_PACKAGE_INVALID")
            self.assertTrue(any("stop_conditions" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
