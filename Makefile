# Docker

docker-build:
	@cd ./docker && docker build -t local/filegateway .

docker-up: 
	@cd ./docker && \
	docker build -t local/filegateway . && \
	docker run -p 8000:8000 -v ~/.filegateway:/mnt/logs:z -e GUNICORN_WORKERS=4 -e GUNICORN_ACCESS_LOG_FILE=/mnt/logs/access.log -e GUNICORN_LOG_FILE=/mnt/logs/error.log -e GUNICORN_LOG_LEVEL=info -d local/filegateway

podman-build:
	@cd ./docker && podman build -t local/filegateway .

podman-up: podman-build
	podman run -p 8000:8000 -v ~/.filegateway:/mnt/logs:z -e GUNICORN_WORKERS=4 -e GUNICORN_ACCESS_LOG_FILE=/mnt/logs/access.log -e GUNICORN_LOG_FILE=/mnt/logs/error.log -e GUNICORN_LOG_LEVEL=info -d local/filegateway
	
# Develop

dev-setup:
ifeq ("$(wildcard .venv)", "")
	@python -m virtualenv .venv
endif
	@source .venv/bin/activate && pip install -e .
		
dev-clean:
ifneq ("$(shell command -v deactivate)","")
	@deactivate
endif
	@rm -rf .venv

# Tests

test: dev-setup 
	@pip install tox && tox