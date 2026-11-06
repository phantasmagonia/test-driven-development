#!/usr/bin/env python3
"""Measure how reliably Claude Code loads the skill on its own.

Each case is a prompt run headless against a fresh copy of a small sample
project, with the skill-only plugin loaded. A case that should
trigger passes only if the skill is invoked before the first file edit.
A case that should not trigger passes only if the skill never loads.

Sessions run without persistence, so the gate hook has no transcript to
read and lets every edit through. The result therefore measures the skill
description alone, not the hook.

This calls the real model and costs money. Use --budget to cap each case.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from typing import Dict, Iterable, List, NamedTuple, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "plugins" / "tdd-gate" / "hooks"))

from transcript import events  # noqa: E402

SKILL = "test-driven-development"


class Case(NamedTuple):
    prompt: str
    should_trigger: bool


def load_cases(path: Path) -> List[Case]:
    raw = json.loads(path.read_text())
    cases = [Case(str(item["prompt"]), bool(item["should_trigger"])) for item in raw["cases"]]
    if not cases:
        raise ValueError(f"{path} has no cases")
    return cases


def passed(should_trigger: bool, seen: List[str]) -> bool:
    if should_trigger:
        return bool(seen) and seen[0] == "skill"
    return "skill" not in seen


def summarize(results: Iterable[Tuple[Case, bool]]) -> Dict[str, Dict[str, int]]:
    summary = {key: {"passed": 0, "total": 0} for key in ("should_trigger", "should_not_trigger")}
    for case, ok in results:
        bucket = summary["should_trigger" if case.should_trigger else "should_not_trigger"]
        bucket["total"] += 1
        bucket["passed"] += int(ok)
    return summary


def run_case(case: Case, fixture: Path, budget: float, timeout: int) -> List[str]:
    with tempfile.TemporaryDirectory() as work:
        project = Path(work) / fixture.name
        shutil.copytree(fixture, project)
        command = [
            "claude", "-p", case.prompt,
            "--output-format", "stream-json", "--verbose",
            "--plugin-dir", str(ROOT / "plugins" / "test-driven-development"),
            "--permission-mode", "acceptEdits",
            "--no-session-persistence",
            "--max-budget-usd", str(budget),
        ]
        process = subprocess.Popen(command, cwd=project, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, text=True)
        try:
            return _collect(process, case.should_trigger, timeout)
        finally:
            if process.poll() is None:
                process.kill()
            process.wait()


def _collect(process: subprocess.Popen, stop_at_first: bool, timeout: int) -> List[str]:
    # A positive case is decided by its first skill-or-edit event, so stop paying after it.
    seen: List[str] = []
    timer = _kill_after(process, timeout)
    try:
        for line in process.stdout:
            seen.extend(events([line], SKILL))
            if stop_at_first and seen:
                break
    finally:
        timer.cancel()
    return seen


def _kill_after(process: subprocess.Popen, seconds: int) -> threading.Timer:
    timer = threading.Timer(seconds, process.kill)
    timer.daemon = True
    timer.start()
    return timer


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cases", type=Path, default=ROOT / "evals" / "triggers.json")
    parser.add_argument("--fixture", type=Path, default=ROOT / "evals" / "fixtures" / "shopping-cart")
    parser.add_argument("--budget", type=float, default=0.5, help="USD limit per case")
    parser.add_argument("--timeout", type=int, default=300, help="seconds per case")
    args = parser.parse_args()

    if shutil.which("claude") is None:
        print("claude CLI not found on PATH", file=sys.stderr)
        return 1

    results = []
    for case in load_cases(args.cases):
        ok = passed(case.should_trigger, run_case(case, args.fixture, args.budget, args.timeout))
        results.append((case, ok))
        expectation = "trigger" if case.should_trigger else "no trigger"
        print(f"{'PASS' if ok else 'FAIL'}  [{expectation}]  {case.prompt}")

    summary = summarize(results)
    for key, bucket in summary.items():
        print(f"{key}: {bucket['passed']}/{bucket['total']}")
    return 0 if all(ok for _, ok in results) else 1


if __name__ == "__main__":
    sys.exit(main())
