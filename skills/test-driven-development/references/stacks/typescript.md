# TypeScript and JavaScript

## Detect

`package.json` `test` script is the source of truth. Then: `vitest.config.*` (Vitest), `jest.config.*` (Jest), `node:test` imports, `playwright.config.*` (E2E). Use the package manager matching the lock file.

## Run

```sh
npm test
npx vitest run src/cart.test.ts -t "rejects negative price"
npx jest src/cart.test.ts -t "rejects negative price"
node --test --test-name-pattern="negative" test/
npx playwright test tests/checkout.spec.ts
npx tsc --noEmit
```

`vitest run`, not bare `vitest`, which watches forever.

## Write

```ts
import { describe, it, expect } from "vitest";
import { cartTotal } from "./cart";

describe("cartTotal", () => {
  it("rejects a negative price", () => {
    expect(() => cartTotal([{ price: -1, quantity: 1 }])).toThrow(/price/);
  });

  it.each([[0, 10], [25, 7.5], [150, 0]])("applies a %i%% discount", (discount, expected) => {
    expect(cartTotal([{ price: 10, quantity: 1 }], discount)).toBe(expected);
  });
});
```

- `toBe` primitives, `toEqual` objects, `toBeCloseTo` floats.
- `await expect(p).rejects.toThrow()`. An unawaited promise passes before asserting.
- Components: Testing Library, query by role and label, not test IDs.

## Seams

- Pass dependencies in. `vi.mock` / `jest.mock` are a fragile fallback with ES modules.
- HTTP: `msw`, or a real local server on port 0.
- Time: fake timers, advanced explicitly, restored after each test.

## End-to-end

Playwright waits for you. Never `waitForTimeout`; use `await expect(locator).toBeVisible()`. Critical flows only.

## Coverage

```sh
npx vitest run --coverage
npx jest --coverage
```

## Watch out

- Snapshots pass when regenerated. Use explicit assertions for new behavior.
- Many test setups strip types without checking. Run `tsc` too.
