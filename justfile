set dotenv-load

_fmt:
  cargo fmt

build: _fmt
  cargo build

run: _fmt
  cargo run -- --token ${TELEGRAM_TOKEN}

help: _fmt
  cargo run -- --help

pre-commit:
	pre-commit run
