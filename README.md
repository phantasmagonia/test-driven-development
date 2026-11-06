# Test-Driven Development for Claude Code

**No logic without a failing test first.**

A Claude Code skill plugin that guides test-first work in any language: start behavior changes with a failing test, finish with passing checks, and report exactly what ran.

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

Restart Claude Code. The directory-listed plugin contains only instructions and runs no hooks.

To try it locally: `claude --plugin-dir /path/to/this/repo/plugins/test-driven-development`

### Directory submission

For the public directory, select branch `directory-skill` and plugin path `.`. That branch contains only the skill, its metadata, icon, license, and documentation. The directory scanned files outside a nested plugin path on `main`, so submitting `main` would include the optional command hooks and Python files. Keep **Auto-publish passing versions** enabled in the developer portal; it is a portal setting, not a repository configuration. Copy skill updates from `main` to `directory-skill` before submitting a new version.

### Install the optional edit-tool gate

For the session reminder and edit gate, also install the separate `tdd-gate` plugin from this repository's marketplace:

```text
/plugin install tdd-gate@test-driven-development
```

The gate requires the skill plugin and `python3` (3.9+). It is not part of the directory listing. To try both plugins locally, pass both plugin directories to `claude --plugin-dir`.

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

## Adopt the workflow without hooks

Claude Code can invoke the installed skill when a coding task matches its description. For a standing preference, add this to a project's `CLAUDE.md` (shared with the team) or to `~/.claude/CLAUDE.md` (personal, across projects):

```md
When changing code, load the test-driven-development skill before editing.
Write a focused failing test for each behavior change, make it pass, then run
the relevant suite. Report the commands actually run and their results.
```

This repository has its own `CLAUDE.md` for contributors. It applies when Claude works in this repository; installing the plugin does not copy it into other projects. Instructions guide Claude's behavior but do not enforce edits.

## Optional edit gate

The separate `tdd-gate` plugin reminds Claude to load the skill and checks Claude Code Edit, Write, and MultiEdit calls.

With `tdd-gate` installed, every session starts with a reminder to load the workflow. Then a hook runs before Edit, Write, and MultiEdit calls. If the file is source code and the skill has not been invoked in the session, the edit is blocked and Claude is told to load it. Docs and config are never blocked. If the hook cannot read its input, it allows the edit instead of locking the session.

With the gate installed, turn it off for one session: `TDD_GATE=off claude`

The gate sees Claude's edit tools. File writes made through shell commands (`sed -i`, `cat > file`) are not gated.

## What it covers

- **Stacks:** Swift, C/C++ with CMake, Go, Python, TypeScript/JavaScript, shell. A general guide handles the rest (Rust, Java, Kotlin, Ruby, PHP, .NET, Elixir, Dart).
- **Legacy code:** characterization tests and seams make untested code safe to change.
- **Integration:** real local servers instead of mocks; reconnect, timeout, shutdown, and cleanup tests.
- **Flaky tests:** no sleeps, controlled clocks and randomness, root-cause fixes.

Guides load only when a project needs them, so they cost no context otherwise.

## Files

```text
.claude-plugin/              marketplace manifest
plugins/test-driven-development/  skill-only plugin, icon, and guides
plugins/tdd-gate/                optional command hooks
```

## Privacy

Neither plugin sends data. The optional gate reads the local session transcript. See [PRIVACY.md](PRIVACY.md).

## License

[MIT](LICENSE)
