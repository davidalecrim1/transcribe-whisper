#!/usr/bin/env python3
"""Transcribe audio files using local Whisper model."""

import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using Whisper")
    parser.add_argument("--file", required=True, help="Path to the audio file")
    parser.add_argument(
        "--output-dir",
        help="Output directory (defaults to a folder named after the audio file, next to it)",
    )
    parser.add_argument("--language", default="Portuguese", help="Language (default: Portuguese)")
    parser.add_argument("--model", default="medium", help="Whisper model (default: medium)")
    args = parser.parse_args()

    audio_path = os.path.expanduser(args.file)
    if not os.path.isfile(audio_path):
        print(f"Error: file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    audio_stem = os.path.splitext(os.path.basename(audio_path))[0]
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(audio_path)), audio_stem)

    os.makedirs(output_dir, exist_ok=True)

    whisper_bin = os.path.join(os.path.dirname(__file__), "venv", "bin", "whisper")
    if not os.path.isfile(whisper_bin):
        print(f"Error: whisper not found at {whisper_bin}. Run 'make setup' first.", file=sys.stderr)
        sys.exit(1)

    cmd = [
        whisper_bin,
        audio_path,
        "--language", args.language,
        "--model", args.model,
        "--output_dir", output_dir,
    ]

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
