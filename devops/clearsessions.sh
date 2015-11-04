#!/usr/bin/env bash

# Usage: devops/clearsessions.sh (from hwcentral root dir)

export WORKON_HOME=/home/oasis/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

workon hwcentral
cd /home/oasis/hwcentral
./manage.py clearsessions
echo 'Expired sessions have been cleaned up'