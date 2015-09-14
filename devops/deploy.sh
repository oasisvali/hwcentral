#!/usr/bin/env bash

# Usage: devops/deploy.sh (from hwcentral root dir)

sudo nginx -s stop
sudo supervisorctl stop gunicorn
git pull origin master
scripts/collab/virtualenv_cleanup.sh
devops/prep-static.sh
devops/truncate-logs.sh
# allow log files to be created inside devops directory
sudo supervisorctl update gunicorn
sudo supervisorctl start gunicorn
sudo nginx