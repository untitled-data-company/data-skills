# Workflow Examples

Full step-by-step walkthroughs. For minimal code patterns see the Pipeline Patterns section in [SKILL.md](SKILL.md). Add more workflow examples here (e.g. verified source setup, custom Python from DB).

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
