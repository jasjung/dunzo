import importlib
from importlib.resources import as_file, files
from pathlib import Path
from types import SimpleNamespace

import pytest

from dunzo import __version__, available_sounds, done, dunzo
from dunzo.done import (
    BUILT_IN_SOUND_FILES,
    BUNDLED_SOUNDS,
    DEFAULT_SOUND,
    _play_file,
    _render_generated_sound,
)


def test_version():
    assert __version__ == "0.2.0"


def test_available_sounds():
    assert available_sounds() == ("success", "positive", "trumpet", "chime")


def test_default_sound_is_success():
    assert DEFAULT_SOUND == "success"


def test_done_uses_requested_sound(monkeypatch):
    done_module = importlib.import_module("dunzo.done")
    played = []
    monkeypatch.setattr(done_module, "play", played.append)

    message = done("positive")

    assert played == ["positive"]
    assert message.startswith("Finished @ (Date)")


def test_dunzo_alias_uses_done(monkeypatch):
    done_module = importlib.import_module("dunzo.done")
    calls = []
    monkeypatch.setattr(
        done_module,
        "done",
        lambda sound="success": calls.append(sound) or "ok",
    )

    assert dunzo("trumpet") == "ok"
    assert calls == ["trumpet"]


@pytest.mark.parametrize("sound", BUNDLED_SOUNDS)
def test_builtin_sounds_are_packaged_mp3s(sound):
    resource = files("dunzo").joinpath("sound_effects", BUILT_IN_SOUND_FILES[sound])
    with as_file(resource) as path:
        content = Path(path).read_bytes()

    assert content.startswith((b"ID3", b"\xff\xf3", b"\xff\xfb"))


def test_generated_chime_renders_valid_wav():
    path = _render_generated_sound("chime")
    try:
        assert Path(path).read_bytes().startswith(b"RIFF")
    finally:
        Path(path).unlink(missing_ok=True)


def test_builtin_playback_can_fall_back_to_terminal_bell(monkeypatch, capsys, tmp_path):
    done_module = importlib.import_module("dunzo.done")
    monkeypatch.setattr(done_module, "_player_command", lambda path: None)

    _play_file(tmp_path / "sound.wav", allow_bell_fallback=True)

    assert capsys.readouterr().out == "\a"


def test_notebook_playback_displays_ipython_audio(monkeypatch, tmp_path):
    done_module = importlib.import_module("dunzo.done")
    displayed = []

    class FakeAudio:
        def __init__(self, *, filename, autoplay):
            self.filename = filename
            self.autoplay = autoplay

    fake_display_module = SimpleNamespace(
        Audio=FakeAudio,
        display=displayed.append,
    )

    def import_display_module(name):
        if name == "IPython.display":
            return fake_display_module
        return importlib.import_module(name)

    monkeypatch.setattr(done_module, "_running_in_notebook", lambda: True)
    monkeypatch.setattr(done_module.importlib, "import_module", import_display_module)
    monkeypatch.setattr(done_module, "_player_command", lambda path: None)

    path = tmp_path / "sound.wav"
    _play_file(path)

    assert len(displayed) == 1
    assert displayed[0].filename == str(path)
    assert displayed[0].autoplay is True


def test_notebook_playback_falls_back_without_ipython(monkeypatch, capsys, tmp_path):
    done_module = importlib.import_module("dunzo.done")

    def raise_import_error(name):
        if name == "IPython.display":
            raise ImportError
        return importlib.import_module(name)

    monkeypatch.setattr(done_module, "_running_in_notebook", lambda: True)
    monkeypatch.setattr(done_module.importlib, "import_module", raise_import_error)
    monkeypatch.setattr(done_module, "_player_command", lambda path: None)

    _play_file(tmp_path / "sound.wav", allow_bell_fallback=True)

    assert capsys.readouterr().out == "\a"
