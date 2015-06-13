#!/usr/bin/env bash

# Usage: devops/run-gunicorn.sh (from hwcentral root dir)

export WORKON_HOME=/home/oasis/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

workon hwcentral
gunicorn hwcentral.wsgi -c devops/gunicorn_conf.py



