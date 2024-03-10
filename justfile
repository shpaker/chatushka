#!/usr/bin/env just --justfile

SOURCE_DIR := "chatushka"
TESTS_DIR := "tests"

lint: mypy ruff

mypy:
    poetry run python -m mypy --pretty --package {{ SOURCE_DIR }}

ruff:
    poetry run python -m ruff check --fix {{ SOURCE_DIR }}

format:
    poetry run python -m ruff format {{ SOURCE_DIR }}
    poetry run python -m ruff format {{ TESTS_DIR }}

pytest:
    poetry run python -m pytest {{ TESTS_DIR }}
