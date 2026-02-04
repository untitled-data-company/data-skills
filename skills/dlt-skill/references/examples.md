# Workflow Examples

Full step-by-step walkthroughs. For minimal code patterns see the Pipeline Patterns section in [SKILL.md](../SKILL.md).

## Table of Contents
- [Creating a Pokemon API Pipeline](#creating-a-pokemon-api-pipeline)
- [Setting Up a GitHub Verified Source](#setting-up-a-github-verified-source)
- [Custom Python Pipeline with Database Source](#custom-python-pipeline-with-database-source)
- [Declarative REST API with Authentication](#declarative-rest-api-with-authentication)

## Creating a Pokemon API Pipeline

**User request**: "Create a pipeline ingesting data from https://pokeapi.co/api/v2/pokemon/ and https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

**Step-by-step:**

1. **Analyze**: REST API with standard patterns → Use declarative approach
2. **Destination**: Ask user (assume DuckDB for this example)
3. **Create pipeline** using declarative REST template
4. **Configure**:
   ```python
   config = {
       "client": {"base_url": "https://pokeapi.co/api/v2/"},
       "resources": [
           {
               "name": "pokemon_list",
               "endpoint": "pokemon",
               "write_disposition": "replace"
           },
           {
               "name": "pokemon_details",
               "endpoint": "pokemon/{name}",
               "write_disposition": "merge",
               "primary_key": "id",
               "include_from_parent": ["name"]
           }
       ]
   }
   ```
5. **No secrets needed** (public API)
6. **Create pipeline code** with config
7. **Test**: Run pipeline
8. **Inspect**: Open dashboard to verify data

---

## Setting Up a GitHub Verified Source

**User request**: "Load my GitHub repository issues and pull requests into BigQuery"

**Step-by-step:**

1. **Analyze**: GitHub is a verified source → Use verified source approach
2. **Destination**: BigQuery (requires credentials)
3. **Install the verified source**:
   ```bash
   dlt init github bigquery
   ```
4. **Configure secrets** in `.dlt/secrets.toml`:
   ```toml
   [sources.github]
   access_token = "ghp_your_github_token"

   [destination.bigquery]
   location = "US"

   [destination.bigquery.credentials]
   project_id = "your-project-id"
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"
   client_email = "service-account@project.iam.gserviceaccount.com"
   ```
5. **Configure** in `.dlt/config.toml`:
   ```toml
   [sources.github]
   owner = "your-org"
   name = "your-repo"
   ```
6. **Create pipeline code**:
   ```python
   import dlt
   from github import github_reactions

   pipeline = dlt.pipeline(
       pipeline_name="github_pipeline",
       destination="bigquery",
       dataset_name="github_data"
   )

   # Load issues and pull requests with reactions
   load_info = pipeline.run(github_reactions("your-org", "your-repo"))
   print(load_info)
   ```
7. **Test**: Run pipeline and check for errors
8. **Inspect**: Open dashboard to verify tables created

---

## Custom Python Pipeline with Database Source

**User request**: "Extract data from our PostgreSQL database and load it into Snowflake with incremental updates"

**Step-by-step:**

1. **Analyze**: Database extraction with custom logic → Use custom Python approach
2. **Destination**: Snowflake (requires credentials)
3. **Install dependencies**:
   ```bash
   pip install dlt[snowflake] psycopg2-binary
   ```
4. **Configure secrets** in `.dlt/secrets.toml`:
   ```toml
   [sources.postgres]
   connection_string = "postgresql://user:password@host:5432/database"

   [destination.snowflake]
   database = "YOUR_DATABASE"
   warehouse = "YOUR_WAREHOUSE"
   role = "YOUR_ROLE"

   [destination.snowflake.credentials]
   username = "your_username"
   password = "your_password"
   host = "your_account.snowflakecomputing.com"
   ```
5. **Create the pipeline**:
   ```python
   import dlt
   import psycopg2
   from dlt.sources.credentials import ConnectionStringCredentials

   @dlt.source
   def postgres_source(connection_string: str = dlt.secrets.value):

       @dlt.resource(write_disposition="merge", primary_key="id")
       def customers():
           """Load customers with incremental updates based on updated_at."""
           conn = psycopg2.connect(connection_string)
           cursor = conn.cursor()
           cursor.execute("""
               SELECT id, name, email, created_at, updated_at
               FROM customers
               WHERE updated_at > %s
           """, (dlt.current.resource_state().get("last_updated", "1970-01-01"),))

           for row in cursor:
               yield {
                   "id": row[0],
                   "name": row[1],
                   "email": row[2],
                   "created_at": row[3],
                   "updated_at": row[4]
               }

           # Update state for next run
           dlt.current.resource_state()["last_updated"] = str(row[4]) if row else None
           cursor.close()
           conn.close()

       @dlt.resource(write_disposition="replace")
       def products():
           """Full refresh of products table."""
           conn = psycopg2.connect(connection_string)
           cursor = conn.cursor()
           cursor.execute("SELECT id, name, price, category FROM products")

           for row in cursor:
               yield {
                   "id": row[0],
                   "name": row[1],
                   "price": row[2],
                   "category": row[3]
               }
           cursor.close()
           conn.close()

       return [customers, products]

   if __name__ == "__main__":
       pipeline = dlt.pipeline(
           pipeline_name="postgres_to_snowflake",
           destination="snowflake",
           dataset_name="postgres_replica"
       )

       load_info = pipeline.run(postgres_source())
       print(load_info)
   ```
6. **Test**: Run pipeline and verify incremental loading works
7. **Inspect**: Check Snowflake tables and dlt dashboard

---

## Declarative REST API with Authentication

**User request**: "Load data from a private API that requires OAuth2 authentication"

**Step-by-step:**

1. **Analyze**: REST API with OAuth2 → Use declarative approach with auth config
2. **Destination**: DuckDB (local testing)
3. **Configure secrets** in `.dlt/secrets.toml`:
   ```toml
   [sources.rest_api]
   api_key = "your_api_key"
   client_id = "your_client_id"
   client_secret = "your_client_secret"
   ```
4. **Create pipeline with OAuth2**:
   ```python
   import dlt
   from dlt.sources.rest_api import rest_api_source

   config = {
       "client": {
           "base_url": "https://api.example.com/v1/",
           "auth": {
               "type": "oauth2_client_credentials",
               "access_token_url": "https://api.example.com/oauth/token",
               "client_id": dlt.secrets["sources.rest_api.client_id"],
               "client_secret": dlt.secrets["sources.rest_api.client_secret"],
           }
       },
       "resources": [
           {
               "name": "users",
               "endpoint": "users",
               "write_disposition": "merge",
               "primary_key": "id",
               "incremental": {
                   "cursor_path": "updated_at",
                   "initial_value": "2024-01-01T00:00:00Z"
               }
           },
           {
               "name": "orders",
               "endpoint": "orders",
               "write_disposition": "append",
               "params": {
                   "status": "completed"
               }
           }
       ]
   }

   if __name__ == "__main__":
       pipeline = dlt.pipeline(
           pipeline_name="private_api",
           destination="duckdb",
           dataset_name="api_data"
       )

       source = rest_api_source(config)
       load_info = pipeline.run(source)
       print(load_info)
   ```
5. **Test**: Run and verify authentication works
6. **Inspect**: Open dashboard to check loaded data
