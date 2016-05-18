#!/usr/bin/env bash
docker-compose down
docker rmi -f biosustain-cobranb
docker rmi jupyterhub
docker rm -v jupyter-svegal
docker volume rm $(docker volume ls -qf dangling=true)
docker network rm jupyterhub-network
docker-machine restart jupyterhub
