# ---- Stage 1: Build wheels ------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

COPY pyproject.toml .
COPY src/ src/

RUN pip wheel --no-cache-dir --wheel-dir=/wheels .

# ---- Stage 2: Production runtime ------------------------------------------
FROM python:3.12-slim

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Install pre-built wheels (runtime deps only, no dev tooling)
COPY --from=builder /wheels /tmp/wheels
RUN pip install --no-cache-dir /tmp/wheels/*.whl \
    && rm -rf /tmp/wheels

# GraphRender HTTP server port
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

USER appuser
WORKDIR /app

CMD ["python", "-m", "graphrender.server"]
