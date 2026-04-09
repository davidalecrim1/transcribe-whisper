VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
WHISPER := $(VENV)/bin/whisper

.PHONY: setup transcribe clean

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install openai-whisper

transcribe:
ifndef FILE
	$(error FILE is required. Usage: make transcribe FILE=audio.mp3)
endif
	$(WHISPER) "$(FILE)" --language Portuguese --model medium --output_dir .

clean:
	rm -rf $(VENV)
