#!/usr/bin/env python3
"""Install CogentNexus ecosystem companion skills into an OpenClaw workspace."""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BEGIN = "<!-- cogentnexus:begin -->"
END = "<!-- cogentnexus:end -->"
ROOT = Path(__file__).resolve().parents[1]


def merge_agents(existing: str, policy: str) -> tuple[str, bool]:
    block = f"{BEGIN}\n{policy.strip()}\n{END}"
    start, finish = existing.find(BEGIN), existing.find(END)
    if (start < 0) != (finish < 0) or (start >= 0 and finish < start):
        raise ValueError("AGENTS.md contains an incomplete CogentNexus managed block")
    if start >= 0:
        finish += len(END)
        updated = existing[:start] + block + existing[finish:]
    else:
        updated = existing.rstrip() + ("\n\n" if existing.strip() else "") + block + "\n"
    if not updated.endswith("\n"):
        updated += "\n"
    return updated, updated != existing


def install(workspace: Path, skip_policy: bool = False) -> None:
    workspace = workspace.resolve()
    source = ROOT / "skills" / "staged-capability-loop"
    target = workspace / "skills" / "staged-capability-loop"
    backup_root = workspace / ".cogent" / "install-backups"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if not (workspace / "skills" / "cogentnexus" / "SKILL.md").exists():
        raise RuntimeError("CogentNexus Core is not installed. Install funggier/cogentnexus first.")

    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        backup_root.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, backup_root / f"staged-capability-loop-{stamp}")
        shutil.rmtree(target)
    shutil.copytree(source, target)

    for required in (target / "SKILL.md", target / "references" / "hybrid-architecture.md", target / "references" / "hybrid-review-guide.md"):
        text = required.read_text(encoding="utf-8")
        if not text.strip() or "\ufffd" in text:
            raise RuntimeError(f"Installed skill validation failed: {required}")

    if not skip_policy:
        agents = workspace / "AGENTS.md"
        existing = agents.read_text(encoding="utf-8") if agents.exists() else ""
        policy = (ROOT / "templates" / "AGENTS.ecosystem.md").read_text(encoding="utf-8")
        updated, changed = merge_agents(existing, policy)
        if changed:
            if agents.exists():
                backup_root.mkdir(parents=True, exist_ok=True)
                shutil.copy2(agents, backup_root / f"AGENTS.pre-ecosystem-{stamp}.md")
            temporary = agents.with_suffix(".md.tmp")
            temporary.write_text(updated, encoding="utf-8", newline="\n")
            temporary.replace(agents)

    print(f"Installed staged-capability-loop to {target}")
    print("CogentNexus Ecosystem policy is active." if not skip_policy else "AGENTS.md policy update skipped.")


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
