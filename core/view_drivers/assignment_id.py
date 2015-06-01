from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenView
from core.view_models.assignment_id import StudentAssignmentIdBody, TeacherAssignmentIdBody, ParentAssignmentIdBody, \
    AdminAssignmentIdBody
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, ParentSidebar, AdminSidebar


class AssignmentIdActiveGet(GroupDrivenView):
    def __init__(self, request, assignment):
        super(AssignmentIdActiveGet, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENT_ID
        self.type = 'active'
        self.assignment = assignment


    def student_view(self):
        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                                   StudentAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def teacher_view(self):
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                                   TeacherAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def parent_view(self):
        return render(self.request, self.template, AuthenticatedBase(ParentSidebar(self.user),
                                                                                   ParentAssignmentIdBody(self.user,
                                                                                                          self.assignment))
                      .as_context())

    def admin_view(self):
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                                   AdminAssignmentIdBody(self.user,
                                                                                                         self.assignment))
                      .as_context())


class AssignmentIdActivePost(GroupDrivenView):
    def __init__(self, request, assignment):
        super(AssignmentIdActivePost, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENT_ID
        self.type = 'active'
        self.assignment = assignment


    def student_view(self):
        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                                   StudentAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def teacher_view(self):
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                                   TeacherAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def parent_view(self):
        return render(self.request, self.template, AuthenticatedBase(ParentSidebar(self.user),
                                                                                   ParentAssignmentIdBody(self.user,
                                                                                                          self.assignment))
                      .as_context())

    def admin_view(self):
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                                   AdminAssignmentIdBody(self.user,
                                                                                                         self.assignment))
                      .as_context())


class AssignmentIdGradedGet(GroupDrivenView):
    def __init__(self, request, assignment):
        super(AssignmentIdGradedGet, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENT_ID
        self.type = 'graded'
        self.assignment = assignment


    def student_view(self):
        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                                   StudentAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def teacher_view(self):
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                                   TeacherAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def parent_view(self):
        return render(self.request, self.template, AuthenticatedBase(ParentSidebar(self.user),
                                                                                   ParentAssignmentIdBody(self.user,
                                                                                                          self.assignment))
                      .as_context())

    def admin_view(self):
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                                   AdminAssignmentIdBody(self.user,
                                                                                                         self.assignment))
                      .as_context())