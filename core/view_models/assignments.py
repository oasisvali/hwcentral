from core.utils.student import get_list_unfinished_assignments
from core.view_models.base import AuthenticatedBody


class AssignmentsBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the assignments views
    """

    def __init__(self):
        pass


class StudentAssignmentsBody(AssignmentsBody):
    """
    Construct the viewmodel for the student assignments page body here. Information needed:
    1. List of ALL upcoming assignments across ALL subjects (name, due date and completion)
    """

    def __init__(self, user):
        self.unfinished_assignments = get_list_unfinished_assignments(user, None)


class ParentAssignmentsBody(AssignmentsBody):
    def __init__(self, user):
        raise


class AdminAssignmentsBody(AssignmentsBody):
    def __init__(self, user):
        raise


class TeacherAssignmentsBody(AssignmentsBody):
    def __init__(self, user):
        raise






