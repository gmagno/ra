.PHONY: clean
clean:
	find . \( -name __pycache__ \
		-o -name "*.pyc" \
		-o -name "*.log" \
		-o -name "*.pkl" \
		-o -name .pytest_cache \
		-o -path "./dist" \
		-o -path "./ra_cpp.egg-info" \
		! -path ".venv/*" \
	\) -exec rm -rf {} +

.PHONY: build
build:
	mkdir -p build && cd build && \
	cmake \
		--config Release \
		--target all \
		-DCMAKE_BUILD_TYPE=Release \
		-DPYTHON_EXECUTABLE:FILEPATH=`which python` \
		-- \
		-j`nproc` \
		.. && \
	make

.PHONY: install-dev
install-dev:
	pip install -e .[dev]

.PHONY: build-conda-pkg
build-conda-pkg:
	conda build \
		-c conda-forge \
		-c schrodinger \
		-c defaults \
		--override-channels --output-folder build/out .
# conda env create -f environment.yml  # <-- use this instead!
# conda install ra-0.1.0-py37_0.tar.bz2  # <-- and this!

.PHONY: test
test:
	pytest test

.PHONY: run
run:
	PYTHONPATH=./build/ python -W ignore -m ra --cfg-dir data/legacy/odeon_ex/

.PHONY: docker-run-bash
docker-run-bash:
	docker run --rm -v `pwd`:/io -ti quay.io/pypa/manylinux1_x86_64 bash
