# pull in the normal settings
from settings import *

# This useless assert statement simply so pycharm doesnt mark the above import as unused and remove it while optimizing
assert SECRET_KEY

# prod secret key should only be on prod server
with open('/etc/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# no debug for us
DEBUG = False
