create-remote-machine:
	docker-machine create --driver generic --generic-ip-address $(MACHINE_IP) --generic-ssh-key $(PATH_TO_SSH) --generic-ssh-user root jupyterhub

create-local-machine:
	docker-machine create --driver virtualbox jupyterhub

rm-machine:
	docker-machine rm jupyterhub

restart-machine:
	docker-machine restart jupyterhub

build-all:
	@eval $$(docker-machine env jupyterhub); \
	docker network create jupyterhub-network; \
	docker volume create --name jupyterhub-data; \
	docker-compose build --force-rm; \
	docker pull $$DOCKER_NOTEBOOK_IMAGE

up:
	@eval $$(docker-machine env jupyterhub); \
	docker-compose up -d

down:
	@eval $$(docker-machine env jupyterhub); \
	docker-compose down

up-local: create-local-machine build-all up

up-remote: create-remote-machine build-all up