# Render Deployment

OpenMemory MCP supports Render web services through Streamable HTTP.

## Blueprint Deploy

1. Push this repository to GitHub.
2. In Render, create a new Blueprint.
3. Select this repository.
4. Render will read `render.yaml`, create the web service, and attach PostgreSQL.

The public MCP endpoint will be:

```text
https://YOUR-SERVICE.onrender.com/mcp
```

## Manual Web Service

Use these settings if you create the service manually:

```text
Runtime: Python
Build command: python -m pip install --upgrade pip && pip install -e ".[postgres]"
Start command: python -m openmemory_mcp
```

Environment variables:

```text
OPENMEMORY_TRANSPORT=http
OPENMEMORY_HTTP_HOST=0.0.0.0
OPENMEMORY_HTTP_PATH=/mcp
OPENMEMORY_DATABASE_URL=postgresql+psycopg://...
OPENMEMORY_EMBEDDING_PROVIDER=hash
```

Render provides the `PORT` environment variable automatically. The server reads it when `OPENMEMORY_HTTP_PORT` is not set.

Free Render Postgres databases are useful for public demos, but Render documents a 1 GB capacity limit and a 30-day expiration window. Upgrade the database plan for durable public production use.

## MCP Client URL

Use Streamable HTTP transport with:

```text
https://YOUR-SERVICE.onrender.com/mcp
```
