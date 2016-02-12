#!/usr/bin/env bash

# Usage: pylon/scripts/notify-due.sh (from hwcentral root dir)

export WORKON_HOME=/home/oasis/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

workon hwcentral
cd /home/oasis/hwcentral
./manage.py runscript notify_due
