from fabric.decorators import task
from fabric.state import env

import common
import docker
import install

env.repository = "https://github.com/applet97/intranet.git"
env.user = "ubuntu"
env.hosts = ["18.194.21.239"]
env.key_filename = "~/intranet.pem"
env.filename = "docker-compose.yml"