.DEFAULT_GOAL := ci

POETRY ?= poetry

.PHONY: ci install lint format-check typecheck test format

# Run the same checks as GitHub Actions, in order, stopping on failure.
# Recursive recipes keep this sequential even when called with make -j.
ci:
	$(MAKE) lint
	$(MAKE) format-check
	$(MAKE) typecheck
	$(MAKE) test

install:
	$(POETRY) install

lint:
	$(POETRY) run ruff check .

format-check:
	$(POETRY) run ruff format --check .

typecheck:
	$(POETRY) run mypy .

test:
	$(POETRY) run pytest

# This target changes files; it is not part of ci.
format:
	$(POETRY) run ruff format .
