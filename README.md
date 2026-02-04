# data-skills

A collection of Claude Code skills for data engineering tasks.

## Overview

This repository contains expert assistant skills designed to help with data engineering workflows. Each skill provides specialized knowledge, templates, and best practices for specific data tools and patterns.

## Available Skills

| Skill | Description | Version | Docs |
|-------|-------------|---------|------|
| [dlt-skill](skills/dlt-skill/) | Data pipelines with [dlt](https://dlthub.com) (data load tool) | 0.1.0 | [Guide](docs/dlt-skill.md) |
| [dlt-dagster](skills/dlt-dagster/) | Run dlt pipelines in [Dagster](https://dagster.io) (Component or Pythonic @dlt_assets) | 0.1.0 | — |
| [uv](skills/uv/) | Python dependencies, venvs, and scripts with [uv](https://docs.astral.sh/uv/) | 0.1.0 | [Guide](docs/uv.md) |

## Installation

Install skills using the Claude Code CLI:

```bash
npx skills add untitled-data-company/data-skills --skill <skill-name>
```

For example, to install the dlt-skill:

```bash
npx skills add untitled-data-company/data-skills --skill dlt-skill
```

To install the dlt-dagster (dlt on Dagster) skill:

```bash
npx skills add untitled-data-company/data-skills --skill dlt-dagster
```

To install the uv (Python environments) skill:

```bash
npx skills add untitled-data-company/data-skills --skill uv
```

### Verify Installation

After installation, the skill should appear when you run `/skills` in Claude Code.

## Repository Structure

```
data-skills/
├── skills/
│   ├── dlt-skill/       # Data pipelines (dlt)
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   ├── references/
│   │   └── scripts/
│   ├── dlt-dagster/     # dlt pipelines in Dagster
│   │   ├── SKILL.md
│   │   ├── assets/templates/
│   │   └── references/
│   └── uv/              # Python venvs & deps (uv)
│       ├── SKILL.md
│       └── references/
├── docs/                # User documentation
│   ├── dlt-skill.md
│   └── uv.md
├── README.md
└── CHANGELOG.md
```

## Contributing

To add a new skill:
1. Create a new directory under `skills/`
2. Add a `SKILL.md` with the skill instructions (frontmatter: name, description)
3. Include any templates, references, or scripts needed
4. Add user documentation in `docs/<skill-name>.md`
5. Add an entry to the "Available Skills" table above

## License

Skills in this repository are provided as-is for use with Claude and other skill-enabled LLMs. Maintained by [Untitled Data Company](https://untitleddata.company/).
