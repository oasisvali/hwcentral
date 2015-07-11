from django.conf.urls import url

from core.utils.constants import HWCentralRegex


TEMPLATE_FILE_EXTENSION = '.html'

class ChartUrlName(object):
    def __init__(self, name, num_ids=1):
        self.name = name + '_chart'
        self.url_matcher = ('^chart/%s' + '/(%s)' * num_ids + '/$') % ((name,) + (HWCentralRegex.NUMERIC,) * num_ids)

class UrlName(object):
    def __init__(self, name):
        self.name = name
        self.url_matcher = '^%s/$' % self.name


class UrlNameWithBase64IdArg(UrlName):
    def __init__(self, name):
        super(UrlNameWithBase64IdArg, self).__init__(name)
        self.url_matcher = '^%s/(%s)/$' % (self.name, HWCentralRegex.BASE64)


class TemplateUrlName(UrlName):
    def get_template(self):
        return self.name + TEMPLATE_FILE_EXTENSION


class StaticUrlName(TemplateUrlName):

    def create_static_route(self):
        # Had to import inside function to resolve circular dependency when inbuilt login view is imported in views
        from core.routing.routers import static_router

        return url(self.url_matcher, static_router, {'template': self.get_template()}, name=self.name)


class AuthenticatedUrlName(TemplateUrlName):
    def __init__(self, name):
        super(AuthenticatedUrlName, self).__init__(name)
        self.template_stub = 'authenticated/' + self.name

    def get_template(self):
        return self.template_stub + TEMPLATE_FILE_EXTENSION


class AuthenticatedUrlNameGroupDriven(AuthenticatedUrlName):
    def get_template(self, group):
        return self.template_stub + '/' + group + TEMPLATE_FILE_EXTENSION


class AuthenticatedUrlNameGroupDrivenWithIdArg(AuthenticatedUrlNameGroupDriven):
    def __init__(self, name):
        super(AuthenticatedUrlNameGroupDrivenWithIdArg, self).__init__(name)
        self.url_matcher = '^%s/(%s)/$' % (self.name, HWCentralRegex.NUMERIC)
        self.name += '_id'
        self.template_stub += '_id'


class AuthenticatedUrlNameGroupTypeDrivenWithIdArg(AuthenticatedUrlNameGroupDrivenWithIdArg):
    def get_template(self, group, type):
        return self.template_stub + '/' + group + '/' + type + TEMPLATE_FILE_EXTENSION


class UrlNames(object):
    INDEX = StaticUrlName('index')
    INDEX.url_matcher = '^/$'
    ABOUT = StaticUrlName('about')

    # REGISTER = TemplateUrlName('register')
    LOGOUT = UrlName('logout')
    LOGIN = TemplateUrlName('login')

    SETTINGS = AuthenticatedUrlNameGroupDriven('settings')
    HOME = AuthenticatedUrlNameGroupDriven('home')

    ASSIGNMENTS = AuthenticatedUrlNameGroupDriven('assignments')
    ASSIGNMENT_ID = AuthenticatedUrlNameGroupTypeDrivenWithIdArg('assignment')

    SUBJECT_ID = AuthenticatedUrlNameGroupDrivenWithIdArg('subject')
    CLASSROOM_ID = AuthenticatedUrlNameGroupDrivenWithIdArg('classroom')

    STUDENT_CHART = ChartUrlName('student')
    SINGLE_SUBJECT_STUDENT_CHART = ChartUrlName('student', 2)
    SUBJECTROOM_CHART = ChartUrlName('subjectroom')
    SUBJECT_TEACHER_SUBJECTROOM_CHART = ChartUrlName('subjectteacher')
    CLASS_TEACHER_SUBJECTROOM_CHART = ChartUrlName('classteacher', 2)
    ASSIGNMENT_CHART = ChartUrlName('assignment')
    STANDARD_ASSIGNMENT_CHART = ChartUrlName('standard_assignment')

    ANNOUNCEMENT = AuthenticatedUrlName('announcement')
    PASSWORD =AuthenticatedUrlName('password')

    SECURE_STATIC = UrlNameWithBase64IdArg('secure_static')
