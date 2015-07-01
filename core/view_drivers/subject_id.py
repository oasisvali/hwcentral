from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, ParentSidebar, AdminSidebar
from core.view_models.subject_id import StudentSubjectIdBody, TeacherSubjectIdBody, ParentSubjectIdBody, \
    AdminSubjectIdBody
from core.view_drivers.base import GroupDrivenView


class SubjectIdGet(GroupDrivenView):
    def __init__(self, request, subject):
        super(SubjectIdGet, self).__init__(request)
        self.urlname = UrlNames.SUBJECT_ID
        self.subject = subject


    def student_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                                   StudentSubjectIdBody(self.user,
                                                                                                        self.subject))
                      .as_context())

    def teacher_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                                   TeacherSubjectIdBody(self.user,
                                                                                                        self.subject))
                      .as_context())

    def parent_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(ParentSidebar(self.user),
                                                                                   ParentSubjectIdBody(self.user,
                                                                                                       self.subject))
                      .as_context())

    def admin_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                                   AdminSubjectIdBody(self.user,
                                                                                                      self.subject))
                      .as_context())