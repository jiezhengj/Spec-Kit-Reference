#!/usr/bin/env python3
"""Replace the project manager from an already approved staged plan.

This helper exists because a running manager cannot safely overwrite its own
module on every platform. It accepts only a plan created by the manager and
only replaces the fixed manager path; all other project mutations remain the
responsibility of ``apply-plan``.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


MANAGER_RELATIVE = Path("tools/spec-kit-governance/governance.py")
RUNTIME_DIR = Path(".spec-kit-governance")


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def plan_hash(plan: dict) -> str:
    body = dict(plan)
    body.pop("plan_sha256", None)
    return hashlib.sha256(canonical(body)).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staging", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--approve-plan-id", required=True)
    parser.add_argument("--approve-plan-sha256", required=True)
    args = parser.parse_args()
    staging = args.staging.resolve()
    project = args.project_root.resolve()
    plan_path = args.plan.resolve()
    runtime_plans = (project / RUNTIME_DIR / "plans").resolve()
    if not staging.is_dir() or not plan_path.is_file():
        raise SystemExit("staging directory and validated plan are required")
    try:
        plan_path.relative_to(runtime_plans)
    except ValueError as exc:
        raise SystemExit("plan must be inside the project runtime plan directory") from exc
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("schema_version") != 1:
        raise SystemExit("unsupported plan schema")
    if plan.get("plan_id") != args.approve_plan_id or plan.get("plan_sha256") != args.approve_plan_sha256 or plan_hash(plan) != args.approve_plan_sha256:
        raise SystemExit("exact plan approval does not match")
    try:
        expires = datetime.fromisoformat(str(plan["expires_at"]).replace("Z", "+00:00"))
    except (KeyError, ValueError) as exc:
        raise SystemExit("plan expiry is invalid") from exc
    if datetime.now(timezone.utc) > expires:
        raise SystemExit("approved plan has expired")
    if plan.get("operation_type") not in {
        "plan-upgrade", "plan-rollback", "upgrade", "rollback",
        "plan-upgrade-governance-v2", "plan-rollback-governance-v2",
    }:
        raise SystemExit("updater accepts only upgrade or rollback plans")
    mutation = next((item for item in plan.get("manager_file_mutations", []) if item.get("path") == MANAGER_RELATIVE.as_posix()), None)
    if not mutation or not mutation.get("content_b64") or mutation.get("action") not in {"create", "replace"}:
        raise SystemExit("validated plan has no manager replacement")
    try:
        content = base64.b64decode(mutation["content_b64"], validate=True)
    except (binascii.Error, ValueError, TypeError) as exc:
        raise SystemExit("manager replacement is not valid base64") from exc
    expected_hash = mutation.get("expected_new_sha256") or mutation.get("new_sha256")
    if hashlib.sha256(content).hexdigest() != expected_hash:
        raise SystemExit("manager replacement checksum mismatch")
    staged_manager = staging / "governance/manager/speckit_governance.py"
    if not staged_manager.is_file() or hashlib.sha256(staged_manager.read_bytes()).hexdigest() != expected_hash:
        raise SystemExit("staged manager does not match the approved replacement")
    target = project / MANAGER_RELATIVE
    try:
        target.resolve(strict=False).relative_to(project)
    except ValueError as exc:
        raise SystemExit("manager target escapes the project root") from exc
    if target.is_symlink():
        raise SystemExit("refusing to replace a symlinked manager")
    current_hash = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
    if current_hash != mutation.get("old_sha256"):
        raise SystemExit("manager changed after the approved plan was created")
    target.parent.mkdir(parents=True, exist_ok=True)
    backup = project / RUNTIME_DIR / "backups" / plan["plan_id"] / "governance.py.bak"
    backup.parent.mkdir(parents=True, exist_ok=True)
    if target.is_file():
        backup.write_bytes(target.read_bytes())
    temp = target.with_name(f".{target.name}.{plan['plan_id']}.updater.tmp")
    temp.write_bytes(content)
    with temp.open("r+b") as handle:
        try:
            os.fsync(handle.fileno())
        except OSError:
            pass
    os.replace(temp, target)
    print(json.dumps({"status": "manager-updated", "path": str(target), "backup": str(backup)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
