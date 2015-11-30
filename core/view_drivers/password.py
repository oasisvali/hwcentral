from django.shortcuts import render

from core.forms.password import CustomPasswordChangeForm
from core.utils.toast import redirect_with_success_toast
from core.view_models.password import PasswordBody
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.routing.urlnames import UrlNames
from core.view_models.base import AuthenticatedVM
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, AdminSidebar, ParentSidebar


class PasswordDriver(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(PasswordDriver, self).__init__(request)
        self.urlname = UrlNames.PASSWORD

    def common_endpoint(self, sidebar):
        raise NotImplementedError('Subclass of PasswordDriver must implement common_endpoint logic')

    def student_endpoint(self):
        return self.common_endpoint()

    def teacher_endpoint(self):
        return self.common_endpoint()

    def admin_endpoint(self):
        return self.common_endpoint()

    def parent_endpoint(self):
        return self.common_endpoint()


class PasswordGet(PasswordDriver):

    def common_endpoint(self):
        form = CustomPasswordChangeForm(self.user)
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedVM(self.user, PasswordBody(form))
                      .as_context())


class PasswordPost(PasswordDriver):

    def common_endpoint(self):
        form = CustomPasswordChangeForm(user=self.user, data=self.request.POST)
        if form.is_valid():
            form.save()
            return redirect_with_success_toast(self.request, 'Your password was changed successfully.')

        return render(self.request, self.template,
                      AuthenticatedVM(self.user, PasswordBody(form)).as_context())

