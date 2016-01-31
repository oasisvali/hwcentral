from core.utils.classroom_id import ClassroomIdUtils
from core.utils.labels import get_user_label, get_average_label, get_classroom_label
from core.view_models.base import AuthenticatedBody
from core.view_models.home import UncorrectedAssignmentRow, TeacherCorrectedAssignmentRow


class ClassroomReportCardRow(object):
    def __init__(self, student, averages, aggregate):
        self.name = get_user_label(student)
        self.student_id = student.pk
        self.averages = [get_average_label(average) for average in averages]
        self.aggregate = get_average_label(aggregate)


class ClassroomReportCard(object):
    def __init__(self, subjects, rows, classroom_averages_by_subject, classroom_average):
        self.subjects = subjects
        self.rows = rows
        self.classroom_averages_by_subject = [get_average_label(average) for average in classroom_averages_by_subject]
        self.classroom_average = get_average_label(classroom_average)

class ClassroomIdBody(AuthenticatedBody):

    def __init__(self, classroom):
        utils = ClassroomIdUtils(classroom)
        self.classroom_id = classroom.pk
        self.classteacher_id = classroom.classTeacher.pk
        self.classteacher_label = get_user_label(classroom.classTeacher)
        self.classroom_label = get_classroom_label(classroom)
        self.uncorrected_assignments = [
            UncorrectedAssignmentRow(uncorrected_assignment, is_active, submissions_received)
            for uncorrected_assignment, is_active, submissions_received
            in utils.get_uncorrected_assignments_with_info()]
        self.corrected_assignments = [TeacherCorrectedAssignmentRow(assignment) for assignment in
                                      utils.get_corrected_assignments()]
        reportcard_subjects = utils.get_contained_room_labels()
        reportcard_rows = [ClassroomReportCardRow(student, averages, aggregate) for
                           student, averages, aggregate in utils.get_reportcard_row_info()]
        classroom_averages_by_subject = utils.get_classroom_averages_by_subject()
        classroom_average = utils.get_classroom_average()
        self.reportcard = ClassroomReportCard(reportcard_subjects, reportcard_rows, classroom_averages_by_subject,
                                              classroom_average)
