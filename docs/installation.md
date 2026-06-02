# Installation Guide

```bash
git clone https://github.com/your-org/openmemory-mcp.git
cd openmemory-mcp
pip install -e ".[dev]"
openmemory-mcp
```

Use SQLite for local mode:

```bash
OPENMEMORY_DATABASE_URL=sqlite:///./openmemory.db openmemory-mcp
```

Install with npm:

```bash
npm install -g openmemory-mcp
npx openmemory-mcp
```

Use PostgreSQL for shared or production memory:

```bash
OPENMEMORY_DATABASE_URL=postgresql+psycopg://openmemory:openmemory@localhost:5432/openmemory openmemory-mcp
```
