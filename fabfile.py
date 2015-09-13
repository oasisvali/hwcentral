from fabric.decorators import task
from fabric.operations import run
from fabric.state import env

from dogapi.fab import setup, notify

setup("11ef54b9111e793be921e57768d67906")

WEB_SERVERS = ['119.9.77.38']
DB_SERVERS = ['119.9.88.54']
env.forward_agent = True
env.port = 1463


@notify
@task
def deploy():
    env.hosts = WEB_SERVERS + DB_SERVERS
    run("devops/deploy.sh")


@notify
@task
def sleep():
    env.hosts = WEB_SERVERS
    run("devops/sleep-mode-on.sh")


@notify
@task
def wake():
    env.hosts = WEB_SERVERS
    run("devops/sleep-mode-off.sh")
