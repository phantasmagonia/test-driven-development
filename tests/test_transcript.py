import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "plugins" / "tdd-gate" / "hooks"))

from transcript import skill_invoked, skill_invoked_before_first_edit  # noqa: E402

SKILL = "test-driven-development"


def assistant(*blocks):
    return json.dumps({"type": "assistant", "message": {"role": "assistant", "content": list(blocks)}})


def tool_use(name, **tool_input):
    return {"type": "tool_use", "id": "toolu_1", "name": name, "input": tool_input}


def user_text(text):
    return json.dumps({"type": "user", "message": {"role": "user", "content": text}})


class SkillInvokedTests(unittest.TestCase):
    def test_empty_transcript_has_no_invocation(self):
        self.assertFalse(skill_invoked([], SKILL))

    def test_skill_tool_call_counts(self):
        self.assertTrue(skill_invoked([assistant(tool_use("Skill", skill=SKILL))], SKILL))

    def test_plugin_namespaced_skill_counts(self):
        line = assistant(tool_use("Skill", skill=f"{SKILL}:{SKILL}"))
        self.assertTrue(skill_invoked([line], SKILL))

    def test_other_skill_does_not_count(self):
        self.assertFalse(skill_invoked([assistant(tool_use("Skill", skill="verify"))], SKILL))

    def test_skill_whose_name_only_ends_the_same_does_not_count(self):
        line = assistant(tool_use("Skill", skill="not-test-driven-development"))
        self.assertFalse(skill_invoked([line], SKILL))

    def test_slash_command_by_user_counts(self):
        line = user_text(f"<command-name>/{SKILL}</command-name>\n<command-args></command-args>")
        self.assertTrue(skill_invoked([line], SKILL))

    def test_slash_command_with_content_blocks_counts(self):
        line = json.dumps({
            "type": "user",
            "message": {"role": "user", "content": [
                {"type": "text", "text": f"<command-name>/{SKILL}:{SKILL}</command-name>"}
            ]},
        })
        self.assertTrue(skill_invoked([line], SKILL))

    def test_mentions_outside_real_messages_do_not_count(self):
        # Transcripts also store request metadata that lists every tool and skill by name.
        line = json.dumps({"type": "api-request-shape", "shape": {
            "tools": [{"name": "Skill"}], "text": f"<command-name>/{SKILL}</command-name>"}})
        self.assertFalse(skill_invoked([line], SKILL))

    def test_assistant_text_naming_the_skill_does_not_count(self):
        line = assistant({"type": "text", "text": f"I will use {SKILL} next."})
        self.assertFalse(skill_invoked([line], SKILL))

    def test_malformed_lines_are_skipped(self):
        lines = ["not json", "", "{\"type\": \"assistant\"}", assistant(tool_use("Skill", skill=SKILL))]
        self.assertTrue(skill_invoked(lines, SKILL))


class InvokedBeforeFirstEditTests(unittest.TestCase):
    def test_skill_then_edit_is_true(self):
        lines = [assistant(tool_use("Skill", skill=SKILL)), assistant(tool_use("Edit", file_path="a.py"))]
        self.assertTrue(skill_invoked_before_first_edit(lines, SKILL))

    def test_edit_then_skill_is_false(self):
        lines = [assistant(tool_use("Write", file_path="a.py")), assistant(tool_use("Skill", skill=SKILL))]
        self.assertFalse(skill_invoked_before_first_edit(lines, SKILL))

    def test_no_skill_is_false(self):
        self.assertFalse(skill_invoked_before_first_edit([assistant(tool_use("Read", file_path="a.py"))], SKILL))

    def test_skill_and_edit_in_the_same_message_respect_block_order(self):
        line = assistant(tool_use("MultiEdit", file_path="a.py"), tool_use("Skill", skill=SKILL))
        self.assertFalse(skill_invoked_before_first_edit([line], SKILL))


if __name__ == "__main__":
    unittest.main()
