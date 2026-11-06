#!/usr/bin/env python3
"""PreToolUse hook: block source-code edits until the TDD skill is loaded.

Exit 2 blocks the edit and shows stderr to Claude. Unreadable input allows
the edit: the gate enforces a habit and must never lock a session.
"""

import json
import os
import sys
from pathlib import PurePath
from typing import Mapping, Optional, TextIO

from transcript import EDIT_TOOLS, skill_invoked

SKILL = "test-driven-development"
BLOCK_EXIT = 2
OPT_OUT_VARIABLE = "TDD_GATE"

SOURCE_EXTENSIONS = frozenset({
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".m", ".mm",
    ".swift", ".kt", ".kts", ".java", ".scala", ".groovy", ".dart",
    ".go", ".rs", ".zig",
    ".py", ".rb", ".php", ".pl", ".lua", ".ex", ".exs", ".erl", ".clj",
    ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts", ".vue", ".svelte",
    ".cs", ".fs", ".vb",
    ".sh", ".bash", ".zsh", ".ps1",
    ".sql",
})

REASON = (
    f"Load the {SKILL} skill before editing source code. "
    "It sets the rules for this change: decide what needs a test, write the failing test first, "
    "then the code. Docs and config files are not gated."
)


def is_source_file(path: str) -> bool:
    return PurePath(path).suffix.lower() in SOURCE_EXTENSIONS


def decide(event: Mapping, env: Mapping[str, str]) -> Optional[str]:
    """Return the reason to block, or None to allow."""
    if env.get(OPT_OUT_VARIABLE, "").lower() == "off":
        return None
    if event.get("tool_name") not in EDIT_TOOLS:
        return None
    tool_input = event.get("tool_input") or {}
    if not is_source_file(str(tool_input.get("file_path", ""))):
        return None
    try:
        with open(str(event.get("transcript_path", "")), encoding="utf-8", errors="replace") as lines:
            return None if skill_invoked(lines, SKILL) else REASON
    except OSError:
        # Without a transcript an invocation can never be seen, so blocking would be permanent.
        return None


def run(stdin: TextIO, stderr: TextIO, env: Mapping[str, str]) -> int:
    try:
        event = json.load(stdin)
    except ValueError as error:
        stderr.write(f"tdd_gate: could not read hook input, allowing the edit ({error})\n")
        return 0
    if not isinstance(event, dict):
        stderr.write("tdd_gate: hook input is not a JSON object, allowing the edit\n")
        return 0
    reason = decide(event, env)
    if reason is None:
        return 0
    stderr.write(reason + "\n")
    return BLOCK_EXIT


if __name__ == "__main__":
    sys.exit(run(sys.stdin, sys.stderr, os.environ))
