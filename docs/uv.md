# uv

**Version 0.1.0**

Expert assistant skill for using [uv](https://docs.astral.sh/uv/) to manage Python dependencies, virtual environments, and scripts.

## Overview

This skill teaches the assistant to use uv correctly: project workflow (pyproject.toml + uv.lock), script workflow (inline metadata), tools (uvx), conversion from requirements.txt or poetry/pipenv, IDE interpreter setup, and best practices (lockfile, CI, Docker, workspaces).

## Installation

```bash
npx skills add untitled-data-company/data-skills --skill uv
```

### Verify Installation

After installation, the skill should appear when you run `/skills` in Claude Code.

## How to Use

### Slash command: `/uv`

The skill is named **`uv`**. In clients that map slash commands to skill names (e.g. `/uv` loads the skill named "uv"), you can invoke it by typing:

```
/uv
```

Then ask what you need (e.g. "add requests", "convert from requirements.txt", "set up the IDE interpreter").

### Install command

| Use case | Command |
|----------|--------|
| Install this skill | `npx skills add untitled-data-company/data-skills --skill uv` |
| Invoke (if supported) | `/uv` |
| List installed skills | `/skills` (in Claude Code) |

### Automatic activation

The skill also activates automatically when you (or the assistant) are working on:

- Python dependencies, venvs, or pyproject.toml
- Adding/removing packages, running scripts with uv
- Converting from requirements.txt, poetry, pipenv, or conda
- Setting the IDE Python interpreter, Docker/CI with uv

So you can also just say what you want, e.g. "Add requests with uv" or "Use uv for this project"; the assistant will apply the skill when it detects uv-related context.

## What the skill covers

- Project workflow: `uv init`, `uv add`, `uv sync`, `uv run`, `uv lock`
- Script workflow: inline script metadata (PEP 723), `uv add --script`, shebang
- Tools: `uvx`, `uv tool install`
- Conversion: requirements.txt → uv; poetry/pipenv → uv (including migrate-to-uv)
- IDE: `.vscode/settings.json` and `python.defaultInterpreterPath`
- References: CLI, Docker/CI, workspaces/resolution, troubleshooting

## Links

- [Skill contents](skills/uv/)
- [uv documentation](https://docs.astral.sh/uv/)
