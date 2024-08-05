LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:=stream-model-duration:${LOCAL_TAG}

test:
	cd tests && pytest unit-tests

quality_checks:
	isort deployment monitoring
	black deployment monitoring
	pylint --recursive=y deployment monitoring

build: quality_checks test
	docker build -t ${LOCAL_IMAGE_NAME} .

integration_test: build
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash tests/integration-tests/run.sh

publish: build integration_test
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash scripts/publish.sh

setup:
	pipenv install --dev
	pre-commit install
