from django.conf.urls import url

from core.modules.constants import HWCentralRegex


class UrlName(object):
    def __init__(self, name):
        self.name = name
        self.url_matcher = '^%s/$' % self.name
        self.template = self.name + '.html'

    def create_static_route(self):
        # Had to import inside function to resolve circular dependency when inbuilt login view is imported in views
        from core.routing.routers import static_router

        return url(self.url_matcher, static_router, {'template': self.template}, name=self.name)


class AuthenticatedUrlName(UrlName):
    def __init__(self, name):
        super(AuthenticatedUrlName, self).__init__(name)
        self.template = 'authenticated/' + self.template


class AuthenticatedUrlNameWithIdArg(AuthenticatedUrlName):
    def __init__(self, name, id_pattern):
        super(AuthenticatedUrlNameWithIdArg, self).__init__(name)
        self.url_matcher = '^%s/(%s)/$' % (self.name, id_pattern)


class UrlNames(object):
    INDEX = UrlName('index')
    HOME = AuthenticatedUrlName('home')
    TEST = AuthenticatedUrlName('test')

    REGISTER = UrlName('register')
    LOGOUT = UrlName('logout')
    LOGIN = UrlName('login')

    NEWS = UrlName('news')
    CONTACT = UrlName('contact')
    ABOUT = UrlName('about')

    STUDENT = AuthenticatedUrlNameWithIdArg('student', HWCentralRegex.USERNAME)
    SUBJECT = AuthenticatedUrlNameWithIdArg('subject', HWCentralRegex.NUMERIC)
    CLASSROOM = AuthenticatedUrlNameWithIdArg('classroom', HWCentralRegex.NUMERIC)
    ASSIGNMENT_ID = AuthenticatedUrlNameWithIdArg('assignment_id', HWCentralRegex.NUMERIC)

    ASSIGNMENT = AuthenticatedUrlName('assignment')

    SCHOOL = AuthenticatedUrlName('school')
    SETTINGS = AuthenticatedUrlName('settings')
