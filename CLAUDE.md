# Working in this repository

For code changes, use the test-driven-development skill if it is available. Before changing behavior, run the existing tests for a baseline, write a focused test, and confirm it fails for the intended reason. Make the smallest change that passes it, then run the relevant suite. Report the exact checks run and any limits.

Changes to prose, metadata, and static assets do not need a new test. Keep the two plugins separate: `plugins/test-driven-development/` contains instructions only; `plugins/tdd-gate/` owns all command hooks.
