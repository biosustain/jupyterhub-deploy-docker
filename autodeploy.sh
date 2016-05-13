# Create Docker machine and activate it
docker-machine create --driver generic --generic-ip-address $1 --generic-ssh-key $2 --generic-ssh-user root jupyterhub
eval "$(docker-machine env jupyterhub)"

# Create Docker network
docker network create jupyterhub-network

# Create data volume
docker volume create --name jupyterhub-data

# SSL security
#docker volume create --name jupyterhub-secrets
#./examples/letsencrypt/letsencrypt.sh \
#  --domain teaching.cameo.bio \
#  --email svegal@biosustain.dtu.dk \
#  --volume jupyterhub-secrets
#export SECRETS_VOLUME=jupyterhub-secrets

docker-compose build

# Pull the required image, wrap it to required scripts and set the env variable to point to it
cd examples/custom-notebook-server
docker build -t biosustain-cobranb .
cd ../..
export DOCKER_NOTEBOOK_IMAGE=biosustain-cobranb

# Run the service
#docker-compose -f examples/letsencrypt/docker-compose.yml up --build
docker-compose up --d
