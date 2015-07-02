# contains all the viewodels that contain the data to render hwcentral charts
import django
from django.db.models import Avg, Count

from core.models import Submission, Assignment, Chapter
from core.utils.labels import get_user_label, get_date_label, get_fraction_label, get_subjectroom_label
from hwcentral.exceptions import InvalidStateException


class BreakdownElement(object):
    """
    Abstract class to reduce duplication between breakdown elements for the student and subjectroom line graphs
    """

    def __init__(self, graded_assignment):
        self.date = get_date_label(graded_assignment.due)
        topic_prevalence = graded_assignment.assignmentQuestionsList.questions.values('chapter').annotate(
            total=Count('chapter'))
        if len(topic_prevalence) != 1:
            raise InvalidStateException(
                'More than 1 chapter covered by questions of assignment: %s' % graded_assignment)
        self.topic = Chapter.objects.get(pk=(topic_prevalence[0]['chapter'])).name
        self.subjectroom_average = get_fraction_label(graded_assignment.average)


class PerformanceBreakdownElement(BreakdownElement):
    def __init__(self, student, graded_assignment):
        super(PerformanceBreakdownElement, self).__init__(graded_assignment)
        self.student_score = get_fraction_label(
            Submission.objects.get(student=student, assignment=graded_assignment).marks)


def get_subjectroom_graded_assignments(subjectroom):
    return Assignment.objects.filter(subjectRoom=subjectroom, due__lte=django.utils.timezone.now()).order_by('due')


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
        self.class_average = get_fraction_label(get_subjectroom_graded_assignments(subjectroom).aggregate(
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


<<<<<<< HEAD
#def get_adjacent_average(graded_assignment, subjectroom):
=======
def get_adjacent_average(graded_assignment, subjectroom):
    """
    Calculates the average for all adjacent (same standard,school different division) subjectrooms which have done the
    same Assignment Question List as the one on the graded assignment
    """
>>>>>>> 4f8326fd5c3649b590fdc34df3822c7bc74fe99e

    return Assignment.objects.filter(assignmentQuestionsList=graded_assignment.assignmentQuestionsList,
                                     subjectRoom__classRoom__school=graded_assignment.subjectRoom.classRoom.school,
                                     subjectRoom__classRoom__standard=graded_assignment.subjectRoom.classRoom.standard,
                                     due__lte=django.utils.timezone.now()).aggregate(Avg('average'))['average__avg']


class SubjectroomPerformanceBreakdownElement(BreakdownElement):
    def __init__(self, graded_assignment, subjectroom):
        super(SubjectroomPerformanceBreakdownElement, self).__init__(graded_assignment)
        self.classroom_average = get_fraction_label(
            get_adjacent_average(graded_assignment, subjectroom))


class SubjectroomPerformanceBreakdown(object):
    def __init__(self, subjectroom):
        self.subject_room = get_subjectroom_label(subjectroom)
        self.subject_teacher = get_user_label(subjectroom.teacher)
        self.listing = []

        for graded_assignment in get_subjectroom_graded_assignments(subjectroom):
            self.listing.append(SubjectroomPerformanceBreakdownElement(graded_assignment, subjectroom))


class AssignmentPerformanceElement(object):
    def __init__(self, submission):
        self.full_name = get_user_label(submission.student)
        self.score = get_fraction_label(submission.marks)

