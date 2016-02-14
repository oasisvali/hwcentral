import django
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from core.utils.constants import HWCentralAssignmentType, HWCentralPracticeSubmissionType


def is_assignment_active(assignment):
    return assignment.assigned < django.utils.timezone.now()


def is_assignment_corrected(assignment):
    return assignment.due < django.utils.timezone.now()


def is_practice_assignment(assignment):
    return assignment.content_type == ContentType.objects.get_for_model(User)

def get_assignment_type(assignment):
    if is_practice_assignment(assignment):
        return HWCentralAssignmentType.PRACTICE

    if not is_assignment_active(assignment):
        return HWCentralAssignmentType.INACTIVE

    if not is_assignment_corrected(assignment):
        return HWCentralAssignmentType.UNCORRECTED

    return HWCentralAssignmentType.CORRECTED


def get_practice_submission_type(submission):
    assert is_practice_assignment(submission.assignment)

    if submission.marks is not None:
        return HWCentralPracticeSubmissionType.CORRECTED
    else:
        return HWCentralPracticeSubmissionType.UNCORRECTED
