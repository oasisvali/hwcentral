# contains all the viewodels that contain the data to render hwcentral charts
import django
from django.db.models import Avg, Count

from core.models import Submission, Assignment
from core.utils.view_model import get_user_label, get_date_label, get_fraction_label
from hwcentral.exceptions import InvalidStateException


class PerformanceBreakdownElement(object):
    def __init__(self, student, graded_assignment):
        self.date = get_date_label(graded_assignment.due)

        # TODO: this should support listing multiple topics eventually
        assignment_topic_relation = 'assignmentQuestionsList__questions__chapter__name'
        #WARNING: MAJORLY JANKY STUFF
        topic_prevalence = Assignment.objects.filter(pk=graded_assignment.pk).values(
            assignment_topic_relation).annotate(total=Count(assignment_topic_relation)).order_by('-total')
        self.topic = topic_prevalence[0][assignment_topic_relation]

        self.class_average = get_fraction_label(graded_assignment.average)
        self.student_score = get_fraction_label(
            Submission.objects.get(student=student, assignment=graded_assignment).marks)


class PerformanceBreakdown(object):
    def __init__(self, student, subjectroom):
        self.subject = subjectroom.subject.name
        self.subject_teacher = get_user_label(subjectroom.teacher)
        self.listing = []
        for graded_assignment in Assignment.objects.filter(subjectRoom=subjectroom,
                                                           due__gte=django.utils.timezone.now()).order_by('due'):
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
            self.class_teacher = get_user_label((student.classes_enrolled_set.all()[0]).classTeacher)
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


class SubjectroomPerformanceElement(object):
    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary


# TODO: this might not be the best-designed viewmodel
class SubjectroomPerformance(object):
    def __init__(self, subjectroom):
        self.subject_room = SubjectroomPerformanceElement(subjectroom, adjacent_subjectroom_divisions)
        self.topics = []
        self.subject_teacher = SubjectroomPerformanceElement(subjectroom.teacher, )
        self.listing = SubjectroomPerformanceElement(subjectroom_averages, get_adjacent_subjectroom_divisions)


#TODO: this belongs in a utils package
def get_adjacent_subjectroom_divisions(subjectroom):

