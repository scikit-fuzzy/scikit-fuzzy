all: clean inplace test
	find skfuzzy -name "*version.py" | xargs rm -f
	find skfuzzy -name "*.pyc" | xargs rm -f

inplace:
	build .

clean-pyc:
	find skfuzzy -name "*.pyc" | xargs rm -f

clean-build:
	rm -rf ./build

clean-version:
	find skfuzzy -name "*version.py" | xargs rm -f

clean-cov:
	rm -rf ./coverage ./.coverage ./htmlcov

clean: clean-build clean-pyc clean-version clean-cov

test:
	python -m pytest

coverage: clean-cov
	python -m pytest --cov=skfuzzy --cov-report html
