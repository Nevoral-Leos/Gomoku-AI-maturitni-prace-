ENV_DIR = env
PYTHON = python3
SCRIPT = runserver.py

all: run

.PHONY: help clean install run

$(ENV_DIR)/bin/activate:
	$(PYTHON) -m venv $(ENV_DIR)

install: $(ENV_DIR)/bin/activate
	$(ENV_DIR)/bin/pip install --upgrade pip
	$(ENV_DIR)/bin/pip install -r requirements.txt

run: $(ENV_DIR)/bin/activate install
	$(ENV_DIR)/bin/python $(SCRIPT)

clean:
	rm -rf $(ENV_DIR)

help:
	@echo "Makefile for managing the project"
	@echo "Targets:"
	@echo "  install   - Create virtual environment and install dependencies"
	@echo "  run       - Run the script in the local environment"
	@echo "  clean     - Remove the virtual environment"
