from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenView
from core.view_models.base import AuthenticatedBase
from core.view_models.classroom_id import StudentClassroomIdBody, TeacherClassroomIdBody, ParentClassroomIdBody, \
    AdminClassroomIdBody
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, AdminSidebar, ParentSidebar


class ClassroomIdGet(GroupDrivenView):
    def __init__(self, request, classroom):
        super(ClassroomIdGet, self).__init__(request)
        self.urlname = UrlNames.CLASSROOM_ID
        self.classroom = classroom


    def student_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                     StudentClassroomIdBody(self.user,
                                                                                            self.classroom))
                      .as_context())

    def teacher_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                     TeacherClassroomIdBody(self.user,
                                                                                            self.classroom))
                      .as_context())

    def parent_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(ParentSidebar(self.user),
                                                                     ParentClassroomIdBody(self.user,
                                                                                           self.classroom))
                      .as_context())

    def admin_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                     AdminClassroomIdBody(self.user,
                                                                                          self.classroom))
                      .as_context())