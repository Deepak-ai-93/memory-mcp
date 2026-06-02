# OpenMemory MCP

OpenMemory MCP is a local-first, self-hosted memory server for MCP-compatible AI coding assistants and agents. It stores project facts, requirements, decisions, issues, tasks, preferences, and architecture notes so tools like Gemini CLI, Claude Code, Cursor, Windsurf, and VS Code agents can share durable context.

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
https://YOUR-SERVICE.onrender.com/mcp
```

See [docs/render.md](docs/render.md).

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
npm run check
```

## License

Apache-2.0
