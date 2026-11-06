---
name: test-driven-development
description: Required before writing, changing, fixing, or refactoring code in any language. Strict test-first workflow - triage what needs tests, write a failing test, make it pass with minimal code, refactor, report exactly what ran. Covers untested legacy code too.
---

# Test-Driven Development

**No logic without a failing test first.**

Every code change follows this cycle. Repeat steps 3-5 per behavior.

1. **Orient**: find the test command, run the suite once.
2. **Triage**: decide which pieces contain logic.
3. **Red**: one test, one behavior, seen failing.
4. **Green**: least code that passes.
5. **Refactor**: clean up while green.
6. **Report**: full suite, then state what ran and what did not.

## 1. Orient

- Find the stack and test command (manifest, CI config, Makefile, README). Load the matching `references/stacks/` file, or `other.md`.
- Run the suite once. Note tests that already fail; do not hide or silently fix them.
- Learn to run a single test.
- No test runner? Choose the smallest practical way to run a focused test, and report what remains unverified.
- Changing untested code? Read `references/legacy-code.md` first.

## 2. Triage: the Logic Gate

| Logic: test first | No logic: write directly |
|---|---|
| Branches, conditions | Data declarations, types |
| Calculations, transformations | Constants, config |
| Parsing, validation | Pass-through wrappers |
| State changes | Static text, styling |
| Error handling that decides | Generated code, boilerplate |

No branch, transformation, or state change: no test needed. Unsure: treat as logic.

State it in one line: *"Test first: discount math, quantity validation. Direct: `Item` type, tax constant."*

## 3. Test level

- **Unit** for pure logic. Most tests.
- **Integration** for code that talks to files, databases, networks, processes, or OS APIs. Use the real thing locally. See `references/integration.md`.
- **End-to-end** only for flows that must never break.

Fake a dependency only if it is slow, nondeterministic, costly, or outside your control. Never fake the code under test. Prefer hand-written fakes to mocking frameworks.

## 4. Red

- One behavior per test, named for it (`rejects_negative_price`). Needs "and"? Split it.
- Call the code like a real caller. Assert on results, not internals.
- Run it. It must fail because the behavior is missing, not from a typo, import, or setup error.
- Passes immediately? The behavior exists (keep the test, say so) or the test is wrong (fix it until it can fail).

## 5. Green

- Simplest code that passes. Add nothing no test asks for.
- Run the new test, then the related suite.

## 6. Refactor

- Remove duplication, improve names, in code and tests.
- Run tests after each step. Red? Undo the step.
- New behavior needs a new red test.

## Bugs

Reproduce the bug in a failing test first. Then fix. The test stays.

## Logic written before its test

Write a test that fails against the current behavior before proceeding. Then make the smallest change that passes it and report the sequence honestly.

## Spikes

Only when the user asks for a spike, prototype, or throwaway code: write it without tests to learn fast. Label it **untested spike** in the report. Before it counts as done, delete it and rebuild test-first.

## Always

- **Never bend tests to pass.** No weakened assertions, skips, or deletions. If a test is wrong, fix it and say so.
- **No sleeping to wait.** Wait on a condition with a deadline, or control time. See `references/async-and-flaky.md`.
- **Tests clean up** every file, port, process, and connection, even on failure.
- **Deterministic.** Control time, randomness, environment, order. Flaky means bug.
- **Offline by default.** Tests needing real services or credentials are opt-in.
- **Coverage finds gaps.** It is not a target.

## Report

Run the full suite, plus linter and type checker if the project has them. Then:

1. **Changes**: behavior change in one or two sentences.
2. **Tests added**: names, each confirmed failing first.
3. **Checks run**: exact commands and results.
4. **Not checked**: what and why (device, credentials, network, pre-existing failures).

No logic changed? One line: *"No logic changed. Ran `<command>`: OK."*

Never claim tests pass without running them in this session.

## Rejected excuses

| Excuse | Answer |
|---|---|
| "Tests after." | They pass on first run and prove nothing. |
| "Too simple." | Then the test is quick. No logic? No test is needed. |
| "Tested by hand." | Not repeatable. |
| "Hard to test." | Too many dependencies. Add a seam. |
| "Just a refactor." | Needs green tests first. None? Characterize first. |
| "Flaky, rerun." | It hides a timing or ordering bug. Find it. |

## References

Load only what the task needs.

- `references/stacks/`: `swift.md`, `cpp-cmake.md`, `go.md`, `python.md`, `typescript.md`, `shell.md`, `other.md`
- `references/legacy-code.md`: getting untested code under test
- `references/integration.md`: real local dependencies, reconnect, shutdown, cleanup
- `references/async-and-flaky.md`: timing, concurrency, flaky tests
