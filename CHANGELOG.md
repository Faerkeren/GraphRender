# Changelog

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Dockerfile with multi-stage build exposing port 8080 and a built-in HEALTHCHECK instruction.
- docker-compose.yml defining the `graph-render` service with health check configuration.
- `GET /health` endpoint returning HTTP 200 with `{"status": "ok"}` (application/json).
- Integration test scaffolding in `tests/integration/` (health check and render smoke tests).
- ADRs: `docs/adr/001-health-check-contract.md` and `docs/adr/002-docker-integration-testing.md`.
- README sections: Docker (build, run, health check), Integration Testing (step-by-step), and Testing.

### Fixed
- Restored README sections that were dropped in previous iterations: Automation (with workflow file paths), Contributing, Security, Governance, Third-Party Notices, and License.


All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Coverage-gated test workflow aligned with GraphLoom for predictable quality checks.
- Automated tag-based release workflow.
- Standardized repository governance templates (`CONTRIBUTING`, `SECURITY`, release process, issue/PR templates).
- README structure aligned with GraphLoom for consistent documentation flow.

## [0.1.0] - 2026-02-16

### Added

- Initial public GraphRender library and CLI.
- ELK-layout JSON to SVG rendering with theming and icon support.
- Persistent icon disk cache and pretty-formatted SVG output.
