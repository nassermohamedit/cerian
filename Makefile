PYTHON_VERSION := $(shell $(PYTHON) -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON := python
VENV := venv

check_python_version:
	@if [ "$(PYTHON_VERSION)" != "3.12" ]; then \
        echo "Error: Python 3.12 is required."; \
        exit 1; \
    fi

setup_dev_env:
	$(PYTHON) -m venv venv
	$(VENV)/bin/python -m pip install --upgrade pytest build setuptools
	@if [ -f requirements.txt ]; then \
        $(VENV)/bin/python -m pip  install -r requirements.txt; \
    fi

setup: check_python_version setup_dev_env

test:
	$(VENV)/bin/pytest tests -m "not slow and not nonrepeatable"

test_all:
	$(VENV)/bin/pytest tests

build:
	$(VENV)/bin/python -m build

install:
	$(VENV)/bin/python -m pip install -e .

