# Docker and CI with uv

Best practices from the uv docs and ecosystem.

## Docker

**Multi-stage (builder pattern):** Use an intermediate stage with the official `ghcr.io/astral-sh/uv` image to build the venv, then copy only `.venv` (and app code) into a slim runtime image. The final image does not need uv or Rust.

**Layer caching:** Copy `uv.lock` and `pyproject.toml` first, then run `uv sync` (or equivalent). Dependencies install in a cached layer that invalidates only when lockfile/metadata change. Copy source code after.

**Environment variables:**
- `UV_COMPILE_BYTECODE=1` — compile bytecode for faster container startup.
- `UV_LINK_MODE=copy` — use copy instead of hardlinks so the venv works correctly when using cache mounts or when copying across stages (hardlinks cannot span filesystems).

**Non-editable install:** Use `--no-editable` when syncing in Docker so the project is installed as a normal package; avoids depending on source in the final image.

**Non-root:** Run the container as a non-root user; copy `.venv` into a directory owned by that user. Excluding uv and build tools from the final image reduces attack surface.

**Build failures:** If packages build from source (no wheel), the builder stage needs compilers and dev headers (e.g. `build-essential`, `python3-dev`). See [troubleshooting.md](troubleshooting.md).

**Minimal Dockerfile (multi-stage):**

```dockerfile
# Build stage
FROM ghcr.io/astral-sh/uv:latest AS builder
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --no-editable --no-dev
COPY . .
RUN uv sync --no-editable --no-dev

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "yourapp"]
```

Docs: https://docs.astral.sh/uv/guides/integration/docker/

## CI (e.g. GitHub Actions)

**Install uv:** Use the official `astral-sh/setup-uv` action so uv is installed and cache can be configured.

**Lockfile:** Use `uv sync --locked` (or equivalent) so the job **fails** if the lockfile is out of sync with `pyproject.toml`. Prevents deploying untested dependency versions.

**Caching:** Configure cache so `uv.lock` and `pyproject.toml` drive cache keys. Prefer a shared/global cache (e.g. on main) so PRs reuse it and unchanged deps don’t reinstall.

**Cache pruning:** On self-hosted or large pipelines, run `uv cache prune --ci` at the end of the job to keep the cache size under control.

**Matrix (multiple Python versions):** Set the Python version in the setup action so the matrix tests the intended interpreters; use `--locked` for reproducibility.

**Minimal GitHub Actions workflow:**

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
      - run: uv sync --locked
      - run: uv run pytest
```

Docs: https://docs.astral.sh/uv/guides/integration/github/
