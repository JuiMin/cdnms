local:
	docker rmi -f cdnms_cdnmsserver
	docker context use default
	# docker-compose --env-file ./env_files/local.env up -d --no-deps --force-recreate cdnmsredis
	docker-compose --env-file ./env_files/local.env up -d --no-deps --force-recreate --build cdnmsserver

prod:
	docker context use cdnms
	docker-compose --env-file ./env_files/prod.env up -d --force-recreate --build cdnmsserver

clean:
	docker system prune -f