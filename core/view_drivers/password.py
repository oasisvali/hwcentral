from django.shortcuts import render, redirect

from core.forms.password import CustomPasswordChangeForm
from core.view_models.password import PasswordBody
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.routing.urlnames import UrlNames
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, AdminSidebar, ParentSidebar
from hwcentral.settings import SUBMIT_SUCCESS_REDIRECT_URL


class PasswordDriver(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(PasswordDriver, self).__init__(request)
        self.urlname = UrlNames.PASSWORD

    def common_endpoint(self, sidebar):
        raise NotImplementedError('Subclass of PasswordDriver must implement common_endpoint logic')

    def student_endpoint(self):
        return self.common_endpoint(StudentSidebar(self.user))

    def teacher_endpoint(self):
        return self.common_endpoint(TeacherSidebar(self.user))

    def admin_endpoint(self):
        return self.common_endpoint(AdminSidebar(self.user))

    def parent_endpoint(self):
        return self.common_endpoint(ParentSidebar(self.user))


class PasswordGet(PasswordDriver):

    def common_endpoint(self,sidebar):
        form = CustomPasswordChangeForm(self.user)
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(sidebar, PasswordBody(form))
                      .as_context() )


class PasswordPost(PasswordDriver):

    def common_endpoint(self,sidebar):
        form = CustomPasswordChangeForm(user=self.user, data=self.request.POST)
        if form.is_valid():
            form.save()
            return redirect(SUBMIT_SUCCESS_REDIRECT_URL)

        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(sidebar, PasswordBody(form)).as_context())

