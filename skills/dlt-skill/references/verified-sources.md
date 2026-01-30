# dlt Verified Sources

## Table of Contents
- [Overview](#overview)
- [Key Characteristics](#key-characteristics)
- [Difference from Core Sources](#difference-from-core-sources)
- [Available Verified Sources](#available-verified-sources)
- [Using Verified Sources](#using-verified-sources)
- [Customizing Verified Sources](#customizing-verified-sources)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Requesting New Verified Sources](#requesting-new-verified-sources)
- [Troubleshooting](#troubleshooting)

## Overview

Verified sources are pre-built, rigorously tested connectors for specific platforms and services. They're developed and maintained by the dlt team and community, providing production-ready pipelines with minimal setup.

## Key Characteristics

- **Pre-built**: Ready-to-use source code for specific platforms
- **Tested**: Rigorously tested against real APIs
- **Customizable**: Provided as Python code that can be modified
- **Maintained**: Regularly updated by dlt team and community

## Difference from Core Sources

- **Core sources** (REST API, SQL, cloud storage) are generic and built into dlt
- **Verified sources** are platform-specific and initialized separately
- Verified sources target individual platforms (Salesforce, GitHub, Stripe, etc.)

## Available Verified Sources

### CRM & Sales
- Salesforce
- HubSpot
- Pipedrive
- Zendesk Sell

### Analytics & Marketing
- Google Analytics
- Google Ads
- Facebook Ads
- Matomo

### Communication
- Slack
- Zendesk
- Intercom

### Development & Productivity
- GitHub
- GitLab
- Jira
- Asana

### Finance & Payments
- Stripe
- Shopify

### Databases
- MongoDB
- PostgreSQL
- MySQL

**Note**: See https://dlthub.com/docs/dlt-ecosystem/verified-sources for the complete list of 30+ verified sources.

## Using Verified Sources

### 1. Discover Available Sources
Browse the verified sources catalog at:
https://dlthub.com/docs/dlt-ecosystem/verified-sources

Or list available sources:
```bash
dlt init --list-sources
```

### 2. Initialize Source
```bash
dlt init <source_name> <destination_name>
```

**Examples:**
```bash
# Initialize Salesforce to BigQuery
dlt init salesforce bigquery

# Initialize GitHub to DuckDB
dlt init github duckdb

# Initialize Stripe to Snowflake
dlt init stripe snowflake
```

This command:
- Downloads verified source code to your working directory
- Creates pipeline Python file
- Generates `.dlt/` configuration directory
- Creates `requirements.txt` with dependencies

### 3. Configure Credentials

Add credentials to `.dlt/secrets.toml`:

```toml
[sources.salesforce]
username = "your-username"
password = "your-password"
security_token = "your-token"

[destination.bigquery]
credentials = "path/to/credentials.json"
project_id = "your-project"
```

### 4. Run Pipeline

```python
import dlt
from salesforce import salesforce_source

if __name__ == '__main__':
    pipeline = dlt.pipeline(
        pipeline_name='salesforce_pipeline',
        destination='bigquery',
        dataset_name='salesforce_data'
    )

    # Load all resources
    load_info = pipeline.run(salesforce_source())
    print(load_info)
```

### 5. Select Specific Resources

Most verified sources provide multiple resources. Select specific ones:

```python
# Load only specific Salesforce objects
source = salesforce_source()
pipeline.run(source.with_resources("Account", "Opportunity", "Contact"))
```

## Customizing Verified Sources

Verified sources are provided as Python code, allowing full customization:

### Modify Resources
```python
from salesforce import salesforce_source

# Get the source
source = salesforce_source()

# Modify or add resources
@dlt.resource(write_disposition='merge', primary_key='Id')
def custom_salesforce_query():
    # Your custom SOQL query
    pass

# Add custom resource to source
source.resources.update({"custom_query": custom_resource})
```

### Configure Resource Behavior
```python
# Change write disposition
source = salesforce_source()
source.resources["Account"].write_disposition = "replace"

# Set incremental loading
source.resources["Opportunity"].apply_hints(
    incremental=dlt.sources.incremental("LastModifiedDate")
)
```

## Best Practices

1. **Start with verified sources** - When available, prefer verified over custom
2. **Review generated code** - Understand what data is being extracted
3. **Configure incremental loading** - Use incremental loading for large datasets
4. **Select necessary resources** - Don't load all resources if you only need some
5. **Check documentation** - Each verified source has specific documentation
6. **Keep sources updated** - Regularly update to get bug fixes and improvements
7. **Test in development** - Validate data before production deployment
8. **Monitor API limits** - Be aware of source platform rate limits

## Common Patterns

### Incremental Loading with Verified Sources
```python
from salesforce import salesforce_source

source = salesforce_source()

# Configure incremental loading on specific resources
source.resources["Opportunity"].apply_hints(
    incremental=dlt.sources.incremental("LastModifiedDate"),
    write_disposition="merge",
    primary_key="Id"
)

pipeline.run(source)
```

### Filtering Data
```python
# Some verified sources support filtering parameters
source = salesforce_source(
    objects=["Account", "Contact"],  # Only load these objects
    start_date="2024-01-01"          # Only load data from this date
)
```

### Multiple Sources in One Pipeline
```python
from salesforce import salesforce_source
from hubspot import hubspot_source

pipeline = dlt.pipeline(
    pipeline_name='crm_pipeline',
    destination='bigquery',
    dataset_name='crm_data'
)

# Load from multiple sources
pipeline.run(salesforce_source())
pipeline.run(hubspot_source())
```

## Requesting New Verified Sources

If you need a source that doesn't exist:
1. Check the GitHub repository for open requests
2. Submit a feature request: https://github.com/dlt-hub/dlt
3. Join the Slack community to discuss
4. Consider contributing your own verified source

## Troubleshooting

### Source Not Found
```bash
# Ensure dlt is up to date
pip install --upgrade dlt

# Check available sources
dlt init --list-sources
```

### Credential Issues
- Verify `.dlt/secrets.toml` has correct credentials
- Check credential format in source-specific documentation
- Ensure secret names match source function parameters

### Missing Dependencies
```bash
# Install all requirements
pip install -r requirements.txt

# Or install source-specific dependencies
pip install dlt[salesforce]
```

### API Rate Limits
- Use incremental loading to reduce API calls
- Configure appropriate delays in source code
- Consider running pipelines during off-peak hours
