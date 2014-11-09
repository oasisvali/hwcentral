#!/bin/sh

# use this script to automate a basic schemamigration from the hwcentral root directory
# Usage: scripts/migrations/basic.sh <app-to-migrate-1> [<app-to-migrate-2>....]

python manage.py schemamigration "$@" --auto
echo 'Do you want to apply the migration? Press any key to continue...'
read -n 1 -s
python manage.py migrate
echo
echo 'Dont forget to register any new models with the admin.'

