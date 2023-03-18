SOURCE_DIR := "chatushka/"
TESTS_DIR := "chatushka/"

format:
  poetry run isort {{ SOURCE_DIR }} {{ TESTS_DIR }}
  poetry run black {{ SOURCE_DIR }} {{ TESTS_DIR }}

ruff:
  poetry run ruff check {{ SOURCE_DIR }} {{ TESTS_DIR }}

linters: format ruff

tests:
  echo foo

ci: linters tests
