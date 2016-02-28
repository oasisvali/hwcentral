from django.contrib.contenttypes.models import ContentType

from core.models import SubjectRoom
from core.routing.urlnames import UrlNames
from core.utils.admin import AdminUtils
from core.utils.labels import get_datetime_label, get_classroom_label, get_subjectroom_label, get_percentage_label, \
    get_user_label, get_average_label, get_focusroom_label
from core.utils.student import StudentUtils
from core.utils.teacher import TeacherUtils
from core.view_models.base import AuthenticatedBody
from core.view_models.utils import Link
from focus.models import Remedial
from hwcentral.exceptions import InvalidContentTypeError


class AssignmentRowBase(object):
    def __init__(self, assignment):
        if assignment.content_type == ContentType.objects.get_for_model(SubjectRoom):
            self.subject = Link(self.get_subjectroom_label(assignment), UrlNames.SUBJECT_ID.name,
                                (assignment.get_subjectroom()).pk)
        elif assignment.content_type == ContentType.objects.get_for_model(Remedial):
            self.subject = Link(get_focusroom_label(self.get_subjectroom_label(assignment)), UrlNames.FOCUS_ID.name,
                                assignment.content_object.focusRoom.pk)
        else:
            raise InvalidContentTypeError(assignment.content_type)
        self.due = get_datetime_label(assignment.due)

    def get_subjectroom_label(self, assignment):
        raise NotImplementedError("subclass of AssignmentRowBase must implement method get_subjectroom_label")

class StudentSubjectroomLabelMixin(object):
    def get_subjectroom_label(self, assignment):
        return (assignment.get_subjectroom()).subject.name


class TeacherSubjectRoomLabelMixin(object):
    def get_subjectroom_label(self, assignment):
        return get_subjectroom_label(assignment.get_subjectroom())


class CorrectedAssignmentRowBase(AssignmentRowBase):
    def __init__(self, assignment):
        super(CorrectedAssignmentRowBase, self).__init__(assignment)
        self.average = get_percentage_label(assignment.average)
        self.assignment_id = assignment.pk


class PracticeAssignmentRow(object):
    def __init__(self, submission):
        self.title = Link(submission.assignment.get_title(), UrlNames.SUBMISSION_ID.name,
                          submission.pk)
        self.subject = submission.assignment.assignmentQuestionsList.subject.name
        self.completion = Link(get_percentage_label(submission.completion), UrlNames.SUBMISSION_ID.name,
                               submission.pk)
        self.marks = Link(get_average_label(submission.marks), UrlNames.SUBMISSION_ID.name,
                          submission.pk)

class StudentCorrectedAssignmentRow(StudentSubjectroomLabelMixin, CorrectedAssignmentRowBase):
    def __init__(self, submission):
        super(StudentCorrectedAssignmentRow, self).__init__(submission.assignment)
        self.title = Link(submission.assignment.get_title(), UrlNames.SUBMISSION_ID.name,
                          submission.pk)
        self.marks = Link(get_percentage_label(submission.marks), UrlNames.SUBMISSION_ID.name, submission.pk)


class TeacherCorrectedAssignmentRow(TeacherSubjectRoomLabelMixin, CorrectedAssignmentRowBase):
    def __init__(self, assignment):
        super(TeacherCorrectedAssignmentRow, self).__init__(assignment)
        self.title = assignment.get_title()
        self.completion = get_percentage_label(assignment.completion)


class ActiveAssignmentRow(StudentSubjectroomLabelMixin, AssignmentRowBase):  # used by student, parent
    def __init__(self, active_assignment, completion):
        super(ActiveAssignmentRow, self).__init__(active_assignment)
        self.title = Link(active_assignment.get_title(), UrlNames.ASSIGNMENT_ID.name,
                          active_assignment.pk)
        self.completion = Link(get_percentage_label(completion), UrlNames.ASSIGNMENT_ID.name, active_assignment.pk)


class UncorrectedAssignmentRow(TeacherSubjectRoomLabelMixin, AssignmentRowBase):  # used by teacher, admin
    def __init__(self, uncorrected_assignment, is_active, submissions_received):
        super(UncorrectedAssignmentRow, self).__init__(uncorrected_assignment)
        self.title = Link(uncorrected_assignment.get_title(), UrlNames.ASSIGNMENT_ID.name,
                          uncorrected_assignment.pk)
        self.opens = get_datetime_label(uncorrected_assignment.assigned)
        self.submissions_received = get_percentage_label(submissions_received)
        self.is_active = is_active
        self.assignment_id = uncorrected_assignment.pk


class ClassroomsTableSubRow(object):
    def __init__(self, link, subjectteacher, average):
        # TODO: rename name to link
        self.name = link
        self.subjectteacher = get_user_label(subjectteacher)
        self.average = get_average_label(average)
        self.id = subjectteacher.pk


class ClassroomsTableFocusroomRow(ClassroomsTableSubRow):
    def __init__(self, focusroom, average):
        super(ClassroomsTableFocusroomRow, self).__init__(
                Link(get_focusroom_label(focusroom.subjectRoom.subject.name), UrlNames.FOCUS_ID.name, focusroom.pk),
                focusroom.subjectRoom.teacher,
                average
        )


class ClassroomsTableSubjectroomRow(ClassroomsTableSubRow):
    def __init__(self, subjectroom, average):
        super(ClassroomsTableSubjectroomRow, self).__init__(
                Link(subjectroom.subject.name, UrlNames.SUBJECT_ID.name, subjectroom.pk),
                subjectroom.teacher,
                average
        )


class ClassroomsTableClassroomRow(object):
    def __init__(self, classroom, subjectroom_rows):
        self.classroom = get_classroom_label(classroom)
        self.classteacher = get_user_label(classroom.classTeacher)
        self.subjectroom_rows = subjectroom_rows


class ClassroomsTable(object):
    def __init__(self, admin, classroom_rows):
        self.school_name = admin.userinfo.school.name
        self.classroom_rows = classroom_rows

class HomeBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the home views
    """
    pass


class StudentHomeBody(HomeBody):

    def __init__(self, user):
        utils = StudentUtils(user)
        self.username = user.username  # used as suffix on the id for the active assignments table
        self.active_assignments = [ActiveAssignmentRow(active_assignment, completion) for active_assignment, completion
                                   in utils.get_active_assignments_with_completion()]
        self.corrected_assignments = [StudentCorrectedAssignmentRow(submission) for submission in
                                      utils.get_corrected_submissions()]
        self.practice_assignments = [PracticeAssignmentRow(submission) for submission in
                                     utils.get_practice_submissions()]


class TeacherHomeBody(HomeBody):
    def __init__(self, user):
        utils = TeacherUtils(user)
        self.uncorrected_assignments = [
            UncorrectedAssignmentRow(uncorrected_assignment, is_active, submissions_received)
            for uncorrected_assignment, is_active, submissions_received
            in utils.get_uncorrected_assignments_with_info()]
        self.corrected_assignments = [TeacherCorrectedAssignmentRow(assignment) for assignment in
                                      utils.get_corrected_assignments()]


class ChildHomeBody(HomeBody):
    def __init__(self, child):
        super(ChildHomeBody, self).__init__()
        self.name = get_user_label(child)
        self.child_id = child.pk


class ParentHomeBody(HomeBody):

    def __init__(self, user):
        self.child_home_bodies = []
        for child in user.home.children.all():
            self.child_home_bodies.append(ChildHomeBody(child))


class AdminHomeBody(HomeBody):

    def __init__(self, user):
        utils = AdminUtils(user)
        self.classrooms_table = ClassroomsTable(user, utils.get_classrooms_table_classroom_rows())
