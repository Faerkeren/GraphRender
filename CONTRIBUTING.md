# Contributing

Thanks for contributing to GraphRender.

## Development Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Running Checks

Run tests:

```bash
python -m pytest -q
```

Run compile sanity checks:

```bash
python -m py_compile main.py src/graphrender/__init__.py src/graphrender/graphrender.py src/graphrender/resources/__init__.py
```

Run a CLI smoke check:

```bash
python main.py examples/input.json -o /tmp/graphrender-check.svg
```

## Project Structure

- `src/graphrender/`: library code
- `main.py`: CLI entrypoint
- `tests/`: pytest suite
- `themes/`: SCSS theme source files
- `.github/workflows/`: CI, tests, release, and secret scanning

## Pull Requests

Before opening a PR:

1. Keep changes focused and atomic.
2. Add or update tests for behavioral changes.
3. Update docs (`README.md`, `CHANGELOG.md`, `THIRD_PARTY_NOTICES.md`) when relevant.
4. Ensure workflows are green (`CI`, `Tests`, `Gitleaks`).

## Commit Guidance

- Use clear, imperative commit messages.
- Prefer conventional prefixes (`feat`, `fix`, `docs`, `test`, `chore`).
- Reference issue numbers when applicable.
- Avoid bundling unrelated changes in one PR.

## Reporting Bugs and Requesting Features

Use GitHub issue templates:

- Bug report
- Feature request

For security issues, follow `SECURITY.md`.
