from __future__ import annotations

import builtins
import importlib
import math
import os
import shutil
import subprocess
import sys
import tempfile
import wave
from array import array
from collections.abc import Iterable, Sequence
from datetime import datetime
from importlib.resources import as_file, files
from pathlib import Path

DEFAULT_SOUND = "success"
GENERATED_SOUNDS = ("chime",)
BUNDLED_SOUNDS = ("success", "positive", "trumpet")
BUILT_IN_SOUNDS = (*BUNDLED_SOUNDS, *GENERATED_SOUNDS)
BUILT_IN_SOUND_FILES = {
    "success": "success.mp3",
    "positive": "positive.mp3",
    "trumpet": "trumpet.mp3",
}
SAMPLE_RATE = 44_100
MAX_AMPLITUDE = 32_767

LIST_OF_SOUNDS = list(BUILT_IN_SOUNDS)


class DunzoPlaybackError(RuntimeError):
    """Raised when dunzo cannot find a local audio player."""


def done(sound: str = DEFAULT_SOUND) -> str:
    """Play a completion sound and return a timestamp message."""
    play(sound)
    now = datetime.now().astimezone().strftime("(Date) %Y-%m-%d (Time) %I:%M:%S %p %Z")
    return f"Finished @ {now}"


def dunzo(sound: str = DEFAULT_SOUND) -> str:
    """Alias for done()."""
    return done(sound)


def play(sound: str = DEFAULT_SOUND) -> None:
    """Play one of dunzo's bundled sounds or a local audio file."""
    if sound in BUNDLED_SOUNDS:
        resource = files("dunzo").joinpath("sound_effects", BUILT_IN_SOUND_FILES[sound])
        with as_file(resource) as sound_path:
            _play_file(sound_path, allow_bell_fallback=True)
        return

    if sound in GENERATED_SOUNDS:
        wav_path = _render_generated_sound(sound)
        try:
            _play_file(wav_path, allow_bell_fallback=True)
        finally:
            wav_path.unlink(missing_ok=True)
        return

    path = Path(sound).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"No built-in sound or audio file named {sound!r}.")
    _play_file(path)


def available_sounds() -> tuple[str, ...]:
    """Return the names of the built-in bundled sounds."""
    return BUILT_IN_SOUNDS


def _render_generated_sound(sound: str) -> Path:
    fd, temp_name = tempfile.mkstemp(prefix=f"dunzo-{sound}-", suffix=".wav")
    os.close(fd)
    path = Path(temp_name)

    if sound != "chime":
        raise ValueError(f"Unknown generated sound: {sound}")

    _write_wav(
        path,
        _melody(
            [(659.25, 0.08), (0, 0.025), (783.99, 0.11), (987.77, 0.18)],
            volume=0.30,
        ),
    )
    return path


def _melody(notes: Sequence[tuple[float, float]], *, volume: float) -> array:
    samples = array("h")
    for frequency, duration in notes:
        samples.extend(_tone(frequency, duration, volume=volume))
    return samples


def _tone(frequency: float, duration: float, *, volume: float) -> Iterable[int]:
    sample_count = int(SAMPLE_RATE * duration)
    attack = max(1, int(sample_count * 0.06))
    release = max(1, int(sample_count * 0.25))

    for index in range(sample_count):
        if frequency <= 0:
            yield 0
            continue

        phase = 2 * math.pi * frequency * (index / SAMPLE_RATE)
        envelope = _envelope(index, sample_count, attack, release)
        yield int(MAX_AMPLITUDE * volume * math.sin(phase) * envelope)


def _envelope(index: int, sample_count: int, attack: int, release: int) -> float:
    if index < attack:
        return index / attack
    if index > sample_count - release:
        return max(0.0, (sample_count - index) / release)
    return 1.0


def _write_wav(path: Path, samples: array) -> None:
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(samples.tobytes())


def _play_file(path: Path, *, allow_bell_fallback: bool = False) -> None:
    if _display_notebook_audio(path):
        return

    command = _player_command(path)
    if command is None:
        if allow_bell_fallback:
            sys.stdout.write("\a")
            sys.stdout.flush()
            return
        raise DunzoPlaybackError(
            "Could not find a supported audio player. Install afplay, paplay, pw-play, "
            "aplay, ffplay, or use Windows PowerShell playback."
        )

    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _display_notebook_audio(path: Path) -> bool:
    if not _running_in_notebook():
        return False

    try:
        display_module = importlib.import_module("IPython.display")
    except ImportError:
        return False

    display_module.display(display_module.Audio(filename=str(path), autoplay=True))
    return True


def _running_in_notebook() -> bool:
    get_ipython = getattr(builtins, "get_ipython", None)
    if get_ipython is None:
        return False

    try:
        shell = get_ipython()
    except Exception:
        return False

    config = getattr(shell, "config", {})
    return "IPKernelApp" in config


def _player_command(path: Path) -> list[str] | None:
    path_text = str(path)
    if sys.platform == "darwin" and shutil.which("afplay"):
        return ["afplay", path_text]
    if sys.platform.startswith("linux"):
        for command in ("paplay", "pw-play", "aplay"):
            if shutil.which(command):
                return [command, path_text]
        if shutil.which("ffplay"):
            return ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path_text]
    if os.name == "nt" and shutil.which("powershell"):
        return [
            "powershell",
            "-NoProfile",
            "-Command",
            f"(New-Object Media.SoundPlayer {path_text!r}).PlaySync();",
        ]
    return None
