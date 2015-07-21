from core.view_models.base import AuthenticatedBody


class ClassroomIdBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the classroom id views
    """

    def __init__(self,classroom):
        self.classroom=classroom


class StudentClassroomIdBody(ClassroomIdBody):
    """
    Construct the viewmodel for the classroom subject id page body here. Information needed:

    """

    def __init__(self, user, classroom):
        super(AdminClassroomIdBody,self).__init__(classroom)


class ParentClassroomIdBody(ClassroomIdBody):
    def __init__(self, user, classroom):
       super(AdminClassroomIdBody,self).__init__(classroom)


class AdminClassroomIdBody(ClassroomIdBody):
    def __init__(self, user, classroom):
        super(AdminClassroomIdBody,self).__init__(classroom)


class TeacherClassroomIdBody(ClassroomIdBody):
    def __init__(self, user, classroom):
       super(AdminClassroomIdBody,self).__init__(classroom)