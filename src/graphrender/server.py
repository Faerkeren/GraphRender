"""Lightweight HTTP server exposing GraphRender as a service.

Endpoints
---------
- ``GET  /health`` – returns ``{"status": "ok"}`` (HTTP 200)
- ``POST /render`` – accepts an ELK JSON body, returns SVG
"""

from __future__ import annotations

import argparse
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

from graphrender import GraphRender

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080


class _Handler(BaseHTTPRequestHandler):
    """HTTP request handler for the GraphRender service."""

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._json_response(200, {"status": "ok"})
        else:
            self._json_response(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/render":
            self._handle_render()
        else:
            self._json_response(404, {"error": "not found"})

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _handle_render(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            graph = json.loads(body)
            renderer = GraphRender(graph)
            svg_text = renderer.to_string()
            self._raw_response(200, "image/svg+xml", svg_text.encode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            self._json_response(400, {"error": str(exc)})

    def _json_response(self, status: int, data: dict) -> None:
        payload = json.dumps(data).encode("utf-8")
        self._raw_response(status, "application/json", payload)

    def _raw_response(self, status: int, content_type: str, payload: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Start the GraphRender HTTP server."""
    server = HTTPServer((host, port), _Handler)
    print(f"GraphRender server listening on {host}:{port}")  # noqa: T201
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GraphRender HTTP server")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Bind address")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Listen port")
    args = parser.parse_args()
    run(host=args.host, port=args.port)
