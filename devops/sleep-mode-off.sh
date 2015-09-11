#!/usr/bin/env bash

# Usage: devops/sleep-mode-off.sh (from hwcentral root dir)

# stop the gunicorn server
sudo supervisorctl stop gunicorn

# delete the sleep mode marker file
sudo rm /etc/hwcentral/sleep

# start the gunicorn server
sudo supervisorctl start gunicorn

