# contains all the viewodels that contain the data to render hwcentral charts
import django
from django.db.models import Avg, Count

from core.models import Submission, Assignment
from core.utils.view_model import get_user_label, get_date_label, get_fraction_label, get_subjectroom_label
from hwcentral.exceptions import InvalidStateException


class BreakdownElement(object):
    """
    Abstract class to reduce duplication between breakdown elements for the student and subjectroom line graphs
    """

    def __init__(self, graded_assignment):
        self.date = get_date_label(graded_assignment.due)

        # TODO: this should support listing multiple topics eventually
        assignment_topic_relation = 'assignmentQuestionsList__questions__chapter__name'
        #WARNING: MAJORLY JANKY STUFF
        topic_prevalence = Assignment.objects.filter(pk=graded_assignment.pk).values(
            assignment_topic_relation).annotate(total=Count(assignment_topic_relation)).order_by('-total')
        self.topic = topic_prevalence[0][assignment_topic_relation]

        self.class_average = get_fraction_label(graded_assignment.average)


class PerformanceBreakdownElement(BreakdownElement):
    def __init__(self, student, graded_assignment):
        super(PerformanceBreakdownElement, self).__init__(graded_assignment)
        self.student_score = get_fraction_label(
            Submission.objects.get(student=student, assignment=graded_assignment).marks)


def get_subjectroom_graded_assignments(subjectroom):
    return Assignment.objects.filter(subjectRoom=subjectroom, due__gte=django.utils.timezone.now()).order_by('due')


class PerformanceBreakdown(object):
    def __init__(self, student, subjectroom):
        self.subject = subjectroom.subject.name
        self.subject_teacher = get_user_label(subjectroom.teacher)
        self.listing = []
        for graded_assignment in get_subjectroom_graded_assignments(subjectroom):
            self.listing.append(PerformanceBreakdownElement(student, graded_assignment))


class PerformanceReportElement(object):
    def __init__(self, student, subjectroom):
        self.subject = subjectroom.subject.name
        self.student_average = get_fraction_label(
            Submission.objects.filter(assignment__subjectRoom=subjectroom, marks__isnull=False).aggregate(Avg('marks'))[
                'marks__avg'])
        self.class_average = get_fraction_label(
            Assignment.objects.filter(subjectRoom=subjectroom, due__gte=django.utils.timezone.now()).aggregate(
                Avg('average'))['average__avg'])


class PerformanceReport(object):
    def __init__(self, student, subjectrooms):
        try:
            self.class_teacher = get_user_label((student.classes_enrolled_set.get()).classTeacher)
        except IndexError:
            raise InvalidStateException("Student %s isn't enrolled in any classes" % student.username)
        self.listing = []
        for subjectroom in subjectrooms:
            self.listing.append(PerformanceReportElement(student, subjectroom))


class StudentPerformance(object):
    def __init__(self, student):
        subjectrooms = list(student.subjects_enrolled_set.all())

        self.performance_report = PerformanceReport(student, subjectrooms)
        self.breakdown_listing = []

        for subjectroom in subjectrooms:
            self.breakdown_listing.append(PerformanceBreakdown(student, subjectroom))


def get_adjacent_average(graded_assignment, subjectroom):


# first find all assignments for same questionslist that were ass


class SubjectroomPerformanceBreakdownElement(BreakdownElement):
    def __init__(self, graded_assignment, subjectroom):
        super(SubjectroomPerformanceBreakdownElement, self).__init__(graded_assignment)
        self.adjacent_average = get_fraction_label(
            get_adjacent_average(graded_assignment, subjectroom))


class SubjectroomPerformanceBreakdown(object):
    def __init__(self, subjectroom):
        self.subject_room = get_subjectroom_label(subjectroom)
        self.subject_teacher = get_user_label(subjectroom.teacher)
        self.listing = []

        for graded_assignment in get_subjectroom_graded_assignments(subjectroom):
            self.listing.append(SubjectroomPerformanceBreakdownElement(graded_assignment, subjectroom))

