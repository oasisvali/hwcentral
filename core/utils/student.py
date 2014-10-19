from collections import defaultdict, namedtuple
import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

from core.models import Assignment, Submission, Announcement, School, ClassRoom, SubjectRoom
from core.utils.constants import HWCentralGroup



# TODO: refactor into a class with user-type assertion on creation so you dont have to do it all the time

# Constants for limiting data returned
MAX_UNFINISHED_ASSIGNMENTS = 10
MAX_GRADED_SUBMISSIONS = 10
MAX_ANNOUNCEMENTS = 10

# TODO: apply limit at this level too?
def get_list_active_assignments(user):
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    # build a list of all assignments - TODO: this might be possible to do in a single query
    assignments = []
    for subject in user.subjects_enrolled_set.all():
        assignments.extend(
            list(Assignment.objects.filter(subjectRoom=subject).filter(due__gte=datetime.datetime.now())))

    return assignments


def get_num_unfinished_assignments(user):
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    # check if 100% submissions have been posted for each assignment
    unfinished_assignments = 0
    for assignment in get_list_active_assignments(user):
        if Submission.objects.filter(assignment=assignment).filter(student=user).filter(completion=1).count() == 0:
            unfinished_assignments += 1
    return unfinished_assignments


def pick_unfinished_assignments(active_assignments, user, limit, offset):
    """
    Implements the logic which determines which of the given active assignments are still unfinished. Also sorts, limits
    and offsets the result.
    @param active_assignments: list of assignments which are still active = due date is in the future
    """

    unfinished_assignments = []

    for assignment in active_assignments:
        best_submission = \
            Submission.objects.filter(assignment=assignment).filter(student=user).order_by('-completion')[:1][
                0]  # dont know if slicing is reqd
        if best_submission.completion != 1:
            assignment.completion = best_submission.completion * 100
            unfinished_assignments.append(assignment)

    # sort and page
    return sorted(unfinished_assignments, key=lambda assignment: assignment.due, reverse=True)[offset:limit]


def get_list_unfinished_assignments_by_subject(user, subject_id, limit=None, offset=0):
    """
    The list is sorted in increasing order of time-to-due date. submission completion value is attached to the
    assignment objects. Returns ALL unfinished assignments if Limit is not specified.
    @param user: The user for whom the assignments list is required. Must be a student
    @param subject_id: The subject for which the assignments are to be listed
    """
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    # first build list of all active assignments for this subject
    active_assignments = Assignment.objects.filter(subjectRoom__pk=subject_id).filter(due__gte=datetime.datetime.now())

    return pick_unfinished_assignments(active_assignments, user, limit, offset)


def get_list_unfinished_assignments(user, limit=MAX_UNFINISHED_ASSIGNMENTS, offset=0):
    """
    The list is sorted in increasing order of time-to-due date. submission completion value is attached to the assignment objects.
    @param user: The user for whom the assignments list is required. Must be a student
    """
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    unfinished_assignments = []
    # NOTE: must first get ALL assignments across subjects so that cumulative chronological list can be made
    active_assignments = get_list_active_assignments(user)

    return pick_unfinished_assignments(active_assignments, user, limit, offset)


def get_list_graded_submissions_by_subject(user, subject_id, limit=None, offset=0):
    """
    The list is sorted in increasing order of time-to-graded date Returns ALL graded submissions for the user for the
    given subject if limit is not specified
    @param user: The user for whom the submissions list is required. Must be a student
    """
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    # marks not null means it is a graded submission
    return list(
        Submission.objects.filter(student=user).filter(assignment__subjectRoom__pk=subject_id)
        .filter(marks__isnull=False).order_by('-assignment__due')[offset:limit])


def get_list_graded_submissions(user, limit=MAX_GRADED_SUBMISSIONS, offset=0):
    """
    The list is sorted in increasing order of time-to-graded date
    @param user: The user for whom the submissions list is required. Must be a student
    """
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    # marks not null means it is a graded submission
    return list(
        Submission.objects.filter(student=user).filter(marks__isnull=False).order_by('-assignment__due')[offset:limit])


def get_list_announcements_by_subject(subject_id, limit=None, offset=0):
    """
    The list is sorted in most-recent to least-recent order. Returns ALL announcements for a subject if limit is not
    specified.
    @param subject_id: The subject for whom the relevant announcements are required
    """

    announcements = Announcement.objects.filter(content_type=ContentType.objects.get_for_model(SubjectRoom),
                                                object_id=subject_id)

    # sort and page
    return sorted(announcements, key=lambda announcement: announcement.timestamp, reverse=True)[offset:limit]


def get_list_announcements(user, limit=MAX_ANNOUNCEMENTS, offset=0):
    """
    The list is sorted in most-recent to least-recent order
    @param user: The user for whom the relevant announcements are required
    """

    # right now only supporting student
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    announcements = []

    # get announcements for this school
    announcements.extend(Announcement.objects.filter(content_type=ContentType.objects.get_for_model(School),
                                                     object_id=user.userinfo.school.pk))
    # get announcements for this class
    for classRoom in user.classes_enrolled_set.all():
        announcements.extend(Announcement.objects.filter(content_type=ContentType.objects.get_for_model(ClassRoom),
                                                         object_id=classRoom.pk))
    # get announcements for all subjects
    for subject in user.subjects_enrolled_set.all():
        announcements.extend(Announcement.objects.filter(content_type=ContentType.objects.get_for_model(SubjectRoom),
                                                         object_id=subject.pk))

    # sort and page
    return sorted(announcements, key=lambda announcement: announcement.timestamp, reverse=True)[offset:limit]


def get_performance_report(user):
    """
    Generates a performance report which is a list of (subject, user_avg, class_avg) namedtuples for each subject
    @param user: The user for whom the performance report is being generated. Must be a student
    """

    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    report = []
    Metric = namedtuple('Metric', 'subject_name user_avg class_avg')
    for subject in user.subjects_enrolled_set.all():
        # get user average in this subject - TODO:This logic means you will need to create shell submissions
        # when there are none at all - do this when assignments are 'marked'
        user_avg = Submission.objects.filter(student=user).filter(assignment__subjectRoom=subject).filter(
            marks__isnull=False).aggregate(Avg('marks'))['marks__avg']
        # get class average in this subject
        class_avg = \
        Submission.objects.filter(assignment__subjectRoom=subject).filter(marks__isnull=False).aggregate(Avg('marks'))[
            'marks__avg']
        report.append(Metric(subject.subject.name, user_avg, class_avg))

    return report


def get_performance_report_by_subject(user, subject_id):
    """
    Generates a performance report which is a list of (chapter, user_avg, class_avg) tuples for each chapter
    @param user: The user for whom the performance report is being generated. Must be a student
    @param subject_id: The subject for which the performance report is being generated
    """

    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    report = defaultdict(lambda: [0, 0])
    Metric = namedtuple('Metric', 'chapter_name', 'user_avg', 'class_avg')
    # for each graded submission, check the set of chapters it addresses
    for submission in Submission.objects.filter(student=user).filter(assignment__subjectRoom__pk=subject_id) \
            .filter(marks__isnull=False):
        for chapter in submission.assignment.questions.values('chapter').distinct():
            chapter_name = chapter['chapter'].name
            report[chapter_name][0] += submission.marks
            report[chapter_name][1] += 1

    return [Metric(chap) for chapter_name, chapter_data in]

