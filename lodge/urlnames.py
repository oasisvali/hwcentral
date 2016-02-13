from core.routing.urlnames import prettify_for_url_matcher
from core.utils.constants import HWCentralRegex
from sphinx.urlnames import AppUrlName


class LodgeUrlName(AppUrlName):
    APP_NAME = 'lodge'

    def __init__(self):
        super(LodgeUrlName, self).__init__(LodgeUrlName.APP_NAME, 'index')
        self.url_matcher = '^%s/(%s)/$' % (
            prettify_for_url_matcher(LodgeUrlName.APP_NAME), HWCentralRegex.NUMERIC)


class LodgeUrlNames(object):
    INDEX = LodgeUrlName()
