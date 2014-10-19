from django.forms import ModelForm

from core.models import UserInfo


class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        exclude = ('user',)