from core.modules.utils.student_utils import get_list_unfinished_assignments, get_list_graded_submissions, \
    get_list_announcements, get_performance_report
from core.view_models.base import AuthenticatedBase


class StudentAuthenticatedBody(object):
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


class ParentAuthenticatedBody(object):
    def __init__(self, user):
        pass


class AdminAuthenticatedBody(object):
    def __init__(self, user):
        pass


class TeacherAuthenticatedBody(object):
    def __init__(self, user):
        pass


class Home(AuthenticatedBase):
    """
    This is the page-level view model which will contain everything else
    """

    def __init__(self, sidebar, authenticated_body):
        super(Home, self).__init__(sidebar, authenticated_body)





