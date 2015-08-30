from core.view_models.base import AuthenticatedBody


class ClassroomIdBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the classroom id views
    """

    def __init__(self, classroom):
        self.classroom=classroom