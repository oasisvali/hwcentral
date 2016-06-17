# contains all the viewodels that contain the data to render hwcentral charts
import django
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Q

from core.models import Submission, Assignment, SubjectRoom
from core.utils.json import JSONModel
from core.utils.labels import get_user_label, get_date_label, get_fraction_label, get_subjectroom_label, \
    get_focusroom_label
from focus.models import Remedial
from hwcentral.exceptions import InvalidStateError, InvalidContentTypeError

CHART_CORRECTED_ASSIGNMENTS_LIMIT = 10

class BreakdownElement(JSONModel):
    """
    Abstract class to reduce duplication between breakdown elements for the student and subjectroom bar graphs
    """

    def __init__(self, graded_assignment):
        self.date = get_date_label(graded_assignment.due)
        self.topic = graded_assignment.assignmentQuestionsList.get_title()
        self.subjectroom_average = get_fraction_label(graded_assignment.average)
        self.assignment_id = graded_assignment.pk


class PerformanceBreakdownElement(BreakdownElement):
    def __init__(self, submission):
        super(PerformanceBreakdownElement, self).__init__(submission.assignment)
        self.student_score = get_fraction_label(submission.marks)
        self.student_completion = get_fraction_label(submission.completion)
        self.submission_id = submission.pk


def get_subjectroom_graded_assignments(subjectroom):
    return Assignment.objects.filter(subjectRoom=subjectroom, due__lte=django.utils.timezone.now()).order_by('-due')


def get_focusroom_graded_assignments(focusroom):
    return Assignment.objects.filter(remedial__focusRoom=focusroom, due__lte=django.utils.timezone.now()).order_by(
        '-due')

class PerformanceBreakdown(JSONModel):
    @classmethod
    def for_subjectroom(cls, student, subjectroom):
        submissions = [Submission.objects.get(student=student, assignment=graded_assignment) for graded_assignment in
                       get_subjectroom_graded_assignments(subjectroom)[:CHART_CORRECTED_ASSIGNMENTS_LIMIT]]
        return cls(
                subjectroom.subject.name,
                subjectroom.teacher,
                submissions
        )

    @classmethod
    def for_focusroom(cls, student, focusroom):
        submissions = []
        assert student.userinfo.school.schoolprofile.focus
        for graded_assignment in get_focusroom_graded_assignments(focusroom):
            if student in graded_assignment.content_object.students.all():
                submissions.append(Submission.objects.get(student=student, assignment=graded_assignment))
                if len(submissions) == CHART_CORRECTED_ASSIGNMENTS_LIMIT:
                    break

        return cls(
                get_focusroom_label(focusroom.subjectRoom.subject.name),
                focusroom.subjectRoom.teacher,
                submissions
        )

    def __init__(self, subject, teacher, submissions):
        self.subject = subject
        self.subject_teacher = get_user_label(teacher)
        self.listing = []
        for submission in submissions:
            self.listing.append(PerformanceBreakdownElement(submission))


class PerformanceReportElement(JSONModel):
    @classmethod
    def build_for_focusroom(cls, focusroom, student):
        assert student.userinfo.school.schoolprofile.focus

        # first check if you can calculate an average
        focusroom_graded_assignments = get_focusroom_graded_assignments(focusroom)
        if focusroom_graded_assignments.count() == 0:
            return None  # element cannot exist with no data

        remedial_assignment_pks = []  # the list of assignments for remedials which included the current student
        for graded_assignment in focusroom_graded_assignments:
            if student in graded_assignment.content_object.students.all():
                remedial_assignment_pks.append(graded_assignment.pk)

        if len(remedial_assignment_pks) == 0:
            return None  # current student has never been in a remedial for this focusroom

        focusroom_average = get_fraction_label(
                focusroom_graded_assignments.aggregate(Avg('average'))['average__avg'])

        submissions = Submission.objects.filter(assignment__pk__in=remedial_assignment_pks,
                                                student=student)
        if submissions.count() == 0:
            raise InvalidStateError(
                'No submissions found for student in remedials belonging to focusroom with graded assignments')

        student_average = get_fraction_label(submissions.aggregate(Avg('marks'))['marks__avg'])

        return cls(student_average, focusroom_average, get_focusroom_label(focusroom.subjectRoom.subject.name))

    @classmethod
    def build_for_subjectroom(cls, subjectroom, student):
        # first check if you can calculate an average

        subjectroom_graded_assignments = get_subjectroom_graded_assignments(subjectroom)
        if subjectroom_graded_assignments.count() == 0:
            return None  # element cannot exist with no data

        subjectroom_average = get_fraction_label(
                subjectroom_graded_assignments.aggregate(Avg('average'))['average__avg'])

        # need to evaluate the graded assignments query beforehand because as on 11/15 LIMIT is not supported for IN subquery
        graded_assignment_pks = list(subjectroom_graded_assignments.values_list('pk', flat=True))
        submissions = Submission.objects.filter(assignment__pk__in=graded_assignment_pks,
                                                student=student)
        if submissions.count() == 0:
            raise InvalidStateError('No submissions found for student belonging to subjectroom with graded assignments')

        student_average = get_fraction_label(submissions.aggregate(Avg('marks'))['marks__avg'])

        return cls(student_average, subjectroom_average, subjectroom.subject.name)

    def __init__(self, student_average, room_average, label):
        self.student_average = student_average
        self.room_average = room_average
        self.label = label

