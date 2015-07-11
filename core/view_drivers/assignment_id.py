from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.utils.constants import AssignmentType
from core.view_drivers.base import GroupDrivenViewTypedTemplate
from core.view_models.assignment_id import StudentAssignmentIdBody, TeacherAssignmentIdBody, ParentAssignmentIdBody, \
    AdminAssignmentIdBody
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, ParentSidebar, AdminSidebar


class AssignmentId(GroupDrivenViewTypedTemplate):
    def __init__(self, request, assignment):
        super(AssignmentId, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENT_ID
        self.assignment = assignment


class AssignmentIdCorrected(AssignmentId):
    def __init__(self, request, assignment):
        super(AssignmentIdCorrected, self).__init__(request, assignment)
        self.type = AssignmentType.CORRECTED


class AssignmentIdUncorrected(AssignmentId):
    def __init__(self, request, assignment):
        super(AssignmentIdUncorrected, self).__init__(request, assignment)
        self.type = AssignmentType.UNCORRECTED


class AssignmentIdUncorrectedGet(AssignmentIdUncorrected):

    def student_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                                   StudentAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def teacher_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                                   TeacherAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def parent_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(ParentSidebar(self.user),
                                                                                   ParentAssignmentIdBody(self.user,
                                                                                                          self.assignment))
                      .as_context())

    def admin_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                                   AdminAssignmentIdBody(self.user,
                                                                                                         self.assignment))
                      .as_context())


class AssignmentIdUncorrectedPost(AssignmentIdUncorrected):



    def student_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                                   StudentAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def teacher_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                                   TeacherAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def parent_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(ParentSidebar(self.user),
                                                                                   ParentAssignmentIdBody(self.user,
                                                                                                          self.assignment))
                      .as_context())

    def admin_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                                   AdminAssignmentIdBody(self.user,
                                                                                                         self.assignment))
                      .as_context())


class AssignmentIdCorrectedGet(AssignmentIdCorrected):


    def student_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                                   StudentAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def teacher_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user),
                                                                                   TeacherAssignmentIdBody(self.user,
                                                                                                           self.assignment))
                      .as_context())

    def parent_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(ParentSidebar(self.user),
                                                                                   ParentAssignmentIdBody(self.user,
                                                                                                          self.assignment))
                      .as_context())

    def admin_endpoint(self):
        return render(self.request, self.template, AuthenticatedBase(AdminSidebar(self.user),
                                                                                   AdminAssignmentIdBody(self.user,
                                                                                                         self.assignment))
                      .as_context())