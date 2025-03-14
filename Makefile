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
run-dev:
	uvicorn $(MAIN):app --reload

# run application in production mode
run-prod:
	uvicorn $(MAIN):app

# start prod
start:
	"$(MAKE)" install
	"$(MAKE)" run-prod

test:
	pytest

# format all file using black
format:
	black .