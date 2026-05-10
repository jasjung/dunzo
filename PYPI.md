# Publishing To PyPI

PyPI versions are permanent. If a file is uploaded for a version, that exact version
cannot be replaced with different contents. If anything is wrong after publishing,
bump to a new version.

Do not put PyPI tokens, private paths, machine names, or account details in tracked
files.

## Choose The Version

Use semantic versioning:

- Patch, such as `0.2.1`, for bug fixes.
- Minor, such as `0.3.0`, for new features.
- Major, such as `1.0.0`, for stable/public API commitments or breaking changes.

Update the version in `pyproject.toml`:

```toml
[project]
version = "0.2.1"
```

## Pre-Release Checks

Run the standard checks:

```sh
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Build fresh distributions:

```sh
uv build
```

Inspect the wheel contents:

```sh
unzip -l dist/dunzo-0.2.1-py3-none-any.whl
```

Confirm the wheel contains only expected package files and metadata. There should be
no secrets, private files, or unlicensed assets.

## Private Wheel Testing

Install the wheel in a clean local environment:

```sh
python3 -m venv /tmp/dunzo-release-test
source /tmp/dunzo-release-test/bin/activate
python -m pip install --upgrade pip
python -m pip install dist/dunzo-0.2.1-py3-none-any.whl
dunzo --list-sounds
dunzo
done positive
python -c "from dunzo import done; print(done('chime'))"
deactivate
```

Also copy the wheel to macOS and run the same style of test before publishing:

```sh
python3 -m venv /tmp/dunzo-mac-test
source /tmp/dunzo-mac-test/bin/activate
python -m pip install --upgrade pip
python -m pip install /path/to/dunzo-0.2.1-py3-none-any.whl
dunzo --list-sounds
dunzo
dunzo positive
done trumpet
python -c "from dunzo import done; print(done('success'))"
deactivate
```

The default macOS player should be `afplay`. If no supported audio player is available,
built-in sounds should fail gently or fall back where reasonable.

## Publish

Store the token outside the repo. For a one-time shell session:

```sh
export UV_PUBLISH_TOKEN="YOUR_PYPI_TOKEN"
uv publish
unset UV_PUBLISH_TOKEN
```

Alternatively, pass the token directly:

```sh
uv publish --token "YOUR_PYPI_TOKEN"
```

## Verify The Public Install

After publishing, test the package from real PyPI:

```sh
python3 -m venv /tmp/dunzo-pypi-test
source /tmp/dunzo-pypi-test/bin/activate
python -m pip install --upgrade pip
python -m pip install dunzo==0.2.1
dunzo --list-sounds
dunzo
deactivate
```

## Commit And Tag

Commit and tag the release if everything looks good:

```sh
git status --short
git add pyproject.toml CHANGELOG.md uv.lock
git commit -m "Release 0.2.1"
git tag v0.2.1
```

Push only when ready:

```sh
git push
git push --tags
```
