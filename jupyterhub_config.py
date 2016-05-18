# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
from tornado import gen
from ldapauthenticator import LDAPAuthenticator
import os


class PasswordPropagatingAuthenticator(LDAPAuthenticator):

    @gen.coroutine
    def authenticate(self, handler, data):
        os.environ["JPY_PASS"] = data['password']
        result = yield super().authenticate(handler, data)
        return result


c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
c.DockerSpawner.extra_start_kwargs = { 'network_mode': network_name, 'privileged': True }
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
c.DockerSpawner.notebook_dir = '/home/jovyan/work'
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { '{username}': '/home/jovyan/work' }
c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# TLS config
c.JupyterHub.port = 443
c.JupyterHub.ssl_key = os.environ['SSL_KEY']
c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# Keep password as env variable - used for accessing mounted folder
c.Spawner.env_keep.append("JPY_PASS")
# Authenticate users with LDAP
c.JupyterHub.authenticator_class = PasswordPropagatingAuthenticator
c.LDAPAuthenticator.server_address = 'ldap://win.dtu.dk'
c.LDAPAuthenticator.server_port = 389
c.LDAPAuthenticator.bind_dn_template = '{username}@win'

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')
c.JupyterHub.db_url = os.path.join('sqlite:///', data_dir, 'jupyterhub.sqlite')
c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

# Whitlelist users and admins
# c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set(["niso", "svegal"])
c.JupyterHub.admin_access = True
# pwd = os.path.dirname(__file__)
# with open(os.path.join(pwd, 'userlist')) as f:
#     for line in f:
#         if not line:
#             continue
#         parts = line.split()
#         name = parts[0]
#         whitelist.add(name)
#         if len(parts) > 1 and parts[1] == 'admin':
#             admin.add(name)
