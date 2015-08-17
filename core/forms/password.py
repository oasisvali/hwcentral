from django  import forms
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm


class CustomPasswordChangeMixin(object):
    """
    Mixin class to add our custom password validation
    """

    MIN_PASSWORD_LENGTH = 8

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        if len(password1) < CustomPasswordChangeMixin.MIN_PASSWORD_LENGTH:
            raise forms.ValidationError(
                "The new password must be at least %d characters long." % CustomPasswordChangeMixin.MIN_PASSWORD_LENGTH)

        return password1


class CustomPasswordChangeForm(CustomPasswordChangeMixin, PasswordChangeForm):
    pass


class CustomSetPasswordForm(CustomPasswordChangeMixin, SetPasswordForm):
    """
    Combines our custom password validation with the inbuilt django new password validation
    """
    pass
