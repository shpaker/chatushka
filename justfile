set dotenv-load

fmt:
  cargo fmt

build: fmt
  cargo build

run: fmt
  cargo run -- --token ${TELEGRAM_TOKEN}

help: fmt
  cargo run -- --help

pre-commit:
	pre-commit run
