from datadog import statsd
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
@statsd.timed('edge.get.index')
def index_get(request):
    statsd.increment('edge.hits.get.index')
    return IndexGet(request).handle()


@login_required
@statsd.timed('edge.get.subject_id')
def subject_id_get(request, subjectroom_id):
    statsd.increment('edge.hits.get.subject_id')
    try:
        subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)
    except Http404, e:
        return Json404Response(e)
    return SubjectIdGet(request, subjectroom).handle()


@login_required
@statsd.timed('edge.get.student_id')
def student_id_get(request, student_id, subjectroom_id):
    statsd.increment('edge.hits.get.student_id')
    try:
        student = get_object_or_404(User, pk=student_id)
        if student.userinfo.group != HWCentralGroup.refs.STUDENT and student.userinfo.group != HWCentralGroup.refs.OPEN_STUDENT:
            raise Http404

        subjectroom = get_object_or_404(SubjectRoom, pk=subjectroom_id)
        if not is_subjectroom_student_relationship(subjectroom, student):
            raise Http404
    except Http404, e:
        return Json404Response(e)
    return StudentIdGet(request, student, subjectroom).handle()
