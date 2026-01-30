# dlt-skill

**Version 0.1.0**

Expert assistant skill for creating and maintaining dlt (data load tool) data pipelines.

## Overview

This Claude skill provides comprehensive guidance for building data pipelines using [dlt](https://dlthub.com), an open-source Python library for loading data from various sources into well-structured datasets.

## Features

- **Three pipeline approaches:**
  - Verified Sources (pre-built connectors for Salesforce, GitHub, Stripe, etc.)
  - Declarative REST API (config-based REST API pipelines)
  - Custom Python (full control with Python code)

- **Expert guidance on:**
  - Pipeline architecture and design
  - Configuration management (.dlt/config.toml, .dlt/secrets.toml)
  - Incremental loading strategies
  - Performance optimization
  - Debugging and troubleshooting

- **Bundled resources:**
  - Reference documentation on core concepts, sources, and destinations
  - Pipeline templates for all three approaches
  - Helper scripts for common tasks
  - Best practices from experienced data engineers

## Installation

```bash
npx skills add untitled-data-company/data-skills --skill dlt-skill
```

### Verify Installation

After installation, the skill should appear when you run `/skills` in Claude Code.

## Usage

Once installed, the skill will automatically activate when you:
- Ask to create data ingestion pipelines
- Work with dlt verified sources
- Build REST API pipelines
- Configure dlt destinations
- Optimize pipeline performance
- Debug or troubleshoot dlt pipelines

## Example Use Cases

1. **Pokemon API Pipeline**: Create a declarative REST API pipeline to ingest data from the Pokemon API
2. **Salesforce Integration**: Set up a verified source pipeline for Salesforce data
3. **Custom Data Source**: Build a custom Python pipeline using packages like simple-salesforce
4. **Performance Tuning**: Optimize large-scale data pipelines for better throughput

## Skill Contents

```
dlt-skill/
├── SKILL.md                 # Main skill instructions (for Claude)
├── references/              # Comprehensive documentation
│   ├── core-concepts.md     # dlt fundamentals
│   ├── verified-sources.md  # Pre-built connectors guide
│   ├── rest-api-source.md   # REST API configuration
│   ├── custom-sources.md    # Custom Python sources
│   ├── incremental-loading.md
│   ├── performance-tuning.md
│   └── troubleshooting.md
├── assets/templates/        # Pipeline templates
│   ├── verified_source_pipeline.py
│   ├── declarative_rest_pipeline.py
│   ├── custom_python_pipeline.py
│   └── .dlt/                # Configuration templates
└── scripts/                 # Helper scripts
    ├── install_packages.py  # Auto-detect and install dependencies
    └── open_dashboard.py    # Open dlt pipeline dashboard
```

## License

This skill is provided as-is for use with Claude and other skill-enabled LLMs. Maintained by [Untitled Data Company](https://untitleddata.company/). The dlt library itself is open-source and maintained by [dltHub](https://github.com/dlt-hub/dlt).
