import os

from core.routing.urlnames import truncate_index_url_matcher, ID_NAME_SUFFIX, prettify_for_url_matcher
from core.utils.constants import HWCentralRegex
from sphinx.urlnames import AppUrlName


class InkUrlName(AppUrlName):
    APP_NAME = 'ink'
    def __init__(self, name):
        super(InkUrlName, self).__init__(InkUrlName.APP_NAME, name)


class InkIndexUrlName(InkUrlName):  # custom case
    def __init__(self):
        super(InkIndexUrlName, self).__init__('index')
        self.url_matcher = truncate_index_url_matcher(self.url_matcher)

class InkUrlNameWithIdArg(InkUrlName):
    def __init__(self, name):
        super(InkUrlNameWithIdArg, self).__init__(name + ID_NAME_SUFFIX)
        self.url_matcher = '^%s/%s/(%s)/$' % (
        prettify_for_url_matcher(InkUrlNameWithIdArg.APP_NAME), prettify_for_url_matcher(name), HWCentralRegex.NUMERIC)


class InkUrlNames(object):
    INDEX = InkIndexUrlName()
    PARENT_ID = InkUrlName('parent')
