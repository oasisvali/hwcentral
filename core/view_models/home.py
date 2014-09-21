from core.modules.constants import HWCentralGroup
from core.view_models.base import AuthenticatedBase
from hwcentral.exceptions import InvalidStateException


class StudentAuthenticatedBody(object):
    def __init__(self, user, user_group):
        pass


class ParentAuthenticatedBody(object):
    def __init__(self, user, user_group):
        pass


class AdminAuthenticatedBody(object):
    def __init__(self, user, user_group):
        pass


class TeacherAuthenticatedBody(object):
    def __init__(self, user, user_group):
        pass


class Home(AuthenticatedBase):
    """
    This is the page-level view model which will contain everything else
    """

    def __init__(self, user):
        super(Home, self).__init__(user)

        if self.user_group == HWCentralGroup.STUDENT:
            self.authenticated_body = StudentAuthenticatedBody(user, self.user_group)
        elif self.user_group == HWCentralGroup.PARENT:
            self.authenticated_body = ParentAuthenticatedBody(user, self.user_group)
        elif self.user_group == HWCentralGroup.ADMIN:
            self.authenticated_body = AdminAuthenticatedBody(user, self.user_group)
        elif self.user_group == HWCentralGroup.TEACHER:
            self.authenticated_body = TeacherAuthenticatedBody(user, self.user_group)
        else:
            raise InvalidStateException('Invalid HWCentralGroup: %s' % self.user_group)





