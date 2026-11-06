# C and C++ with CMake

## Detect

- `enable_testing()` + `add_test(...)` in `CMakeLists.txt`: CTest.
- `CMakePresets.json`: use the presets.
- Framework: GoogleTest (`gtest/gtest.h`), Catch2, doctest, or plain executables that exit nonzero on failure.

## Run

```sh
cmake --preset debug && cmake --build --preset debug && ctest --preset debug

cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug && cmake --build build --parallel
ctest --test-dir build --output-on-failure
ctest --test-dir build -R CartTotal --output-on-failure
./build/tests/cart_tests --gtest_filter='Cart.*'
```

Rebuild before every run. Stale binaries lie.

## Write

```cpp
#include <gtest/gtest.h>
#include "cart.hpp"

TEST(Cart, RejectsNegativePrice) {
  EXPECT_THROW(Cart{}.add(-1.0), std::invalid_argument);
}
```

```cmake
include(GoogleTest)
add_executable(cart_tests cart_tests.cpp)
target_link_libraries(cart_tests PRIVATE cart GTest::gtest_main)
gtest_discover_tests(cart_tests)
```

Hand-written check helpers: print what failed, exit nonzero.

## Seams

- Small abstract interfaces or template parameters.
- One thin adapter around OS and network calls.
- Link seams for C, as a last resort.

## Sanitizers

```sh
cmake -S . -B build-asan -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer"
cmake --build build-asan && ctest --test-dir build-asan --output-on-failure
```

`-fsanitize=thread` for concurrency, in its own build.

## Coverage

GCC: `--coverage`, then `gcovr`. Clang: `-fprofile-instr-generate -fcoverage-mapping`, then `llvm-profdata merge` and `llvm-cov report`.

## Watch out

- Warnings as errors apply to tests too.
- Undefined behavior can pass by accident. Sanitizers catch it.
