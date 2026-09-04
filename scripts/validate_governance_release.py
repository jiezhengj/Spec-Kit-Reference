#!/usr/bin/env python3
"""Validate deterministic governance release artifacts without installing them."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def expected_contract(version: str) -> dict[str, object]:
    if not SEMVER_RE.fullmatch(version):
        raise ValueError("release version is not a concrete semantic version")
    major, minor, patch = (int(part) for part in version.split("."))
    if (major, minor, patch) == (1, 3, 0):
        return {
            "release_line": "bridge",
            "project_config_schema_version": 1,
            "strict_workflow_governance": False,
            "requires_bridge_migration": False,
        }
    if major >= 2:
        return {
            "release_line": "strict",
            "project_config_schema_version": 2,
            "strict_workflow_governance": True,
            "requires_bridge_migration": True,
            "minimum_bridge_version": "1.3.0",
        }
    return {
        "release_line": "legacy",
        "project_config_schema_version": 1,
        "strict_workflow_governance": False,
        "requires_bridge_migration": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("index", type=Path)
    args = parser.parse_args()
    index = json.loads(args.index.read_text(encoding="utf-8"))
    root = args.index.parent
    try:
        expected_metadata_contract = expected_contract(index.get("version", ""))
    except ValueError as error:
        raise SystemExit(str(error)) from error
    source = index.get("source", {})
    if not isinstance(source, dict) or not isinstance(source.get("revision"), str) or len(source["revision"]) != 40 or not isinstance(source.get("worktree_status_sha256"), str) or len(source["worktree_status_sha256"]) != 64:
        raise SystemExit("release source provenance is missing or malformed")
    content_hashes: dict[str, dict[str, str]] = {}
    is_bridge = expected_metadata_contract["release_line"] == "bridge"
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
                bridge_required = {
                    "governance/manager/speckit_governance.py",
                    "governance/manager/bootstrap_updater.py",
                    "governance/release/SOURCE_METADATA.json",
                    "governance/release/COMPATIBILITY.md",
                    "governance/schemas/project-config.schema.json",
                    "governance/schemas/project-config-migration-record.schema.json",
                    "governance/schemas/operation-plan.schema.json",
                }
                strict_required = bridge_required | {
                    "governance/project/GOVERNANCE_LOADER.md",
                    "governance/project/POLICY.md",
                    "governance/project/REFERENCE.md",
                    "governance/project/REFERENCE_UPDATE_CHECK.md",
                    "governance/schemas/artifact-review.schema.json",
                    "governance/schemas/task-readiness-report.schema.json",
                    "governance/schemas/cold-start-review.schema.json",
                    "governance/schemas/workflow-governance.schema.json",
                    "governance/spec-kit-native/bundle.yml",
                    "governance/spec-kit-native/presets/tiny-model-tasks/preset.yml",
                    "governance/spec-kit-native/workflows/governed-sdd/workflow.yml",
                    "SPEC_KIT_REFERENCE.md",
                }
                required = bridge_required if is_bridge else strict_required
                if is_bridge:
                    required |= {
                        "governance/project/PROJECT_CONFIG.default.json",
                        "governance/project/POLICY.md",
                        "governance/project/START_HERE.md",
                    }
                if not required.issubset(names):
                    raise SystemExit(f"portable artifact missing required files: {sorted(required - set(names))}")
                if is_bridge:
                    if any(name.startswith("governance/spec-kit-native/") for name in names):
                        raise SystemExit("bridge artifact must not contain companion source")
                    bridge_config = json.loads(archive.read("governance/project/PROJECT_CONFIG.default.json"))
                    if bridge_config.get("schema_version") != 1 or "workflow_governance" in bridge_config:
                        raise SystemExit("bridge artifact must carry the frozen v1 project configuration")
                metadata = json.loads(archive.read("governance/release/SOURCE_METADATA.json"))
                if (
                    metadata.get("schema_version") != 2
                    or metadata.get("repository") != source.get("repository")
                    or metadata.get("revision") != source.get("revision")
                    or metadata.get("version") != index.get("version")
                    or metadata.get("reviewed_upstream_revision") != source.get("reviewed_upstream_revision")
                    or metadata.get("compatibility") != expected_metadata_contract
                ):
                    raise SystemExit(f"portable source metadata does not match release provenance: {path}")
            else:
                required = {
                    "extension.yml",
                    "scripts/python/bootstrap_governance.py",
                    "governance/manager/speckit_governance.py",
                }
                if not is_bridge:
                    required |= {
                        "governance/spec-kit-native/bundle.yml",
                        "governance/spec-kit-native/presets/tiny-model-tasks/preset.yml",
                        "governance/spec-kit-native/workflows/governed-sdd/workflow.yml",
                    }
                if not required.issubset(names):
                    raise SystemExit(f"extension artifact missing required files: {sorted(required - set(names))}")
                if is_bridge and any(name.startswith("governance/spec-kit-native/") for name in names):
                    raise SystemExit("bridge extension must not contain companion source")
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
    if not is_bridge:
        companion_prefix = "governance/spec-kit-native/"
        companion_files = [name for name in portable if name.startswith(companion_prefix)]
        if not companion_files:
            raise SystemExit("portable artifact has no companion source")
        for portable_name in companion_files:
            if portable.get(portable_name) != extension.get(portable_name):
                raise SystemExit(f"portable/extension companion mismatch: {portable_name}")
    print("governance release validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
