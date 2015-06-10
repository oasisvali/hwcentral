#!/usr/bin/env bash

# Usage: devops/run_gunicorn.sh (from hwcentral root dir)

source /usr/local/bin/virtualenvwrapper.sh

workon hwcentral
gunicorn hwcentral.wsgi -c devops/gunicorn_conf.py



