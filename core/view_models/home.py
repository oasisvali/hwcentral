from core.view_models.base import AuthenticatedBase


class Home(AuthenticatedBase):
    """
    This is the page-level view model which will contain everything else
    """

    def __init__(self, user):
        super(Home, self).__init__(user)



