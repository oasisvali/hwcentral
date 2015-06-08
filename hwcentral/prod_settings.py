# pull in the normal settings
from settings import *

# This useless assert statement simply so pycharm doesnt mark the above import as unused and remove it while optimizing
assert SECRET_KEY

# no debug for us
DEBUG = False
