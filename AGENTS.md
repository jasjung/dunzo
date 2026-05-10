# Agent Notes For Dunzo

This repo is for the `dunzo` Python package. Treat packaging compatibility and clean
PyPI releases as first-class concerns.

## Maintainer Preferences

- Prefer high-compatibility packaging over clever implementation choices.
- Keep runtime Python dependencies at zero unless a dependency clearly solves a
  cross-platform problem better than the standard library.
- Use standard `pyproject.toml` metadata and UV workflows.
- Keep bundled package data explicit in `pyproject.toml`.
- Before recommending or performing a PyPI release, verify the built wheel, not only
  the source tree.
- Do not put PyPI tokens, private paths, machine names, or secrets in tracked files.

## Compatibility Expectations

- The package should install cleanly from a wheel in a fresh virtual environment.
- The wheel should stay `py3-none-any` unless platform-specific code is intentionally
  introduced.
- Built-in sounds should work across common macOS, Linux, and Windows environments
  as much as practical. Be careful with MP3-only playback because some default players
  are WAV-oriented.
- If playback cannot work on a system, built-in sounds should fail gently or fall back
  where reasonable.

## Routine Checks

Run these before considering changes ready:

```sh
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv build
unzip -l dist/dunzo-*-py3-none-any.whl
```

For release confidence, also install the wheel in a clean temporary virtual environment
and smoke-test the import and console commands.

## Release Notes

- Follow `MAINTAINING.md` for release procedure.
- PyPI versions are permanent. If a bad file is uploaded, bump to a new version.
- Move `CHANGELOG.md` entries from `Unreleased` into a dated version section before
  publishing.
