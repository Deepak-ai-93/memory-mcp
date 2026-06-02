# Gemini CLI Setup

## Remote Render Server

The live Render MCP endpoint is:

```text
https://openmemory-mcp-8gnp.onrender.com/mcp
```

If the server has `OPENMEMORY_API_KEY` configured, Gemini CLI must send it as a bearer token.

Add with the Gemini CLI command:

```bash
gemini mcp add openmemory https://openmemory-mcp-8gnp.onrender.com/mcp --transport http -H "Authorization: Bearer YOUR_OPENMEMORY_API_KEY"
```

Or edit `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "openmemory": {
      "httpUrl": "https://openmemory-mcp-8gnp.onrender.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_OPENMEMORY_API_KEY"
      }
    }
  }
}
```

After editing settings, run this in Gemini CLI:

```text
/mcp reload
```

Then ask Gemini:

```text
Remember in project "demo": The backend uses FastMCP and PostgreSQL.
Search memory in project "demo" for backend stack.
```

## Local Server

Add OpenMemory MCP to your Gemini CLI MCP server configuration:

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
