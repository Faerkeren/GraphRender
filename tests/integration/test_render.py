"""Integration tests for the ``POST /render`` endpoint."""

from __future__ import annotations

import json
import urllib.error
import urllib.request


def test_render_minimal_graph(service_url: str) -> None:
    """POST /render with a minimal ELK graph returns valid SVG."""
    graph = {
        "id": "root",
        "width": 100,
        "height": 100,
        "children": [],
        "edges": [],
    }
    data = json.dumps(graph).encode("utf-8")
    req = urllib.request.Request(
        f"{service_url}/render",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        body = resp.read().decode("utf-8")
        assert "<svg" in body


def test_render_invalid_json_returns_400(service_url: str) -> None:
    """POST /render with invalid JSON returns HTTP 400."""
    req = urllib.request.Request(
        f"{service_url}/render",
        data=b"not-json",
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req)
        raise AssertionError("Expected HTTPError for bad payload")  # noqa: TRY301
    except urllib.error.HTTPError as exc:
        assert exc.code == 400
