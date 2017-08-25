from fabric.context_managers import settings
from fabric.contrib import files
from fabric.decorators import task
from fabric.operations import sudo, run, put
from fabric.state import env
from fabfile.common import apt_get, apt_get_update

@task
def install():
    """
    """
    print "Installing requirements"

    apt_get_update()

    apt_get("build-essential", "git", "wget")

    git_install()

    run("wget -qO- https://get.docker.com/ | sh")

    sudo("curl -L https://github.com/docker/compose/releases/download/1.10.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose")
    sudo("chmod +x /usr/local/bin/docker-compose")

@task
def git_install():
    """
    """
    with settings(warn_only=True):
        global repository
        result = run("cd ~; git clone {0}".format(env.repository))
        if not result.return_code == 0:
            run("cd ~/mlm; git pull")