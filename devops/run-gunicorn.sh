#!/usr/bin/env bash

# Usage: devops/run-gunicorn.sh (from hwcentral root dir)

export WORKON_HOME=/home/oasis/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

workon hwcentral
# exec is needed otherwise supervisor just supervises this script and not the forked gunicorn processes
exec gunicorn hwcentral.wsgi -c devops/gunicorn_conf.py



