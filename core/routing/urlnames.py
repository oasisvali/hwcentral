from django.conf.urls import url

from core.utils.constants import HWCentralRegex


TEMPLATE_FILE_EXTENSION = '.html'
ID_NAME_SUFFIX = '_id'



def prettify_for_url_matcher(name):
    return name.replace('_', '-')

class ChartUrlName(object):
    """
    This is to be used for chart endpoints - no templates, urlname has _chart suffix, matcher has chart/prefix
    """

    CHART_NAME_SUFFIX = '_chart'

    def __init__(self, name, num_ids=1):
        self.name = name + ChartUrlName.CHART_NAME_SUFFIX
        self.url_matcher = ('^chart/%s' + '/(%s)' * num_ids + '/$') % (
        (prettify_for_url_matcher(name),) + (HWCentralRegex.NUMERIC,) * num_ids)

class UrlName(object):
    """
    Base for most UrlNames. No template. default behavior is to set the urlname and matcher as the string passed in
    """
    def __init__(self, name):
        self.name = name
        self.url_matcher = '^%s/$' % name


class UrlNameWithMultipleIdArg(object):
    """
    Same as UrlName, adds the id suffix to the name and matcher takes a variable number of id arguments
    """

    def __init__(self, name, num_ids):
        self.name = name + ID_NAME_SUFFIX
        self.url_matcher = ('^%s' + '/(%s)' * num_ids + '/$') % (
        (prettify_for_url_matcher(name),) + (HWCentralRegex.NUMERIC,) * num_ids)

class UrlNameWithBase64Arg(UrlName):
    """
    Same as UrlName but the matcher takes a Base64 argument
    """
    def __init__(self, name):
        super(UrlNameWithBase64Arg, self).__init__(name)
        self.url_matcher = '^%s/(%s)/$' % (prettify_for_url_matcher(self.name), HWCentralRegex.BASE64)


class SubUrlName(object):
    """
    For endpoints which are 2nd level urls. No template, matcher has a 2-level domain {name/sub_name}.
    Name also contains url and sub-url
    """

    def __init__(self, name, sub_name):
        self.name = name + '_' + sub_name
        self.url_matcher = '^%s/%s/$' % (prettify_for_url_matcher(name), prettify_for_url_matcher(sub_name))


class SubUrlNameWithIdArg(SubUrlName):
    """
    Same as SubUrlName but matcher now takes an id argument. Also adds id suffix to name
    """

    def __init__(self, name, sub_name):
        super(SubUrlNameWithIdArg, self).__init__(name, sub_name)
        self.name += ID_NAME_SUFFIX
        self.url_matcher = '^%s/%s/(%s)/$' % (
        prettify_for_url_matcher(name), prettify_for_url_matcher(sub_name), HWCentralRegex.NUMERIC)


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

    def create_static_route(self, context):
        # Had to import inside function to resolve circular dependency when inbuilt login view is imported in views
        from core.routing.routers import static_router

        return url(self.url_matcher, static_router, {'template': self.get_template(), 'context': context},
                   name=self.name)


class AuthenticatedUrlName(TemplateUrlName):
    """
    Same as TemplateUrlName, except since the endpoint is authenticated, the template path has an authenticated path prefix
    """
    def __init__(self, name):
        super(AuthenticatedUrlName, self).__init__(name)
        self.template_stub = 'authenticated/' + self.name

    def get_template(self):
        return self.template_stub + TEMPLATE_FILE_EXTENSION


class AuthenticatedUrlNameWithIdArg(AuthenticatedUrlName):
    """
    Same as AuthenticatedUrlName, but adds an id suffix to name and template path. matcher takes id argument
    """

    def __init__(self, name):
        super(AuthenticatedUrlNameWithIdArg, self).__init__(name)
        self.url_matcher = '^%s/(%s)/$' % (prettify_for_url_matcher(self.name), HWCentralRegex.NUMERIC)
        self.name += ID_NAME_SUFFIX
        self.template_stub += ID_NAME_SUFFIX

class AuthenticatedUrlNameGroupDriven(AuthenticatedUrlName):
    """
    Same as AuthenticatedUrlName, but incorporates the group into the template path as it is group driven
    """
    def get_template(self, group):
        return self.template_stub + '/' + group + TEMPLATE_FILE_EXTENSION


class AuthenticatedUrlNameGroupDrivenWithIdArg(AuthenticatedUrlNameWithIdArg, AuthenticatedUrlNameGroupDriven):
    """
    Combines functionality of AuthenticatedUrlNameGroupDriven with AuthernticatedUrlNameWithIdArg
    """
    pass


class AuthenticatedUrlNameTypeDrivenWithIdArg(AuthenticatedUrlNameWithIdArg):
    """
    Same as AuthenticatedUrlNameWithIdArg, but adds a type element to the template path
    """

    def get_template(self, type):
        return self.template_stub + '/' + type + TEMPLATE_FILE_EXTENSION


class UrlNames(object):
    INDEX = StaticUrlName('index')
    INDEX.url_matcher = '^$'
    ABOUT = StaticUrlName('about')

    # REGISTER = TemplateUrlName('register')
    LOGOUT = UrlName('logout')
    LOGIN = TemplateUrlName('login')

    SETTINGS = AuthenticatedUrlNameGroupDriven('settings')
    HOME = AuthenticatedUrlNameGroupDriven('home')

    ASSIGNMENT_ID = AuthenticatedUrlNameWithIdArg('assignment')
    ASSIGNMENT_PREVIEW_ID = SubUrlNameWithIdArg('assignment', 'preview')

    SUBMISSION_ID = AuthenticatedUrlNameTypeDrivenWithIdArg('submission')

    SUBJECT_ID = AuthenticatedUrlNameGroupDrivenWithIdArg('subject')
    PARENT_SUBJECT_ID = UrlNameWithMultipleIdArg('subject', 2)
    CLASSROOM_ID = AuthenticatedUrlNameWithIdArg('classroom')

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
    ASSIGNMENT_OVERRIDE = SubUrlName('assignment', 'override')

    SECURE_STATIC = UrlNameWithBase64Arg('secure_static')
