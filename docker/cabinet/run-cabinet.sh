#!/usr/bin/env bash

# clone the cabinet repo
git clone git@github.com:sidhantp/hwcentral-cabinet.git

cd hwcentral-cabinet

# run nginx
scripts/docker-init.sh