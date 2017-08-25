from fabric.decorators import task
from fabric.operations import sudo, run
from fabric.state import env

@task
def cmd(*args):
	"""
	"""
	sudo('cd ~/mlm; docker-compose -f ' + env.filename + ' ' + ' '.join(args))

@task
def up():
	"""
	"""
	cmd("up", "-d")

@task
def clear_container():
	"""
	"""
	cmd("sudo docker stop $(docker ps - a - q)")
	cmd("sudo docker rm $(docker ps -a - q)")

@task
def build():
	"""
	"""
	cmd("build")

@task
def ps():
	"""
	"""
	cmd("ps")

@task
def ssh(*args):
	sudo("sudo docker exec -i -t %s bash" % ' '.join(args))