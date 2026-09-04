#!/usr/bin/env python3
"""Build deterministic portable and extension governance artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORTABLE_FILES = [
    "governance/project",
    "governance/manager",
    "governance/resolver",
    "governance/schemas",
    "governance/release",
    "governance/spec-kit-native",
    "governance/extension/speckit-governance",
    "SPEC_KIT_REFERENCE.md",
]
BRIDGE_PORTABLE_FILES = [
    "governance/manager",
    "governance/schemas",
    "governance/release",
    "governance/extension/speckit-governance",
]
EXTENSION_ROOT = "governance/extension/speckit-governance"
COMPANION_ROOT = "governance/spec-kit-native"
BRIDGE_PROJECT_ROOT = "governance/bridge/project"
REQUIRED_SOURCE_FILES = ("GLOBAL_POLICY.md", "SPEC_KIT_REFERENCE.md", "UPSTREAM_BASELINE")
SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_output(*args: str) -> str | None:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def files_under(relative: str) -> list[Path]:
    path = ROOT / relative
    if path.is_file():
        return [path]
    return sorted((item for item in path.rglob("*") if item.is_file() and "__pycache__" not in item.parts and item.suffix != ".pyc"), key=lambda p: p.relative_to(ROOT).as_posix())


def release_contract(version: str) -> dict[str, object]:
    """Return explicit compatibility metadata for a concrete release version."""
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


def deterministic_zip(
    output: Path,
    roots: list[str],
    *,
    strip_root: str | None = None,
    extra_entries: dict[str, bytes] | None = None,
    entry_overrides: dict[str, bytes] | None = None,
) -> dict[str, str]:
    entries: list[tuple[str, Path | bytes]] = []
    for root in roots:
        for path in files_under(root):
            name = path.relative_to(ROOT).as_posix()
            if strip_root:
                prefix = strip_root.rstrip("/") + "/"
                if name.startswith(prefix):
                    name = name[len(prefix):]
            entries.append((name, path))
    for name, data in (extra_entries or {}).items():
        entries.append((name, data))
    entries.sort(key=lambda item: item[0])
    names = [name for name, _ in entries]
    if len(set(names)) != len(names):
        raise ValueError("release archive contains duplicate paths")
    output.parent.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, path_or_data in entries:
            data = (entry_overrides or {}).get(name)
            if data is None:
                data = path_or_data if isinstance(path_or_data, bytes) else path_or_data.read_bytes()
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            source_suffix = "" if isinstance(path_or_data, bytes) else path_or_data.suffix
            mode = 0o755 if source_suffix in {".py", ".sh", ".ps1"} else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            hashes[name] = digest(data)
    return hashes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    missing = [name for name in REQUIRED_SOURCE_FILES if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit(f"canonical governance source file(s) missing: {', '.join(missing)}")
    if (ROOT / "global-policy.md").exists():
        raise SystemExit("legacy global-policy.md must not exist; use GLOBAL_POLICY.md")
    if not SEMVER_RE.fullmatch(args.version):
        raise SystemExit("version must be a concrete semantic version")
    if not (ROOT / COMPANION_ROOT).is_dir():
        raise SystemExit(f"companion source missing: {COMPANION_ROOT}")
    output = args.output_dir.resolve()
    portable = output / f"speckit-governance-{args.version}-portable.zip"
    extension = output / f"speckit-governance-{args.version}-extension.zip"
    revision = git_output("rev-parse", "HEAD")
    raw_status = git_output("status", "--porcelain=v1", "--untracked-files=all") or ""
    baseline = (ROOT / "UPSTREAM_BASELINE").read_text(encoding="utf-8").strip() if (ROOT / "UPSTREAM_BASELINE").is_file() else None
    if not revision or len(revision) != 40 or not baseline or len(baseline) != 40:
        raise SystemExit("release source provenance requires a Git revision and reviewed upstream baseline")
    compatibility = release_contract(args.version)
    source_metadata = json.dumps(
        {
            "schema_version": 2,
            "repository": "https://github.com/jiezhengj/Spec-Kit-Reference",
            "revision": revision,
            "version": args.version,
            "reviewed_upstream_revision": baseline,
            "compatibility": compatibility,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"
    is_bridge = compatibility["release_line"] == "bridge"
    bridge_project_entries = {
        f"governance/project/{item.relative_to(ROOT / BRIDGE_PROJECT_ROOT).as_posix()}": item.read_bytes()
        for item in files_under(BRIDGE_PROJECT_ROOT)
    } if is_bridge else {}
    extension_yml = (ROOT / EXTENSION_ROOT / "extension.yml").read_text(encoding="utf-8")
    extension_yml = re.sub(r"(?m)^version: .+$", f"version: {args.version}", extension_yml, count=1).encode("utf-8")
    manager_bytes = (ROOT / "governance/manager/speckit_governance.py").read_bytes()
    if is_bridge:
        manager_text = manager_bytes.decode("utf-8")
        manager_text = re.sub(r'(?m)^GOVERNANCE_PACKAGE_VERSION = ".+"$', 'GOVERNANCE_PACKAGE_VERSION = "1.3.0"', manager_text, count=1)
        manager_text = re.sub(r'(?m)^POLICY_VERSION = ".+"$', 'POLICY_VERSION = "1.2.0"', manager_text, count=1)
        manager_text = re.sub(r'(?m)^MANAGER_VERSION = ".+"$', 'MANAGER_VERSION = "1.3.0"', manager_text, count=1)
        manager_bytes = manager_text.encode("utf-8")
    portable_overrides = {
        f"{EXTENSION_ROOT}/extension.yml": extension_yml,
        "governance/manager/speckit_governance.py": manager_bytes,
    }
    portable_hashes = deterministic_zip(
        portable,
        BRIDGE_PORTABLE_FILES if is_bridge else PORTABLE_FILES,
        extra_entries={"governance/release/SOURCE_METADATA.json": source_metadata, **bridge_project_entries},
        entry_overrides=portable_overrides,
    )
    extension_hashes = deterministic_zip(
        extension,
        [EXTENSION_ROOT, "governance/manager"] if is_bridge else [EXTENSION_ROOT, COMPANION_ROOT, "governance/manager"],
        strip_root=EXTENSION_ROOT,
        entry_overrides={
            "extension.yml": extension_yml,
            "governance/manager/speckit_governance.py": manager_bytes,
        },
    )
    manifest = {
        "schema_version": 1,
        "version": args.version,
        "source": {
            "repository": "https://github.com/jiezhengj/Spec-Kit-Reference",
            "revision": revision,
            "worktree_status_sha256": digest(raw_status.encode("utf-8")),
            "worktree_clean": raw_status == "",
            "reviewed_upstream_revision": baseline,
        },
        "portable_artifact": {"path": portable.name, "sha256": digest(portable.read_bytes()), "content_sha256": portable_hashes},
        "extension_artifact": {"path": extension.name, "sha256": digest(extension.read_bytes()), "content_sha256": extension_hashes},
        "extension_install_argv": ["specify", "extension", "add", "__STAGED_EXTENSION_DIRECTORY__"],
    }
    (output / "latest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
