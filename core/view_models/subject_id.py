from core.utils.student import StudentSubjectIdUtils
from core.utils.teacher import TeacherSubjectIdUtils, AdminSubjectIdUtils
from core.view_models.base import AuthenticatedBody
from core.view_models.home import AnnouncementRow, ActiveAssignmentRow, StudentCorrectedAssignmentRow, \
    UncorrectedAssignmentRow, TeacherCorrectedAssignmentRow


class SubjectIdBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the subject id views
    """

    def __init__(self, subjectroom):
        self.subjectroom_id = subjectroom.pk

class StudentSubjectIdBody(SubjectIdBody):
    def __init__(self, user, subjectroom):
        super(StudentSubjectIdBody, self).__init__(subjectroom)
        utils = StudentSubjectIdUtils(user, subjectroom)
        self.announcements = [AnnouncementRow(announcement) for announcement in utils.get_announcements()]
        self.active_assignments = [ActiveAssignmentRow(active_assignment, completion) for active_assignment, completion
                                   in utils.get_active_assignments_with_completion()]
        self.corrected_assignments = [StudentCorrectedAssignmentRow(submission) for submission in
                                      utils.get_corrected_submissions()]


class TeacherSubjectIdBody(SubjectIdBody):
    def __init__(self, user, subjectroom):
        super(TeacherSubjectIdBody, self).__init__(subjectroom)
        utils = TeacherSubjectIdUtils(user, subjectroom)
        self.announcements = [AnnouncementRow(announcement) for announcement in utils.get_announcements()]
        self.uncorrected_assignments = [
            UncorrectedAssignmentRow(uncorrected_assignment, is_active, submissions_received)
            for uncorrected_assignment, is_active, submissions_received
            in utils.get_uncorrected_assignments_with_info()]
        self.corrected_assignments = [TeacherCorrectedAssignmentRow(assignment) for assignment in
                                      utils.get_corrected_assignments()]


class ParentSubjectIdBody(StudentSubjectIdBody):
    def __init__(self, child, subjectroom):
        super(ParentSubjectIdBody, self).__init__(child, subjectroom)


class AdminSubjectIdBody(TeacherSubjectIdBody):
    def __init__(self, user, subjectroom):
        super(TeacherSubjectIdBody, self).__init__(subjectroom)
        utils = AdminSubjectIdUtils(user, subjectroom)
        self.announcements = [AnnouncementRow(announcement) for announcement in utils.get_announcements()]
        self.uncorrected_assignments = [
            UncorrectedAssignmentRow(uncorrected_assignment, is_active, submissions_received)
            for uncorrected_assignment, is_active, submissions_received
            in utils.get_uncorrected_assignments_with_info()]
        self.corrected_assignments = [TeacherCorrectedAssignmentRow(assignment) for assignment in
                                      utils.get_corrected_assignments()]
