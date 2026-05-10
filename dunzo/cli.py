from __future__ import annotations

import argparse
import subprocess

from .done import DEFAULT_SOUND, DunzoPlaybackError, available_sounds, done


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dunzo",
        description="Play a small completion sound.",
    )
    parser.add_argument(
        "sound",
        nargs="?",
        default=DEFAULT_SOUND,
        help="Built-in sound name or path to a local audio file.",
    )
    parser.add_argument(
        "--list-sounds",
        action="store_true",
        help="Show built-in sound names and exit.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_sounds:
        parser.exit(message="\n".join(available_sounds()) + "\n")

    try:
        timestamp = done(args.sound)
    except (DunzoPlaybackError, FileNotFoundError, subprocess.CalledProcessError) as exc:
        parser.exit(status=1, message=f"dunzo: {exc}\n")

    parser.exit(message=f"{timestamp}! Played {args.sound} sound\n")


if __name__ == "__main__":
    main()
