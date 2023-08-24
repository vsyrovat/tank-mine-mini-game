.PHONY: fmt lint test

fmt:
	pipenv run fmt

lint:
	pipenv run lint

test:
	pipenv run pytest -v