class PerformanceReport(JSONModel):
    def __init__(self, student):
        self.class_teacher = get_user_label((student.classes_enrolled_set.get()).classTeacher)
        self.listing = []
        focus = student.userinfo.school.schoolprofile.focus
        for subjectroom in student.subjects_enrolled_set.all():
            elem = PerformanceReportElement.build_for_subjectroom(subjectroom, student)
            if elem is not None:
                self.listing.append(elem)
            if focus:
                elem = PerformanceReportElement.build_for_focusroom(subjectroom.focusroom, student)
                if elem is not None:
                    self.listing.append(elem)


class StudentPerformance(JSONModel):
    def __init__(self, student):
        self.performance_report = PerformanceReport(student)
        self.breakdown_listing = []

        focus = student.userinfo.school.schoolprofile.focus

        for subjectroom in student.subjects_enrolled_set.all():
            self.breakdown_listing.append(PerformanceBreakdown.for_subjectroom(student, subjectroom))
            if focus:
                self.breakdown_listing.append(PerformanceBreakdown.for_focusroom(student, subjectroom.focusroom))


def get_standard_adjacent_assignments(assignment):
    """
    Returns queryset of adjacent assignments (assignments made for the same questions list for the same standard in the same school
    but for diffferent subjectrooms/focusrooms) for the given assignment
    """
    now = django.utils.timezone.now()

    # build the assignment filter
    assignment_filter = Q(assignmentQuestionsList=assignment.assignmentQuestionsList, due__lte=now)

    if assignment.content_type == ContentType.objects.get_for_model(SubjectRoom):
        assignment_filter &= Q(
                subjectRoom__classRoom__school=(assignment.get_subjectroom()).classRoom.school,
                subjectRoom__classRoom__standard=(assignment.get_subjectroom()).classRoom.standard
        )
    elif assignment.content_type == ContentType.objects.get_for_model(Remedial):
        assignment_filter &= Q(
            remedial__focusRoom__subjectRoom__classRoom__school=(assignment.get_subjectroom()).classRoom.school,
            remedial__focusRoom__subjectRoom__classRoom__standard=(assignment.get_subjectroom()).classRoom.standard
        )
    else:
        raise InvalidContentTypeError(assignment.content_type)

    return Assignment.objects.filter(assignment_filter)


def get_standard_average(graded_assignment):
    """
    Calculates the average for all adjacent (same standard,school different division) subjectrooms which have done the
    same Assignment Question List as the one on the graded assignment
    """

    return get_standard_adjacent_assignments(graded_assignment).aggregate(Avg('average'))['average__avg']


class RoomPerformanceBreakdownElement(BreakdownElement):
    def __init__(self, graded_assignment):
        super(RoomPerformanceBreakdownElement, self).__init__(graded_assignment)
        self.standard_average = get_fraction_label(
            get_standard_average(graded_assignment))
        self.subjectroom_completion = get_fraction_label(graded_assignment.completion)


class RoomPerformanceBreakdown(JSONModel):
    @classmethod
    def for_subjectroom(cls, subjectroom):
        return cls(
                get_subjectroom_label(subjectroom),
                subjectroom.teacher,
                get_subjectroom_graded_assignments(subjectroom)
        )

    @classmethod
    def for_focusroom(cls, focusroom):
        return cls(
                get_focusroom_label(get_subjectroom_label(focusroom.subjectRoom)),
                focusroom.subjectRoom.teacher,
                get_focusroom_graded_assignments(focusroom)
        )

    def __init__(self, label, teacher, graded_assignments):
        self.subject_room = label
        self.subject_teacher = get_user_label(teacher)
        self.listing = []

        for graded_assignment in graded_assignments[:CHART_CORRECTED_ASSIGNMENTS_LIMIT]:
            self.listing.append(RoomPerformanceBreakdownElement(graded_assignment))


class AssignmentPerformanceElement(JSONModel):
    def __init__(self, submission):
        self.full_name = get_user_label(submission.student)
        self.score = get_fraction_label(submission.marks)
        self.submission_id = submission.pk


class AssignmentCompletionElement(JSONModel):
    @classmethod
    def build_from_submission(cls, submission):
        return cls(submission.student, submission.completion)

    @classmethod
    def build_shell(cls, student):
        return cls(student, 0.0)

    def __init__(self, student, completion):
        self.full_name = get_user_label(student)
        self.completion = get_fraction_label(completion)

class AnonAssignmentPerformanceElement(JSONModel):
    def __init__(self, submission):
        self.score = get_fraction_label(submission.marks)

