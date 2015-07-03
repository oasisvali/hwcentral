from core.view_models.base import AuthenticatedBody

class AnnouncementBody(AuthenticatedBody):
    """
    Abstract class that is used to store the form for the Announcement creation views
    """

    def __init__(self,form):
        self.form = form