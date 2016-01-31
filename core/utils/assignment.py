import django

from core.utils.constants import HWCentralAssignmentType


def is_assignment_active(assignment):
    return assignment.assigned < django.utils.timezone.now()


def is_assignment_corrected(assignment):
    return assignment.due < django.utils.timezone.now()


def get_assignment_type(assignment):
    if not is_assignment_active(assignment):
        return HWCentralAssignmentType.INACTIVE

    if not is_assignment_corrected(assignment):
        return HWCentralAssignmentType.UNCORRECTED

    return HWCentralAssignmentType.CORRECTED