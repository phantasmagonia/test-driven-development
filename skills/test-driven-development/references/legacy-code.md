# Untested code

Code without tests cannot be changed safely, and often cannot be tested without changing it. Break the loop in small steps.

## Order

1. **Change point**: what has to change.
2. **Test point**: where a test can observe it, ideally a public entry point nearby.
3. **Break dependencies**: add a seam if the code builds its own database, network, or global state. Keep edits mechanical.
4. **Characterize**: pin down current behavior.
5. **Change test-first**: normal red, green, refactor.

## Characterization tests

1. Call the code with a realistic input.
2. Assert a wrong value (`assert result == "?"`).
3. Run it. The failure shows the real value.
4. Put that value in the assertion.
5. Repeat for every input the change affects, including errors.

These are the only tests written after the code. They are the setup for TDD, not an exception to it.

Current behavior looks wrong? Keep the test, add a comment, tell the user. Fixing it is a separate change with its own failing test.

Large outputs: save a golden file once, compare against it, review every diff by hand.

## Seams

| Seam | How | For |
|---|---|---|
| Parameter | Pass the dependency in | Clocks, randomness, clients |
| Interface | Depend on a small interface, pass a fake | Storage, network, OS |
| Default argument | `init(client: Client = RealClient())` | Keeping callers unchanged |
| Subclass and override | Move the hard call to a method, override it | Classes not yet redesignable |
| Setting | Read a path or command from config with a default | Scripts, CLIs |
| Link or PATH | Swap an object file or stub a command | C, shell |

Prefer the top rows.

## New code in hard code

- **Sprout**: write the new logic as a new tested function; call it from the old code in one line.
- **Wrap**: rename the old function; a new function with the old name does the new work and calls it.

## Rules

- Before tests exist, only mechanical refactors: rename, extract, add parameter. Prefer automated tools.
- Leave untouched code alone.
- Report what is characterized and which suspected bugs remain.
