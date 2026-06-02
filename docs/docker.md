# Docker Guide

Build and run with PostgreSQL:

```bash
docker compose -f docker/docker-compose.yml up --build
```

For SQLite inside a container, mount a local data directory and set:

```bash
OPENMEMORY_DATABASE_URL=sqlite:////data/openmemory.db
```
