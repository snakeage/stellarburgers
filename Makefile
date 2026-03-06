.PHONY: help install lint test test-smoke test-regression test-negative test-workflow collect

help:
	@echo "Available commands:"
	@echo "  make install          - install dependencies"
	@echo "  make lint             - run pre-commit on all files"
	@echo "  make test             - run full pytest"
	@echo "  make test-smoke       - run smoke tests"
	@echo "  make test-regression  - run regression tests"
	@echo "  make test-negative    - run negative tests"
	@echo "  make test-workflow    - run workflow tests"
	@echo "  make collect          - collect tests only"

install:
	.venv/bin/pip install -r requirements.txt

lint:
	.venv/bin/pre-commit run --all-files

test:
	.venv/bin/pytest -q

test-smoke:
	.venv/bin/pytest -m smoke -q

test-regression:
	.venv/bin/pytest -m regression -q

test-negative:
	.venv/bin/pytest -m negative -q

test-workflow:
	.venv/bin/pytest -m workflow -q

collect:
	.venv/bin/pytest --collect-only -q
