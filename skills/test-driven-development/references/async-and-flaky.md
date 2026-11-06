# Timing, concurrency, flaky tests

A flaky test is a real bug in the test or the code, almost always about time or order.

## Never sleep to wait

A sleep guesses machine speed: too short on CI, wasted time locally. Wait for the condition:

```text
deadline = now + 2s
until condition():
    if now > deadline: fail("not met within 2s")
    pause 10-50ms
```

Better: wait on a signal from the code (callback, future, channel, expectation).

## Control time

Inject the clock (`now()` function, clock object, scheduler). Tests advance a fake clock. A 30-minute timeout test runs in milliseconds.

## Control randomness and order

- Seed or inject randomness.
- Do not rely on map or set order unless guaranteed.
- Do not rely on test order. Shuffle to find hidden coupling.

## Concurrency

- Run under the race detector or thread sanitizer.
- Every thread, task, or goroutine a test starts ends before the test does.
- Force interleavings with barriers or latches, not luck.

## Fixing a flaky test

1. **Reproduce**: loop it hundreds of times, under load or in parallel.
2. **Find the cause**: sleeps, shared state, real clocks, unseeded randomness, fixed ports, leftover files, unawaited async.
3. **Fix it**, then loop again.

No retries to hide flakiness. If you must disable a test, give the reason and tell the user.
