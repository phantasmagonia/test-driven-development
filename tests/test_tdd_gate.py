import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "plugins" / "tdd-gate" / "hooks"))

from tdd_gate import BLOCK_EXIT, is_source_file, decide, run  # noqa: E402

SKILL_CALL = json.dumps({"type": "assistant", "message": {"content": [
    {"type": "tool_use", "name": "Skill", "input": {"skill": "test-driven-development"}}]}})


class IsSourceFileTests(unittest.TestCase):
    def test_code_files_are_source(self):
        for path in ["a.py", "src/App.swift", "lib/x.ts", "Comp.tsx", "main.go", "core.cpp",
                     "core.hpp", "lib.rs", "Main.kt", "run.sh", "App.java", "x.rb", "y.php"]:
            with self.subTest(path=path):
                self.assertTrue(is_source_file(path))

    def test_docs_config_and_data_are_not_source(self):
        for path in ["README.md", "notes.txt", "package.json", "pyproject.toml", "ci.yml",
                     "config.yaml", "Info.plist", "logo.png", ".gitignore", "Makefile", "data.csv"]:
            with self.subTest(path=path):
                self.assertFalse(is_source_file(path))

    def test_extension_match_ignores_case(self):
        self.assertTrue(is_source_file("LEGACY.PY"))

    def test_empty_path_is_not_source(self):
        self.assertFalse(is_source_file(""))


class DecideTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)

    def transcript(self, *lines):
        path = Path(self.dir.name) / "t.jsonl"
        path.write_text("\n".join(lines) + "\n")
        return str(path)

    def event(self, file_path="src/app.py", tool="Edit", transcript_path=None):
        return {"hook_event_name": "PreToolUse", "tool_name": tool,
                "tool_input": {"file_path": file_path},
                "transcript_path": transcript_path or self.transcript()}

    def test_blocks_source_edit_before_skill(self):
        reason = decide(self.event(), env={})
        self.assertIsNotNone(reason)
        self.assertIn("test-driven-development", reason)

    def test_allows_source_edit_after_skill(self):
        self.assertIsNone(decide(self.event(transcript_path=self.transcript(SKILL_CALL)), env={}))

    def test_allows_non_source_edit_before_skill(self):
        self.assertIsNone(decide(self.event(file_path="README.md"), env={}))

    def test_ignores_tools_that_do_not_edit_files(self):
        self.assertIsNone(decide(self.event(tool="Read"), env={}))

    def test_opt_out_variable_disables_gate(self):
        self.assertIsNone(decide(self.event(), env={"TDD_GATE": "off"}))

    def test_missing_transcript_allows_because_no_invocation_could_ever_be_seen(self):
        reason = decide(self.event(transcript_path=str(Path(self.dir.name) / "missing.jsonl")), env={})
        self.assertIsNone(reason)


class RunTests(unittest.TestCase):
    def test_block_writes_reason_to_stderr_and_returns_block_code(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
            transcript = handle.name
        self.addCleanup(Path(transcript).unlink)
        stdin = io.StringIO(json.dumps({"tool_name": "Write", "tool_input": {"file_path": "a.go"},
                                        "transcript_path": transcript}))
        stderr = io.StringIO()
        self.assertEqual(run(stdin, stderr, env={}), BLOCK_EXIT)
        self.assertIn("test-driven-development", stderr.getvalue())

    def test_unexpected_tool_input_shape_allows_and_explains(self):
        stdin = io.StringIO(json.dumps({"tool_name": "Edit", "tool_input": "unexpected"}))
        stderr = io.StringIO()
        self.assertEqual(run(stdin, stderr, env={}), 0)
        self.assertIn("tdd_gate", stderr.getvalue())

    def test_malformed_input_allows_and_explains(self):
        stderr = io.StringIO()
        self.assertEqual(run(io.StringIO("{not json"), stderr, env={}), 0)
        self.assertIn("tdd_gate", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
