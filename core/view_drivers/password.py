from django.shortcuts import render

from core.forms.password import NewPasswordChangeForm
from core.view_models.password import PasswordChangeBody
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.routing.urlnames import UrlNames
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, AdminSidebar, ParentSidebar


class PasswordChangeGet(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(PasswordChangeGet, self).__init__(request)
        self.urlname = UrlNames.PASSWORD

    def common_endpoint(self,sidebar):
        form = NewPasswordChangeForm(self.user)
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(sidebar,PasswordChangeBody(form))
                      .as_context() )

    def student_endpoint(self):
        return self.common_endpoint(StudentSidebar(self.user))
    def teacher_endpoint(self):
        return self.common_endpoint(TeacherSidebar(self.user))
    def admin_endpoint(self):
        return self.common_endpoint(AdminSidebar(self.user))
    def parent_endpoint(self):
        return self.common_endpoint(ParentSidebar(self.user))

# TODO: find a way to replace the hardcoded links.

class PasswordChangePost(GroupDrivenViewCommonTemplate):
    PASSWORD_SUCCESS_TEMPLATE = 'authenticated/password_success.html'

    def __init__(self, request):
        super(PasswordChangePost, self).__init__(request)
        self.urlname = UrlNames.PASSWORD

    def common_endpoint(self,sidebar):
        form = NewPasswordChangeForm(user=self.user, data=self.request.POST)
        if form.is_valid():
            form.save()
            return render(self.request,
                      AuthenticatedBase(sidebar,PasswordChangeBody(form)).as_context())

        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(sidebar,PasswordChangeBody(form)).as_context())

    def student_endpoint(self):
        return self.common_endpoint(StudentSidebar(self.user))
    def teacher_endpoint(self):
        return self.common_endpoint(TeacherSidebar(self.user))
    def admin_endpoint(self):
        return self.common_endpoint(AdminSidebar(self.user))
    def parent_endpoint(self):
        return self.common_endpoint(ParentSidebar(self.user))

