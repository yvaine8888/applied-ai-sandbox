# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A tiny Flask web application used as the practice playground for the
**Code2College Applied AI Cohort**. It's intentionally incomplete — each
task in `tasks/` walks the student through fixing or adding one piece.

## Stack

- Python 3.10+
- Flask 3.x
- pytest
- Jinja2 templates, vanilla HTML/CSS

## How to run things

```bash
# Run the app
python app.py
# → http://localhost:5000

# Run all tests
pytest

# Run tests for a single task
pytest tests/test_task_01.py

# Run a single test by name
pytest tests/test_task_01.py::test_empty_title_shows_error
```

`pyproject.toml` sets `pythonpath = ["."]` so plain `pytest` (without
`python -m`) can import `app.py` from the repo root. CI runs `pytest -v`
on every push to `main` and every PR
(`.github/workflows/test.yml`).

## Architecture

- `app.py` exposes a `create_app()` factory. `tests/conftest.py` calls
  it per test to produce a fresh `Flask` app and `test_client`, so test
  cases are isolated by construction — there's no shared state between
  tests to clear.
- Notes are stored on the app instance as `app.notes` (a list of
  `{"title", "body"}` dicts). The list resets on every `create_app()`
  call and on every `python app.py` restart — there is no database,
  and that's intentional. Tests assert against `app.notes` directly
  (e.g., `app.notes.clear()`, `len(app.notes)`) rather than only going
  through HTTP.
- Routes are defined inside `create_app()` so they close over the same
  `app.notes`. New routes (e.g., TASK 02's delete) belong inside the
  factory, not at module scope.

## Conventions

- Each task corresponds to a `tests/test_task_NN.py` file. The task is
  "done" when those tests pass.
- Don't edit `tests/` to make them pass — change `app.py` / `templates/`
  instead. The tests are the spec.
- Keep changes scoped to the task. Don't refactor unrelated files.
- When unsure, prefer reading the test file first — it tells you exactly
  what behavior is expected.

## Auth
- Use Flask-Login + werkzeug.security for password hashing.
- Never roll a custom auth flow; never store plaintext passwords.
- Password reset / email verification are out of scope for now.

## Working with Claude here

- Always read the task file before writing code.
- Plan before implementing — ask Claude for a plan first.
- Run `pytest` after each substantive change.
- If Claude proposes editing a test to "make it pass," push back. The
  tests are the spec.
