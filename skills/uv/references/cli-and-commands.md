# uv CLI Reference

Summary of uv commands and options. Full docs: https://docs.astral.sh/uv/

**Migration:** Converting from requirements.txt to a uv project: https://docs.astral.sh/uv/guides/migration/pip-to-project/

## Project Commands

| Command | Purpose |
|---------|---------|
| `uv init [name]` | Create new project (pyproject.toml, optional dir) |
| `uv add <pkg>...` | Add dependency; updates pyproject.toml and lockfile |
| `uv add -r requirements.txt` | Add all dependencies from a requirements file (import) |
| `uv add -r requirements.in -c requirements.txt` | Import with locked versions preserved |
| `uv add --dev <pkg>` | Add dev/optional dependency |
| `uv remove <pkg>` | Remove dependency |
| `uv sync` | Install from lockfile; create/update .venv |
| `uv lock` | Resolve and write lockfile only |
| `uv export` | Export lockfile to requirements.txt etc. |
| `uv tree` | Show dependency tree |
| `uv run <cmd>` | Run command in project venv (creates if needed) |
| `uv run script.py` | Run script in project env |

## Script Commands

| Command | Purpose |
|---------|---------|
| `uv add --script <file> <pkg>` | Add dependency for script (writes inline metadata) |
| `uv run script.py` | Run script; uses inline deps or project env |

## Tools

| Command | Purpose |
|---------|---------|
| `uvx <pkg> [args]` | Run tool once (ephemeral env); alias for `uv tool run` |
| `uv tool install <pkg>` | Install tool for repeated use |
| `uv tool run <pkg> [args]` | Run installed tool |

## Python & Venvs

| Command | Purpose |
|---------|---------|
| `uv venv [path]` | Create virtual environment (default .venv) |
| `uv venv --python 3.11` | Create venv with specific Python |
| `uv python install 3.11` | Install Python version |
| `uv python pin 3.11` | Pin version in .python-version |
| `uv python list` | List installed Python versions |

## Pip Interface

| Command | Purpose |
|---------|---------|
| `uv pip install <pkg>` | Install into current venv (pip-compatible) |
| `uv pip sync requirements.txt` | Install from locked requirements |
| `uv pip compile requirements.in -o requirements.txt` | Resolve and lock (e.g. --universal) |

## Build & Publish

| Command | Purpose |
|---------|---------|
| `uv build` | Build sdist and wheel |
| `uv publish` | Upload to index |

## Options (common)

- `--python <version>`: Use specific Python (e.g. `uv run --python 3.11 python app.py`)
- `--no-cache`: Disable cache
- `--no-install-project`: Don't install the project itself (e.g. when syncing deps only)

## Lockfile and Layout

- Lockfile: `uv.lock` (commit it).
- Default venv: `.venv` in project root.
- Use `uv sync` after clone or after changing dependencies.
