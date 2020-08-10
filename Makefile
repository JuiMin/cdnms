build-ui:
	cd ./src/static && npm install && npm run build

start: build-ui
	# Start local dev env
	cd ./src && ./main.py

local: build-ui
	docker context use default
	# docker-compose --env-file ./env_files/local.env up -d --no-deps --force-recreate cdnmsredis
	docker-compose --env-file ./env_files/local.env up -d --no-deps --force-recreate --build cdnmsserver

log:
	docker logs cdnmsserver

prod:
	docker context use cdnms
	docker-compose --env-file ./env_files/prod.env up -d --force-recreate --build cdnmsserver

clean:
	rm -rf ./src/static/dist ./src/static/node_modules
	docker system prune -f