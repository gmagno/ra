
# -- Setup ----------------------------#

.PHONY: clean
clean:
	rm -rf dist/ build/ nb_py.egg* && \
	find . \( -name __pycache__ \
		-o -name "*.pyc" \
		-o -name .pytest_cache \
		-o -name .eggs \
		\) -exec rm -rf {} +\


# -- Development ----------------------#

.PHONY: test
test:
	pytest test

.PHONY: run
run:
	python ra/ra.py

