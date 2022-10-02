VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
PROJECT = bobotinho
.DEFAULT_GOAL = help

$(VENV)/bin/activate: requirements.txt requirements-dev.txt
	@python3.9 -m venv $(VENV)
	@$(PIP) install -U pip
	@$(PIP) install -r requirements-dev.txt
	@$(VENV) pre-commit install

help:  ## ❓ Show the help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<command>\033[36m\033[0m\nCommands:\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

install: $(VENV)/bin/activate  ## ⬇️  Install the virtual env project

version: $(VENV)/bin/activate  ## 🔢 Show the current environment
	@$(PYTHON) --version
	@$(PIP) --version
	@$(PIP) freeze

run: $(VENV)/bin/activate  ## 🏃 Run bot
	@$(PYTHON) -m ${PROJECT}

test: $(VENV)/bin/activate  ## 🧪 Run tests
	@pre-commit run --hook-stage manual pytest

format: $(VENV)/bin/activate  ## ✍  Format code
	@pre-commit run --hook-stage manual isort
	@pre-commit run --hook-stage manual end-of-file-fixer
	@pre-commit run --hook-stage manual trailing-whitespace
	@pre-commit run --hook-stage manual check-json
	@pre-commit run --hook-stage manual pretty-format-json
	@pre-commit run --hook-stage manual black

lint: $(VENV)/bin/activate  ## 🔎 Lint code
	@pre-commit run --hook-stage manual debug-statements
	@pre-commit run --hook-stage manual flake8
	@pre-commit run --hook-stage manual mypy

clear:  ## 🧹 Clean unused files
	@$(PYTHON) -Bc "for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()"
	@$(PYTHON) -Bc "for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()"
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

uninstall:  ## 🗑️  Uninstall the virtual env project
	@rm -rf $(VENV)
