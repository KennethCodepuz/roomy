# Infrastructure (local development)

## Postgres (Docker Compose)

Database runs in Docker on **host port `5433`** so it does not clash with a system Postgres on **`5432`**.

### Prerequisites

- Docker Engine + Docker Compose v2 (`docker compose version`)

### Start

From the repository root:

```bash
docker compose -f infra/compose.yaml up -d
docker compose -f infra/compose.yaml ps
```

### Stop

```bash
docker compose -f infra/compose.yaml down
```

To remove containers **and** the named volume (wipes local DB data):

```bash
docker compose -f infra/compose.yaml down -v
```

### Verify connectivity

Host `psql` (if installed); defaults match `compose.yaml` (`roomy` / `roomy_dev` on port `5433`). You will be prompted for the password (avoids putting it in shell history):

```bash
psql -h 127.0.0.1 -p 5433 -U roomy -d roomy_dev -c "select 1 as ok;"
```

Or via the container (no password needed for this check):

```bash
docker compose -f infra/compose.yaml exec db psql -U roomy -d roomy_dev -c "select 1 as ok;"
```

### Notes

- Prefer a **gitignored** `.env` for `POSTGRES_PASSWORD` (and later app DB URLs) instead of committing real passwords in `compose.yaml`.
- Staging/production Compose files can be added later (for example `compose.dev.yml` overrides) without changing this local flow.
