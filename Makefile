# assign variable for main.py path
MAIN := app/main.py
# assign variable for requirements.txt path
REQS_FILE := requirements.txt

# add package to require
reqs-update:
	pipreqs . --force

# install all packages from requirements.txt
install:
	pip install -r $(REQS_FILE)

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