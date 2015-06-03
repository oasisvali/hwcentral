from django.conf.urls import url

from core.utils.constants import HWCentralRegex


class UrlName(object):
    def __init__(self, name):
        self.name = name
        self.url_matcher = '^%s/$' % self.name

    def get_template(self):
        return self.name + '.html'

    def create_static_route(self):
        # Had to import inside function to resolve circular dependency when inbuilt login view is imported in views
        from core.routing.routers import static_router

        return url(self.url_matcher, static_router, {'template': self.get_template()}, name=self.name)


class AuthenticatedUrlName(UrlName):
    def __init__(self, name):
        super(AuthenticatedUrlName, self).__init__(name)
        self.template_stub = 'authenticated/' + self.name

    def get_template(self):
        return self.template_stub + '.html'

    def get_group_driven_template(self, group, type):
        template = self.template_stub + '/' + group
        if type is not None:
            template += '_' + type
        return template + '.html'


class AuthenticatedUrlNameWithIdArg(AuthenticatedUrlName):
    def __init__(self, name, id_pattern):
        super(AuthenticatedUrlNameWithIdArg, self).__init__(name)
        self.url_matcher = '^%s/(%s)/$' % (self.name, id_pattern)
        self.name += '_id'
        self.template_stub += '_id'


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

    ASSIGNMENTS = AuthenticatedUrlName('assignments')
    ASSIGNMENT_ID = AuthenticatedUrlNameWithIdArg('assignment', HWCentralRegex.NUMERIC)

    SUBJECT_ID = AuthenticatedUrlNameWithIdArg('subject', HWCentralRegex.NUMERIC)

    # SCHOOL = AuthenticatedUrlName('school')
    STUDENT = AuthenticatedUrlNameWithIdArg('student', HWCentralRegex.USERNAME)
    CLASSROOM = AuthenticatedUrlNameWithIdArg('classroom', HWCentralRegex.NUMERIC)
