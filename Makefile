VENV := venv
VENV_DIA := venv-diarize
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
PIP_DIA := $(VENV_DIA)/bin/pip
WHISPERX := $(VENV_DIA)/bin/whisperx
TRANSCRIBE := $(PYTHON) transcribe.py
MODEL ?= turbo
# Empty means auto-detect
LANGUAGE ?=
LANG_FLAG := $(if $(LANGUAGE),--language=$(LANGUAGE))

.PHONY: setup setup-diarize transcribe diarize clean

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install mlx-whisper

# whisperX requires Python <3.14 due to ctranslate2 compatibility
setup-diarize:
	python3.12 -m venv $(VENV_DIA)
	$(PIP_DIA) install --upgrade pip
	$(PIP_DIA) install whisperx

transcribe:
ifndef FILE
	$(error FILE is required. Usage: make transcribe FILE=audio.mp3 [MODEL=turbo] [LANGUAGE=en])
endif
	caffeinate -i $(TRANSCRIBE) --file="$(FILE)" --model=$(MODEL) $(LANG_FLAG)

diarize:
ifndef FILE
	$(error FILE is required. Usage: make diarize FILE=audio.mp3 HF_TOKEN=your_token)
endif
ifndef HF_TOKEN
	$(error HF_TOKEN is required. Get it at https://huggingface.co/settings/tokens after accepting pyannote terms)
endif
	caffeinate -i $(WHISPERX) "$(FILE)" --model medium --diarize --hf_token "$(HF_TOKEN)" --output_dir .

clean:
	rm -rf $(VENV) $(VENV_DIA)
