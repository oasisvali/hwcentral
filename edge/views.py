from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from core.models import SubjectRoom
from core.utils.json import Json404Response
from core.utils.references import HWCentralGroup
from core.utils.user_checks import is_subjectroom_student_relationship
from edge.view_drivers import IndexGet, SubjectIdGet, StudentIdGet


@login_required
def index_get(request):
    return IndexGet(request).handle()


@login_required
def subject_id_get(request, subjectroom_id):
    try:
        subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)
    except Http404, e:
        return Json404Response(e)
    return SubjectIdGet(request, subjectroom).handle()


@login_required
def student_id_get(request, student_id, subjectroom_id):
    try:
        student = get_object_or_404(User, pk=student_id)
        if student.userinfo.group != HWCentralGroup.refs.STUDENT:
            raise Http404

        subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)
        if not is_subjectroom_student_relationship(subjectroom, student):
            raise Http404
    except Http404, e:
        return Json404Response(e)
    return StudentIdGet(request, student, subjectroom).handle()
