# Integration tests

For code that talks to files, databases, networks, processes, or the OS. A fake here only tests your assumptions. Use the real thing, locally.

| Dependency | Local stand-in |
|---|---|
| Files | Fresh temporary directory per test |
| HTTP, TCP, UDP | Small in-test server on `127.0.0.1`, port 0 |
| Database | In-memory engine or throwaway instance |
| External command | Real if safe and fast; else a stub on `PATH` |
| Third-party API | Local server replaying recorded responses |

**Port 0** gets a free port from the OS. Read it back; never hard-code ports.

## Startup

- Bind before handing out the address.
- Async startup: wait on a ready signal or poll with a deadline.
- Keep test servers tiny: answer, answer wrong, stall, or drop.

## Unhappy paths

Test each integration point for:

- **Failure**: refused, error status, malformed or truncated data.
- **Timeout**: accepted, never answered. Code gives up in time.
- **Reconnect**: dropped mid-session. Code recovers or fails clearly, never loops forever.
- **Shutdown**: closes connections, ends threads and tasks, returns promptly, even mid-request.
- **Cleanup**: no leftover sockets, processes, files, or timers.

## Ownership

- A test closes what it opens, even on failure. Use the framework's cleanup hook.
- No test depends on another's state.

## Live tests

For real services, credentials, or devices:

- Opt-in only (environment variable or separate target). Skip visibly when off.
- Credentials from the environment, never in files.
- Report when they were not run.
