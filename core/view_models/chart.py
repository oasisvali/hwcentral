# contains all the viewodels that contain the data to render hwcentral charts
import django
from django.db.models import Avg

from core.models import Submission, Assignment
from core.utils.json import JSONModel
from core.utils.labels import get_user_label, get_date_label, get_fraction_label, get_subjectroom_label

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
    def __init__(self, student, graded_assignment):
        super(PerformanceBreakdownElement, self).__init__(graded_assignment)
        # submission object should exist for all students that have graded assignments
        submission = Submission.objects.get(student=student, assignment=graded_assignment)
        self.student_score = get_fraction_label(submission.marks)
        self.submission_id = submission.pk


def get_subjectroom_graded_assignments(subjectroom):
    return Assignment.objects.filter(subjectRoom=subjectroom, due__lte=django.utils.timezone.now()).order_by('due')[:CHART_CORRECTED_ASSIGNMENTS_LIMIT]


class PerformanceBreakdown(JSONModel):
    def __init__(self, student, subjectroom):
        self.subject = subjectroom.subject.name
        self.subject_teacher = get_user_label(subjectroom.teacher)
        self.listing = []
        for graded_assignment in get_subjectroom_graded_assignments(subjectroom):
            self.listing.append(PerformanceBreakdownElement(student, graded_assignment))


class PerformanceReportElement(JSONModel):
    @classmethod
    def build_for_subjectroom(cls, subjectroom, student):
        # first check if you can calculate an average

        subjectroom_graded_assignments = get_subjectroom_graded_assignments(subjectroom)
        subjectroom_average = None
        if subjectroom_graded_assignments.count() > 0:
            subjectroom_average = get_fraction_label(
                subjectroom_graded_assignments.aggregate(Avg('average'))['average__avg'])
        else:
            return None  # element cannot exist with no data

        student_average = None

        # need to evaluate the graded assignments query beforehand because as on 11/15 LIMIT is not supported for IN subquery
        graded_assignment_pks = list(subjectroom_graded_assignments.values_list('pk', flat=True))
        submissions = Submission.objects.filter(assignment__pk__in=graded_assignment_pks,
                                                assignment__due__lte=django.utils.timezone.now(), student=student)
        if submissions.count() > 0:
            student_average = get_fraction_label(submissions.aggregate(Avg('marks'))['marks__avg'])
        else:
            return None  # element cannot exist if no data

        return cls(student_average, subjectroom_average, subjectroom)

    def __init__(self, student_average, subjectroom_average, subjectroom):
        self.student_average = student_average
        self.subjectroom_average = subjectroom_average
        self.subjectroom_id = subjectroom.pk
        self.subject = subjectroom.subject.name

class PerformanceReport(JSONModel):
    def __init__(self, student, subjectrooms):
        self.class_teacher = get_user_label((student.classes_enrolled_set.get()).classTeacher)
        self.listing = []
        for subjectroom in subjectrooms:
            elem = PerformanceReportElement.build_for_subjectroom(subjectroom, student)
            if elem is not None:
                self.listing.append(elem)


class StudentPerformance(JSONModel):
    def __init__(self, student):
        subjectrooms = list(student.subjects_enrolled_set.all())

        self.performance_report = PerformanceReport(student, subjectrooms)
        self.breakdown_listing = []

        for subjectroom in subjectrooms:
            self.breakdown_listing.append(PerformanceBreakdown(student, subjectroom))


def get_standard_adjacent_assignments(assignment):
    """
    Returns queryset of adjacent assignments (assignments made for the same questions list for the same standard in the same school
    but for diffferent subjectrooms) for the given assignment
    """
    return Assignment.objects.filter(assignmentQuestionsList=assignment.assignmentQuestionsList,
                                     subjectRoom__classRoom__school=assignment.subjectRoom.classRoom.school,
                                     subjectRoom__classRoom__standard=assignment.subjectRoom.classRoom.standard,
                                     due__lte=django.utils.timezone.now())


def get_standard_average(graded_assignment):
    """
    Calculates the average for all adjacent (same standard,school different division) subjectrooms which have done the
    same Assignment Question List as the one on the graded assignment
    """

    return get_standard_adjacent_assignments(graded_assignment).aggregate(Avg('average'))['average__avg']


class SubjectroomPerformanceBreakdownElement(BreakdownElement):
    def __init__(self, graded_assignment):
        super(SubjectroomPerformanceBreakdownElement, self).__init__(graded_assignment)
        self.standard_average = get_fraction_label(
            get_standard_average(graded_assignment))


class SubjectroomPerformanceBreakdown(JSONModel):
    def __init__(self, subjectroom):
        self.subject_room = get_subjectroom_label(subjectroom)
        self.subject_teacher = get_user_label(subjectroom.teacher)
        self.listing = []

        for graded_assignment in get_subjectroom_graded_assignments(subjectroom):
            self.listing.append(SubjectroomPerformanceBreakdownElement(graded_assignment))


class AssignmentPerformanceElement(JSONModel):
    def __init__(self, submission):
        self.full_name = get_user_label(submission.student)
        self.score = get_fraction_label(submission.marks)
        self.submission_id = submission.pk


class AnonAssignmentPerformanceElement(JSONModel):
    def __init__(self, submission):
        self.score = get_fraction_label(submission.marks)

