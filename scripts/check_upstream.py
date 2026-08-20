"""Detect unreviewed commits in the official Spec Kit upstream repository.

This command is deliberately read-only with respect to local policy files and
the reviewed baseline. It may update Git's remote-tracking refs by fetching.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE_FILE = ROOT / "UPSTREAM_BASELINE"
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
OFFICIAL_UPSTREAM_URLS = {
    "https://github.com/github/spec-kit.git",
    "https://github.com/github/spec-kit",
    "git@github.com:github/spec-kit.git",
    "ssh://git@github.com/github/spec-kit.git",
}


class CheckError(RuntimeError):
    """An actionable error while checking upstream."""


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise CheckError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def read_baseline() -> str:
    if not BASELINE_FILE.is_file():
        raise CheckError(f"missing baseline file: {BASELINE_FILE}")
    baseline = BASELINE_FILE.read_text(encoding="utf-8").strip()
    if not SHA_RE.fullmatch(baseline):
        raise CheckError(
            "UPSTREAM_BASELINE must contain exactly one 40-character commit SHA; "
            f"found {baseline!r}. Complete the initial upstream review first."
        )
    return baseline.lower()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare UPSTREAM_BASELINE with upstream/main."
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="use the existing upstream/main ref instead of fetching",
    )
    return parser.parse_args()


def is_ancestor(older: str, newer: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    detail = result.stderr.strip() or result.stdout.strip()
    raise CheckError(
        f"could not compare upstream history for {older} and {newer}: {detail}"
    )


def main() -> int:
    args = parse_args()
    baseline = read_baseline()

    remote = git("remote", "get-url", "upstream")
    if remote.rstrip("/") not in OFFICIAL_UPSTREAM_URLS:
        raise CheckError(
            "the upstream remote must point to the official GitHub Spec Kit "
            f"repository; found {remote!r}"
        )

    if not args.no_fetch:
        git("fetch", "--quiet", "upstream", "main")

    latest = git("rev-parse", "upstream/main").lower()
    if not SHA_RE.fullmatch(latest):
        raise CheckError(f"upstream/main did not resolve to a commit SHA: {latest!r}")

    baseline_exists = subprocess.run(
        ["git", "cat-file", "-e", f"{baseline}^{{commit}}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if baseline_exists.returncode != 0:
        raise CheckError(
            "the reviewed baseline commit is not available locally; "
            "run the checker without --no-fetch"
        )

    if not is_ancestor(baseline, latest):
        if is_ancestor(latest, baseline):
            raise CheckError(
                "upstream/main is older than UPSTREAM_BASELINE; the local "
                "remote-tracking ref is stale, so rerun without --no-fetch"
            )
        raise CheckError(
            "UPSTREAM_BASELINE is not an ancestor of upstream/main; "
            "inspect possible upstream history rewriting or an invalid baseline"
        )

    print(f"Reviewed baseline: {baseline}")
    print(f"Upstream latest:   {latest}")

    if baseline == latest:
        print("No unreviewed Spec Kit upstream changes.")
        return 0

    commits = git("log", "--oneline", f"{baseline}..{latest}")
    files = git("diff", "--name-only", f"{baseline}..{latest}")

    print("\nUnreviewed upstream changes detected.")
    print("\nCommits:")
    print(commits or "(none)")
    print("\nChanged files:")
    print(files or "(none)")
    print("\nReview the changes before updating local policy or UPSTREAM_BASELINE.")
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (CheckError, OSError) as exc:
        print(f"upstream check failed: {exc}", file=sys.stderr)
        sys.exit(1)
