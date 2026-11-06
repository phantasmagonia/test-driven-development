# Other stacks

## Find the test command

Check in order. CI is the most trustworthy.

1. CI config: `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/`, `Jenkinsfile`
2. Task runners: `Makefile`, `justfile`, `Taskfile.yml`, `package.json` scripts, `scripts/`
3. Docs: `CONTRIBUTING.md`, `README.md`
4. The manifest:

| Manifest | All | One |
|---|---|---|
| `Cargo.toml` | `cargo test` | `cargo test cart::rejects_negative` |
| `pom.xml` | `mvn test` | `mvn test -Dtest=CartTest#rejectsNegative` |
| `build.gradle(.kts)` | `./gradlew test` | `./gradlew test --tests 'CartTest.rejectsNegative'` |
| `*.csproj`, `*.sln` | `dotnet test` | `dotnet test --filter Name~RejectsNegative` |
| `Gemfile` (RSpec) | `bundle exec rspec` | `bundle exec rspec spec/cart_spec.rb:12` |
| `Gemfile` (Minitest) | `bin/rails test` | `ruby -Itest test/cart_test.rb -n /negative/` |
| `composer.json` | `vendor/bin/phpunit` | `vendor/bin/phpunit --filter rejectsNegative` |
| `mix.exs` | `mix test` | `mix test test/cart_test.exs:12` |
| `pubspec.yaml` | `flutter test` / `dart test` | `flutter test test/cart_test.dart --plain-name negative` |
| `build.zig` | `zig build test` | per build script |

## No tests at all

Add the runner the language's own docs recommend, with one passing test. Tell the user which and why.

Before starting, know three things: how to run everything, how to run one test, what a failure looks like.
