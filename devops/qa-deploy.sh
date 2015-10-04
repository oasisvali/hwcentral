#!/usr/bin/env bash

# Usage: devops/qa-deploy.sh (from hwcentral root dir)

# stash the nginx conf changes
git stash

devops/deploy.sh

# unstash the nginx conf changes
git stash apply
sudo nginx -s reload