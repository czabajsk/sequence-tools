
DOCKER_IMAGE = "uam_dash"

# create virtual environment
%.txt: %.in
	pip-compile --generate-hashes $<

.PHONY:
venv: requirements.txt
	python3.9 -m venv .venv
	. .venv/bin/activate; \
	pip install --upgrade virtualenv; \
	pip install --upgrade pip pip-tools setuptools wheel; \
	pip install -r requirements.txt

# build docker image
.PHONY:
docker-build:
	docker build -t $(DOCKER_IMAGE) .


# running app in docker
.PHONY:
docker-run: docker-build
	docker run --rm -p 8000:8000 $(DOCKER_IMAGE)

# run tests
.PHONY: docker-build
test: 
	docker run --rm $(DOCKER_IMAGE) python -m pytest 

.PHONY: venv
black:
	black src/

.PHONY: venv
pylint:
	pylint src/

.PHONY: venv
mypy:
	mypy src/

# cleanup
.PHONY:
venv-clean:
	rm -rf .venv