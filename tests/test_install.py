from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.install import BEGIN, END, merge_agents


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


if __name__ == "__main__":
    unittest.main()
