# Maintaining Dunzo

This file is for project maintenance notes that are safe to keep in the public repo.
Do not put PyPI tokens, machine names, private paths, or account details here.

## Routine Development

```sh
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

When behavior changes, update tests and add an entry to `CHANGELOG.md` under `Unreleased`.
For day-to-day notes, add a dated file in `logs/`.

## Audio Assets

Dunzo bundles short notification sounds from Pixabay under the Pixabay Content License.
Pixabay attribution is not required, but keep these source and license notes with the repo.
Do not redistribute the sounds as standalone stock audio assets.

- `dunzo/sound_effects/positive.mp3`
  Source: https://pixabay.com/sound-effects/film-special-effects-success-1-6297/
  License: Pixabay Content License
- `dunzo/sound_effects/success.mp3`
  Source: https://pixabay.com/sound-effects/film-special-effects-powerup-success-523645/
  License: Pixabay Content License
- `dunzo/sound_effects/trumpet.mp3`
  Source: https://pixabay.com/sound-effects/film-special-effects-success-fanfare-trumpets-6185/
  License: Pixabay Content License

The `chime` built-in sound is generated at runtime from simple waveforms and has no bundled
source audio asset.

## Private Local Testing

Build the package:

```sh
uv build
```

Install the wheel in a clean environment on the same machine:

```sh
python3 -m venv /tmp/dunzo-test
source /tmp/dunzo-test/bin/activate
python -m pip install --upgrade pip
python -m pip install dist/dunzo-0.2.0-py3-none-any.whl
dunzo --list-sounds
dunzo
done trumpet
python -c "from dunzo import done; print(done())"
deactivate
```

## Private Mac Testing

Build on Linux:

```sh
uv build
```

Copy the wheel to the Mac using any private transfer method, such as `scp`, AirDrop,
or a private file sync folder. Do not upload to TestPyPI if the goal is private testing;
TestPyPI is public.

On the Mac:

```sh
python3 -m venv /tmp/dunzo-mac-test
source /tmp/dunzo-mac-test/bin/activate
python -m pip install --upgrade pip
python -m pip install /path/to/dunzo-0.2.0-py3-none-any.whl
dunzo --list-sounds
dunzo
dunzo positive
done trumpet
python -c "from dunzo import done; print(done('success'))"
deactivate
```

The default macOS player should be `afplay`. If no supported audio player is available,
built-in sounds fall back to the terminal bell.

## Pre-Release Checklist

1. Confirm `pyproject.toml` has the intended version.
2. Update `CHANGELOG.md`.
3. Run:

```sh
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv build
```

4. Inspect the built wheel contents:

```sh
unzip -l dist/dunzo-0.2.0-py3-none-any.whl
```

5. Privately test the wheel on Linux and macOS.
6. Confirm no secrets, private paths, or unlicensed assets are included.
7. Commit the release changes.
8. Tag the release after publishing succeeds.

## Publishing

See `PYPI.md` for the full PyPI publishing procedure. PyPI versions are permanent:
if anything is wrong after publishing, bump to a new version.

## Dependency Maintenance

Dunzo intentionally has no runtime Python dependencies. Keep it that way unless a
dependency solves a real cross-platform problem better than the standard library.

For development tools:

```sh
uv sync --upgrade
uv run ruff check .
uv run pytest
```

Review `uv.lock` changes before committing.
