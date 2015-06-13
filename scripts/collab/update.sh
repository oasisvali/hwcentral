#!/usr/bin/env bash

# use this script to automate updating your dev setup with the upstream hwcentral repository
# Usage: scripts/collab/update.sh (run from root hwcentral directory)

echo 'RUN THIS SCRIPT FROM HWCENTRAL ROOT ONLY'
echo
echo 'If that is not the case, quit this script and cd ~/hwcentral'
echo
echo 'Press enter to continue or ctrl+C to quit...'
pause
echo
echo 'Continuing...'
echo

git status

echo 'Please check the above git status output ^'
echo
echo 'YOU SHOULD BE ON MASTER AND HAVE NO CHANGES'
echo
echo 'If that is not the case, quit this script and first commit your changes on your dev branch and switch to master'
echo
echo 'Press enter to continue or ctrl+C to quit...'
pause
echo
echo 'Continuing...'
echo

echo "Pulling from upstream (oasis's fork)"
git pull upstream master
echo "Pushing to origin (your fork)"
git push origin master

echo -n "VIRTUAL ENV = "
echo $VIRTUAL_ENV

echo 'Please check the above virtualenv output ^'
echo
echo 'YOU SHOULD BE IN VIRTUALENV HWCENTRAL'
echo
echo 'If that is not the case, quit this script and first workon hwcentral'
echo
echo 'Press enter to continue or ctrl+C to quit...'
pause
echo
echo 'Continuing...'
echo

echo 'Updating virtualenv'
pip install -r pip-requirements.txt
echo

scripts/collab/data-update.sh

echo
echo
echo 'Script completed. Dont forget to rebase your dev branch(es) on top of the current master by:'
echo '1. git checkout <dev-branch>'
echo '2. git rebase master'
echo '3. git push -f origin <dev-branch>'

