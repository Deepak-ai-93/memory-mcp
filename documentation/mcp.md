# OpenMemory MCP - Codex Build Specification

You are a senior Python, MCP, and AI infrastructure engineer.

Build a production-ready open-source MCP server called OpenMemory MCP.

Goal:
Create a universal memory layer for AI coding assistants and AI agents.

The MCP server should work with:

* Gemini CLI
* Claude Code
* Cursor
* Windsurf
* VS Code AI agents
* Any MCP-compatible client

Architecture Principles:

1. Open Source (Apache 2.0)
2. Local-first
3. Self-hosted
4. Multi-project memory
5. Extensible plugin architecture
6. FastMCP-based implementation
7. PostgreSQL support
8. SQLite support for local mode
9. Docker support
10. Production-ready structure

Repository Structure:

openmemory-mcp/
├── src/
│   ├── server.py
│   ├── config/
│   ├── tools/
│   ├── services/
│   ├── memory/
│   ├── storage/
│   ├── models/
│   └── utils/
│
├── tests/
├── docs/
├── docker/
├── examples/
├── README.md
├── LICENSE
└── pyproject.toml

Core MCP Tools:

1. remember

Purpose:
Store a memory.

Input:

* project
* content
* type
* tags

Output:

* memory_id
* status

2. search_memory

Purpose:
Semantic memory retrieval.

Input:

* project
* query
* limit

Output:

* matching memories

3. add_decision

Purpose:
Store architecture or business decisions.

Input:

* project
* decision
* reason

Output:

* decision_id

4. get_decisions

Purpose:
Retrieve project decisions.

Input:

* project

Output:

* decision history

5. project_context

Purpose:
Return project summary.

Output:

* stack
* requirements
* decisions
* standards

6. timeline

Purpose:
Return chronological project memory.

Input:

* project
* date_range

Output:

* ordered events

Memory Types:

* fact
* decision
* requirement
* task
* issue
* meeting
* architecture
* preference

Database Requirements:

Support:

1. SQLite
2. PostgreSQL

Abstract storage layer.

Future databases should be pluggable.

Embedding Layer:

Create interface:

EmbeddingProvider

Implement:

* OpenAI embeddings
* Gemini embeddings
* Local sentence-transformers

Storage Interfaces:

MemoryRepository
DecisionRepository
ProjectRepository

Use dependency injection.

Search Features:

* keyword search
* semantic search
* hybrid search

Security:

* input validation
* project isolation
* safe tool execution
* no shell execution
* no arbitrary code execution

Testing:

Minimum:

* unit tests
* integration tests
* MCP tool tests

Documentation:

Generate:

* installation guide
* Gemini CLI setup guide
* Claude Code setup guide
* Cursor setup guide
* Docker guide

Examples:

Include example workflows:

* software project memory
* startup memory
* architecture decisions
* coding standards memory

Deliverables:

1. Fully working FastMCP server
2. Dockerfile
3. Docker Compose
4. GitHub Actions CI
5. Complete README
6. Example MCP configurations
7. Apache 2.0 license

Success Criteria:

A developer can install OpenMemory MCP, connect Gemini CLI, save project knowledge, retrieve memory later, and share memory across AI tools.
