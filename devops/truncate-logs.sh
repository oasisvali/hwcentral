#!/usr/bin/env bash

# Usage: devops/truncate-logs.sh (from hwcentral root dir)

sudo truncate devops/nginx_access.log --size=0
sudo truncate devops/nginx_error.log --size=0
truncate devops/gunicorn_access.log --size=0
truncate devops/gunicorn_stderr.log --size=0