# GraphRender - Session Notes

Use this file as a running log between work sessions.

## Entry Template

### YYYY-MM-DD
- Summary:
- Changes:
- Files touched:
- Tests run:
- Known issues:
- Next steps:

## Current

### 2026-02-26
- Summary: Removed external theme package dependency and made theme resolution self-contained.
- Changes:
  - Updated `default_theme_css()` to serve bundled default CSS only.
  - Removed CLI compatibility args tied to older theme-id workflows.
  - Removed optional theme package dependency from `pyproject.toml`.
  - Updated tests for theme-css-only invocation paths.
- Files touched:
  - `src/graphrender/resources/__init__.py`
  - `main.py`
  - `tests/test_resources.py`
  - `tests/test_cli_main.py`
  - `pyproject.toml`
  - `README.md`
  - `PROJECT_CONTEXT.md`
  - `SESSION_NOTES.md`
- Tests run:
  - Pending.
- Known issues: none.
- Next steps:
  - Validate dependent services (GraphAPI) continue passing profile-driven CSS correctly.

### 2026-02-26
- Summary: Added GraphAPI profile bundle adapter support and deterministic CSS class token normalization.
- Changes:
  - Added `src/graphrender/profile.py` with profile bundle validation and render kwargs helpers.
  - Added `GraphRender.from_profile_bundle(...)` constructor helper.
  - Normalized node/edge type classes via `css_class_token()` for predictable CSS selectors.
  - Added adapter + class alignment tests.
  - Updated docs/context notes.
- Files touched:
  - `src/graphrender/profile.py`
  - `src/graphrender/graphrender.py`
  - `src/graphrender/__init__.py`
  - `tests/test_profile_adapter.py`
  - `README.md`
  - `PROJECT_CONTEXT.md`
  - `SESSION_NOTES.md`
- Tests run:
  - `./.venv/bin/python -m pytest -q` (62 passed)
- Known issues: none.
- Next steps:
  - Add more snapshot coverage for profile-driven CSS behavior on complex graphs.

### 2026-02-25
- Summary: Added persistent project/session context documentation.
- Changes:
  - Introduced `PROJECT_CONTEXT.md`.
  - Introduced `SESSION_NOTES.md`.
- Files touched:
  - `PROJECT_CONTEXT.md`
  - `SESSION_NOTES.md`
- Tests run: not run (docs-only update).
- Known issues: none.
- Next steps:
  - Keep this log updated when renderer behavior or theming changes.
