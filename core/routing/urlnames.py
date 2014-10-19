from django.conf.urls import url

from core.utils.constants import HWCentralRegex


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

    def get_template(self, group='', type=''):
        return 'authenticated/' + self.name + group + type + '.html'


class AuthenticatedUrlNameWithIdArg(AuthenticatedUrlName):
    def __init__(self, name, id_pattern):
        super(AuthenticatedUrlNameWithIdArg, self).__init__(name)
        self.url_matcher = '^%s/(%s)/$' % (self.name, id_pattern)
        self.name = self.name + '_id'


class UrlNames(object):
    INDEX = UrlName('index')

    REGISTER = UrlName('register')
    LOGOUT = UrlName('logout')
    LOGIN = UrlName('login')

    NEWS = UrlName('news')
    CONTACT = UrlName('contact')
    ABOUT = UrlName('about')

    SETTINGS = AuthenticatedUrlName('settings')
    HOME = AuthenticatedUrlName('home')
    TEST = AuthenticatedUrlName('test')

    ASSIGNMENT = AuthenticatedUrlName('assignment')
    ASSIGNMENT_ID = AuthenticatedUrlNameWithIdArg('assignment', HWCentralRegex.NUMERIC)

    SUBJECT_ID = AuthenticatedUrlNameWithIdArg('subject', HWCentralRegex.NUMERIC)

    # SCHOOL = AuthenticatedUrlName('school')
    # STUDENT = AuthenticatedUrlNameWithIdArg('student', HWCentralRegex.USERNAME)
    # CLASSROOM = AuthenticatedUrlNameWithIdArg('classroom', HWCentralRegex.NUMERIC)
