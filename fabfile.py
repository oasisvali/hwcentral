from fabric.operations import run
from fabric.state import env

env.hosts = ['119.9.77.38']
env.forward_agent = True


def deploy():
    print env.shell
    run("devops/deploy.sh")


def sleep():
    run("devops/sleep-mode-on.sh")


def wake():
    run("devops/sleep-mode-off.sh")
