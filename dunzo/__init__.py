from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .done import available_sounds, done, dunzo, play

try:
    __version__ = version("dunzo")
except PackageNotFoundError:
    __version__ = "0.2.0"

__all__ = ["__version__", "available_sounds", "done", "dunzo", "play"]
