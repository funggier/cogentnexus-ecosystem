#!/usr/bin/env python3
"""Install CogentNexus Ecosystem companion routing into an OpenClaw workspace."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "unknown"


def validate_core_baseline(workspace: Path) -> Path:
    core = workspace / "skills" / "cogentnexus"
    host = core / "scripts" / "host.py"
    required = (
        core / "SKILL.md",
        host,
        core / "templates" / "AGENTS.cogentnexus.md",
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError(
            "CogentNexus Core v0.8+ Host baseline is not installed in this workspace. "
            "Install a compatible funggier/cogentnexus release first. Missing: " + ", ".join(missing)
        )
    return host


def run_checked(command: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or f"command failed: {command}").strip())
    return result


def install(workspace: Path, skip_policy: bool = False) -> None:
    workspace = workspace.resolve()
    host = validate_core_baseline(workspace)

    source = ROOT / "skills" / "staged-capability-loop"
    target = workspace / "skills" / "staged-capability-loop"
    backup_root = workspace / ".cogent" / "install-backups"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        backup_root.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, backup_root / f"staged-capability-loop-{stamp}")
        shutil.rmtree(target)
    shutil.copytree(source, target)

    for required in (
        target / "SKILL.md",
        target / "references" / "hybrid-architecture.md",
        target / "references" / "hybrid-review-guide.md",
    ):
        text = required.read_text(encoding="utf-8")
        if not text.strip() or "\ufffd" in text:
            raise RuntimeError(f"Installed skill validation failed: {required}")

    if not skip_policy:
        policy = ROOT / "templates" / "AGENTS.ecosystem.md"
        run_checked(
            [
                sys.executable,
                str(host),
                "--root",
                str(workspace / ".cogent"),
                "policy",
                "register",
                str(policy),
            ]
        )

    print(f"Installed CogentNexus Ecosystem v{VERSION}")
    print(f"Installed staged-capability-loop to {target}")
    if skip_policy:
        print("Managed policy registration skipped.")
    else:
        print("Combined continuity + lane policy is registered durably with CogentNexus Host.")
        print("The registered Ecosystem policy will survive cnx disable/enable and Core updates.")
    print("Start a fresh OpenClaw session before testing DIRECT/STAGED routing.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.home() / ".openclaw" / "workspace")
    parser.add_argument("--skip-agents-policy", action="store_true")
    args = parser.parse_args()
    try:
        install(args.workspace, args.skip_agents_policy)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
