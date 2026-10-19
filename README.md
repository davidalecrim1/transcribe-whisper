# transcribe-whisper

Local audio and video transcription using [MLX Whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper). Runs entirely offline on Apple Silicon, no API key needed.

## Requirements

- Apple Silicon Mac
- Python 3
- ffmpeg: `brew install ffmpeg`

## Setup

```bash
make setup
```

This creates a virtual environment and installs `mlx-whisper`. Models are downloaded from Hugging Face on first use and cached.

## Transcribe

```bash
make transcribe FILE=/path/to/audio.mp4
```

Or call the script directly:

```bash
python3 transcribe.py --file=/path/to/audio.m4a
```

The output is a Markdown file with the same name as the input, written next to it:

```md
# interview

- **Duration:** 01:09:20
- **Model:** mlx-community/whisper-large-v3-turbo (MLX) · language `en`
- **Source:** `interview.mp4`

## Transcript

- **[00:00:12]** Some text from the interview.
- **[00:00:18]** More text.
```

## Options

| Flag | Default | Options |
|------|---------|---------|
| `--file` | required | Path to the audio or video file |
| `--output-dir` | same dir as input | Any directory path |
| `--model` | `turbo` | `tiny`, `base`, `small`, `medium`, `large-v3`, `turbo`, or a Hugging Face repo |
| `--language` | auto-detect | Any language code, e.g. `en`, `pt` |

Make targets accept `MODEL` and `LANGUAGE` too:

```bash
make transcribe FILE=/path/to/audio.m4a MODEL=large-v3 LANGUAGE=pt
```

### Model comparison

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| `tiny` | 39M | fastest | lowest |
| `base` | 74M | very fast | low |
| `small` | 244M | fast | decent |
| `medium` | 769M | moderate | good |
| `large-v3` | 1.5G | slow | best |
| `turbo` | 809M | fast | near large-v3 |

Speed is measured on GPU via MLX, which is one to two orders of magnitude faster than CPU inference. `turbo` is the default: close to `large-v3` accuracy at several times its speed.

The `transcribe` target runs under `caffeinate -i`, so the Mac will not sleep during long files.

## Speaker diarization

WhisperX runs on the CPU through CTranslate2 and is much slower than MLX. It needs a Hugging Face token with access to the pyannote models:

```bash
make setup-diarize
make diarize FILE=/path/to/audio.mp3 HF_TOKEN=your_token
```

`setup-diarize` requires Python 3.12 because CTranslate2 does not support newer versions.

## Clean

```bash
make clean
```
