# assign variable for main.py path
MAIN := app/main.py

# create venv
venv-init:
	uv venv

# activate venv
venv-activate:
	source ./.venv/Scripts/activate

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