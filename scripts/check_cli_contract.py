"""检查官方 Spec Kit CLI 的输出契约是否仍被本仓库的解析器接受。

只使用 Python 标准库、已安装的官方 `specify` CLI 和一个临时初始化项目；
不修改本仓库文件，也不改动任何已有项目。
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import spec_kit_component_updater as updater


TIMEOUT_SECONDS = 180
INIT_ARGS = (
    "init",
    "probe",
    "--integration",
    "generic",
    "--integration-options=--commands-dir .agents/skills --skills",
    "--script",
    "py",
    "--non-interactive",
)


def configure_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="校验官方 Spec Kit CLI 输出契约。"
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="跳过需要联网的 self check 和工作流搜索检查",
    )
    return parser.parse_args()


def capture(cli: str, args: tuple[str, ...], cwd: Path | None = None) -> tuple[int | None, str]:
    try:
        result = subprocess.run(
            [cli, *args],
            cwd=str(cwd) if cwd is not None else None,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return None, f"执行超时（>{TIMEOUT_SECONDS} 秒）"
    except OSError as error:
        return None, f"无法执行：{error}"
    return result.returncode, result.stdout


def snippet(output: str, limit: int = 300) -> str:
    collapsed = " ".join(output.split())
    return collapsed[:limit] + ("…" if len(collapsed) > limit else "")


class Contract:
    def __init__(self, cli: str) -> None:
        self.cli = cli
        self.failures: list[str] = []

    def expect(self, label: str, args: tuple[str, ...], parse, cwd: Path | None = None) -> object | None:
        returncode, output = capture(self.cli, args, cwd=cwd)
        command = "specify " + " ".join(args)
        if returncode != 0:
            self.failures.append(f"{label}：`{command}` 退出码 {returncode}；{snippet(output)}")
            print(f"失败：{label}（命令退出码 {returncode}）")
            return None
        try:
            parsed = parse(output)
        except (ValueError, KeyError, TypeError) as error:
            self.failures.append(f"{label}：解析 `{command}` 输出失败；{error}")
            print(f"失败：{label}（解析异常）")
            return None
        if parsed is None:
            self.failures.append(f"{label}：无法从 `{command}` 输出识别预期内容；{snippet(output)}")
            print(f"失败：{label}（输出无法识别）")
            return None
        print(f"通过：{label}")
        return parsed

    def expect_non_empty(self, label: str, args: tuple[str, ...], parse, cwd: Path) -> None:
        parsed = self.expect(label, args, parse, cwd=cwd)
        if parsed is not None and not parsed:
            self.failures.append(f"{label}：`specify {' '.join(args)}` 返回空结果")
            print(f"失败：{label}（结果为空）")

    def skip(self, label: str, reason: str) -> None:
        print(f"跳过：{label}（{reason}）")


def run_contract(cli: str, offline: bool) -> int:
    contract = Contract(cli)
    print(f"官方 CLI：{cli}")

    version = contract.expect("CLI 版本", ("--version",), updater.parse_cli_version)
    if not offline:
        contract.expect("CLI 更新检查", ("self", "check"), updater.parse_self_check)
    else:
        contract.skip("CLI 更新检查", "离线模式")

    with tempfile.TemporaryDirectory(prefix="specify-contract-") as temp:
        parent = Path(temp)
        returncode, output = capture(cli, INIT_ARGS, cwd=parent)
        project = parent / "probe"
        if returncode != 0 or not (project / ".specify").is_dir():
            contract.failures.append(
                "项目初始化：`specify init` 未能生成 .specify 目录；"
                f"退出码 {returncode}；{snippet(output)}"
            )
            print("失败：项目初始化")
        else:
            print("通过：项目初始化")
            contract.expect("集成状态", ("integration", "status", "--json"),
                            updater.parse_installed_integrations, cwd=project)
            contract.expect("扩展清单", ("extension", "list", "--json"),
                            updater.parse_installed_extensions, cwd=project)
            contract.expect_non_empty("扩展目录", ("extension", "catalog", "list"),
                                      updater.parse_extension_catalogs, cwd=project)
            contract.expect_non_empty("工作流目录", ("workflow", "catalog", "list"),
                                      updater.parse_workflow_catalogs, cwd=project)
            contract.expect("工作流元数据", ("workflow", "info", "speckit"),
                            updater.parse_workflow_info_version, cwd=project)
            if not offline:
                contract.expect(
                    "工作流搜索",
                    ("workflow", "search", "speckit"),
                    lambda output: updater.parse_workflow_search_version(output, "speckit"),
                    cwd=project,
                )
            else:
                contract.skip("工作流搜索", "离线模式")

    if contract.failures:
        print("\n契约检查失败：")
        for failure in contract.failures:
            print(f"- {failure}")
        if version is not None:
            print(f"\n请按 `specify` {version} 的实际输出更新解析器与文档。")
        return 1

    print("\n全部契约检查通过。")
    return 0


def main() -> int:
    configure_streams()
    args = parse_args()
    cli = shutil.which("specify")
    if cli is None:
        print("错误：PATH 中找不到 specify；请先安装官方 CLI 后重试。", file=sys.stderr)
        return 1
    return run_contract(cli, args.offline)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"契约检查无法完成：{error}", file=sys.stderr)
        sys.exit(1)
