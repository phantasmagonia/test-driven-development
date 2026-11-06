# Shell scripts

Install, deploy, and release scripts are often the least tested code in a project. They are testable.

## Detect

`*.sh`, `*.bash`, `*.zsh`, or files starting with `#!/bin/sh` / `#!/usr/bin/env bash`. Tests: `*.bats` in `test/`.

## Tools

- `shellcheck script.sh` on every script you touch.
- `bats test/` to run tests.
- Neither available? A plain script that runs the target, checks results, exits nonzero on failure.

## Write

Run the script; check exit code, output, and files.

```bash
#!/usr/bin/env bats

setup() {
  WORK=$(mktemp -d); STUBS="$WORK/bin"; mkdir -p "$STUBS"
  PATH="$STUBS:$PATH"
}
teardown() { rm -rf "$WORK"; }

@test "fails with usage when no argument is given" {
  run ./install.sh
  [ "$status" -eq 2 ]
  [[ "$output" == *usage* ]]
}

@test "restarts the service after copying the config" {
  printf '#!/bin/sh\necho "$@" >> "%s/calls"\n' "$WORK" > "$STUBS/systemctl"
  chmod +x "$STUBS/systemctl"
  run ./install.sh --prefix "$WORK"
  [ "$status" -eq 0 ]
  [ -f "$WORK/etc/app.conf" ]
  grep -q "restart app" "$WORK/calls"
}
```

## Seams

- **Stub commands on PATH** (`systemctl`, `curl`, `ssh`, `codesign`). Stubs record arguments and print canned output.
- **Configurable paths**: `PREFIX=${PREFIX:-/usr/local}`.
- **Bash functions + main guard**: `[[ "${BASH_SOURCE[0]}" == "$0" ]] && main "$@"`, so tests can `source` and call functions.

## Test

- Bad arguments: clear message, nonzero exit.
- A failing command stops the script and leaves nothing half-done.
- Safe to run twice, if it should be.
- Temp files removed on success, failure, and interrupt (`trap ... EXIT`).
- Paths with spaces.

## Watch out

- Never let tests touch real system paths, servers, or credentials.
- `/bin/sh` is not always bash. Test with the shell in the shebang.
