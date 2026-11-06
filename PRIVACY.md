# Privacy

The `test-driven-development` plugin contains instructions only. It runs no code and reads no files or credentials.

The optional `tdd-gate` plugin runs command hooks. It reads the `TDD_GATE` environment variable, hook input, and the local Claude Code session transcript to check whether the skill was invoked. It writes nothing, sends nothing, makes no network calls, and retains nothing after each check exits.
