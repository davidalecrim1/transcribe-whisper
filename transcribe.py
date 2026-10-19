#!/usr/bin/env python3
"""Transcribe audio or video files locally using MLX Whisper on Apple Silicon."""

import argparse
import os
import sys
import time

import mlx_whisper

MODELS = {
    "tiny": "mlx-community/whisper-tiny-mlx",
    "base": "mlx-community/whisper-base-mlx",
    "small": "mlx-community/whisper-small-mlx",
    "medium": "mlx-community/whisper-medium-mlx",
    "large-v3": "mlx-community/whisper-large-v3-mlx",
    "turbo": "mlx-community/whisper-large-v3-turbo",
}
DEFAULT_MODEL = "turbo"


def hhmmss(seconds):
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio using MLX Whisper")
    parser.add_argument("--file", required=True, help="Path to the audio or video file")
    parser.add_argument(
        "--output-dir",
        help="Output directory (defaults to the input file's directory)",
    )
    parser.add_argument(
        "--language",
        help="Language code, e.g. en, pt (default: auto-detect)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model: {', '.join(MODELS)} or a Hugging Face repo (default: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    media_path = os.path.expanduser(args.file)
    if not os.path.isfile(media_path):
        print(f"Error: file not found: {media_path}", file=sys.stderr)
        sys.exit(1)

    model = MODELS.get(args.model, args.model)
    output_dir = os.path.expanduser(args.output_dir) if args.output_dir else os.path.dirname(os.path.abspath(media_path))
    os.makedirs(output_dir, exist_ok=True)

    stem = os.path.splitext(os.path.basename(media_path))[0]
    output_path = os.path.join(output_dir, f"{stem}.md")

    print(f"Transcribing {media_path} with {model}", file=sys.stderr)
    started = time.time()
    result = mlx_whisper.transcribe(
        media_path,
        path_or_hf_repo=model,
        language=args.language,
        condition_on_previous_text=False,
        hallucination_silence_threshold=2.0,
        verbose=False,
    )

    segments = [s for s in result["segments"] if s["text"].strip()]
    duration = segments[-1]["end"] if segments else 0

    with open(output_path + ".part", "w", encoding="utf-8") as f:
        f.write(f"# {stem}\n\n")
        f.write(f"- **Duration:** {hhmmss(duration)}\n")
        f.write(f"- **Model:** {model} (MLX) · language `{result.get('language', 'unknown')}`\n")
        f.write(f"- **Source:** `{os.path.basename(media_path)}`\n")
        f.write("\n## Transcript\n\n")
        for seg in segments:
            f.write(f"- **[{hhmmss(seg['start'])}]** {seg['text'].strip()}\n")
    os.replace(output_path + ".part", output_path)

    elapsed = time.time() - started
    print(f"Wrote {output_path} ({len(segments)} segments, {elapsed:.0f}s elapsed)", file=sys.stderr)


if __name__ == "__main__":
    main()
