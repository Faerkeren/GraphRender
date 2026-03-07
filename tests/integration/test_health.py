"""Integration tests for the ``GET /health`` endpoint."""

from __future__ import annotations

import json
import urllib.request


def test_health_returns_200_with_ok_status(service_url: str) -> None:
    """GET /health must return HTTP 200 with ``{"status": "ok"}``."""
    req = urllib.request.Request(f"{service_url}/health", method="GET")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        assert resp.headers.get("Content-Type") == "application/json"
        body = json.loads(resp.read().decode("utf-8"))
        assert body == {"status": "ok"}


def test_unknown_route_returns_404(service_url: str) -> None:
    """GET on an unknown path must return HTTP 404."""
    req = urllib.request.Request(f"{service_url}/nonexistent", method="GET")
    try:
        urllib.request.urlopen(req)
        raise AssertionError("Expected HTTPError for unknown route")  # noqa: TRY301
    except urllib.error.HTTPError as exc:
        assert exc.code == 404
