# uv Usage Examples

## New project from scratch

```bash
uv init my-app
cd my-app
uv add requests httpx
uv add --dev pytest ruff
uv run python -c "import requests; print(requests.get('https://example.com').status_code)"
uv run pytest
```

## Add a dependency to existing project

```bash
uv add django
# or with version
uv add "django>=4.2"
# dev dependency
uv add --dev black
```

## Run script with inline dependencies (no project)

**script.py:**

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
import requests
print(requests.get("https://api.github.com").json()["current_user_url"])
```

```bash
uv run script.py
```

Or add deps from CLI:

```bash
uv add --script script.py requests
uv run script.py
```

## Run script via shebang (executable without typing uv run)

**script.py** (make executable: `chmod +x script.py`, then run as `./script.py`):

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
import requests
print(requests.get("https://example.com").status_code)
```

```bash
chmod +x script.py
./script.py
```

## One-off CLI tool

```bash
uvx ruff check .
uvx black --check .
uvx pycowsay "Hello from uv"
```

## Convert from requirements.txt to uv (pyproject.toml + uv.lock)

After the user confirms they want to convert:

```bash
uv init
uv add -r requirements.txt
uv sync
# optionally: remove or keep requirements.txt
```

If you have requirements.in and locked requirements.txt and want to preserve exact versions:

```bash
uv init
uv add -r requirements.in -c requirements.txt
uv sync
```

## Use uv with existing requirements.txt (no conversion)

```bash
uv venv
uv pip sync requirements.txt
# or compile from .in
uv pip compile requirements.in -o requirements.txt --universal
uv pip sync requirements.txt
```

## Pin and use specific Python

```bash
uv python pin 3.11
uv python install 3.11
uv sync
uv run python --version
```

## Run with different Python (one-off)

```bash
uv run --python 3.10 python script.py
```

## Migrate from Poetry or Pipenv to uv

After the user confirms they want to switch:

```bash
uvx migrate-to-uv
# then
uv sync
# remove poetry.lock / Pipfile / Pipfile.lock after confirming everything works
```
