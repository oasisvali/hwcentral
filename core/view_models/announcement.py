from core.routing.urlnames import UrlNames
from core.view_models.base import FormBody


class AnnouncementBody(FormBody):
    """
    Used to store the viewmodels for the Announcement creation views
    """

    def __init__(self, form):
        super(AnnouncementBody, self).__init__(form, UrlNames.ANNOUNCEMENT.name)

