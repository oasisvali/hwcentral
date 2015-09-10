#!/usr/bin/env bash

# Usage: devops/deploy.sh (from hwcentral root dir)

git pull origin master
sudo supervisorctl stop gunicorn
scripts/collab/virtualenv_cleanup.sh
devops/prep-deploy.sh
sudo nginx -s reload
sudo supervisorctl update gunicorn
sudo supervisorctl start gunicorn
# allow log files to be created inside devops directory
chmod 777 devops/