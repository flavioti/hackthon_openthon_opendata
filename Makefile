app_version := $(shell eval poetry version --short)

.PHONY: build run compose
build:
	@echo $(app_version)
	docker build --no-cache --build-arg APP_VERSION=$(app_version) --tag resolvrisk_bureau:$(app_version) .

run:
	docker run \
	--name resolvrisk_bureau \
	--log-driver json-file \
	--log-opt max-size=10m \
	--log-opt max-file=3 \
	resolvrisk_bureau:$(app_version)

compose:
	docker-compose up --build --env-file .env
