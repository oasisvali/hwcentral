from core.routing.urlnames import SubUrlName, truncate_index_url_matcher


class SphinxUrlName(SubUrlName):
    def __init__(self, name):
        super(SphinxUrlName, self).__init__('sphinx', name)


class SphinxIndexUrlName(SphinxUrlName):  # custom case
    def __init__(self):
        super(SphinxIndexUrlName, self).__init__('index')
        self.url_matcher = truncate_index_url_matcher(self.url_matcher)


class SphinxUrlNames(object):
    INDEX = SphinxIndexUrlName()
    DEAL_SUBPART = SphinxUrlName('deal_subpart')
