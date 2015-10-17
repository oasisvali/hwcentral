#!/usr/bin/env bash

# clone the cabinet repo (only sanity test branch is needed for now)
git clone -b sanity_test git@github.com:sidhantp/hwcentral-cabinet.git

cd hwcentral-cabinet

# run nginx
scripts/docker-init.sh