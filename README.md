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
make transcribe FILE=audio.mp3
```

Output files (`.txt`, `.srt`, `.vtt`, `.tsv`, `.json`) are written to the current directory.

## Options

To change the model or language, edit the `transcribe` target in the Makefile:

| Flag | Default | Options |
|------|---------|---------|
| `--model` | `medium` | `tiny`, `base`, `small`, `medium`, `large` |
| `--language` | `Portuguese` | Any language name or code |
| `--output_format` | all | `txt`, `srt`, `vtt`, `tsv`, `json` |

Example with custom options:

```bash
venv/bin/whisper audio.mp3 --language Portuguese --model large --output_format srt --output_dir .
```
