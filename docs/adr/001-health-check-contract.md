# ADR 001: Standardised Health Check Endpoint Contract

## Status

Accepted

## Context

The GraphRapids suite comprises multiple services that are orchestrated
locally by Graphras and deployed independently.  A uniform mechanism is
needed so that Docker Compose health checks, CI pipelines, and the
Graphras pre-push loop can reliably determine whether a service is ready
to accept traffic.

## Decision

Every service in the GraphRapids suite **MUST** expose:

| Property        | Value                          |
|-----------------|--------------------------------|
| Method          | `GET`                          |
| Path            | `/health`                      |
| Success status  | `200 OK`                       |
| Content-Type    | `application/json`             |
| Response body   | `{"status": "ok"}`             |

The endpoint **MUST NOT** require authentication and **MUST NOT** perform
expensive downstream checks (database, external APIs).  It is a
liveness/readiness indicator only.

## Consequences

- All Docker Compose `healthcheck` blocks can use the same test command.
- Graphras can poll a single, well-known path per service.
- If a deeper readiness probe is needed later, a separate `/ready`
  endpoint can be introduced without breaking the existing contract.
