#!/usr/bin/env bash

# Usage: devops/configure-cron.sh (from hwcentral root dir)

sudo cp devops/grade.cron /etc/cron.d/hwcentral_grade
sudo cp devops/sleep.cron /etc/cron.d/hwcentral_sleep

# force reload of cron config by making service restart
sudo service cron restart