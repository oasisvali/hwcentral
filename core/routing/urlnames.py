from django.conf.urls import url

from core.utils.constants import HWCentralRegex


TEMPLATE_FILE_EXTENSION = '.html'

class ChartUrlName(object):
    """
    This is to be used for chart endpoints - no templates, urlname has _chart suffix, matcher has chart/prefix
    """
    def __init__(self, name, num_ids=1):
        self.name = name + '_chart'
        self.url_matcher = ('^chart/%s' + '/(%s)' * num_ids + '/$') % ((name,) + (HWCentralRegex.NUMERIC,) * num_ids)

class UrlName(object):
    """
    Base for most UrlNames. No template. default behavior is to set the urlname and matcher as the string passed in
    """
    def __init__(self, name):
        self.name = name
        self.url_matcher = '^%s/$' % self.name


class UrlNameWithBase64Arg(UrlName):
    """
    Same as UrlName but the matcher takes a Base64 argument
    """
    def __init__(self, name):
        super(UrlNameWithBase64Arg, self).__init__(name)
        self.url_matcher = '^%s/(%s)/$' % (self.name, HWCentralRegex.BASE64)


class TemplateUrlName(UrlName):
    """
    Same as UrlName but provides access to a template
    """
    def get_template(self):
        return self.name + TEMPLATE_FILE_EXTENSION


class StaticUrlName(TemplateUrlName):
    """
    Same as TemplateUrlName, but to be used for static views (direct-to-template, no view logic)
    """
    def create_static_route(self):
        # Had to import inside function to resolve circular dependency when inbuilt login view is imported in views
        from core.routing.routers import static_router

        return url(self.url_matcher, static_router, {'template': self.get_template()}, name=self.name)


class AuthenticatedUrlName(TemplateUrlName):
    """
    Same as TemplateUrlName, except since the endpoint is authenticated, the template path has an authenticated path prefix
    """
    def __init__(self, name):
        super(AuthenticatedUrlName, self).__init__(name)
        self.template_stub = 'authenticated/' + self.name

    def get_template(self):
        return self.template_stub + TEMPLATE_FILE_EXTENSION


class AuthenticatedUrlNameGroupDriven(AuthenticatedUrlName):
    """
    Same as AuthenticatedUrlName, but incorporates the group into the template path as it is group driven
    """
    def get_template(self, group):
        return self.template_stub + '/' + group + TEMPLATE_FILE_EXTENSION


class AuthenticatedUrlNameGroupDrivenWithIdArg(AuthenticatedUrlNameGroupDriven):
    """
    Same as AuthenticatedUrlNameGroupDriven, but adds an id suffix to name and template path. matcher takes an id argument
    """
    def __init__(self, name):
        super(AuthenticatedUrlNameGroupDrivenWithIdArg, self).__init__(name)
        self.url_matcher = '^%s/(%s)/$' % (self.name, HWCentralRegex.NUMERIC)
        self.name += '_id'
        self.template_stub += '_id'


class AuthenticatedUrlNameGroupTypeDrivenWithIdArg(AuthenticatedUrlNameGroupDrivenWithIdArg):
    """
    Same as AuthenticatedUrlNameGroupDrivenWithIdArg but adds a type element to the template path
    """
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
    ASSIGNMENT = AuthenticatedUrlName('assignment')

    SECURE_STATIC = UrlNameWithBase64Arg('secure_static')
