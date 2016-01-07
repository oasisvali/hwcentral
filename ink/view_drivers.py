from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from core.utils.references import HWCentralGroup
from ink.urlnames import InkUrlNames


class ParentIdBase(object):
    def __init__(self, student_id):
        student = get_object_or_404(User, pk=student_id)
        if student.userinfo.group != HWCentralGroup.refs.STUDENT:
            raise Http404
        self.student = student
        self.template = InkUrlNames.PARENT_ID.template

class ParentIdGet(ParentIdBase):
    def handle(self):
        return render(request, )


