from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts.install import ROOT, install, validate_core_baseline


class EcosystemInstallerTests(unittest.TestCase):
    def _make_core_surface(self, workspace: Path) -> Path:
        core = workspace / "skills" / "cogentnexus"
        (core / "scripts").mkdir(parents=True)
        (core / "templates").mkdir(parents=True)
        (core / "SKILL.md").write_text("# CogentNexus\n", encoding="utf-8")
        host = core / "scripts" / "host.py"
        host.write_text("# host\n", encoding="utf-8")
        (core / "templates" / "AGENTS.cogentnexus.md").write_text("# core policy\n", encoding="utf-8")
        return host

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
            expected = self._make_core_surface(workspace)
            self.assertEqual(validate_core_baseline(workspace), expected)

    @patch("scripts.install.run_checked")
    def test_install_registers_policy_with_host(self, run_checked):
        with TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "workspace"
            host = self._make_core_surface(workspace)
            install(workspace, skip_policy=False)
            installed = workspace / "skills" / "staged-capability-loop" / "SKILL.md"
            self.assertTrue(installed.is_file())
            run_checked.assert_called_once()
            command = run_checked.call_args.args[0]
            self.assertEqual(command[1], str(host))
            self.assertEqual(command[2:5], ["--root", str(workspace / ".cogent"), "policy"])
            self.assertEqual(command[5], "register")
            self.assertEqual(Path(command[6]), ROOT / "templates" / "AGENTS.ecosystem.md")

    @patch("scripts.install.run_checked")
    def test_skip_policy_does_not_register(self, run_checked):
        with TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "workspace"
            self._make_core_surface(workspace)
            install(workspace, skip_policy=True)
            run_checked.assert_not_called()


if __name__ == "__main__":
    unittest.main()
