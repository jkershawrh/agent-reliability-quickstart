PYTHON ?= python3

.PHONY: test lint run precommit
test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check src tests

precommit: lint test
	git diff --check

run:
	RELIABILITY_PROFILE=config/reliability-profile.lab.yaml $(PYTHON) -m uvicorn src.main:app --reload --port 8080

