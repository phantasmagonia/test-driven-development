# Test-Driven Development for Claude Code

A skill that guides Claude through test-first code changes: confirm a focused test fails, make it pass with the smallest change, then report what was checked. It supports multiple languages and includes guides for legacy code, integration tests, and flaky tests.

## Install

Install **Test Driven Development** from the Claude plugin directory once it is listed. To try a local clone in Claude Code:

```sh
claude --plugin-dir /path/to/test-driven-development
```

## Use

Ask for a coding change normally. Claude Code can select the skill automatically when the task matches its description; you can also invoke `/test-driven-development` directly. A command is not required for every task.

For a standing preference across projects, add this once to `~/.claude/CLAUDE.md`. To share it with a team, put it in the project's `CLAUDE.md` instead:

```md
For code changes, load the test-driven-development skill before editing.
Write a focused failing test for each behavior change, make it pass, then run
relevant tests and report the exact commands and results.
```

The skill and `CLAUDE.md` guide Claude's behavior. They do not enforce edits.

## Workflow

1. Find the project's test command and run a baseline.
2. Identify the behavior that needs a test.
3. Write a focused test and confirm it fails for the intended reason.
4. Make the smallest change that passes it.
5. Refactor while tests stay green.
6. Report the checks run and any limits.

The full workflow and stack-specific guidance live in [SKILL.md](skills/test-driven-development/SKILL.md).

## Privacy

This plugin contains instructions only. It has no hooks or executable code. See [PRIVACY.md](PRIVACY.md).

## License

[MIT](LICENSE)
