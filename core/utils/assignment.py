import django
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from core.models import SubjectRoom
from core.utils.constants import HWCentralAssignmentType, HWCentralStudentAssignmentSubmissionType
from core.utils.references import HWCentralGroup, HWCentralOpen
from focus.models import Remedial
from hwcentral.exceptions import InvalidStateError, InvalidContentTypeError


def is_assignment_active(assignment):
    return assignment.assigned < django.utils.timezone.now()


def is_assignment_corrected(assignment):
    return assignment.due < django.utils.timezone.now()

def get_assignment_type(assignment):
    if is_open_assignment(assignment):
        return HWCentralAssignmentType.OPEN

    if is_practice_assignment(assignment):
        return HWCentralAssignmentType.PRACTICE

    if not is_assignment_active(assignment):
        return HWCentralAssignmentType.INACTIVE

    if not is_assignment_corrected(assignment):
        return HWCentralAssignmentType.UNCORRECTED

    return HWCentralAssignmentType.CORRECTED


def is_student_assignment(assignment):
    return assignment.content_type == ContentType.objects.get_for_model(User)


def is_practice_assignment(assignment):
    return is_student_assignment(assignment) and (
    assignment.content_object.userinfo.group == HWCentralGroup.refs.STUDENT)


def is_corrected_practice_assignment(assignment):
    return is_practice_assignment(assignment) and (assignment.marks is not None)


def is_open_assignment(assignment):
    return is_student_assignment(assignment) and (
    assignment.content_object.userinfo.group == HWCentralGroup.refs.OPEN_STUDENT)


def is_corrected_open_assignment(assignment):
    return is_open_assignment(assignment) and (assignment.marks is not None)


def get_student_assignment_submission_type(submission):
    assert is_student_assignment(submission.assignment)

    if (submission.marks is not None) and (submission.assignment.average is not None):
        return HWCentralStudentAssignmentSubmissionType.CORRECTED
    elif (submission.marks is None) and (submission.assignment.average is None):
        return HWCentralStudentAssignmentSubmissionType.UNCORRECTED
    else:
        raise InvalidStateError(
            "Student Assignment Submission %s has only one of marks and assignment average non null" % submission)


def check_homework_assignment(assignment):
    """
    checks that the given assignment is homework for a subjectroom or remedial
    """
    if assignment.content_type == ContentType.objects.get_for_model(User):
        raise InvalidStateError("Practice/Open assignment is not a homework assignment.")
    elif (assignment.content_type != ContentType.objects.get_for_model(Remedial)) and (
                assignment.content_type != ContentType.objects.get_for_model(SubjectRoom)):
        raise InvalidContentTypeError(assignment.content_type)


def get_open_assignment_subjectroom(assignment):
    assert is_open_assignment(assignment)

    return HWCentralOpen.refs.SUBJECTROOMS.get(subject=assignment.assignmentQuestionsList.subject)
