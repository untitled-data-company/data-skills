# Workspaces and Resolution

## Workspaces (monorepos)

For multiple related packages in one repo, uv **workspaces** use a single lockfile and shared resolution.

**Setup:** At the repo root, add to `pyproject.toml`:

```toml
[tool.uv.workspace]
members = ["apps/*", "libs/*"]
```

Each member is a directory with its own `pyproject.toml`. The root holds the single `uv.lock`.

**Local dependencies:** In a member’s `pyproject.toml`, depend on another member via `source = { workspace = true }` (or the equivalent for your layout). uv links internal packages without publishing to PyPI.

**Run per member:** `uv run --package <member-name> <command>` runs in the context of that workspace member (e.g. `uv run --package my-app pytest`).

**Benefits:** One lockfile keeps versions consistent across the monorepo; no “dependency hell” between apps and libs. Good fit for Polylith-style layouts; use linting (e.g. ruff, pyright) at the root to enforce import boundaries between members.

Docs: https://docs.astral.sh/uv/concepts/projects/workspaces/

## Resolution strategies

**Default:** uv resolves to the **highest** compatible versions (latest features and security patches).

**Library / bounds testing:** Use `--resolution lowest-direct` to force the **oldest** compatible version of **direct** dependencies while keeping transitive deps at their resolved versions. Useful for checking that a library works with the minimum declared versions. A blanket “lowest everything” often fails due to transitive deps.

**Platform constraints:** In `pyproject.toml`, use `tool.uv.sources` or environment settings to restrict resolution to a subset of platforms if the project doesn’t support all environments; can speed up resolution for large graphs.

Docs: https://docs.astral.sh/uv/concepts/resolution/
