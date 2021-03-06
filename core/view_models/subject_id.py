from core.utils.admin import AdminSubjectIdUtils
from core.utils.labels import get_user_label, get_average_label, get_subjectroom_label
from core.utils.open_student import OpenStudentSubjectIdUtils, calculate_open_aql_average
from core.utils.student import StudentSubjectIdUtils
from core.utils.teacher import TeacherSubjectIdUtils
from core.view_models.base import AuthenticatedBody
from core.view_models.home import ActiveAssignmentRow, StudentCorrectedAssignmentRow, \
    UncorrectedAssignmentRow, TeacherCorrectedAssignmentRow, OpenAssignmentRowCorrected, \
    OpenAssignmentRowUncorrected


class RoomReportCardRow(object):

    def __init__(self, student, average):
        self.name = get_user_label(student)
        self.student_id = student.pk
        self.average = get_average_label(average)


class RoomReportCard(object):
    def __init__(self, room_average, rows):
        self.room_average = get_average_label(room_average)
        self.rows = rows

class SubjectIdBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the subject id views
    """

    def __init__(self, subjectroom):
        self.subjectroom_id = subjectroom.pk
        self.subjectroom_label = get_subjectroom_label(subjectroom)
        self.subjectteacher_label = get_user_label(subjectroom.teacher)       

class StudentSubjectIdBody(SubjectIdBody):
    def __init__(self, user, subjectroom):
        super(StudentSubjectIdBody, self).__init__(subjectroom)
        utils = StudentSubjectIdUtils(user, subjectroom)
        self.active_assignments = [ActiveAssignmentRow(active_assignment, completion) for active_assignment, completion
                                   in utils.get_active_assignments_with_completion()]
        self.corrected_assignments = [StudentCorrectedAssignmentRow(submission) for submission in
                                      utils.get_corrected_submissions()]


class OpenStudentSubjectIdBody(AuthenticatedBody):
    def __init__(self, user, subjectroom):
        utils = OpenStudentSubjectIdUtils(user, subjectroom)
        self.corrected_assignments = [OpenAssignmentRowCorrected(submission, calculate_open_aql_average(
            submission.assignment.assignmentQuestionsList)) for submission
                                      in utils.get_corrected()]
        self.uncorrected_assignments = [OpenAssignmentRowUncorrected(submission) for submission in
                                        utils.get_uncorrected()]

        self.subjectroom_id = subjectroom.pk
        self.subjectroom_label = subjectroom.subject.name


class TeacherSubjectIdBody(SubjectIdBody):
    def __init__(self, user, subjectroom):
        super(TeacherSubjectIdBody, self).__init__(subjectroom)
        utils = TeacherSubjectIdUtils(user, subjectroom)
        self.uncorrected_assignments = [
            UncorrectedAssignmentRow(uncorrected_assignment, is_active, submissions_received)
            for uncorrected_assignment, is_active, submissions_received
            in utils.get_uncorrected_assignments_with_info()]
        self.corrected_assignments = [TeacherCorrectedAssignmentRow(assignment) for assignment in
                                      utils.get_corrected_assignments()]
        self.reportcard = RoomReportCard(utils.get_subjectroom_average(),
                                         [RoomReportCardRow(student, average) for student, average in
                                          utils.get_subjectroom_reportcard_info()])


class ParentSubjectIdBody(StudentSubjectIdBody):
    def __init__(self, child, subjectroom):
        super(ParentSubjectIdBody, self).__init__(child, subjectroom)
        self.child_name = get_user_label(child)
        self.child_id= child.pk


class AdminSubjectIdBody(TeacherSubjectIdBody):
    def __init__(self, user, subjectroom):
        super(TeacherSubjectIdBody, self).__init__(subjectroom)
        utils = AdminSubjectIdUtils(user, subjectroom)
        self.uncorrected_assignments = [
            UncorrectedAssignmentRow(uncorrected_assignment, is_active, submissions_received)
            for uncorrected_assignment, is_active, submissions_received
            in utils.get_uncorrected_assignments_with_info()]
        self.corrected_assignments = [TeacherCorrectedAssignmentRow(assignment) for assignment in
                                      utils.get_corrected_assignments()]
        self.reportcard = RoomReportCard(utils.get_subjectroom_average(),
                                         [RoomReportCardRow(student, average) for student, average in
                                          utils.get_subjectroom_reportcard_info()])
