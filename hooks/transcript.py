"""Find skill invocations in Claude Code transcripts (JSON Lines).

Only real messages count: transcripts also hold request metadata that
names every skill, which would fool a plain text search.
"""

import json
from typing import Iterable, Iterator, Optional, Tuple

EDIT_TOOLS = frozenset({"Edit", "Write", "MultiEdit"})


def skill_invoked(lines: Iterable[str], skill: str) -> bool:
    """True if Claude called the skill or the user ran it as a slash command."""
    return any(kind == "skill" for kind in events(lines, skill))


def skill_invoked_before_first_edit(lines: Iterable[str], skill: str) -> bool:
    """True if the skill was invoked before any file-editing tool call."""
    for kind in events(lines, skill):
        if kind == "skill":
            return True
        if kind == "edit":
            return False
    return False


def events(lines: Iterable[str], skill: str) -> Iterator[str]:
    """Yield "skill" for each invocation and "edit" for each file edit, in order."""
    for line in lines:
        record = _parse(line)
        if record is None:
            continue
        role, content = record
        if role == "assistant":
            yield from _assistant_events(content, skill)
        elif role == "user" and _has_slash_command(content, skill):
            yield "skill"


def _parse(line: str) -> Optional[Tuple[str, object]]:
    try:
        record = json.loads(line)
    except ValueError:
        return None
    if not isinstance(record, dict) or record.get("type") not in ("assistant", "user"):
        return None
    message = record.get("message")
    if not isinstance(message, dict):
        return None
    return record["type"], message.get("content")


def _assistant_events(content: object, skill: str) -> Iterator[str]:
    if not isinstance(content, list):
        return
    for block in content:
        if not isinstance(block, dict) or block.get("type") != "tool_use":
            continue
        name = block.get("name")
        tool_input = block.get("input") if isinstance(block.get("input"), dict) else {}
        if name == "Skill" and _names_skill(tool_input.get("skill"), skill):
            yield "skill"
        elif name in EDIT_TOOLS:
            yield "edit"


def _has_slash_command(content: object, skill: str) -> bool:
    tags = (f"<command-name>/{skill}</command-name>", f"<command-name>/{skill}:{skill}</command-name>")
    return any(tag in text for text in _texts(content) for tag in tags)


def _texts(content: object) -> Iterator[str]:
    """User content is either a plain string or a list of content blocks."""
    if isinstance(content, str):
        yield content
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and isinstance(block.get("text"), str):
                yield block["text"]


def _names_skill(value: object, skill: str) -> bool:
    # Plugin skills are namespaced as "<plugin>:<skill>".
    return isinstance(value, str) and (value == skill or value.endswith(f":{skill}"))
