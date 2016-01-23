import os

from core.routing.urlnames import truncate_index_url_matcher, ID_NAME_SUFFIX, prettify_for_url_matcher
from core.utils.constants import HWCentralRegex
from sphinx.urlnames import AppUrlName


class EdgeUrlName(AppUrlName):
    APP_NAME = 'edge'

    def __init__(self, name):
        super(EdgeUrlName, self).__init__(EdgeUrlName.APP_NAME, name)


class EdgeIndexUrlName(EdgeUrlName):  # custom case
    def __init__(self):
        super(EdgeIndexUrlName, self).__init__('index')
        self.url_matcher = truncate_index_url_matcher(self.url_matcher)

    def get_template(self, group):
        return os.path.join(EdgeIndexUrlName.APP_NAME, 'index', group + '.html')


class EdgeUrlNameWithIdArg(EdgeUrlName):
    def __init__(self, name):
        super(EdgeUrlNameWithIdArg, self).__init__(name + ID_NAME_SUFFIX)
        self.url_matcher = '^%s/%s/(%s)/$' % (
            prettify_for_url_matcher(EdgeUrlNameWithIdArg.APP_NAME), prettify_for_url_matcher(name),
            HWCentralRegex.NUMERIC)


class EdgeUrlNameWith2IdArg(EdgeUrlNameWithIdArg):
    def __init__(self, name):
        super(EdgeUrlNameWith2IdArg, self).__init__(name)
        self.url_matcher = '^%s/%s/(%s)/(%s)/$' % (
            prettify_for_url_matcher(EdgeUrlNameWithIdArg.APP_NAME), prettify_for_url_matcher(name),
            HWCentralRegex.NUMERIC, HWCentralRegex.NUMERIC)

class EdgeUrlNames(object):
    INDEX = EdgeIndexUrlName()
    SUBJECT_ID = EdgeUrlNameWithIdArg('subject')
    STUDENT_ID = EdgeUrlNameWith2IdArg('student')
