import os

from core.routing.urlnames import SubUrlName, truncate_index_url_matcher

class AppUrlName(SubUrlName):
    def __init__(self, app_name, name):
        super(AppUrlName, self).__init__(app_name, name)
        self.template = os.path.join(app_name, name + '.html')

class SphinxUrlName(AppUrlName):
    APP_NAME = 'sphinx'
    def __init__(self, name):
        super(SphinxUrlName, self).__init__(SphinxUrlName.APP_NAME, name)


class SphinxIndexUrlName(SphinxUrlName):  # custom case
    def __init__(self):
        super(SphinxIndexUrlName, self).__init__('index')
        self.url_matcher = truncate_index_url_matcher(self.url_matcher)


class SphinxUrlNames(object):
    INDEX = SphinxIndexUrlName()
    DEAL = SphinxUrlName('deal')
    TAGS = SphinxUrlName('tags')
    REVISION = SphinxUrlName('revision')
