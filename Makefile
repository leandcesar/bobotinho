VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
PROJECT = bobotinho
.DEFAULT_GOAL = help

$(VENV)/bin/activate: requirements.txt requirements-dev.txt
	@python3 -m venv $(VENV)
	@$(PIP) install -U pip
	@$(PIP) install -r requirements-dev.txt

help:  ## ❓ Show the help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<command>\033[36m\033[0m\nCommands:\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

install: $(VENV)/bin/activate  ## ⬇️  Install the virtual env project

uninstall:  ## 🗑️  Uninstall the virtual env project
	@rm -rf $(VENV)

version: $(VENV)/bin/activate  ## 🔢 Show the current environment
	@$(PYTHON) --version
	@$(PIP) --version
	@$(PIP) freeze

run: $(VENV)/bin/activate  ## 🏃 Run the project
	@$(PYTHON) -m ${PROJECT}

clean:  ## 🧹 Clean unused files
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

format: $(VENV)/bin/activate  ## ✍  Format code
	@$(VENV)/bin/isort ${PROJECT}/
	@$(VENV)/bin/brunette ${PROJECT}/ --config=setup.cfg

lint: $(VENV)/bin/activate  ## 🔎 Lint code
	@$(VENV)/bin/brunette ${PROJECT}/ --config=setup.cfg --check
	@$(VENV)/bin/flake8 ${PROJECT}/ --config=setup.cfg --count --show-source --statistics --benchmark
