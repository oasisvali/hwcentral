from fabric.operations import run
from fabric.state import env

env.hosts = ['119.9.77.38', '119.9.88.54']
env.forward_agent = True
env.port = 1463

def deploy():
    print env.shell
    run("devops/deploy.sh")


def sleep():
    run("devops/sleep-mode-on.sh")


def wake():
    run("devops/sleep-mode-off.sh")
