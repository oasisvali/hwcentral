#!/usr/bin/env bash

# Usage: devops/sleep-mode-on.sh (from hwcentral root dir)

# stop the gunicorn server
sudo supervisorctl stop gunicorn

# touch the sleep mode marker file
sudo touch /etc/hwcentral/sleep

# start the gunicorn server
sudo supervisorctl start gunicorn