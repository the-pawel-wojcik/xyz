.PHONY: upload

upload:
	cd dist; rm *
	python -m build
	python -m pip install --upgrade twine
	python -m twine upload --repository pypi dist/*
