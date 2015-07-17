from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.view_models.base import AuthenticatedBase
from core.view_models.home import StudentHomeBody, TeacherHomeBody, ParentHomeBody, AdminHomeBody
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, ParentSidebar, AdminSidebar
from core.view_drivers.base import GroupDrivenViewGroupDrivenTemplate


class HomeGet(GroupDrivenViewGroupDrivenTemplate):
    def __init__(self, request):
        super(HomeGet, self).__init__(request)
        self.urlname = UrlNames.HOME


    def student_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedBase(StudentSidebar(self.user), StudentHomeBody(self.user))
                      .as_context())

    def teacher_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedBase(TeacherSidebar(self.user), TeacherHomeBody(self.user))
                      .as_context())

    def parent_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedBase(ParentSidebar(self.user), ParentHomeBody(self.user))
                      .as_context())

    def admin_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedBase(AdminSidebar(self.user), AdminHomeBody(self.user))
                      .as_context())