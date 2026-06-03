# Authentication in OpenMemory MCP

OpenMemory MCP supports API key authentication for its HTTP-based transports (HTTP, SSE, Streamable HTTP). This ensures that only authorized clients can access your memory server when it is exposed to the internet.

## How it Works

When an API key is configured, the server uses a `Bearer` token authentication scheme. Every request to the MCP endpoint must include an `Authorization` header with a valid key.

## Configuration

You can configure one or more API keys using the `OPENMEMORY_API_KEY` environment variable.

### Single API Key

Set the environment variable to your desired secret key:

```bash
OPENMEMORY_API_KEY=your-secret-key-here
```

### Multiple API Keys

You can provide multiple authorized keys by separating them with commas. This is useful for giving different keys to different users or services.

```bash
OPENMEMORY_API_KEY=key-for-alice,key-for-bob,service-account-key
```

## Client Setup

To connect to a secured OpenMemory MCP server, you must pass the API key in the headers.

### General MCP Config

```json
{
  "mcpServers": {
    "openmemory": {
      "transport": "http",
      "url": "https://your-server.com/mcp",
      "headers": {
        "Authorization": "Bearer your-secret-key-here"
      }
    }
  }
}
```

### Gemini CLI

```bash
gemini mcp add openmemory https://your-server.com/mcp --transport http -H "Authorization: Bearer your-secret-key-here"
```

### Claude Code

Add the server to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "openmemory": {
      "command": "npx",
      "args": ["-y", "openmemory-mcp"],
      "env": {
        "OPENMEMORY_TRANSPORT": "http",
        "OPENMEMORY_HTTP_URL": "https://your-server.com/mcp",
        "OPENMEMORY_API_KEY": "your-secret-key-here"
      }
    }
  }
}
```
*(Note: Client implementations vary; some might expect headers directly in the config).*

## Security Considerations

1.  **Transport Layer Security (TLS):** Always use HTTPS when deploying the server publicly. API keys sent over plain HTTP can be intercepted.
2.  **Key Rotation:** If a key is compromised, remove it from the `OPENMEMORY_API_KEY` list and restart the server.
3.  **Local Usage (stdio):** Authentication is currently not enforced for `stdio` transport, as it is assumed that the local environment is secure. If you need to secure local access, ensure only authorized users can run the server process.

## Troubleshooting

- **401 Unauthorized:** The API key is missing or incorrect. Check your `Authorization` header format: `Bearer <key>`.
- **406 Not Acceptable:** This is common when visiting the `/mcp` endpoint in a browser. It indicates that the server is working but expects an MCP client connection.
- **No Authentication:** If you haven't set `OPENMEMORY_API_KEY`, the server will be public. A warning is printed to the console during startup if an HTTP transport is used without an API key.
