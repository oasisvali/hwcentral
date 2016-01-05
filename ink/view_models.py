from core.view_models.base import FormViewModel
from ink.urlnames import InkUrlNames


class IndexViewModel(FormViewModel):
    """
    Used to store the viewmodels that define the Index view
    """

    def __init__(self, main_form, password_form):
        super(IndexViewModel, self).__init__(main_form, InkUrlNames.INDEX.name)
        self.password_form = password_form
