.PHONY: help setup test lint fmt data baselines patch das figures paper all clean

help:  ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS=":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

setup:  ## install dev dependencies
	uv sync --extra dev

test:  ## run the golden tests
	pytest

lint:  ## static checks
	ruff check src tests

fmt:  ## autofix + format
	ruff check --fix src tests && ruff format src tests

data:  ## generate the controlled benchmark
	python -m polarity_circuits.cli generate --out data/controlled --n 400

baselines:  ## score models (behavioural pass)
	python -m polarity_circuits.cli score --config configs/controlled.yaml

patch:  ## activation patching
	python -m polarity_circuits.cli patch --config configs/controlled.yaml

das:  ## distributed alignment search
	python -m polarity_circuits.cli das --config configs/das.yaml

figures:  ## build paper figures
	python -m polarity_circuits.cli figures

paper:  ## compile the paper (needs acl.sty in paper/)
	cd paper && latexmk -pdf main.tex

all: data baselines patch das figures  ## full reproduction
	@echo "done. results/ updated."

clean:  ## remove build artifacts (keeps data/ and results/)
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
