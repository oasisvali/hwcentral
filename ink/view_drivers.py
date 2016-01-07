from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from core.models import School, UserInfo, Home
from core.utils.references import HWCentralGroup
from core.utils.toast import render_with_success_toast, render_with_error_toast
from core.view_models.base import AuthenticatedVM
from ink.forms import ParentForm
from ink.models import Dossier
from ink.urlnames import InkUrlNames
from ink.view_models import ParentIdBody
from scripts.setup.full_school import build_username, SETUP_PASSWORD, send_activation_email


class ParentIdBase(object):
    def __init__(self, request, student_id):
        student = get_object_or_404(User, pk=student_id)
        if student.userinfo.group != HWCentralGroup.refs.STUDENT:
            raise Http404
        self.request = request
        self.user = request.user
        self.student = student
        self.template = InkUrlNames.PARENT_ID.template

class ParentIdGet(ParentIdBase):
    def handle(self):
        return render(self.request, self.template, AuthenticatedVM(self.user, ParentIdBody(self.student, ParentForm())).as_context())

class ParentIdPost(ParentIdBase):
    def handle(self):
        parent_form = ParentForm(self.request.POST)
        if parent_form.is_valid():
            # make parent account
            fname = parent_form.cleaned_data['fname']
            lname = parent_form.cleaned_data['lname']
            email = parent_form.cleaned_data['email']

            username = build_username(fname, lname)
            group = HWCentralGroup.refs.PARENT
            school = self.user.userinfo.school

            password = SETUP_PASSWORD

            parent = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            parent.first_name = fname
            parent.last_name = lname
            parent.save()

            userinfo = UserInfo(user=parent)
            userinfo.group = group
            userinfo.school = school
            userinfo.save()

            # finally, save the dossier on the new user
            dossier = Dossier(user=parent)
            dossier.flagged = False
            dossier.phone = parent_form.cleaned_data['phone']
            dossier.save()

            # make home
            home = Home(parent=parent)
            home.save()
            home.children.add(self.student)
            home.save()

            # send activation email
            send_activation_email(email)

            return render_with_success_toast(self.request,
                                         '<div>The new account has been activated!</div><h3>username: %s</h3>' % username,
                                         self.template, AuthenticatedVM(self.user, ParentIdBody(self.student, ParentForm())).as_context())
        else:
            return render_with_error_toast(self.request,
                                       'There was a problem with your information. Please fix the errors and try again.',
                                       self.template, AuthenticatedVM(self.user, ParentIdBody(self.student, parent_form)).as_context())

