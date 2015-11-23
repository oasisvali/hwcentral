from core.utils.admin import AdminUtils
from core.utils.constants import VIEWMODEL_KEY
from core.utils.labels import get_user_label
from core.utils.parent import ParentUtils
from core.utils.references import HWCentralGroup
from core.utils.student import StudentUtils
from core.utils.teacher import TeacherUtils
from hwcentral.exceptions import InvalidHWCentralGroupError


class VM(object):
    """
    Abstract class that is used to provide as_context functionality to page-level view models
    """

    def as_context(self):
        return {VIEWMODEL_KEY: self}


class FormViewModel(VM):
    def __init__(self, form, form_action_url_name):
        self.form = form
        self.form.action_url_name = form_action_url_name

class AuthenticatedBody(object):
    """
    Abstract class that is used to store any common data between the bodies of all the authenticated views
    """


class AuthenticatedVM(VM):
    """
    Class that is used to provide sidebar view model to all page-level view models for authenticated pages
    """

    def __init__(self, user, authenticated_body):
        from core.view_models.sidebar import AdminSidebar, TeacherSidebar, ParentSidebar, StudentSidebar

        if user.userinfo.group == HWCentralGroup.refs.STUDENT:
            self.sidebar = StudentSidebar(user)
            utils = StudentUtils(user)
        elif user.userinfo.group == HWCentralGroup.refs.PARENT:
            self.sidebar = ParentSidebar(user)
            utils = ParentUtils(user)
        elif user.userinfo.group == HWCentralGroup.refs.TEACHER:
            self.sidebar = TeacherSidebar(user)
            utils = TeacherUtils(user)
        elif user.userinfo.group == HWCentralGroup.refs.ADMIN:
            self.sidebar = AdminSidebar(user)
            utils = AdminUtils(user)
        else:
            raise InvalidHWCentralGroupError(user.userinfo.group)

        self.userinfo = UserInfo(user, utils.get_announcements_count())
        self.authenticated_body = authenticated_body


class BaseFormBody(AuthenticatedBody):
    """
    Abstract class that provides the most basic functionality for a form-defined viewmodel -> it wraps a form object
    """

    def __init__(self, form):
        self.form = form


class FormBody(BaseFormBody):
    """
    Abstract class that is used to store common logic for all form view models
    """

    def __init__(self, form, form_action_url_name):
        """
        @param form: django form object that the template this viewmodel is passed to will render
        @param form_action_url_name: url name for the POST endpoint for the form of this body
        """
        super(FormBody, self).__init__(form)
        self.form.action_url_name = form_action_url_name


class ReadOnlyFormBody(BaseFormBody):
    """
    Assumes that the form passed in has the read-only functionality and applies it so that a read-only form can be rendered
    """
    pass


class UserInfo(object):
    """
    Container for storing user info
    """

    def __init__(self, user, announcement_count):
        self.name = get_user_label(user)
        self.user_id = user.pk
        self.announcement_count = announcement_count