#!/usr/bin/env bash

# run this script from hwcentral root directory to dump the current mysql data

OUTFILE="hwcentral/fixtures/test_data.json"
TMPFILE="__tmp__"

# excluding session history and
# admin actions history and
# permissions data - which is recreated automatically on migrate
python manage.py dumpdata core auth sites --natural-foreign --indent 4 --exclude sessions --exclude admin --exclude auth.permission > $TMPFILE
cat $TMPFILE > $OUTFILE
rm $TMPFILE

echo "Test data has been dumped to $OUTFILE"
echo "Dont forget to check the dumped data and commit it to the repo"
