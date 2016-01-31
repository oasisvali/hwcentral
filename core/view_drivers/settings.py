from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenViewGroupDrivenTemplate
from core.view_models.base import AuthenticatedVM
from core.view_models.settings import StudentSettingsBody, TeacherSettingsBody, ParentSettingsBody, AdminSettingsBody


class SettingsGet(GroupDrivenViewGroupDrivenTemplate):
    def __init__(self, request):
        super(SettingsGet, self).__init__(request)
        self.urlname = UrlNames.SETTINGS


    def student_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedVM(self.user, StudentSettingsBody(self.user))
                      .as_context())

    def teacher_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedVM(self.user, TeacherSettingsBody(self.user))
                      .as_context())

    def parent_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedVM(self.user, ParentSettingsBody(self.user))
                      .as_context())

    def admin_endpoint(self):
        return render(self.request, self.template,
                      AuthenticatedVM(self.user, AdminSettingsBody(self.user))
                      .as_context())