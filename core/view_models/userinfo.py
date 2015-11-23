from core.utils.labels import get_user_label


class BaseUserInfo(object):
    """
    Container for storing user info
    """

    def __init__(self, user):
        self.name = get_user_label(user)
        self.user_id = user.pk


class HeaderUserInfo(BaseUserInfo):
    def __init__(self, user, announcement_count):
        super(HeaderUserInfo, self).__init__(user)
        self.announcement_count = announcement_count
