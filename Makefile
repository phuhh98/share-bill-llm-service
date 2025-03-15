# assign variable for main.py path
MAIN := app.main
# assign variable for requirements.txt path
REQS_FILE := requirements.txt

# add package to require
add-package:
	pipreqs . --force

# install all packages from requirements.txt
install:
	pip install -r $(REQS_FILE)

# run application with fastapi dev mode
# uvicorn $(MAIN):app --reload
run-dev:
	fastapi dev app/main.py

# run application in production mode
# uvicorn $(MAIN):app
run-prod:
	fastapi run app/main.py

# start prod
start:
	"$(MAKE)" install
	"$(MAKE)" run-prod

test:
	pytest

lint:
	ruff check --fix .