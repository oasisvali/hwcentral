from core.view_models.base import AuthenticatedBody


class AssignmentIdBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the assignment id views
    """

    def __init__(self):
        pass


class StudentAssignmentIdBody(AssignmentIdBody):
    """
    Construct the viewmodel for the student subject id page body here. Information needed:
    1. List of ALL upcoming assignments for this subject (name, due date and completion)
    2. List of ALL graded assignments for this subject (name, grade)
    3. List of ALL announcements for this subject (timestamp and content)
    4. Performance report for this subject with breakdown by chapter (user_avg vs class_avg)
    """

    def __init__(self, user, assignment):
        raise


class ParentAssignmentIdBody(AssignmentIdBody):
    def __init__(self, user, assignment):
        raise


class AdminAssignmentIdBody(AssignmentIdBody):
    def __init__(self, user, assignment):
        raise


class TeacherAssignmentIdBody(AssignmentIdBody):
    def __init__(self, user, assignment):
        raise