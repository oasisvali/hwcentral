#!/usr/bin/env bash

# Usage: scripts/collab/prep-static.sh (from hwcentral root dir)

echo 'Removing existing data in dev database'
python manage.py reset_db
echo 'Updating local dev database'
python manage.py migrate
echo 'Loading test data'
python manage.py loaddata test_data
