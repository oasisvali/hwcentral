from core.routing.urlnames import UrlNames
from core.view_models.base import FormBody


class PracticeBody(FormBody):
    """
    Used to store the viewmodels that define the body for the Practice Assignment creation views
    """

    def __init__(self, form):
        super(PracticeBody, self).__init__(form, UrlNames.PRACTICE.name)
