### Quick context

This repository converts old YouTube annotation XML files into subtitle formats (ASS/SSA/SRT). The package entry point is the console script `Annotations2Sub` (defined in `pyproject.toml` -> `project.scripts`). Primary code lives under `src/Annotations2Sub/` and tests under `src/tests/`.

### Big picture

- Purpose: read YouTube annotation XML and emit subtitle files (ASS/SRT). See `README.md` for user-facing usage: `Annotations2Sub <file.xml>`.
- Core modules:
  - `src/Annotations2Sub/convert.py` — main conversion logic and transformations.
  - `src/Annotations2Sub/Annotations.py` — XML parsing and annotation data structures.
  - `src/Annotations2Sub/subtitles/` — subtitle formats, styles, events and drawing helpers.
  - `src/Annotations2Sub/_main.py` / `src/Annotations2Sub/__main__.py` — CLI wiring and entry point.

### Why things are organized this way

- Separation of concerns: parsing (`Annotations.py`) vs transformation (`convert.py`) vs output formatting (`subtitles/*`). Tests exercise conversion against baseline `.test` files in `src/tests/testCase/Baseline/`.

### How to run, test and lint (developer workflows)

- Install locally for quick manual runs:

  python -m pip install -e .

- Run the CLI on a sample file:

  Annotations2Sub src/tests/testCase/Baseline/annotations.xml.test

- Run unit tests (pytest is used in CI):

  python -m pip install -e .[dev]
  pytest

- CI notes: GitHub Actions workflows live in `.github/workflows/` and use `pytest --cov` and mypy/black checks. Keep test fixtures in `src/tests/testCase/` and binary locale files under `src/Annotations2Sub/locales/`.

### Project-specific patterns and conventions

- Tests use `.test` files under `src/tests/testCase/` as input fixtures and also contain expected output files with suffixes like `.ass.test` and `.transform.ass.test` — prefer adding new fixtures there when adding conversion tests.
- The package exposes typed stubs via `py.typed` (see `src/Annotations2Sub/py.typed`) — prefer adding type hints and keeping mypy happy (CI runs mypy).
- Localization: gettext `.po`/`.mo` files are in `src/Annotations2Sub/locales/`. When changing user-facing strings update `.po` files and regenerate `.mo`.
- Avoid changing public CLI signature in `_main.py` without updating `pyproject.toml` `project.scripts` mapping.

### Common code locations to inspect when making changes

- CLI & entry: `src/Annotations2Sub/_main.py`, `src/Annotations2Sub/__main__.py`
- Parsing: `src/Annotations2Sub/Annotations.py`
- Conversion workflows: `src/Annotations2Sub/convert.py`
- Subtitle format implementation: `src/Annotations2Sub/subtitles/*.py`
- Utilities: `src/Annotations2Sub/utils.py`, `cli_utils.py`
- Tests & fixtures: `src/tests/`, especially `src/tests/testCase/Baseline/`

### Examples for common edits

- To add a new subtitle format, implement formatter under `subtitles/` and add a test fixture in `src/tests/testCase/` comparing expected `.ass.test` or `.srt.test`.
- To change parsing of a new annotation type, update `Annotations.py` and add a unit test in `src/tests/unittest/`.

### Integration points & external deps

- No external network calls; core behavior is file-based conversion.
- Build/packaging uses setuptools (see `pyproject.toml`). Release CI workflow exists at `.github/workflows/release.yml`.
- CI uploads coverage to Codecov; tests in CI install pytest and run coverage in `test.yml`.

### Safety for automated edits

- Small, self-contained changes are safe: updating docstrings, small refactors in `utils.py`, adding tests/fixtures.
- Avoid broad imports reorganization or changing public CLI without updating `pyproject.toml` and tests.

### Where to ask questions

- Open issues on GitHub at https://github.com/USED255/Annotations2Sub/issues. For design/context questions reference specific test fixtures in `src/tests/testCase/Baseline/`.

Please review and tell me if you want additional examples or to preserve/merge content from an existing copilot instructions file.
