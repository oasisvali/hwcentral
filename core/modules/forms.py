from django.forms import forms, ModelForm
from core.models import UserInfo


class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        exclude = ('user',)