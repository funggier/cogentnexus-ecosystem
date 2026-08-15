#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.2.0":
        errors.append(f"VERSION must be 0.2.0, got {version}")

    required = [
        ROOT / "README.md",
        ROOT / "docs" / "INTEGRATION.md",
        ROOT / "docs" / "COMPATIBILITY.md",
        ROOT / "docs" / "INSTALL.th.md",
        ROOT / "docs" / "releases" / f"v{version}.md",
        ROOT / "templates" / "AGENTS.ecosystem.md",
        ROOT / "skills" / "staged-capability-loop" / "SKILL.md",
        ROOT / "scripts" / "install.py",
    ]
    for path in required:
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            errors.append(f"missing or empty: {path.relative_to(ROOT)}")

    policy = (ROOT / "templates" / "AGENTS.ecosystem.md").read_text(encoding="utf-8")
    lane = policy.find("Choose the lightest reliable lane first")
    load = policy.find("Load the `cogentnexus` skill")
    if lane < 0 or load < 0 or lane > load:
        errors.append("lane admission must occur before CogentNexus skill loading")
    if "DIRECT conversation stays lightweight" not in policy:
        errors.append("DIRECT lightweight invariant missing")

    installer = (ROOT / "scripts" / "install.py").read_text(encoding="utf-8")
    for marker in ("host.py", "policy", "register", "validate_core_baseline"):
        if marker not in installer:
            errors.append(f"installer missing marker: {marker}")

    compatibility = (ROOT / "docs" / "COMPATIBILITY.md").read_text(encoding="utf-8")
    for marker in ("0.2.x", "0.8.x", "2026.7.1-2"):
        if marker not in compatibility:
            errors.append(f"compatibility missing: {marker}")

    forbidden = [
        "CogentNexus remains the mandatory cognitive runtime",
        "Use CogentNexus for every user request",
        "Load and apply the `cogentnexus` skill before reasoning",
        "Mandatory Runtime and Routing",
    ]
    current = [ROOT / "README.md", ROOT / "docs" / "INTEGRATION.md", ROOT / "docs" / "COMPATIBILITY.md", ROOT / "templates" / "AGENTS.ecosystem.md", ROOT / "skills" / "staged-capability-loop" / "SKILL.md"]
    for path in current:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                errors.append(f"legacy phrase in {path.relative_to(ROOT)}: {phrase}")

    if errors:
        print("Ecosystem baseline consistency FAILED")
        for error in errors:
            print("-", error)
        return 1
    print("Ecosystem baseline consistency PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
