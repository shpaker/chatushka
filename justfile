SOURCE_DIR := "chatushka/"

format:
  poetry run isort {{ SOURCE_DIR }}
  poetry run black {{ SOURCE_DIR }}

ruff:
  poetry run ruff check {{ SOURCE_DIR }}

linters: format ruff

tests:
  echo foo

ci: linters tests
