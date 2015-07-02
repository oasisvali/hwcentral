from core.view_models.base import AuthenticatedBody


class ClassroomIdBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the classroom id views
    """

    def __init__(self):
        pass


class StudentClassroomIdBody(ClassroomIdBody):
    """
    Construct the viewmodel for the classroom subject id page body here. Information needed:

    """

    def __init__(self, user, classroom):
        raise


class ParentClassroomIdBody(ClassroomIdBody):
    def __init__(self, user, subject):
        raise


class AdminClassroomIdBody(ClassroomIdBody):
    def __init__(self, user, subject):
        raise


class TeacherClassroomIdBody(ClassroomIdBody):
    def __init__(self, user, subject):
        raise