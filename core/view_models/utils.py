from core.utils.labels import get_user_label, get_classroom_label


class Link(object):
    """
    Just a container class to hold the label and the id (passed as a url param) for a link in a viewmodel
    """

    def __init__(self, label, id, urlname=None):
        self.label = label
        self.id = id
        self.urlname = urlname


class UserInfo(object):
    """
    Container for storing user info
    """

    def __init__(self, user):
        self.user_school = user.userinfo.school.name
        self.name = get_user_label(user)
        self.user_id=user.pk


class StudentInfo(UserInfo):
    """
    Special container for student because student's userinfo also includes classroom label
    """

    def __init__(self, user):
        super(StudentInfo, self).__init__(user)
        self.classroom = get_classroom_label(user.classes_enrolled_set.get())
