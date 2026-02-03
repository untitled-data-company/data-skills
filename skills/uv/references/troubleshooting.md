# uv Troubleshooting

Common issues and how to resolve them.

## uv: command not found

uv is not installed or not on PATH.

**Fix:**

- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux) or see https://docs.astral.sh/uv/getting-started/installation/
- Ensure the install directory is on PATH (installer usually adds it).
- In CI or scripts, use the full path or ensure the environment has uv installed.

## Lockfile conflicts or uv.lock out of date

After pulling changes or editing `pyproject.toml`, the lockfile may be stale or conflict.

**Fix:**

- Run `uv lock` to refresh the lockfile from `pyproject.toml`.
- Run `uv sync` to install from the updated lockfile.
- If conflicts persist, ensure only one lockfile (uv.lock) is used; remove or ignore poetry.lock / Pipfile.lock if the project has switched to uv.

## Resolution errors (no matching version, conflicts)

uv cannot resolve dependency versions (e.g. incompatible constraints).

**Fix:**

- Relax or align version constraints in `pyproject.toml` (e.g. `package>=x,<y`).
- Run `uv lock --verbose` (or check the error) to see which package causes the conflict.
- Remove the problematic dependency temporarily, run `uv lock`, then add it back with a compatible version.

## .venv not found or wrong Python

IDE or terminal uses a different Python than the project’s `.venv`.

**Fix:**

- Run `uv sync` to create or update `.venv` from the lockfile.
- Set the workspace interpreter to the project’s `.venv`: add or update `python.defaultInterpreterPath` in `.vscode/settings.json` (see IDE Setup in SKILL.md).
- Use `uv run <command>` so uv uses the project’s `.venv` automatically.

## Permission or cache errors

**Fix:**

- Run with `--no-cache` to bypass cache: `uv sync --no-cache` (debug only).
- Clear cache: `uv cache prune` (or `uv cache prune --ci` in CI to keep cache lean).
- Ensure the project directory and `.venv` are writable; on Windows, avoid installing under Program Files.

## Slow or hanging resolution

**Fix:**

- Check network; uv fetches package metadata from PyPI or configured indexes.
- Try `uv lock --no-cache` once to rule out cache corruption.
- For private indexes, ensure `tool.uv.index` or env vars are set correctly (see uv docs).

## Build failures (no wheel, building from source)

When a pre-built wheel is not available, uv builds the package from source and needs compilers and dev headers.

**Fix:**

- Install build tools: e.g. `build-essential`, `python3-dev`, `libffi-dev` (Linux); Xcode Command Line Tools (macOS); Visual Studio Build Tools (Windows).
- In Docker: use a builder stage that includes `build-essential` or equivalent; the final runtime image can stay slim.
- See https://docs.astral.sh/uv/reference/troubleshooting/build-failures/

## Cloud sync (OneDrive, Dropbox, etc.)

Projects under cloud-synced folders can hang or conflict because `.venv` and `.git` have many small files and frequent changes.

**Fix:**

- Exclude `.venv` from sync in the cloud client’s settings, or
- Put the venv elsewhere: set `UV_PROJECT_ENVIRONMENT` to a path outside the synced folder (e.g. a local temp or cache dir). The project stays in sync; the venv does not.

## Cache and multi-user / shared systems

uv uses a global cache (e.g. `~/.cache/uv`) and prefers hardlinks into `.venv`. For best performance and correctness:

- Keep the cache on the **same filesystem** as the project’s `.venv` so hardlinking works.
- On shared systems (e.g. jump boxes, HPC): **do not share one cache** across users; each user should have their own cache to avoid permission and consistency issues.

## Private indexes and corporate proxies

**Authentication:** Define indexes in `pyproject.toml` (e.g. `[[tool.uv.index]]`); **never hardcode credentials**. Use environment variables (e.g. `UV_INDEX_<NAME>_USERNAME`, `UV_INDEX_<NAME>_PASSWORD` for a named index).

**TLS / corporate proxies:** If uv fails with certificate errors behind an SSL-inspecting proxy, use the system certificate store: set `UV_NATIVE_TLS=1` or run with `--native-tls`. Use `HTTPS_PROXY` / `NO_PROXY` as needed for the proxy.
