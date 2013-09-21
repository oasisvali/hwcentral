# TODO: turn the 2 methods to member variables set in constructor
class UrlName():
    def __init__(self, name):
        self.name = name

    def toUrl(self):
        return '/' + self.name + '/'

    def toUrlMatcher(self):
        return '^' + self.name + '/$'