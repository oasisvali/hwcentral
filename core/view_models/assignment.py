from core.routing.urlnames import UrlNames
from core.view_models.base import FormBody


class AssignmentBody(FormBody):
    """
    Used to store the viewmodels that define the body for the Assignment creation views
    """

    def __init__(self, form):
        super(AssignmentBody, self).__init__(form, UrlNames.ASSIGNMENT.name)

