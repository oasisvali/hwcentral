from fabric.decorators import hosts, task
from fabric.operations import run
from fabric.state import env

WEB_SERVERS = ['119.9.77.38']
DB_SERVERS = ['119.9.88.54']
env.forward_agent = True
env.port = 1463

@task
@hosts(WEB_SERVERS + DB_SERVERS)
def deploy():
    run("devops/deploy.sh")


@task
@hosts(WEB_SERVERS)
def sleep():
    run("devops/sleep-mode-on.sh")


@task
@hosts(WEB_SERVERS)
def wake():
    run("devops/sleep-mode-off.sh")
