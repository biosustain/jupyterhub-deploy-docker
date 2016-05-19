# jupyterhub-deploy-docker

This repository provides a reference deployment of [JupyterHub](https://github.com/jupyter/jupyterhub), a multi-user [Jupyter Notebook](http://jupyter.org/) environment, on a **single host** using [Docker](https://docs.docker.com).  

Forked from [jupyterhub-deploy-docker](https://github.com/jupyterhub/jupyterhub-deploy-docker) - find more thorough documentation there

Features added:
* Allows users to work in their remote dtu-storage folders
* Uses modification of [LDAPAuthenticator](https://github.com/jupyterhub/ldapauthenticator) to authenticate users with DTU credentials

# To deploy

Copy the TLS certificate chain and key files for the JupyterHub server to a directory named `secrets` within this repository directory. These will be added to the JupyterHub Docker image at build time.

```
mkdir -p secrets
cp jupyterhub.pem jupyterhub.key secrets/
```
    
If you deploy on remote host, pass IP address and path to SSH key to ```make``` command

```
make MACHINE_IP=<ip> PATH_TO_SSH=<path> up-remote
```

If you deploy locally

```
make up-local
```