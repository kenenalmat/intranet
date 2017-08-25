from fabric.decorators import task
from fabric.state import env

import common
import docker
import install

env.repository = "https://github.com/applet97/intranet.git"
env.user = "ubuntu"
env.hosts = ["35.156.208.108"]
env.key_filename = "~/intranet.pem"
env.filename = "docker-compose.yml"