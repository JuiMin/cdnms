localserver:
	docker-compose up -d --no-deps --force-recreate cdnmsredis
	docker-compose up -d --no-deps --force-recreate --build cdnmsserver