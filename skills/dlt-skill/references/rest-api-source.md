# Declarative REST API Source

## Table of Contents
- [Overview](#overview)
- [Configuration Structure](#configuration-structure)
- [Client Configuration](#client-configuration)
- [Authentication Methods](#authentication-methods)
- [Resource Configuration](#resource-configuration)
- [Endpoint Configuration](#endpoint-configuration)
- [Pagination Patterns](#pagination-patterns)
- [Resource Relationships (Parent-Child)](#resource-relationships-parent-child)
- [Incremental Loading](#incremental-loading)
- [Processing Steps](#processing-steps)
- [Resource Defaults](#resource-defaults)
- [Complete Examples](#complete-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The declarative REST API source enables data extraction from REST APIs using a configuration dictionary. This approach is easier to use than custom Python code but can handle complex API patterns including authentication, pagination, and nested resources.

**When to use:**
- REST APIs with standard patterns
- APIs with clear endpoint structures
- When you want configuration-based approach
- Rapid prototyping and development

**When to use custom Python instead:**
- Very complex custom logic required
- Non-standard API patterns
- Need fine-grained control over every request

## Configuration Structure

```python
from dlt.sources.rest_api import rest_api_source

config: RESTAPIConfig = {
    "client": {
        # Client configuration (base URL, auth, etc.)
    },
    "resource_defaults": {
        # Default settings for all resources
    },
    "resources": [
        # List of API endpoints/resources
    ]
}

source = rest_api_source(config)
```

## Client Configuration

### Basic Client
```python
"client": {
    "base_url": "https://api.example.com/v1/",
}
```

### With Authentication
```python
"client": {
    "base_url": "https://api.github.com/repos/dlt-hub/dlt/",
    "auth": {
        "token": dlt.secrets["github_token"]  # Bearer token
    }
}
```

### With Headers
```python
"client": {
    "base_url": "https://api.example.com/",
    "headers": {
        "User-Agent": "MyApp/1.0",
        "Accept": "application/json"
    }
}
```

### With Paginator Default
```python
"client": {
    "base_url": "https://api.example.com/",
    "paginator": {
        "type": "page_number",
        "page_param": "page",
        "page_size": 100
    }
}
```

## Authentication Methods

### Bearer Token
```python
"auth": {
    "type": "bearer",
    "token": dlt.secrets["api_token"]
}
```

### Basic Authentication
```python
"auth": {
    "type": "http_basic",
    "username": dlt.secrets["username"],
    "password": dlt.secrets["password"]
}
```

### API Key in Header
```python
"auth": {
    "type": "api_key",
    "name": "X-API-Key",
    "api_key": dlt.secrets["api_key"],
    "location": "header"
}
```

### API Key in Query Parameter
```python
"auth": {
    "type": "api_key",
    "name": "api_key",
    "api_key": dlt.secrets["api_key"],
    "location": "query"
}
```

### OAuth2 Client Credentials
```python
"auth": {
    "type": "oauth2_client_credentials",
    "client_id": dlt.secrets["client_id"],
    "client_secret": dlt.secrets["client_secret"],
    "access_token_url": "https://auth.example.com/oauth/token"
}
```

## Resource Configuration

### Simple Resource (String)
```python
"resources": [
    "users",      # GET /users
    "products",   # GET /products
]
```

### Detailed Resource (Dictionary)
```python
"resources": [
    {
        "name": "users",
        "endpoint": {
            "path": "users",
            "params": {
                "status": "active"
            }
        },
        "write_disposition": "merge",
        "primary_key": "id"
    }
]
```

## Endpoint Configuration

### Basic Endpoint
```python
"endpoint": {
    "path": "issues"
}
```

### With Query Parameters
```python
"endpoint": {
    "path": "issues",
    "params": {
        "sort": "updated",
        "state": "open",
        "per_page": 100
    }
}
```

### With Data Selector (JSONPath)
```python
"endpoint": {
    "path": "results",
    "data_selector": "data.items"  # Extract data.items from response
}
```

### POST Request with JSON Body
```python
"endpoint": {
    "path": "search",
    "method": "POST",
    "json": {
        "query": "dlt",
        "filters": ["python", "data"]
    }
}
```

## Pagination Patterns

### Auto-Detection
dlt automatically detects common pagination patterns. No configuration needed in most cases.

### JSON Link Pagination
```python
"paginator": {
    "type": "json_link",
    "next_url_path": "pagination.next"  # JSONPath to next page URL
}
```

### Header Link Pagination (GitHub-style)
```python
"paginator": {
    "type": "header_link",
    "links_path": "link"  # Header name containing next link
}
```

### Offset Pagination
```python
"paginator": {
    "type": "offset",
    "limit": 100,
    "offset_param": "offset",
    "limit_param": "limit",
    "total_path": "total"  # Optional: JSONPath to total count
}
```

### Page Number Pagination
```python
"paginator": {
    "type": "page_number",
    "page_param": "page",
    "page_size": 100,
    "total_path": "meta.total_pages"
}
```

### Cursor Pagination
```python
"paginator": {
    "type": "cursor",
    "cursor_path": "next_cursor",
    "cursor_param": "cursor"
}
```

### Single Page (No Pagination)
```python
"paginator": "single_page"
```

## Resource Relationships (Parent-Child)

Define child resources that depend on parent resources:

```python
"resources": [
    {
        "name": "issues",
        "endpoint": "issues",
        "primary_key": "number"
    },
    {
        "name": "issue_comments",
        "endpoint": {
            "path": "issues/{number}/comments",  # Use parent field
            "params": {
                "issue_id": "{number}"  # Also works in params
            }
        },
        "include_from_parent": ["id", "number"]  # Fields to include from parent
    }
]
```

**Placeholder locations:**
- URL paths: `"path": "issues/{issue_id}/comments"`
- Query params: `"params": {"parent_id": "{issue_id}"}`
- JSON body: `"json": {"issue": "{issue_id}"}`
- Headers: `"headers": {"X-Issue-ID": "{issue_id}"}`

## Incremental Loading

Load only new or changed data:

```python
{
    "name": "posts",
    "endpoint": {
        "path": "posts",
        "params": {
            "created_since": "{incremental.start_value}"
        }
    },
    "incremental": {
        "cursor_path": "created_at",
        "initial_value": "2024-01-01T00:00:00Z"
    },
    "write_disposition": "merge",
    "primary_key": "id"
}
```

**Incremental parameters:**
- `cursor_path` - Field to track (e.g., timestamp, ID)
- `initial_value` - Starting point for first run
- `end_value` - Optional end value
- Placeholders: `{incremental.start_value}`, `{incremental.end_value}`, `{incremental.last_value}`

## Processing Steps

Transform data before loading:

```python
{
    "name": "users",
    "endpoint": "users",
    "processing_steps": [
        # Filter: Keep only matching items
        {"filter": lambda item: item["age"] >= 18},

        # Map: Transform each item
        {"map": lambda item: {**item, "full_name": f"{item['first_name']} {item['last_name']}"}},

        # Yield map: Transform and yield multiple items
        {"yield_map": lambda item: [item, item.get("metadata")]}
    ]
}
```

## Resource Defaults

Set defaults for all resources:

```python
"resource_defaults": {
    "write_disposition": "merge",
    "primary_key": "id",
    "endpoint": {
        "params": {
            "api_version": "v2"
        }
    }
}
```

Individual resources can override these defaults.

## Complete Examples

### Example 1: Pokemon API
```python
from dlt.sources.rest_api import rest_api_source

config = {
    "client": {
        "base_url": "https://pokeapi.co/api/v2/",
    },
    "resources": [
        {
            "name": "pokemon_list",
            "endpoint": {
                "path": "pokemon",
                "params": {
                    "limit": 100
                }
            },
            "write_disposition": "replace"
        },
        {
            "name": "pokemon_details",
            "endpoint": {
                "path": "pokemon/{name}",
            },
            "write_disposition": "merge",
            "primary_key": "id",
            "include_from_parent": ["name"]
        }
    ]
}

source = rest_api_source(config)

pipeline = dlt.pipeline(
    pipeline_name="pokemon",
    destination="duckdb",
    dataset_name="pokemon_data"
)
pipeline.run(source)
```

### Example 2: GitHub Issues with Auth and Incremental
```python
config = {
    "client": {
        "base_url": "https://api.github.com/repos/dlt-hub/dlt/",
        "auth": {
            "token": dlt.secrets["github_token"]
        }
    },
    "resource_defaults": {
        "primary_key": "id",
        "write_disposition": "merge"
    },
    "resources": [
        {
            "name": "issues",
            "endpoint": {
                "path": "issues",
                "params": {
                    "state": "all",
                    "since": "{incremental.start_value}"
                }
            },
            "incremental": {
                "cursor_path": "updated_at",
                "initial_value": "2024-01-01T00:00:00Z"
            }
        },
        {
            "name": "issue_comments",
            "endpoint": "issues/{number}/comments",
            "include_from_parent": ["id", "number"]
        }
    ]
}
```

## Best Practices

1. **Use resource defaults** - Avoid repetition for common settings
2. **Set appropriate write dispositions** - Use merge for stateful data, append for events
3. **Define primary keys** - Essential for merge operations
4. **Use incremental loading** - Reduce API calls and data transfer
5. **Handle pagination explicitly** - When auto-detection doesn't work
6. **Test with small limits** - Use small page sizes during development
7. **Use data selectors** - Extract specific parts of complex responses
8. **Leverage parent-child relationships** - Model API dependencies correctly
9. **Store secrets properly** - Never hardcode credentials
10. **Monitor rate limits** - Be aware of API rate limiting

## Troubleshooting

### Pagination Not Working
- Check API response structure
- Explicitly configure paginator type
- Verify JSONPath selectors

### Authentication Failures
- Verify credentials in `.dlt/secrets.toml`
- Check auth type matches API requirements
- Test credentials with curl/Postman first

### Missing Data
- Use `data_selector` to extract correct fields
- Check for nested response structures
- Verify endpoint paths are correct

### Child Resources Not Loading
- Ensure parent resource has required fields
- Check placeholder syntax: `{field_name}`
- Verify `include_from_parent` includes needed fields
