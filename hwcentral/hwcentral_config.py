# This file loads in all the configuration required by hwcentral. It is triggered by django when it sources settings.py
# In the future, this should be modularized on an app-by-app basis. Also figure out how to run this only once
# Refer to http://programmers.stackexchange.com/questions/121221/when-to-use-constants-vs-config-files-to-maintain-configuration


def load_site_configs():
    print('Loading HWCentral config ...')