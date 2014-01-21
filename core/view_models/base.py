from core.modules.constants import VIEWMODEL_KEY
from core.view_models.sidebar import Sidebar


class Base(object):
    """
    Abstract class that is used to provide as_context functionality to page-level view models
    """

    def as_context(self):
        return {VIEWMODEL_KEY: self}


class AuthenticatedBase(Base):
    """
    Abstract class that is used to provide sidebar view model to all page-level view models for authenticated pages
    """

    def __init__(self, user):
        self.sidebar = Sidebar(user)