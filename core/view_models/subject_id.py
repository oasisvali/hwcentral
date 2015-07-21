from core.utils.student import get_list_unfinished_assignments_by_subject, get_list_graded_submissions_by_subject, \
    get_list_announcements_by_subject, get_performance_report_by_subject
from core.view_models.base import AuthenticatedBody


class SubjectIdBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the subject id views
    """

    def __init__(self):
        pass


class StudentSubjectIdBody(SubjectIdBody):
    """
    Construct the viewmodel for the student subject id page body here. Information needed:
    1. List of ALL upcoming assignments for this subject (name, due date and completion)
    2. List of ALL graded assignments for this subject (name, grade)
    3. List of ALL announcements for this subject (timestamp and content)
    4. Performance report for this subject with breakdown by chapter (user_avg vs class_avg)
    """

    def __init__(self, user, subject):
        self.subject = subject
        # self.unfinished_assignments = get_list_unfinished_assignments_by_subject(user, subject)
        # self.graded_submissions = get_list_graded_submissions_by_subject(user, subject)
        # self.announcements = get_list_announcements_by_subject(subject)
        # self.perf_report = get_performance_report_by_subject(user, subject)


class ParentSubjectIdBody(SubjectIdBody):
    def __init__(self, user, subject):
        self.subject = subject


class AdminSubjectIdBody(SubjectIdBody):
    def __init__(self, user, subject):
        self.subject = subject


class TeacherSubjectIdBody(SubjectIdBody):
    def __init__(self, user, subject):
        self.subject = subject