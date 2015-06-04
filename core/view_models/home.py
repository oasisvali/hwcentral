from core.utils.student import get_list_unfinished_assignments, get_list_graded_submissions, \
    get_list_announcements, get_performance_report
from core.view_models.base import AuthenticatedBody
from core.utils.parent import get_list_active_subject_assignments


class HomeBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the home views
    """

    def __init__(self):
        pass


class StudentHomeBody(HomeBody):
    """
    Construct the viewmodel for the student home page body here. Information needed:
    1. List of upcoming assignments (name, subject, due date and completion)
    2. List of graded assignments (name, subject, grade)
    3. List of announcements (origin, type, timestamp and content)
    4. Performance report (avg, class avg) for each subject

    Lists 1-3 are in most-recent-first order

    The data for the class distribution per assignment is served via ajax call
    """

    def __init__(self, user):
        self.unfinished_assignments = get_list_unfinished_assignments(user)
        self.graded_submissions = get_list_graded_submissions(user)
        self.announcements = get_list_announcements(user)
        self.perf_report = get_performance_report(user)


class ParentHomeBody(HomeBody):
    """
    Construct viewmodle for parent home page here. Information needed:
    1. List of subjects per student and
    2. The assignment per subject of each student.
    3.

    """
    def __init__(self, user):
        # self.announcements = get_list_announcements(user)
        self.graded_submissions = get_list_active_subject_assignments(user)


class AdminHomeBody(HomeBody):
    def __init__(self, user):
        raise


class TeacherHomeBody(HomeBody):
    def __init__(self, user):
        raise





