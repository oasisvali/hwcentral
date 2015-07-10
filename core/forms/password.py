from django  import forms
from hwcentral import  settings
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.sites.models import Site




MIN_PASSWORD_LENGTH = 8
def validate_password(form):
        password1 = form.cleaned_data.get('new_password1')

        if len(password1) < MIN_PASSWORD_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % MIN_PASSWORD_LENGTH)

        return password1

class NewPasswordChangeForm(PasswordChangeForm):

    def clean_new_password1(self):
        return validate_password(self)




class ForgotPasswordForm(SetPasswordForm):

    def clean_new_password1(self):
        return validate_password(self)
