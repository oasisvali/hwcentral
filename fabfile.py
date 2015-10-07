import logging
import os

from fabric.decorators import hosts, task
from fabric.operations import run, get
from fabric.state import env

WEB_SERVERS = ['119.9.77.38']
QA_SERVER = '128.199.130.205'
DB_SERVER = '119.9.88.54'
env.forward_agent = True
env.port = 1463

# Workaround for: No handlers could be found for logger "paramiko.transport"
# (see https://github.com/fabric/fabric/issues/51#issuecomment-96341022)
logging.basicConfig()
paramiko_logger = logging.getLogger("paramiko.transport")
paramiko_logger.disabled = True

DATA_DUMP_DIR = '../hwcentral-data/'

@task
@hosts(WEB_SERVERS + [DB_SERVER])
def deploy():
    run("devops/deploy.sh")


@task
@hosts([QA_SERVER])
def qa_deploy():
    run("devops/qa-deploy.sh")

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
def grade_overnight():
    run("./manage.py runscript grade_overnight -v3")


@task
@hosts(DB_SERVER)
def backup():
    run("devops/backup.sh")


@task
@hosts(WEB_SERVERS[0])
def db_health_check():
    run("./manage.py runscript scripts.database.enforcer -v3")


@task
@hosts(WEB_SERVERS[0])
def grab_data_dump(filename):
    filename = filename + '.json'

    run("scripts/fixtures/dump-data.sh %s" % filename)
    get(os.path.join("~/hwcentral", filename), os.path.join(DATA_DUMP_DIR, filename))
