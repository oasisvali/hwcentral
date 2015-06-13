#!/usr/bin/env bash

# Usage: devops/prep_static.sh (from hwcentral root dir)

rm -rf ./static_root    # TODO: use the location specified in settings.py, this is duplication

./manage.py collectstatic



