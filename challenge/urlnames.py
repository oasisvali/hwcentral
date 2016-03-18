from core.routing.urlnames import prettify_for_url_matcher
from core.utils.constants import HWCentralRegex
from sphinx.urlnames import AppUrlName


class ChallengeUrlName(AppUrlName):
    APP_NAME = 'challenge'

    def __init__(self):
        super(ChallengeUrlName, self).__init__(ChallengeUrlName.APP_NAME, 'index')
        self.url_matcher = '^%s/(%s)/$' % (
            prettify_for_url_matcher(ChallengeUrlName.APP_NAME), HWCentralRegex.NUMERIC)


class ChallengeUrlNames(object):
    INDEX = ChallengeUrlName()
