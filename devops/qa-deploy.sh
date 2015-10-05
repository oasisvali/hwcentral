#!/usr/bin/env bash

# Usage: devops/qa-deploy.sh (from hwcentral root dir)

# reset local nginx conf changes
git checkout devops/nginx.conf

devops/deploy.sh

# reapply the nginx conf changes
sed -i "s/server_name hwcentral.in www.hwcentral.in/server_name 128.199.130.205/" devops/nginx.conf

# reload nginx
sudo ngnix -s reload