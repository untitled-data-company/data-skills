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

- **Comprehensive resources:**
  - Reference documentation on core concepts, sources, and destinations
  - Pipeline templates for all three approaches
  - Helper scripts for common tasks
  - Best practices from experienced data engineers

## Installation

Install the skill in your Claude environment by loading the `dlt-skill.skill` package.

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

## Contents

- `dlt-skill/` - Skill source directory
  - `SKILL.md` - Main skill instructions
  - `references/` - Comprehensive documentation on dlt concepts
  - `assets/templates/` - Pipeline templates for quick start
  - `scripts/` - Helper scripts for common tasks
- `dlt-skill.skill` - Packaged skill file for installation

## Contributing

This skill was created using the Claude Agent SDK skill-creator tool. To modify or extend the skill, edit the files in the `dlt-skill/` directory and re-package using the packaging script.

## License

This skill is provided as-is for use with Claude and other skill enabled LLMs. This skill is maintained by [Untitled Data Company](https://untitleddata.company/). The dlt library itself is open-source and maintained by [dltHub](https://github.com/dlt-hub/dlt).
