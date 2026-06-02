# NPM Setup

OpenMemory MCP can be installed and launched through npm. The npm package is a Node wrapper around the Python FastMCP server.

```bash
npm install -g openmemory-mcp
openmemory-mcp
```

You can also use it without a global install:

```bash
npx -y openmemory-mcp
```

The npm `postinstall` script runs `python -m pip install .` inside the package so the Python server and dependencies are available. Set `OPENMEMORY_PYTHON` if you need a specific Python executable.

```bash
OPENMEMORY_PYTHON=python3.12 npx -y openmemory-mcp
```

To skip Python installation during npm install:

```bash
OPENMEMORY_SKIP_PYTHON_INSTALL=1 npm install -g openmemory-mcp
```
