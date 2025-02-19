#!/usr/bin/env just --justfile

SOURCE_DIR := "chatushka"
TESTS_DIR := "tests"

lint: ruff mypy

mypy:
    uv run python -m mypy --pretty --package {{ SOURCE_DIR }}

ruff:
    uv run python -m ruff check --fix --unsafe-fixes {{ SOURCE_DIR }}

format:
    uv run python -m ruff format {{ SOURCE_DIR }}
    uv run python -m ruff format {{ TESTS_DIR }}

tests:
    uv run python -m pytest {{ TESTS_DIR }}
