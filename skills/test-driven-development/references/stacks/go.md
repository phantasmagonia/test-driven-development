# Go

## Detect

`go.mod`. Tests are `*_test.go` beside the code. Fixtures in `testdata/`.

## Run

```sh
go test ./...
go test ./internal/cart -run 'TestTotal/negative_price'
go test ./... -count=1        # skip the cache
go test ./... -race
go vet ./...
```

Use `-count=1` when tests touch files, network, or environment.

## Write

```go
func TestTotal(t *testing.T) {
	tests := []struct {
		name     string
		items    []Item
		discount float64
		want     float64
	}{
		{"empty cart", nil, 0, 0},
		{"discount applies", []Item{{Price: 10, Qty: 1}}, 25, 7.5},
		{"discount above 100 is capped", []Item{{Price: 10, Qty: 1}}, 150, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := Total(tt.items, tt.discount); got != tt.want {
				t.Errorf("Total() = %v, want %v", got, tt.want)
			}
		})
	}
}
```

- Red step: add one row.
- `t.Helper()` in assertion helpers. `t.TempDir()`, `t.Cleanup()`, `t.Setenv()` all clean up on failure.

## Seams

Small interfaces defined where they are used. Accept interfaces, return structs.

## Network

```go
srv := httptest.NewServer(http.HandlerFunc(handler)); t.Cleanup(srv.Close)
ln, _ := net.Listen("tcp", "127.0.0.1:0")
pc, _ := net.ListenPacket("udp", "127.0.0.1:0")
```

## Golden files and fuzzing

- Large output: `testdata/*.golden` with an `-update` flag. Review regenerated diffs.
- Parsers: `FuzzXxx(f *testing.F)`, `go test -fuzz=FuzzXxx -fuzztime=30s`. Crashes become test cases.

## Coverage

```sh
go test ./... -coverprofile=cover.out && go tool cover -func=cover.out
```

## Watch out

- `t.Parallel()` subtests share no mutable state. Check with `-race`.
- Goroutines a test starts must finish before it returns. `WaitGroup` or done channel, never sleep.
