from fabric.decorators import hosts, task
from fabric.operations import run
from fabric.state import env

WEB_SERVERS = ['119.9.77.38']
DB_SERVER = '119.9.88.54'
env.forward_agent = True
env.port = 1463

@task
@hosts(WEB_SERVERS + [DB_SERVER])
def deploy():
    run("devops/deploy.sh")


@task
@hosts(WEB_SERVERS + [DB_SERVER])
def dd_restart():
    run("sudo /etc/init.d/datadog-agent restart")

@task
@hosts(WEB_SERVERS)
def sleep():
    run("devops/sleep-mode-on.sh")


@task
@hosts(WEB_SERVERS)
def wake():
    run("devops/sleep-mode-off.sh")


@task
@hosts(WEB_SERVERS[0])
def grade():
    run("./manage.py runscript scripts.grade_overnight -v3")


@task
@hosts(DB_SERVER)
def backup():
    run("devops/backup.sh")
