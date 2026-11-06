# Test-Driven Development for Claude Code

**No logic without a failing test first.**

A Claude Code plugin that makes Claude work test-first in any language. Every change starts with a failing test, ends with a passing one, and closes with a report of exactly what was checked.

## Why

AI assistants write code first and tests later, if at all. A test written after the code passes on its first run and proves nothing. Then come the shortcuts: loosened assertions, skipped tests, "all tests pass" with nothing run.

| Without | With |
|---|---|
| Code first, tests maybe | A failing test before every piece of logic |
| Tests that never failed | Every new test seen failing first |
| "Should work now" | The exact commands run and their results |
| Bugs that come back | A regression test with every fix |
| Legacy code changed blind | Current behavior pinned down, then changed |

## Install

In Claude Code:

```text
/plugin marketplace add phantasmagonia/test-driven-development
/plugin install test-driven-development@test-driven-development
```

Restart Claude Code. Done. Requires `python3` (3.9+) for the edit gate.

To try without installing: `claude --plugin-dir /path/to/this/repo`

## Use

Ask for changes as usual: *"fix the rounding bug"*, *"add retries to the uploader"*. Or start it directly with `/test-driven-development`.

Claude then follows one cycle:

1. **Orient**: find the test command, run the suite for a baseline.
2. **Triage**: mark which pieces contain logic. Only those need tests.
3. **Red**: write one test, watch it fail.
4. **Green**: write the least code that passes.
5. **Refactor**: clean up, tests stay green.
6. **Report**: what changed, which tests were added, what ran, what was not checked.

```text
Changes:     discounts outside 0-100% are rejected; totals can no longer go negative.
Tests added: test_rejects_discount_above_100_percent, test_rejects_negative_discount
             (both seen failing: "ValueError not raised").
Checks run:  python3 -m unittest -> 5 tests, OK.
Not checked: nothing outstanding.
```

## It gets used, every time

Claude may skip a skill. This plugin does not allow that for code.

Every session starts with a reminder to load the workflow. Then a hook runs before every file edit. If the file is source code and the workflow is not active, the edit is blocked and Claude is told to load it. Docs and config are never blocked. If the hook cannot read its input, it allows the edit instead of locking the session.

In a real session, Claude went straight for the code. The gate stopped it, Claude loaded the workflow, wrote two tests, saw both fail, then fixed the code.

Turn the gate off for one session: `TDD_GATE=off claude`

The gate sees Claude's edit tools. File writes made through shell commands (`sed -i`, `cat > file`) are not gated.

## What it covers

- **Stacks:** Swift, C/C++ with CMake, Go, Python, TypeScript/JavaScript, shell. A general guide handles the rest (Rust, Java, Kotlin, Ruby, PHP, .NET, Elixir, Dart).
- **Legacy code:** characterization tests and seams make untested code safe to change.
- **Integration:** real local servers instead of mocks; reconnect, timeout, shutdown, and cleanup tests.
- **Flaky tests:** no sleeps, controlled clocks and randomness, root-cause fixes.

Guides load only when a project needs them, so they cost no context otherwise.

## Files

```text
.claude-plugin/   plugin and marketplace manifests, icon
skills/           the workflow (SKILL.md) and its guides
hooks/            the edit gate
```

## Privacy

Collects nothing, sends nothing. See [PRIVACY.md](PRIVACY.md).

## License

[MIT](LICENSE)
