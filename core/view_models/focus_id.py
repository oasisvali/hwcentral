from core.utils.admin import AdminFocusIdUtils
from core.utils.labels import get_user_label, get_subjectroom_label, get_focusroom_label
from core.utils.student import StudentFocusIdUtils
from core.utils.teacher import TeacherFocusIdUtils
from core.view_models.base import AuthenticatedBody
from core.view_models.home import ActiveAssignmentRow, StudentCorrectedAssignmentRow, \
    UncorrectedAssignmentRow, TeacherCorrectedAssignmentRow
from core.view_models.subject_id import RoomReportCard, RoomReportCardRow


class FocusIdBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the focus id views
    """

    def __init__(self, focusroom):
        self.focusroom_id = focusroom.pk
        self.focusroom_label = get_focusroom_label(get_subjectroom_label(focusroom.subjectRoom))
        self.subjectteacher_label = get_user_label(focusroom.subjectRoom.teacher)


class StudentFocusIdBody(FocusIdBody):
    def __init__(self, user, focusroom):
        super(StudentFocusIdBody, self).__init__(focusroom)
        utils = StudentFocusIdUtils(user, focusroom)
        self.active_assignments = [ActiveAssignmentRow(active_assignment, completion) for active_assignment, completion
                                   in utils.get_active_assignments_with_completion()]
        self.corrected_assignments = [StudentCorrectedAssignmentRow(submission) for submission in
                                      utils.get_corrected_submissions()]


class TeacherFocusIdBody(FocusIdBody):
    def __init__(self, user, focusroom):
        super(TeacherFocusIdBody, self).__init__(focusroom)
        utils = TeacherFocusIdUtils(user, focusroom)
        self.uncorrected_assignments = [
            UncorrectedAssignmentRow(uncorrected_assignment, is_active, submissions_received)
            for uncorrected_assignment, is_active, submissions_received
            in utils.get_uncorrected_assignments_with_info()]
        self.corrected_assignments = [TeacherCorrectedAssignmentRow(assignment) for assignment in
                                      utils.get_corrected_assignments()]
        self.reportcard = RoomReportCard(utils.get_focusroom_average(),
                                         [RoomReportCardRow(student, average) for student, average in
                                          utils.get_focusroom_reportcard_info()])


class ParentFocusIdBody(StudentFocusIdBody):
    def __init__(self, child, focusroom):
        super(ParentFocusIdBody, self).__init__(child, focusroom)
        self.child_name = get_user_label(child)
        self.child_id = child.pk


class AdminFocusIdBody(TeacherFocusIdBody):
    def __init__(self, user, focusroom):
        super(TeacherFocusIdBody, self).__init__(focusroom)
        utils = AdminFocusIdUtils(user, focusroom)
        self.uncorrected_assignments = [
            UncorrectedAssignmentRow(uncorrected_assignment, is_active, submissions_received)
            for uncorrected_assignment, is_active, submissions_received
            in utils.get_uncorrected_assignments_with_info()]
        self.corrected_assignments = [TeacherCorrectedAssignmentRow(assignment) for assignment in
                                      utils.get_corrected_assignments()]
        self.reportcard = RoomReportCard(utils.get_focusroom_average(),
                                         [RoomReportCardRow(student, average) for student, average in
                                          utils.get_focusroom_reportcard_info()])
