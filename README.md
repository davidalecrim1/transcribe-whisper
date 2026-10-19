# transcribe-whisper

Local audio transcription using [OpenAI Whisper](https://github.com/openai/whisper). Runs entirely offline, no API key needed.

## Requirements

- Python 3
- ffmpeg: `brew install ffmpeg`

## Setup

```bash
make setup
```

This creates a virtual environment and installs Whisper (~1.5GB for the medium model, downloaded on first run).

## Transcribe

```bash
python3 transcribe.py --file=/path/to/audio.m4a
```

Output files (`.txt`, `.srt`, `.vtt`, `.tsv`, `.json`) are written to the same directory as the input file by default.

## Options

| Flag | Default | Options |
|------|---------|---------|
| `--file` | required | Path to the audio file |
| `--output-dir` | same dir as input | Any directory path |
| `--model` | `medium` | `tiny`, `base`, `small`, `medium`, `large`, `large-v2`, `large-v3` |
| `--language` | `Portuguese` | Any language name or code |

### Model comparison

| Model | Size | VRAM | Speed | Accuracy |
|-------|------|------|-------|----------|
| `tiny` | 39M | ~1GB | ~32x | lowest |
| `base` | 74M | ~1GB | ~16x | low |
| `small` | 244M | ~2GB | ~6x | decent |
| `medium` | 769M | ~5GB | ~2x | good |
| `large` | 1.5GB | ~10GB | 1x | better |
| `large-v2` | 1.5GB | ~10GB | 1x | better |
| `large-v3` | 1.5GB | ~10GB | 1x | best |

Speed is relative to `large`. For Portuguese, `large-v3` gives the best results.

Example with custom options:

```bash
python3 transcribe.py --file=/path/to/audio.m4a --model=large-v3 --output-dir=/tmp/transcripts
```
