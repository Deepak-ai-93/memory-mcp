# Gemini CLI Setup

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
