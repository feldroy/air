.DEFAULT_GOAL := help # Sets default action to be help

define PRINT_HELP_PYSCRIPT # start of Python section
import re, sys

output = []
# Loop through the lines in this file
for line in sys.stdin:
    # if the line has a command and a comment start with
    #   two pound signs, add it to the output
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        output.append("%-10s %s" % (target, help))
# Sort the output in alphanumeric order
output.sort()
# Print the help result
print('\n'.join(output))
endef
export PRINT_HELP_PYSCRIPT # End of python section

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean:  ## Run all the formatting, linting, and testing commands
	ruff format .
	ruff check . --fix
	ruff check --select I --fix .
	ty check .
	pytest .

MAKECMDGOALS ?= .	

testall:  ## Run all the tests for all the supported Python versions
	uv run --python=3.10 --with pytest --with httpx pytest
	uv run --python=3.11 --with pytest --with httpx pytest
	uv run --python=3.12 --with pytest --with httpx pytest
	uv run --python=3.13 --with pytest --with httpx pytest

test:  ## Run all the tests, but allow for arguments to be passed
	@echo "Running with arg: $(filter-out $@,$(MAKECMDGOALS))"
	uv run --python=3.13 --with pytest --with httpx pytest $(filter-out $@,$(MAKECMDGOALS))

pdb:  ## Run all the tests, but on failure, drop into the debugger
	@echo "Running with arg: $(filter-out $@,$(MAKECMDGOALS))"
	uv run --python=3.13 --with pytest --with httpx pytest --pdb --maxfail=10 --pdbcls=IPython.terminal.debugger:TerminalPdb $(filter-out $@,$(MAKECMDGOALS))

coverage:  ## Run coverage, and build to HTML
	coverage run -m pytest .
	coverage report -m
	coverage html

%:
	@:	

build:  ## Build the project, useful for checking that packaging is correct
	rm -rf build
	rm -rf dist
	uv build

VERSION=v$(shell grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)

version:  ## Print the current version of the project
	@echo "Current version is $(VERSION)"

tag:  ## Tag the current version in git and put to github
	echo "Tagging version $(VERSION)"
	git tag -a $(VERSION) -m "Creating version $(VERSION)"
	git push origin $(VERSION)

doc: ## Serve docs locally
	uv run --with "mkdocs-material" --with "mkdocstrings[python]" mkdocs serve -a localhost:3000

doc-build: ## Build and deploy docs
	mkdocs gh-deploy --force