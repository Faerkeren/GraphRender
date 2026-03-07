"""Shared fixtures and configuration for integration tests.

Integration tests are skipped unless the ``INTEGRATION=1`` environment
variable is set.  This ensures the default ``pytest`` invocation only
runs unit tests.
"""

from __future__ import annotations

import os
import time
import urllib.error
import urllib.request

import pytest

SERVICE_URL: str = os.environ.get("SERVICE_URL", "http://localhost:8080")
_HEALTH_TIMEOUT: int = int(os.environ.get("HEALTH_TIMEOUT", "30"))


# ------------------------------------------------------------------
# Marker registration
# ------------------------------------------------------------------

def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test (requires running service)",
    )


# ------------------------------------------------------------------
# Auto-skip when INTEGRATION is not enabled
# ------------------------------------------------------------------

def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if os.environ.get("INTEGRATION") == "1":
        return
    skip_marker = pytest.mark.skip(
        reason="Integration tests require INTEGRATION=1 environment variable",
    )
    for item in items:
        fspath = str(item.fspath)
        if "tests/integration" in fspath or "tests\\integration" in fspath:
            item.add_marker(skip_marker)


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

def _poll_health(base_url: str, timeout: int) -> None:
    """Block until ``GET /health`` returns 200 or *timeout* seconds elapse."""
    deadline = time.monotonic() + timeout
    last_exc: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(f"{base_url}/health", timeout=3) as resp:
                if resp.status == 200:
                    return
        except (urllib.error.URLError, OSError) as exc:
            last_exc = exc
        time.sleep(1)
    msg = f"Service at {base_url} not healthy after {timeout}s"
    if last_exc:
        msg = f"{msg}: {last_exc}"
    raise TimeoutError(msg)


@pytest.fixture(scope="session", autouse=True)
def _wait_for_service() -> None:
    """Wait for the service to become healthy before running any tests."""
    if os.environ.get("INTEGRATION") != "1":
        return
    _poll_health(SERVICE_URL, timeout=_HEALTH_TIMEOUT)


@pytest.fixture()
def service_url() -> str:
    """Base URL of the running GraphRender service."""
    return SERVICE_URL
