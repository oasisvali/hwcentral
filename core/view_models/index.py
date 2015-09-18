from core.routing.urlnames import UrlNames
from core.view_models.base import FormViewModel


class IndexViewModel(FormViewModel):
    """
    Used to store the viewmodels that define the Index view
    """

    def __init__(self, form):
        super(IndexViewModel, self).__init__(form, UrlNames.INDEX.name)
