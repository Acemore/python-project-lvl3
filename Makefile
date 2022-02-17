build:
	poetry build

install:
	poetry install

lint:
	poetry run flake8 page_loader tests

package-install:
	python3 -m pip install --user dist/*.whl

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

.PHONY: build install lint package-install test
