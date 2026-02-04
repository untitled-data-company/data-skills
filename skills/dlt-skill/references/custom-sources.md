# Creating Custom Sources in dlt

## Table of Contents
- [Overview](#overview)
- [Core Decorators](#core-decorators)
- [Yield Patterns](#yield-patterns)
- [Dynamic Resource Creation](#dynamic-resource-creation)
- [Using Python Packages](#using-python-packages)
- [Configuration and Secrets](#configuration-and-secrets)
- [REST API Helper](#rest-api-helper)
- [Schema Management](#schema-management)
- [Best Practices](#best-practices)
- [Complete Example: Multi-Endpoint API](#complete-example-multi-endpoint-api)
- [Error Handling](#error-handling)

## Overview

Custom sources allow you to extract data from any Python-accessible data source. Use custom sources when:
- No verified source exists for your data source
- You need custom logic or transformations
- Working with proprietary or internal APIs
- Using Python packages to access data

## Core Decorators

### @dlt.source
Defines a source function that returns one or more resources.

```python
@dlt.source
def my_source(api_key=dlt.secrets.value):
    return my_resource()
```

**Key principles:**
- Sources should yield or return resources
- Do NOT extract data in the source function
- Leave data extraction to resources
- Source functions execute before `pipeline.run()` or `pipeline.extract()`

### @dlt.resource
Defines a resource that extracts data.

```python
@dlt.resource(write_disposition='append')
def my_resource():
    for item in fetch_data():
        yield item
```

**Key parameters:**
- `write_disposition` - How to write data ('append', 'replace', 'merge')
- `primary_key` - Primary key field(s) for merge operations
- `name` - Resource name (defaults to function name)
- `max_table_nesting` - Control nested table depth

## Yield Patterns

### Pattern 1: Yield Individual Items
```python
@dlt.resource
def users():
    response = requests.get("https://api.example.com/users")
    for user in response.json():
        yield user
```

### Pattern 2: Yield Pages (Recommended for Performance)
```python
@dlt.resource
def users():
    response = requests.get("https://api.example.com/users")
    yield response.json()  # Yield entire page
```

### Pattern 3: Yield from Generator
```python
def fetch_data():
    # Generator function
    for page in range(10):
        yield fetch_page(page)

@dlt.resource
def my_resource():
    yield from fetch_data()
```

## Dynamic Resource Creation

Create resources programmatically for multiple endpoints:

```python
@dlt.source
def my_api(api_key=dlt.secrets.value):
    endpoints = ["companies", "deals", "products"]

    def create_resource(endpoint):
        url = f"https://api.example.com/{endpoint}"
        response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
        yield response.json()

    for endpoint in endpoints:
        yield dlt.resource(
            create_resource(endpoint),
            name=endpoint,
            write_disposition='merge',
            primary_key='id'
        )
```

## Using Python Packages

Integrate Python packages for data extraction:

```python
from simple_salesforce import Salesforce

@dlt.source
def salesforce_source(
    username=dlt.secrets.value,
    password=dlt.secrets.value,
    security_token=dlt.secrets.value
):
    sf = Salesforce(
        username=username,
        password=password,
        security_token=security_token
    )

    @dlt.resource(write_disposition='merge', primary_key='Id')
    def accounts():
        records = sf.query_all("SELECT Id, Name, Industry FROM Account")
        yield records['records']

    @dlt.resource(write_disposition='merge', primary_key='Id')
    def opportunities():
        records = sf.query_all("SELECT Id, Name, Amount, StageName FROM Opportunity")
        yield records['records']

    return accounts, opportunities
```

## Configuration and Secrets

### Accessing Secrets
```python
@dlt.source
def my_source(
    api_key=dlt.secrets.value,              # From .dlt/secrets.toml
    base_url=dlt.config.value,              # From .dlt/config.toml
    timeout: int = 30                        # Default value
):
    pass
```

### Secrets File (.dlt/secrets.toml)
```toml
[sources.my_source]
api_key = "your-secret-key"
```

### Config File (.dlt/config.toml)
```toml
[sources.my_source]
base_url = "https://api.example.com"
timeout = 60
```

## REST API Helper

Use built-in REST client for common patterns:

```python
from dlt.sources.helpers.rest_client import paginate
from dlt.sources.helpers.rest_client.auth import BearerTokenAuth
from dlt.sources.helpers.rest_client.paginators import HeaderLinkPaginator

@dlt.resource(write_disposition='merge', primary_key='id')
def github_issues(api_token=dlt.secrets.value):
    url = "https://api.github.com/repos/dlt-hub/dlt/issues"

    for page in paginate(
        url,
        auth=BearerTokenAuth(api_token),
        paginator=HeaderLinkPaginator(),
        params={"state": "open"}
    ):
        yield page
```

## Schema Management

### Control Table Nesting
```python
@dlt.source(max_table_nesting=2)
def my_source():
    return my_resource()
```

Limits how deeply nested tables are generated from nested data structures. For the declarative REST API source, set `max_table_nesting` per resource in the resource dict; see [rest-api-source.md](rest-api-source.md) Resource configuration.

### Resource Selection
Enable users to select specific resources:

```python
source = my_source()
pipeline.run(source.with_resources("users", "orders"))
```

## Best Practices

1. **Yield pages, not rows** - Better performance, fewer iterations
2. **Use generators** - Memory efficient for large datasets
3. **Keep sources lightweight** - Don't extract data in source functions
4. **Leverage decorators** - Use `@dlt.resource` for clear resource definition
5. **Handle pagination properly** - Use built-in helpers when possible
6. **Implement error handling** - Catch and handle API errors gracefully
7. **Use appropriate write dispositions** - Match disposition to data characteristics
8. **Set primary keys for merge** - Essential for upsert operations
9. **Limit table nesting** - Prevent excessive nested table generation
10. **Document resource parameters** - Make sources reusable and configurable

## Complete Example: Multi-Endpoint API

```python
import requests
from typing import Iterator, Any
import dlt

@dlt.source
def pokemon_api(base_url: str = "https://pokeapi.co/api/v2"):
    """
    Source for Pokemon API data.
    """

    @dlt.resource(write_disposition='replace', primary_key='name')
    def pokemon_list() -> Iterator[dict]:
        """Fetch list of all Pokemon."""
        url = f"{base_url}/pokemon"
        while url:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            yield data['results']
            url = data.get('next')

    @dlt.resource(write_disposition='merge', primary_key='id')
    def pokemon_details(pokemon_names: list[str]) -> Iterator[dict]:
        """Fetch detailed data for specific Pokemon."""
        for name in pokemon_names:
            url = f"{base_url}/pokemon/{name}"
            response = requests.get(url)
            response.raise_for_status()
            yield response.json()

    return pokemon_list, pokemon_details

# Usage
if __name__ == '__main__':
    pipeline = dlt.pipeline(
        pipeline_name='pokemon_pipeline',
        destination='duckdb',
        dataset_name='pokemon_data'
    )

    # Load all Pokemon and their details
    source = pokemon_api()
    load_info = pipeline.run(source)
    print(load_info)
```

## Error Handling

```python
@dlt.resource
def resilient_resource():
    for item_id in range(100):
        try:
            data = fetch_data(item_id)
            yield data
        except requests.exceptions.RequestException as e:
            # Log error and continue
            print(f"Failed to fetch {item_id}: {e}")
            continue
        except Exception as e:
            # Critical error - stop
            raise
```
