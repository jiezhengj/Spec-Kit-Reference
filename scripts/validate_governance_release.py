#!/usr/bin/env python3
"""Validate deterministic governance release artifacts without installing them."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("index", type=Path)
    args = parser.parse_args()
    index = json.loads(args.index.read_text(encoding="utf-8"))
    root = args.index.parent
    source = index.get("source", {})
    if not isinstance(source, dict) or not isinstance(source.get("revision"), str) or len(source["revision"]) != 40 or not isinstance(source.get("worktree_status_sha256"), str) or len(source["worktree_status_sha256"]) != 64:
        raise SystemExit("release source provenance is missing or malformed")
    content_hashes: dict[str, dict[str, str]] = {}
    for key in ("portable_artifact", "extension_artifact"):
        artifact = index[key]
        path = root / artifact["path"]
        if not path.is_file() or sha256(path) != artifact["sha256"]:
            raise SystemExit(f"artifact checksum mismatch: {path}")
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if names != sorted(names) or any(name.endswith("/") for name in names) or any("__pycache__" in name or name.endswith(".pyc") for name in names):
                raise SystemExit(f"artifact is not canonical: {path}")
            if key == "portable_artifact":
                required = {
                    "governance/manager/speckit_governance.py",
                    "governance/manager/bootstrap_updater.py",
                    "governance/project/GOVERNANCE_LOADER.md",
                    "governance/project/POLICY.md",
                    "governance/project/REFERENCE.md",
                    "governance/project/REFERENCE_UPDATE_CHECK.md",
                    "governance/release/SOURCE_METADATA.json",
                    "governance/schemas/operation-plan.schema.json",
                    "SPEC_KIT_REFERENCE.md",
                }
                if not required.issubset(names):
                    raise SystemExit(f"portable artifact missing required files: {sorted(required - set(names))}")
                metadata = json.loads(archive.read("governance/release/SOURCE_METADATA.json"))
                if (
                    metadata.get("schema_version") != 1
                    or metadata.get("repository") != source.get("repository")
                    or metadata.get("revision") != source.get("revision")
                    or metadata.get("version") != index.get("version")
                    or metadata.get("reviewed_upstream_revision") != source.get("reviewed_upstream_revision")
                ):
                    raise SystemExit(f"portable source metadata does not match release provenance: {path}")
            else:
                required = {"extension.yml", "scripts/python/bootstrap_governance.py", "governance/manager/speckit_governance.py"}
                if not required.issubset(names):
                    raise SystemExit(f"extension artifact missing required files: {sorted(required - set(names))}")
            actual_hashes = {
                name: hashlib.sha256(archive.read(name)).hexdigest()
                for name in names
            }
            declared_hashes = artifact.get("content_sha256")
            if not isinstance(declared_hashes, dict) or actual_hashes != declared_hashes:
                raise SystemExit(f"content checksum map mismatch: {path}")
            content_hashes[key] = declared_hashes
    portable = content_hashes["portable_artifact"]
    extension = content_hashes["extension_artifact"]
    shared = {
        "governance/manager/speckit_governance.py": "governance/manager/speckit_governance.py",
        "governance/manager/bootstrap_updater.py": "governance/manager/bootstrap_updater.py",
    }
    for portable_name, extension_name in shared.items():
        if portable.get(portable_name) != extension.get(extension_name):
            raise SystemExit(f"portable/extension shared file mismatch: {portable_name}")
    extension_entry = "governance/extension/speckit-governance/extension.yml"
    if portable.get(extension_entry) != extension.get("extension.yml"):
        raise SystemExit("portable/extension extension.yml mismatch")
    print("governance release validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
