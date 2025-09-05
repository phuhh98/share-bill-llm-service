# assign variable for main.py path
MAIN := app/main.py

# create venv
venv-init:
	uv venv

# activate venv
# base on os to activate venv
venv-activate:
	@if [ -f ./.venv/bin/activate ]; then source ./.venv/bin/activate; fi
	@if [ -f ./.venv/Scripts/activate ]; then source ./.venv/Scripts/activate; fi

# install all packages from requirements.txt
install: venv-init
	uv sync

# run application with fastapi dev mode
# uvicorn $(MAIN):app --reload
run-dev:
	fastapi dev $(MAIN)

# run application in production mode
# uvicorn $(MAIN):app
run-prod:
	fastapi run $(MAIN)

# start prod
start:
	"$(MAKE)" install
	"$(MAKE)" run-prod

test:
	pytest

lint:
	ruff check --fix .

help:
	@echo "Makefile commands:"
	@echo "  venv-init        Create a virtual environment"
	@echo "  venv-activate    Activate the virtual environment"
	@echo "  install          Install all packages from requirements.txt"
	@echo "  run-dev          Run application in development mode with auto-reload"
	@echo "  run-prod         Run application in production mode"
	@echo "  start            Install dependencies and run application in production mode"
	@echo "  test             Run tests using pytest"
	@echo "  lint             Check and fix code style issues using ruff"
	@echo "  help             Display this help message"