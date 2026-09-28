"""检查官方 Spec Kit 上游是否有尚未审阅的提交。

此命令不会修改本地政策文件或已审阅基线。获取上游时只会更新 Git 远端跟踪引用。
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
    """检查上游时需要维护者处理的错误。"""


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise CheckError(f"git {' '.join(args)} 执行失败：{detail}")
    return result.stdout.strip()


def read_baseline() -> str:
    if not BASELINE_FILE.is_file():
        raise CheckError(f"找不到基线文件：{BASELINE_FILE}")
    baseline = BASELINE_FILE.read_text(encoding="utf-8").strip()
    if not SHA_RE.fullmatch(baseline):
        raise CheckError(
            "UPSTREAM_BASELINE 必须只包含一个 40 位提交 SHA；"
            f"当前内容为 {baseline!r}。请先完成首次上游审查。"
        )
    return baseline.lower()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="比较 UPSTREAM_BASELINE 与官方 upstream/main。"
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="使用已有 upstream/main 引用，不重新获取",
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
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    detail = result.stderr.strip() or result.stdout.strip()
    raise CheckError(
        f"无法比较上游提交 {older} 与 {newer}：{detail}"
    )


def main() -> int:
    args = parse_args()
    baseline = read_baseline()

    remote = git("remote", "get-url", "upstream")
    if remote.rstrip("/") not in OFFICIAL_UPSTREAM_URLS:
        raise CheckError(
            "upstream 远端必须指向 GitHub Spec Kit 官方仓库；"
            f"当前地址为 {remote!r}"
        )

    if not args.no_fetch:
        git("fetch", "--quiet", "upstream", "main")

    latest = git("rev-parse", "upstream/main").lower()
    if not SHA_RE.fullmatch(latest):
        raise CheckError(f"upstream/main 未解析为提交 SHA：{latest!r}")

    baseline_exists = subprocess.run(
        ["git", "cat-file", "-e", f"{baseline}^{{commit}}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if baseline_exists.returncode != 0:
        raise CheckError(
            "本地找不到已审阅的基线提交；请在不带 --no-fetch 的情况下重试"
        )

    if not is_ancestor(baseline, latest):
        if is_ancestor(latest, baseline):
            raise CheckError(
                "upstream/main 早于 UPSTREAM_BASELINE，说明本地远端引用可能已过期；"
                "请在不带 --no-fetch 的情况下重试"
            )
        raise CheckError(
            "UPSTREAM_BASELINE 不是 upstream/main 的祖先；"
            "请检查上游历史改写或错误的基线"
        )

    print(f"已审阅基线：{baseline}")
    print(f"当前上游：    {latest}")

    if baseline == latest:
        print("没有待审阅的 Spec Kit 上游变更。")
        return 0

    commits = git("log", "--oneline", f"{baseline}..{latest}")
    files = git("diff", "--name-only", f"{baseline}..{latest}")

    print("\n发现尚未审阅的上游变更。")
    print("\n提交：")
    print(commits or "(none)")
    print("\n变更路径：")
    print(files or "(none)")
    print("\n请先审阅变更，再更新本地政策或 UPSTREAM_BASELINE。")
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (CheckError, OSError) as exc:
        print(f"上游检查失败：{exc}", file=sys.stderr)
        sys.exit(1)
