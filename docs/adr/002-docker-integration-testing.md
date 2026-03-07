# ADR 002: Dockerised Integration Testing Pattern

## Status

Accepted

## Context

Graphras currently runs only unit tests before creating a pull request.
Changes that break inter-service contracts are caught only after the PR
is already open in CI.  We need a pattern for running integration tests
against a live instance of each service **before** pushing to GitHub.

## Decision

Each service repository in the GraphRapids suite adopts the following
conventions:

1. **Dockerfile** at the repo root — multi-stage build with a slim
   production runtime stage and no dev dependencies.
2. **docker-compose.yml** at the repo root — defines the service
   (kebab-case name matching the repo, e.g. `graph-render`) with a
   `healthcheck` block.
3. **`tests/integration/`** directory containing pytest-based integration
   tests that target a live service.
4. Integration tests are **opt-in**: they require `INTEGRATION=1` and are
   skipped by the default `pytest` invocation.
5. The service URL is configurable via `SERVICE_URL` (default
   `http://localhost:<port>`).
6. `HEALTHCHECK` in the Dockerfile and `healthcheck` in Compose both
   target `GET /health` per ADR 001.

Graphras orchestrates the flow as:

```
docker compose up -d --build
→ wait for healthy
→ INTEGRATION=1 pytest tests/integration/
→ docker compose down
```

## Consequences

- Every repo gains a uniform integration-test workflow.
- The pattern is reusable by developers running tests manually.
- CI pipelines are **not** affected; integration tests are local/Graphras
  only for now.
- Port collisions across services are mitigated by per-service default
  ports and `${SERVICE_PORT:-…}` overrides in Compose.
