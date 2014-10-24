from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenView
from core.view_models.assignments import StudentAssignmentsBody, TeacherAssignmentsBody, ParentAssignmentsBody, \
    AdminAssignmentsBody
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, ParentSidebar, AdminSidebar


class AssignmentsGet(GroupDrivenView):
    def __init__(self, request):
        super(AssignmentsGet, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENTS


    def student_view(self):
        return render(self.request, self.urlname.get_template(), AuthenticatedBase(StudentSidebar(self.user),
                                                                                   StudentAssignmentsBody(self.user))
                      .as_context())

    def teacher_view(self):
        return render(self.request, self.urlname.get_template(), AuthenticatedBase(TeacherSidebar(self.user),
                                                                                   TeacherAssignmentsBody(self.user))
                      .as_context())

    def parent_view(self):
        return render(self.request, self.urlname.get_template(), AuthenticatedBase(ParentSidebar(self.user),
                                                                                   ParentAssignmentsBody(self.user))
                      .as_context())

    def admin_view(self):
        return render(self.request, self.urlname.get_template(), AuthenticatedBase(AdminSidebar(self.user),
                                                                                   AdminAssignmentsBody(self.user))
                      .as_context())