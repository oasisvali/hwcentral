#!/usr/bin/env bash

# Usage: devops/update.sh (from hwcentral root dir)

git pull origin master
sudo supervisorctl stop gunicorn
devops/prep-deploy.sh
sudo supervisorctl start gunicorn

