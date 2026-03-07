# GraphRender

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![CI](https://github.com/Faerkeren/GraphRender/actions/workflows/ci.yml/badge.svg)](https://github.com/Faerkeren/GraphRender/actions/workflows/ci.yml)
[![Tests](https://github.com/Faerkeren/GraphRender/actions/workflows/test.yml/badge.svg)](https://github.com/Faerkeren/GraphRender/actions/workflows/test.yml)
[![Secret Scan](https://github.com/Faerkeren/GraphRender/actions/workflows/gitleaks.yml/badge.svg)](https://github.com/Faerkeren/GraphRender/actions/workflows/gitleaks.yml)

GraphRender converts laid-out ELK JSON into styled SVG diagrams.

It is intended for pipelines where layout is already computed and rendering must be deterministic, inspectable, and themeable.

## Features

- Render nodes, ports, edges, and labels from ELK layout output
- Support nested/compound graphs with coordinate normalization
- Style output with embedded CSS or custom CSS/SCSS/SASS themes
- Profile-bundle adapter for `renderCss` bundle payloads
- Optional Iconify icon rendering with persistent disk cache
- Pretty-formatted SVG output for readable diffs

## Requirements

- Python `>=3.10`
- `svg.py>=1.0`
- Optional: Dart Sass CLI (`sass`) for `.scss` / `.sass` themes

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Quick Start

```bash
# Render an ELK JSON file
python main.py examples/input.json -o output/output.svg

# Render with a custom theme
python main.py examples/input.json --theme themes/theme.scss -o output/custom-theme.svg

# Disable embedded theme
python main.py examples/input.json --no-theme -o output/no-theme.svg
```

## CLI Reference

```bash
python main.py <layout.json> [-o output.svg] [--theme theme.css|theme.scss|theme.sass] [--no-theme]
```

- `<layout.json>`: ELK output JSON with resolved coordinates
- `-o`, `--output`: output SVG path (default: `<input_stem>.svg`)
- `--theme`: CSS/SCSS/SASS theme file path
- `--no-theme`: disable embedded theme block in output SVG

## Python API

```python
from graphrender import GraphRender

renderer = GraphRender.from_file(
    "examples/input.json",
    embed_theme=True,
    theme_css=None,
)

renderer.write("output/output.svg")
svg_text = renderer.to_string()

# Profile-bundle-driven render configuration
profile_bundle = {
    "profileId": "runtime",
    "profileVersion": 1,
    "checksum": "abc",
    "renderCss": ".node.router > rect { fill: #334455; }",
}
renderer = GraphRender.from_profile_bundle(
    graph={"id": "root", "children": [], "edges": []},
    profile_bundle=profile_bundle,
)
```

Main constructor options:

- `padding`
- `node_style`
- `port_style`
- `edge_style`
- `font_size`
- `embed_theme`
- `theme_css`

## Profile Adapter + Class Alignment

`graphrender.profile` provides:

- `resolve_profile_render_bundle()`
- `render_kwargs_from_profile_bundle()`
- `css_class_token()`

`css_class_token()` normalizes `node.type`/`edge.type` values into CSS-safe class names, so selectors remain deterministic.

## Input Expectations

GraphRender assumes layout is already done.

Typical input includes:

- root dimensions (`width`, `height`) or resolvable node extents
- `children` with node geometry (`x`, `y`, `width`, `height`)
- `ports` and optional `labels`
- `edges` with routed `sections` (or source/target ports for fallback)

## Icon Support and Cache

If a node has an `icon` value (Iconify name like `mdi:router`), GraphRender fetches icon SVGs and reuses them via `<defs>/<use>`.

Caching behavior:

- In-memory cache for the current render process
- Persistent disk cache across runs
- Corrupted cache entries are auto-healed (deleted and fetched again)

Configure cache location with:

```bash
export GRAPHRENDER_ICON_CACHE_DIR=/path/to/cache
```

If unset, GraphRender uses platform cache locations (for example `~/.cache/graphrender/icons` on Linux/macOS).

Set `GRAPHRENDER_ICON_CACHE_DIR` to an empty string to disable persistent disk caching entirely.

## HTTP Server

GraphRender includes a lightweight HTTP server for service-oriented deployments:

```bash
python -m graphrender.server
```

The server exposes:

- `GET /health` — returns `{"status": "ok"}` (HTTP 200)
- `POST /render` — accepts ELK JSON body, returns SVG

Default port: **8080**. Override with `--port`:

```bash
python -m graphrender.server --port 9090
```

## Docker

Build and run the GraphRender service image:

```bash
docker build -t graph-render .
docker run -p 8080:8080 graph-render
```

The Dockerfile uses a multi-stage build. The final image contains only the installed Python package and its runtime dependencies.

Exposed port: **8080**

## Integration Testing

Integration tests verify GraphRender against a live service instance. They live in `tests/integration/` and are **not** executed by the default `pytest` command.

### Prerequisites

- Docker and Docker Compose installed
- Python 3.10+ with pytest

### Steps

1. **Build and start the service:**

   ```bash
   docker compose up -d --build
   ```

2. **Wait for the service to be healthy:**

   ```bash
   docker compose ps
   ```

   The `graph-render` service should show status `healthy`.

3. **Run integration tests:**

   ```bash
   INTEGRATION=1 pytest tests/integration/ -v
   ```

   Override the default service URL (`http://localhost:8080`) with `SERVICE_URL`:

   ```bash
   INTEGRATION=1 SERVICE_URL=http://localhost:8080 pytest tests/integration/ -v
   ```

4. **Tear down:**

   ```bash
   docker compose down
   ```

### Notes

- Integration tests require `INTEGRATION=1` to run. Without it, they are automatically skipped.
- Tests are self-contained and idempotent — they create their own test data and can be run repeatedly without side effects.
- The health-check polling fixture waits up to 30 seconds (configurable via `HEALTH_TIMEOUT`) for the service to become ready.
