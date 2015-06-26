__author__ = 'hrishikesh'
from django import forms
from core import models


def get_content_types(username):
    if username == 2:
        return ("classroom", "school")
    elif username == "3":
        pass


def get_content_objects():
    return ("0", "1", "2")
    pass


username = " "


class PostModelForm(forms.Form):
    content_type = forms.ModelChoiceField(queryset=get_content_types(username), required=True)
    object_id = forms.ModelChoiceField(queryset=get_content_objects(), required=True)
    message = forms.CharField(required=True)

    class meta:
        fields = ('content_type', 'object_id', 'message',)
