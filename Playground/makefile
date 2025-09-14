IMAGE_NAME=health-service
CONTAINERS=health1 health2 health3

.PHONY: build run stop restart logs

build:
	docker build -t $(IMAGE_NAME) .

stop:
	@for c in $(CONTAINERS); do \
		echo "Stopping/removing $$c..."; \
		docker stop $$c 2>/dev/null || true; \
		docker rm $$c 2>/dev/null || true; \
	done

run:
	docker run -d -p 8001:8000 --name health1 $(IMAGE_NAME)
	docker run -d -p 8002:8000 --name health2 $(IMAGE_NAME)
	docker run -d -p 8003:8000 --name health3 $(IMAGE_NAME)

restart: build stop run

logs:
	@for c in $(CONTAINERS); do \
		echo "--- Logs $$c ---"; \
		docker logs $$c; \
	done