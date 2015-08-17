#!/usr/bin/env bash

# Usage: devops/update.sh (from hwcentral root dir)

git pull origin master
sudo supervisorctl stop gunicorn
scripts/collab/virtualenv_cleanup.sh
devops/prep-deploy.sh
sudo nginx -s reload
sudo supervisorctl start gunicorn

