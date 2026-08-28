#!/usr/bin/env python3
"""Build deterministic portable and extension governance artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
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
    "governance/extension/speckit-governance",
    "SPEC_KIT_REFERENCE.md",
]
EXTENSION_ROOT = "governance/extension/speckit-governance"
REQUIRED_SOURCE_FILES = ("GLOBAL_POLICY.md", "SPEC_KIT_REFERENCE.md", "UPSTREAM_BASELINE")


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


def deterministic_zip(output: Path, roots: list[str], *, strip_root: str | None = None, extra_entries: dict[str, bytes] | None = None) -> dict[str, str]:
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
    output.parent.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, path_or_data in entries:
            data = path_or_data if isinstance(path_or_data, bytes) else path_or_data.read_bytes()
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            mode = 0o755 if path.suffix in {".py", ".sh", ".ps1"} else 0o644
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
    if any(char in args.version for char in "<> \t\r\n"):
        raise SystemExit("version must be a concrete value")
    output = args.output_dir.resolve()
    portable = output / f"speckit-governance-{args.version}-portable.zip"
    extension = output / f"speckit-governance-{args.version}-extension.zip"
    revision = git_output("rev-parse", "HEAD")
    raw_status = git_output("status", "--porcelain=v1", "--untracked-files=all") or ""
    baseline = (ROOT / "UPSTREAM_BASELINE").read_text(encoding="utf-8").strip() if (ROOT / "UPSTREAM_BASELINE").is_file() else None
    if not revision or len(revision) != 40 or not baseline or len(baseline) != 40:
        raise SystemExit("release source provenance requires a Git revision and reviewed upstream baseline")
    source_metadata = json.dumps(
        {
            "schema_version": 1,
            "repository": "https://github.com/jiezhengj/Spec-Kit-Reference",
            "revision": revision,
            "version": args.version,
            "reviewed_upstream_revision": baseline,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"
    portable_hashes = deterministic_zip(
        portable,
        PORTABLE_FILES,
        extra_entries={"governance/release/SOURCE_METADATA.json": source_metadata},
    )
    extension_hashes = deterministic_zip(extension, [EXTENSION_ROOT, "governance/manager"], strip_root=EXTENSION_ROOT)
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
