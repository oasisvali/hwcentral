import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

from core.models import Assignment, Submission, Announcement, School, ClassRoom, SubjectRoom
from core.modules.constants import HWCentralGroup


# TODO: refactor into a class with user-type assertion on creation so you dont have to do it all the time

# Constants for limiting data returned
MAX_UNFINISHED_ASSIGNMENTS = 10
MAX_GRADED_SUBMISSIONS = 10
MAX_ANNOUNCEMENTS = 10


def get_num_unfinished_assignments(user):
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    # check if 100% submissions have been posted for each assignment
    unfinished_assignments = 0
    for assignment in get_list_active_assignments(user):
        if Submission.objects.filter(assignment=assignment).filter(student=user).filter(completion=1).count() == 0:
            unfinished_assignments += 1
    return unfinished_assignments


def get_list_active_assignments(user):
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    # build a list of all assignments - TODO: this might be possible to do in a single query
    assignments = []
    for subject in user.subjects_enrolled_set.all():
        assignments.extend(
            list(Assignment.objects.filter(subjectRoom=subject).filter(due__gte=datetime.datetime.now())))

    return assignments


def get_list_unfinished_assignments(user, limit=MAX_UNFINISHED_ASSIGNMENTS, offset=0):
    """
    The list is sorted in increasing order of time-to-due date. submission completion value is attached to the assignment objects.
    @param user: The user for whom the assignments list is required. Must be a student
    """
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    unfinished_assignments = []
    # NOTE: must first get ALL assignments across subjects so that cumulative chronological list can be made
    for assignment in get_list_active_assignments(user):
        best_submission = \
        Submission.objects.filter(assignment=assignment).filter(student=user).order_by('-completion')[:1][
            0]  # dont know if slicing is reqd
        if best_submission.completion != 1:
            assignment.completion = best_submission.completion * 100
            unfinished_assignments.append(assignment)

    # sort and page
    return sorted(unfinished_assignments, key=lambda assignment: assignment.due, reverse=True)[offset:limit]


def get_list_graded_submissions(user, limit=MAX_GRADED_SUBMISSIONS, offset=0):
    """
    The list is sorted in increasing order of time-to-graded date
    @param user: The user for whom the submissions list is required. Must be a student
    """
    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    # marks not null means it is a graded submission
    return list(
        Submission.objects.filter(student=user).filter(marks__isnull=False).order_by('-assignment__due')[offset:limit])


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
    Generates a performance report which is a list of (subject, user_avg, class_avg) tuples for each subject
    @param user: The user for whom the performance report is being generated. Must be a student
    """

    assert user.userinfo.group.pk == HWCentralGroup.STUDENT

    report = []
    for subject in user.subjects_enrolled_set.all():
        # get user average in this subject - TODO:This logic means you will need to create shell submissions
        # when there are none at all - do this when assignments are 'marked'
        user_avg = Submission.objects.filter(student=user).filter(assignment__subjectRoom=subject).filter(
            marks__isnull=False).aggregate(Avg('marks'))['marks__avg']
        # get class average in this subject
        class_avg = \
        Submission.objects.filter(assignment__subjectRoom=subject).filter(marks__isnull=False).aggregate(Avg('marks'))[
            'marks__avg']
        report.append((subject.subject.name, user_avg, class_avg))

    return report

