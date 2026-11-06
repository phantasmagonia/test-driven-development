import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class PluginPackagingTests(unittest.TestCase):
    def test_marketplace_sources_are_separate_plugins(self):
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        sources = {item["name"]: ROOT / item["source"] for item in marketplace["plugins"]}
        self.assertEqual(set(sources), {"test-driven-development", "tdd-gate"})
        for name, directory in sources.items():
            manifest = json.loads((directory / ".claude-plugin/plugin.json").read_text())
            self.assertEqual(manifest["name"], name)

        skill = sources["test-driven-development"]
        self.assertTrue((skill / "skills/test-driven-development/SKILL.md").is_file())
        self.assertFalse((skill / "hooks").exists())
        self.assertFalse((skill / ".mcp.json").exists())

        gate = sources["tdd-gate"]
        hooks = json.loads((gate / "hooks/hooks.json").read_text())["hooks"]
        self.assertEqual(set(hooks), {"SessionStart", "PreToolUse"})
        self.assertFalse((gate / "skills").exists())


if __name__ == "__main__":
    unittest.main()
