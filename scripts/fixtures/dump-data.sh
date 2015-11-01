#!/usr/bin/env bash

# run this script from hwcentral root directory to dump the current mysql data
# Usage: scripts/fixtures/dump-data.sh [<path to output file>]

OUTFILE=${1:-"core/fixtures/db_dump.json"}
TMPFILE="db_dump.json"

# excluding session history and admin actions history and
# permissions data - which is recreated automatically on migrate
./manage.py runscript scripts.fixtures.dump_data
mv $TMPFILE $OUTFILE

echo "Test data has been dumped to $OUTFILE"
echo "Dont forget to check the dumped data and commit it to the repo"
