from django.conf.urls import url

from core.utils.constants import HWCentralRegex


class ChartUrlName(object):
    def __init__(self, name, num_ids=1):
        self.name = name + '_chart'
        self.url_matcher = ('^chart/%s' + '/(%s)' * num_ids + '/$') % ((name,) + (HWCentralRegex.NUMERIC,) * num_ids)

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
    def __init__(self, name):
        super(AuthenticatedUrlNameWithIdArg, self).__init__(name)
        self.url_matcher = '^%s/(%s)/$' % (self.name, HWCentralRegex.NUMERIC)
        self.name += '_id'
        self.template_stub += '_id'


class AuthenticatedUrlNameWithMultipleIdArg(AuthenticatedUrlNameWithIdArg):
    def __init__(self, name, id_patterns):
        super(AuthenticatedUrlNameWithMultipleIdArg, self).__init__(name, None)
        self.url_matcher = ('^%s' + '/(%s)' * len(id_patterns) + '/$') % ((name,) + id_patterns)


class UrlNames(object):
    INDEX = UrlName('index')
    ABOUT = UrlName('about')

    REGISTER = UrlName('register')
    LOGOUT = UrlName('logout')
    LOGIN = UrlName('login')

    SETTINGS = AuthenticatedUrlName('settings')
    HOME = AuthenticatedUrlName('home')

    ASSIGNMENTS = AuthenticatedUrlName('assignments')
    ASSIGNMENT_ID = AuthenticatedUrlNameWithIdArg('assignment')

    SUBJECT_ID = AuthenticatedUrlNameWithIdArg('subject')
    CLASSROOM_ID = AuthenticatedUrlNameWithIdArg('classroom')

    STUDENT_CHART = ChartUrlName('student')
    SINGLE_SUBJECT_STUDENT_CHART = ChartUrlName('student', 2)
    SUBJECTROOM_CHART = ChartUrlName('subjectroom')
    SUBJECT_TEACHER_SUBJECTROOM_CHART = ChartUrlName('subjectteacher')
    CLASS_TEACHER_SUBJECTROOM_CHART = ChartUrlName('classteacher', 2)
    ASSIGNMENT_CHART = ChartUrlName('assignment')

    STANDARD_ASSIGNMENT_CHART = ChartUrlName('standard_assignment')

    ANNOUNCEMENT = AuthenticatedUrlName('announcement')

