# Changelog

All notable changes to this project should be documented here.

## Unreleased

- Migrated project metadata from Poetry-specific configuration to standard `pyproject.toml`
  metadata for UV workflows.
- Removed runtime dependencies on Click, Playsound, and PyObjC.
- Added Pixabay-sourced built-in MP3 sounds: `success`, `positive`, and `trumpet`.
- Added `chime` as a generated built-in sound.
- Made `success` the default sound.
- Added `dunzo()` as a Python alias for `done()`.
- Added `dunzo` command while keeping the existing `done` command.
- Added automatic IPython audio display for Jupyter and Colab notebooks.
- Added private testing and release maintenance documentation.
