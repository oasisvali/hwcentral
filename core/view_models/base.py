from core.utils.constants import VIEWMODEL_KEY


class Base(object):
    """
    Abstract class that is used to provide as_context functionality to page-level view models
    """

    def as_context(self):
        return {VIEWMODEL_KEY: self}


class AuthenticatedBody(object):
    """
    Abstract class that is used to store any common data between the bodies of all the authenticated views
    """


class AuthenticatedBase(Base):
    """
    Class that is used to provide sidebar view model to all page-level view models for authenticated pages
    """

    def __init__(self, sidebar, authenticated_body):
        self.sidebar = sidebar
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
        self.form.form_action_url_name = form_action_url_name


class ReadOnlyFormBody(BaseFormBody):
    """
    Assumes that the form passed in has the read-only functionality and applies it so that a read-only form can be rendered
    """

    def __init__(self, readonly_form):
        super(ReadOnlyFormBody, self).__init__(readonly_form)
        self.form.make_readonly()


        