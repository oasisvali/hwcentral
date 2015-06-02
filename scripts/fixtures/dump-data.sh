#!/bin/sh

# run this script from hwcentral root directory to dump the current mysql data

OUTFILE="hwcentral/fixtures/test_data.json"
TMPFILE="__tmp__"

python manage.py dumpdata core auth --natural --indent 4 -e sessions -e admin -e contenttypes -e auth.Permission > $TMPFILE
tail -n +2 $TMPFILE > $OUTFILE
rm $TMPFILE

echo "Test data has been dumped to $OUTFILE"
echo "Dont forget to check the dumped data and commit it to the repo"
