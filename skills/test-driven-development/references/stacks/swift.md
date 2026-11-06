# Swift

## Detect

- `Package.swift`: SwiftPM, tests in `Tests/<Target>Tests/`.
- `*.xcodeproj` / `*.xcworkspace`: Xcode. `project.yml` (XcodeGen) or `Project.swift` (Tuist): edit the spec, regenerate.
- `import Testing` = Swift Testing, `import XCTest` = XCTest. Match the file; prefer Swift Testing for new files (Swift 6+).

## Run

```sh
swift test
swift test --filter CartTests/rejectsNegativePrice

xcrun simctl list devices available
xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 16'
xcodebuild test -scheme App -destination 'platform=macOS' -only-testing:AppTests/CartTests/testRejectsNegativePrice
```

Search `xcodebuild` output for `error:` and `failed`, or pipe through `xcbeautify`. A build error is not a red test.

## Write

```swift
import Testing
@testable import Shop

@Suite struct CartTests {
    @Test func rejectsNegativePrice() {
        #expect(throws: CartError.negativePrice) { try Cart().add(price: -1) }
    }

    @Test(arguments: [0, 1, 99])
    func acceptsValidQuantity(_ quantity: Int) throws {
        #expect(try Cart().adding(quantity: quantity).count == quantity)
    }
}
```

- `#expect` continues on failure; `#require` stops and unwraps (`try #require(cart.first)`).
- Main-actor code: mark the test or suite `@MainActor`.
- XCTest: `XCTestCase`, `test…` methods, `XCTAssertEqual`, `XCTAssertThrowsError`, `XCTUnwrap`.

## Seams

A small protocol in front of the network, clock, storage, or system frameworks, injected with a real default:

```swift
protocol Clock { func now() -> Date }
struct SystemClock: Clock { func now() -> Date { Date() } }

struct Session {
    let clock: any Clock
    init(clock: any Clock = SystemClock()) { self.clock = clock }
}
```

## Async

- `async` test, `await` directly. No fire-and-forget `Task {}`.
- Events: `confirmation` (Swift Testing) or `await fulfillment(of:timeout:)` (XCTest).
- No `Task.sleep` to wait.
- Networking: real local `NWListener` on port 0.

## Coverage

```sh
swift test --enable-code-coverage && swift test --show-codecov-path
xcodebuild test ... -enableCodeCoverage YES -resultBundlePath build/T.xcresult
xcrun xccov view --report build/T.xcresult
```

## Watch out

- XCUITest is slow and fragile. Critical flows only.
- Simulator names change per Xcode. List, don't guess.
- Entitlement, signing, or device-only code: keep it thin, test the logic behind it, report the gap.
