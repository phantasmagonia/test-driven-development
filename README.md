# Test-Driven Development for Claude Code

**No logic without a failing test first.**

A skill-only Claude Code plugin that guides test-first work in any language. It contains Markdown instructions and references, with no hooks or executable code.

## Why

Tests written after implementation can pass immediately without showing that they catch the missing behavior. This workflow asks Claude to see a focused test fail first, make it pass with minimal code, and report exactly what ran.

## Install

Install Test Driven Development from the Claude plugin directory when its listing is approved. To try a local clone in Claude Code, run: claude --plugin-dir /path/to/test-driven-development

## Use

Ask for a code change as usual, or invoke /test-driven-development directly. The skill follows one cycle for each behavior:

1. Find the project's test command and run a baseline.
2. Decide what logic needs a test.
3. Write a focused test and confirm it fails for the intended reason.
4. Make the smallest change that passes it.
5. Refactor while tests stay green.
6. Report the exact commands run, results, and limits.

The skill includes guides for Swift, C/C++, Go, Python, TypeScript/JavaScript, shell, legacy code, integration tests, and flaky tests. Claude loads those references only when relevant.

## Standing instructions

To make this workflow a standing preference without hooks, add this to a project's CLAUDE.md or your ~/.claude/CLAUDE.md:

~~~md
When changing code, load the test-driven-development skill before editing.
Write a focused failing test for each behavior change, make it pass, then run
relevant tests and report the commands actually run.
~~~

Instructions guide Claude's behavior; they do not enforce edits.

## Directory submission

Submit this repository's main branch with the plugin path at the repository root. Keep **Auto-publish passing versions** enabled in the developer portal. That setting lives in the portal, not this repository.

The repository contains only the skill, its metadata, icon, license, and Markdown documentation. Keep command hooks and executable files out of this branch.

## Privacy

This plugin contains instructions only. See [PRIVACY.md](PRIVACY.md).

## License

[MIT](LICENSE)
