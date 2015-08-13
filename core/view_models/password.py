from core.routing.urlnames import UrlNames
from core.view_models.base import FormBody


class PasswordBody(FormBody):
    """
    Used to store the viewmodels that define the Password change views
    """

    def __init__(self, form):
        super(PasswordBody, self).__init__(form, UrlNames.PASSWORD.name)
