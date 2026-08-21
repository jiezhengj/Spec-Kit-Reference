#!/usr/bin/env python3
"""Validated extension bootstrap; mutation remains in the portable manager."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    artifact = args.artifact_root.resolve()
    project = args.project_root.resolve()
    extension = artifact / "extension.yml"
    if not extension.is_file():
        raise SystemExit("artifact extension.yml is required")
    manager = artifact / "governance/manager/speckit_governance.py"
    if not manager.is_file():
        raise SystemExit("artifact manager is missing")
    print(json.dumps({"status": "validated", "artifact": str(artifact), "project": str(project), "manager_sha256": sha256(manager)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
