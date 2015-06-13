#!/usr/bin/env bash

# Usage: scripts/collab/prep-static.sh (from hwcentral root dir)

echo 'Updating local dev database'
python manage.py migrate
echo 'Removing existing data in dev database'
python manage.py flush
echo 'Loading test data'
python manage.py loaddata test_data
