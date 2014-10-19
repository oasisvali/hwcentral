from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, ParentSidebar, AdminSidebar
from core.view_models.subject_id import StudentSubjectIdBody, TeacherSubjectIdBody, ParentSubjectIdBody, \
    AdminSubjectIdBody
from core.views.base import GroupDrivenView


class SubjectIdGet(GroupDrivenView):
    def __init__(self, request, subject_id):
        super(SubjectIdGet, self).__init__(request)
        self.urlname = UrlNames.SUBJECT_ID
        self.subject_id = subject_id


    def student_view(self):
        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                     StudentSubjectIdBody(self.user, self.subject_id))
                      .as_context())

    def teacher_view(self):
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                     TeacherSubjectIdBody(self.user, self.subject_id))
                      .as_context())

    def parent_view(self):
        return render(self.request, self.template, AuthenticatedBase(ParentSidebar(self.user),
                                                                     ParentSubjectIdBody(self.user, self.subject_id))
                      .as_context())

    def admin_view(self):
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                     AdminSubjectIdBody(self.user, self.subject_id))
                      .as_context())