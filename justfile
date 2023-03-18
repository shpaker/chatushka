SOURCE_DIR := "chatushka/"

ruff:
  poetry run ruff check --fix {{ SOURCE_DIR }}
