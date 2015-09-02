import django
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from core.models import Assignment, Submission, Announcement, School, ClassRoom, SubjectRoom


# Constants for limiting data returned
from core.utils.references import HWCentralGroup

MAX_UNFINISHED_ASSIGNMENTS = 10
MAX_GRADED_SUBMISSIONS = 10
MAX_ANNOUNCEMENTS = 10


class StudentUtils(object):
    def __init__(self, student):
        assert student.userinfo.group == HWCentralGroup.refs.STUDENT
        self.student = student

    def get_num_unfinished_assignments(self):
        # check if 100% submissions have been posted for each assignment
        num_unfinished_assignments = 0
        for assignment in self.get_active_assignments():
            try:
                submission = Submission.objects.get(assignment=assignment, student=self.student)
                if submission.completion < 1:
                    num_unfinished_assignments += 1
            except Submission.DoesNotExist:
                num_unfinished_assignments += 1

        return num_unfinished_assignments

    def get_enrolled_subjectroom_ids(self):
        return self.student.subjects_enrolled_set.values_list('pk', flat=True)

    def get_active_assignments(self):
        now = django.utils.timezone.now()
        student_subjectroom_ids = self.get_enrolled_subjectroom_ids()

        return Assignment.objects.filter(subjectRoom__pk__in=student_subjectroom_ids, due__gte=now,
                                         assigned__lte=now).order_by('-due')

    def get_announcements(self):
        school_type = ContentType.objects.get_for_model(School)
        classroom_type = ContentType.objects.get_for_model(ClassRoom)
        subjectroom_type = ContentType.objects.get_for_model(SubjectRoom)
        student_subjectroom_ids = self.get_enrolled_subjectroom_ids()

        query = (Q(content_type=school_type, object_id=self.student.userinfo.school.pk) |
                 Q(content_type=classroom_type, object_id=self.student.classes_enrolled_set.get().pk) |
                 Q(content_type=subjectroom_type, object_id__in=student_subjectroom_ids))

        return Announcement.objects.filter(query).order_by('-timestamp')

    def get_active_assignments_with_completion(self):
        result = []
        for active_assignment in self.get_active_assignments():
            try:
                submission = Submission.objects.get(student=self.student, assignment=active_assignment)
                completion = submission.completion
            except Submission.DoesNotExist:
                completion = 0.0
            result.append((active_assignment, completion))
        return result

    def get_corrected_submissions(self):
        now = django.utils.timezone.now()
        return Submission.objects.filter(student=self.student, assignment__due__lte=now).order_by('-assignment__due')


def get_list_unfinished_assignments_by_subject(user, subject_id, limit=None, offset=0):
    """
    The list is sorted in increasing order of time-to-due date. submission completion value is attached to the
    assignment objects. Returns ALL unfinished assignments if Limit is not specified.
    @param user: The user for whom the assignments list is required. Must be a student
    @param subject_id: The subject for which the assignments are to be listed
    """
    assert user.userinfo.group == HWCentralGroup.refs.STUDENT

    # first build list of all active assignments for this subject
    active_assignments = Assignment.objects.filter(subjectRoom__pk=subject_id).filter(
        due__gte=django.utils.timezone.now())

    return pick_unfinished_assignments(active_assignments, user, limit, offset)


def get_list_unfinished_assignments(user, limit=MAX_UNFINISHED_ASSIGNMENTS, offset=0):
    """
    The list is sorted in increasing order of time-to-due date. submission completion value is attached to the assignment objects.
    @param user: The user for whom the assignments list is required. Must be a student
    @param limit: Used for paging through results. If set to None, all unfinished assignments are returned
    """
    assert user.userinfo.group == HWCentralGroup.refs.STUDENT

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
    assert user.userinfo.group == HWCentralGroup.refs.STUDENT

    # marks not null means it is a graded submission
    return list(
        Submission.objects.filter(student=user, assignment__subjectRoom__pk=subject_id, marks__isnull=False)
        .order_by('-assignment__due')[offset:limit])


def get_list_graded_submissions(user, limit=MAX_GRADED_SUBMISSIONS, offset=0):
    """
    The list is sorted in increasing order of time-to-graded date
    @param user: The user for whom the submissions list is required. Must be a student
    """
    assert user.userinfo.group == HWCentralGroup.refs.STUDENT

    # marks not null means it is a graded submission
    return list(
        Submission.objects.filter(student=user, marks__isnull=False).order_by('-assignment__due')[offset:limit])


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
