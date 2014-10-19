from core.models import SubjectRoom
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
    """

    def __init__(self, user, subject_id):
        self.subject = SubjectRoom.objects.get(pk=subject_id)
        self.unfinished_assignments = get_list_unfinished_assignments_by_subject(user, subject_id)
        self.graded_submissions = get_list_graded_submissions_by_subject(user, subject_id)
        self.announcements = get_list_announcements_by_subject(subject_id)
        self.perf_report = get_performance_report_by_subject(user, subject_id)


class ParentSubjectIdBody(SubjectIdBody):
    def __init__(self, user):
        pass


class AdminSubjectIdBody(SubjectIdBody):
    def __init__(self, user):
        pass


class TeacherSubjectIdBody(SubjectIdBody):
    def __init__(self, user):
        pass






