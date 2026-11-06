# Python

## Detect

- pytest: `[tool.pytest.ini_options]`, `pytest.ini`, `conftest.py`, or a pytest dependency.
- unittest: `unittest.TestCase` and no pytest config.
- Environment: `uv.lock` → `uv run`, `poetry.lock` → `poetry run`, `tox.ini` / `noxfile.py` → project sessions.

## Run

```sh
uv run pytest
uv run pytest tests/test_cart.py::test_rejects_negative_price
uv run pytest -k "discount and not tax"
uv run pytest -x --lf
python -m unittest tests.test_cart.CartTests.test_rejects_negative_price
```

## Write

```python
import pytest
from shop.cart import cart_total


def test_rejects_negative_price():
    with pytest.raises(ValueError, match="price"):
        cart_total([{"price": -1, "quantity": 1}])


@pytest.mark.parametrize("discount, expected", [(0, 10.0), (25, 7.5), (150, 0.0)])
def test_discount(discount, expected):
    assert cart_total([{"price": 10, "quantity": 1}], discount) == expected
```

- Plain `assert`. Floats: `pytest.approx`.
- Fixtures: `tmp_path`, `monkeypatch`, `capsys`. Shared ones in `conftest.py`.

## Seams

- Pass collaborators in. Beats patching.
- Patching: patch where the name is **used** (`shop.cart.fetch_rates`), not defined.
- `autospec=True`, so wrong signatures fail.
- Inject time instead of patching `datetime`.

## Integration

Files: `tmp_path`. HTTP: `http.server` on port 0 in a thread, or the project's tool (`respx`, `responses`, `pytest-httpserver`). Database: in-memory SQLite or a throwaway fixture.

Parsers and math: `hypothesis`. Each failure becomes a regression test.

## Coverage

```sh
uv run pytest --cov=shop --cov-branch --cov-report=term-missing
```

## Watch out

- Pass alone, fail together: shared globals, caches, env, or working directory. Reset in a fixture.
- Async: use the plugin the project already has (`pytest-asyncio` or `anyio`).
