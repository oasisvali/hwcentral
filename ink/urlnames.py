from core.routing.urlnames import SubUrlName, truncate_index_url_matcher


class InkUrlName(SubUrlName):
    def __init__(self, name):
        super(InkUrlName, self).__init__('ink', name)


class InkIndexUrlName(InkUrlName):  # custom case
    def __init__(self):
        super(InkIndexUrlName, self).__init__('index')
        self.url_matcher = truncate_index_url_matcher(self.url_matcher)
        self.template = self.name + '.html'


class InkUrlNames(object):
    INDEX = InkIndexUrlName()
