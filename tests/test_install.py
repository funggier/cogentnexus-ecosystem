from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.install import BEGIN, END, merge_agents, validate_core_baseline

ROOT = Path(__file__).resolve().parents[1]


class EcosystemInstallerTests(unittest.TestCase):
    def test_append_preserves_user_content(self):
        updated, changed = merge_agents("# User policy\n", "## Ecosystem")
        self.assertTrue(changed)
        self.assertTrue(updated.startswith("# User policy\n"))
        self.assertEqual(updated.count(BEGIN), 1)
        self.assertEqual(updated.count(END), 1)

    def test_update_same_block_is_idempotent(self):
        first, _ = merge_agents("", "## Ecosystem")
        second, changed = merge_agents(first, "## Ecosystem")
        self.assertFalse(changed)
        self.assertEqual(first, second)

    def test_replaces_core_policy_with_ecosystem_policy(self):
        existing = f"# User\n\n{BEGIN}\n## Core\n{END}\n"
        updated, changed = merge_agents(existing, "## Ecosystem")
        self.assertTrue(changed)
        self.assertIn("## Ecosystem", updated)
        self.assertNotIn("## Core", updated)
        self.assertEqual(updated.count(BEGIN), 1)

    def test_incomplete_block_fails_closed(self):
        with self.assertRaises(ValueError):
            merge_agents(f"{BEGIN}\nbroken", "## Ecosystem")

    def test_policy_selects_lane_before_core_loading(self):
        policy = (ROOT / "templates" / "AGENTS.ecosystem.md").read_text(encoding="utf-8")
        self.assertIn("Choose the lightest reliable lane first", policy)
        self.assertIn("Load the `cogentnexus` skill", policy)
        self.assertNotIn("Load and apply the `cogentnexus` skill before reasoning", policy)
        self.assertNotIn("Use CogentNexus for every user request", policy)

    def test_core_baseline_requires_host_controller(self):
        with TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            core = workspace / "skills" / "cogentnexus"
            core.mkdir(parents=True)
            (core / "SKILL.md").write_text("# CogentNexus\n", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                validate_core_baseline(workspace)

    def test_core_baseline_accepts_required_surface(self):
        with TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            core = workspace / "skills" / "cogentnexus"
            (core / "scripts").mkdir(parents=True)
            (core / "templates").mkdir(parents=True)
            (core / "SKILL.md").write_text("# CogentNexus\n", encoding="utf-8")
            (core / "scripts" / "host.py").write_text("# host\n", encoding="utf-8")
            (core / "templates" / "AGENTS.cogentnexus.md").write_text("# policy\n", encoding="utf-8")
            validate_core_baseline(workspace)


if __name__ == "__main__":
    unittest.main()
