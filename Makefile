all: clean inplace test
	find skfuzzy -name "*version.py" | xargs rm -f
	find skfuzzy -name "*.pyc" | xargs rm -f

inplace:
	python setup.py build_src --inplace build_ext --inplace

clean-pyc:
	find skfuzzy -name "*.pyc" | xargs rm -f

clean-build:
	rm -rf ./build

clean-version:
	find pyril -name "*version.py" | xargs rm -f

clean-cov:
	rm -rf ./coverage ./.coverage ./htmlcov

clean: clean-build clean-pyc

test:
	nosetests -s -v skfuzzy

coverage: clean-cov
	nosetests skfuzzy --with-coverage --cover-package=skfuzzy
