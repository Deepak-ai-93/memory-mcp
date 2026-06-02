# GitHub to Render Deployment Guide

This guide shows how to deploy OpenMemory MCP from GitHub to Render and how users can connect to it after deployment.

OpenMemory MCP runs locally over stdio by default. On Render, it runs as a public Streamable HTTP MCP server at:

```text
https://YOUR-SERVICE.onrender.com/mcp
```

## Important Public-Use Note

The current server does not include authentication. If you deploy it as a public Render web service, anyone with the MCP URL can call the tools and read/write memory.

Use the public Render deployment for demos, shared community memory, or non-sensitive data. For private project memory, deploy your own instance or add authentication before sharing the URL.

## What You Need

- A GitHub account
- A Render account
- This repository pushed to GitHub
- Optional: a paid Render Postgres plan for durable production use

## Step 1: Push Code to GitHub

If the repo is already pushed, skip this step.

```bash
git init
git remote add origin https://github.com/YOUR-USER/memory-mcp.git
git add .
git commit -m "Initial OpenMemory MCP server"
git branch -M main
git push -u origin main
```

For this project, the GitHub repo is:

```text
https://github.com/Deepak-ai-93/memory-mcp
```

## Step 2: Confirm Render Files Exist

The repository should include:

```text
render.yaml
docs/render.md
src/openmemory_mcp/server.py
src/openmemory_mcp/config/settings.py
```

`render.yaml` tells Render to create:

- A Python web service
- A Render Postgres database
- Environment variables for HTTP MCP transport

## Step 3: Create Render Blueprint

1. Open the Render Dashboard.
2. Click `New`.
3. Select `Blueprint`.
4. Connect your GitHub account if Render asks.
5. Choose the `memory-mcp` repository.
6. Render will detect `render.yaml`.
7. Review the service and database settings.
8. Click `Apply` or `Deploy`.

Render will build the service with:

```bash
python -m pip install --upgrade pip && pip install -e ".[postgres]"
```

Render will start the MCP server with:

```bash
python -m openmemory_mcp
```

## Step 4: Wait for Deploy

Open the Render service logs and wait for the deploy to finish.

The server must bind to:

```text
0.0.0.0:$PORT
```

OpenMemory MCP does this automatically on Render.

## Step 5: Get the Public MCP URL

After deploy, Render gives the service a public hostname like:

```text
https://openmemory-mcp.onrender.com
```

The MCP endpoint is:

```text
https://openmemory-mcp.onrender.com/mcp
```

Replace `openmemory-mcp` with your actual Render service name.

From the Render Overview screen:

1. Click the `openmemory-mcp` web service row.
2. Open the service `Dashboard` or `Settings` page.
3. Look for the public service URL near the top of the page. It usually looks like:

```text
https://openmemory-mcp-xxxx.onrender.com
```

4. Add `/mcp` at the end.

Your public MCP URL is:

```text
https://openmemory-mcp-xxxx.onrender.com/mcp
```

Do not use the database row named `openmemory-mcp-db` as the MCP URL. The database is only for storage; users connect to the `openmemory-mcp` web service.

## Step 6: Connect an MCP Client

Use Streamable HTTP transport and the `/mcp` endpoint.

Generic remote MCP config:

```json
{
  "mcpServers": {
    "openmemory": {
      "transport": "http",
      "url": "https://YOUR-SERVICE.onrender.com/mcp"
    }
  }
}
```

Some MCP clients use `streamable-http` instead of `http`:

```json
{
  "mcpServers": {
    "openmemory": {
      "transport": "streamable-http",
      "url": "https://YOUR-SERVICE.onrender.com/mcp"
    }
  }
}
```

Client configuration formats vary. If your client does not support remote HTTP MCP servers yet, use the local `npx` setup instead:

```json
{
  "mcpServers": {
    "openmemory": {
      "command": "npx",
      "args": ["-y", "openmemory-mcp"]
    }
  }
}
```

## Step 7: Test the Memory Tools

Ask your MCP-compatible assistant to store a memory:

```text
Remember for project "demo-app": The backend uses FastMCP and PostgreSQL.
```

Then ask:

```text
Search memory in project "demo-app" for backend stack.
```

Expected behavior:

- The assistant calls `remember`.
- The server stores the memory in Render Postgres.
- The assistant later calls `search_memory`.
- The matching memory is returned.

## Tools Users Can Call

Users connected to the MCP server can use:

- `remember`: store project memory
- `search_memory`: search saved memory
- `add_decision`: store architecture or business decisions
- `get_decisions`: retrieve decision history
- `project_context`: get stack, requirements, decisions, and standards
- `timeline`: view chronological memory events

## Example User Workflows

Store a requirement:

```text
Remember in project "crm": Users must be able to export reports as CSV.
```

Store a decision:

```text
Add decision in project "crm": Use PostgreSQL because reporting queries need relational joins.
```

Retrieve project context:

```text
Get project context for "crm".
```

Search previous memory:

```text
Search memory in project "crm" for report export.
```

## Updating the Render Deployment

After you make code changes:

```bash
git add .
git commit -m "Update OpenMemory MCP"
git push
```

Render will redeploy automatically if auto-deploy is enabled.

## Troubleshooting

If Render deploy fails, check these first:

- `render.yaml` exists at the repo root.
- The service start command is `python -m openmemory_mcp`.
- `OPENMEMORY_TRANSPORT` is set to `http`.
- `OPENMEMORY_HTTP_HOST` is set to `0.0.0.0`.
- `OPENMEMORY_DATABASE_URL` is populated from the Render Postgres database.
- The logs show the server binding to the Render `PORT`.

If a client cannot connect:

- Confirm the URL ends with `/mcp`.
- Confirm the client supports remote Streamable HTTP MCP servers.
- Try redeploying the Render service.
- Check that the Render service is awake. Free web services may sleep when idle.

## Production Recommendations

For real public production use:

- Add authentication before sharing the endpoint broadly.
- Use a paid Render Postgres plan.
- Avoid storing secrets or private customer data.
- Add backups and monitoring.
- Consider rate limiting.
- Use separate deployments for separate organizations or communities.
