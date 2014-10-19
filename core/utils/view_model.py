def get_classroom_label(classroom):
    return '{0} - {1}'.format(classroom.standard.number, classroom.division)


def get_user_label(user):
    return '{0} {1}'.format(user.first_name, user.last_name)


class Link(object):
    """
    Just a container class to hold the label and the id (passed as a url param) for a link in a viewmodel
    """

    def __init__(self, label, id, urlname=None):
        self.label = label
        self.id = id
        self.urlname = urlname