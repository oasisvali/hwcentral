from core.view_models.announcement import AnnouncementBody
from core.view_models.passwordchange import PasswordChangeBody

__author__ = 'hrishikesh'
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.routing.urlnames import UrlNames
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar, TeacherSidebar, AdminSidebar, ParentSidebar


class PasswordChangeGet(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(PasswordChangeGet, self).__init__(request)
        self.urlname = UrlNames.ANNOUNCEMENT
    def student_endpoint(self):
        form = PasswordChangeForm(self.user)
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(StudentSidebar(self.user),PasswordChangeBody(form))
                      .as_context() )

    def teacher_endpoint(self):
        form = PasswordChangeForm(self.user)
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(TeacherSidebar(self.user),PasswordChangeBody(form))
                      .as_context() )
    def admin_endpoint(self):
        form = PasswordChangeForm(self.user)
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(AdminSidebar(self.user),PasswordChangeBody(form))
                      .as_context() )
    def parent_endpoint(self):
        form = PasswordChangeForm(self.user)
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(ParentSidebar(self.user),PasswordChangeBody(form))
                      .as_context() )

# TODO: find a way to replace the hardcoded links.
class PasswordChangePost(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(PasswordChangePost, self).__init__(request)
        self.urlname = UrlNames.ANNOUNCEMENT
    def student_endpoint(self):
        form = PasswordChangeForm(user=self.request.user, data=self.request.POST)
        if form.is_valid():
            form.new_password1 = form.save()
            return render(self.request,'/home/hrishikesh/hwcentral/core/templates/authenticated/password_success.html')
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(StudentSidebar(self.request.user),PasswordChangeBody(form)).as_context())

    def teacher_endpoint(self):
        form = PasswordChangeForm(user=self.request.user, data=self.request.POST)
        if form.is_valid():
            form.new_password1 = form.save()
            return render(seld.request,'/home/hrishikesh/hwcentral/core/templates/authenticated/password_success.html')
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(TeacherSidebar(self.request.user),PasswordChangeBody(form))
                          .as_context() )
    def admin_endpoint(self):
        form = PasswordChangeForm(user=self.request.user, data=self.request.POST)
        if form.is_valid():
            form.new_password1 = form.save()
            return render(self.request,'/home/hrishikesh/hwcentral/core/templates/authenticated/password_success.html')
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(AdminSidebar(self.request.user),PasswordChangeBody(form))
                          .as_context() )
    def parent_endpoint(self):
        form = PasswordChangeForm(user=self.request.user, data=self.request.POST)
        if form.is_valid():
            form.new_password1 = form.save()
            return render(self.request,'/home/hrishikesh/hwcentral/core/templates/authenticated/password_success.html')
        return render(self.request, UrlNames.PASSWORD.get_template(),
                      AuthenticatedBase(ParentSidebar(self.request.user),PasswordChangeBody(form))
                          .as_context() )