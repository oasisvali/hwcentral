from django.http import Http404

from core.utils.references import HWCentralGroup


def check_student(student):
    """
    Checks if object passed in is a student user, otherwise raises 404
    """
    if student.userinfo.group != HWCentralGroup.refs.STUDENT:
        raise Http404


def check_subjectteacher(subjectteacher):
    """
    Checks if object passed in is a subjectteacher user, otherwise raises 404
    """
    if subjectteacher.userinfo.group != HWCentralGroup.refs.TEACHER or subjectteacher.subjects_managed_set.count() == 0:
        raise Http404


def check_classteacher(classteacher):
    """
    Checks if object passed in is a classteacher user, otherwise raises 404
    """
    if classteacher.userinfo.group != HWCentralGroup.refs.TEACHER or classteacher.classes_managed_set.count() == 0:
        raise Http404
