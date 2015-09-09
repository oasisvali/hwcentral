from django.http import Http404
from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.base import AuthenticatedBase
from core.view_models.classroom_id import ClassroomIdBody
from core.view_models.sidebar import TeacherSidebar, AdminSidebar


class ClassroomIdGet(GroupDrivenViewCommonTemplate):
    def __init__(self, request, classroom):
        super(ClassroomIdGet, self).__init__(request)
        self.urlname = UrlNames.CLASSROOM_ID
        self.classroom = classroom

    def student_endpoint(self):
        raise Http404

    def teacher_endpoint(self):
        if self.classroom.classTeacher != self.user:
            raise Http404
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                     ClassroomIdBody(self.classroom))
                      .as_context())

    def parent_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        if self.classroom.school != self.user.userinfo.school:
            raise Http404
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                     ClassroomIdBody(self.classroom))
                      .as_context())