# OpenMemory MCP

OpenMemory MCP is a local-first, self-hosted memory server for MCP-compatible AI coding assistants and agents. It stores project facts, requirements, decisions, issues, tasks, preferences, and architecture notes so tools like Gemini CLI, Claude Code, Cursor, Windsurf, and VS Code agents can share durable context.

## Use The Public MCP Server

Live public endpoint:

```text
https://openmemory-mcp-8gnp.onrender.com/mcp
```

Service status page:

```text
https://openmemory-mcp-8gnp.onrender.com
```

Health check:

```text
https://openmemory-mcp-8gnp.onrender.com/health
```

Use the `/mcp` URL in MCP clients. Opening `/mcp` in a browser may show `406 Not Acceptable`; that is normal because it expects MCP client requests.

### Public & Open Source
OpenMemory MCP is a public and open-source project. Anyone can connect to the public endpoint and use the memory tools.

### Client Configuration Examples

#### 1. Gemini CLI
Add the server:
```bash
gemini mcp add openmemory https://openmemory-mcp-8gnp.onrender.com/mcp --transport http
```

#### 2. Generic MCP Config (JSON)
For clients like Claude Desktop or IDE plugins:
```json
{
  "mcpServers": {
    "openmemory": {
      "transport": "http",
      "url": "https://openmemory-mcp-8gnp.onrender.com/mcp"
    }
  }
}
```

Example prompts after connecting:

```text
Remember in project "demo": The backend uses FastMCP and PostgreSQL.
Search memory in project "demo" for backend stack.
Add decision in project "demo": Use PostgreSQL because shared agents need durable memory.
Get project context for "demo".
```

Public-use note: Do not store secrets, private customer data, API keys, or confidential project details on the public server unless you operate a private secured deployment.

## Features

- FastMCP-based MCP server
- SQLite by default, PostgreSQL for production
- Multi-project memory isolation
- Hybrid keyword and semantic search
- Pluggable embedding providers: offline hash, OpenAI, Gemini, sentence-transformers
- Repository interfaces for memory, decisions, and projects
- Docker and Docker Compose support

## Install

```bash
pip install -e ".[dev]"
```

Or install through npm:

```bash
npm install -g openmemory-mcp
```

Run locally over stdio:

```bash
openmemory-mcp
```

You can also run it with `npx`:

```bash
npx -y openmemory-mcp
```

The default database is stored at `~/.openmemory-mcp/openmemory.db`.

## Configuration

Environment variables use the `OPENMEMORY_` prefix.

```bash
OPENMEMORY_DATABASE_URL=sqlite:///./openmemory.db
OPENMEMORY_EMBEDDING_PROVIDER=hash
OPENMEMORY_EMBEDDING_MODEL=text-embedding-3-small
```

PostgreSQL example:

```bash
OPENMEMORY_DATABASE_URL=postgresql+psycopg://openmemory:openmemory@localhost:5432/openmemory
```

## Management CLI

OpenMemory MCP includes a built-in CLI for manual memory management without needing an AI agent.

Run the CLI using `openmemory-mcp` or `python -m openmemory_mcp`.

### Commands

- **Serve (Default):** Start the MCP server.
  ```bash
  openmemory-mcp serve
  ```

- **Remember:** Store a project memory.
  ```bash
  openmemory-mcp remember --project "demo" --content "The backend uses FastAPI." --tags "tech,backend"
  ```

- **Search:** Search project memories.
  ```bash
  openmemory-mcp search --project "demo" --query "backend" --limit 5
  ```

- **Decisions:** Add or list project decisions.
  ```bash
  openmemory-mcp add-decision --project "demo" --decision "Use SQLite" --reason "Simplicity"
  openmemory-mcp decisions --project "demo"
  ```

- **Project Context:** Get a summary of the project.
  ```bash
  openmemory-mcp context --project "demo"
  ```

- **Timeline:** View project event history.
  ```bash
  openmemory-mcp timeline --project "demo" --limit 20
  ```

## MCP Tools

- `remember(project, content, type, tags)` stores a memory.
- `search_memory(project, query, limit)` retrieves matching memories.
- `add_decision(project, decision, reason)` stores a decision and rationale.
- `get_decisions(project)` returns decision history.
- `project_context(project)` returns stack, requirements, decisions, and standards.
- `timeline(project, start, end, limit)` returns chronological project events.

## Example Client Config

```json
{
  "mcpServers": {
    "openmemory": {
      "command": "openmemory-mcp",
      "env": {
        "OPENMEMORY_DATABASE_URL": "sqlite:///./openmemory.db"
      }
    }
  }
}
```

More examples are in [examples/mcp-configs.json](examples/mcp-configs.json).

## Docker

```bash
docker compose -f docker/docker-compose.yml up --build
```

## Render

This repo includes [render.yaml](render.yaml) for public Render deployment. It runs the MCP server over Streamable HTTP at `/mcp`.

```text
https://openmemory-mcp-8gnp.onrender.com/mcp
```

See [docs/github-to-render-deploy.md](docs/github-to-render-deploy.md) for the full step-by-step deployment and user setup guide.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
npm run check
```

## License

Apache-2.0
