#!/usr/bin/env bash

# Usage: grader/scripts/grade-overnight.sh (from hwcentral root dir)

export WORKON_HOME=/home/oasis/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

workon hwcentral
cd /home/oasis/hwcentral
./manage.py runscript grade_overnight
