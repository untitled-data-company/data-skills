# data-skills

A collection of Claude Code skills for data engineering tasks.

## Overview

This repository contains expert assistant skills designed to help with data engineering workflows. Each skill provides specialized knowledge, templates, and best practices for specific data tools and patterns.

## Available Skills

| Skill | Description | Version | Docs |
|-------|-------------|---------|------|
| [dlt-skill](skills/dlt-skill/) | Data pipelines with [dlt](https://dlthub.com) (data load tool) | 0.1.0 | [Guide](docs/dlt-skill.md) |

## Installation

Install skills using the Claude Code CLI:

```bash
npx skills add untitled-data-company/data-skills --skill <skill-name>
```

For example, to install the dlt-skill:

```bash
npx skills add untitled-data-company/data-skills --skill dlt-skill
```

### Verify Installation

After installation, the skill should appear when you run `/skills` in Claude Code.

## Repository Structure

```
data-skills/
├── skills/
│   └── dlt-skill/       # Skill package (for Claude)
│       ├── SKILL.md     # Main skill instructions
│       ├── assets/      # Templates and configurations
│       ├── references/  # Reference documentation
│       └── scripts/     # Helper scripts
├── docs/                # User documentation
│   └── dlt-skill.md     # dlt-skill guide
├── README.md            # This file
└── CHANGELOG.md         # Version history
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
