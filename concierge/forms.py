from django.forms import ModelForm, TextInput, EmailInput

from concierge.models import Enquirer


class EnquirerForm(ModelForm):
    class Meta:
        model = Enquirer
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Name'}),
            'school': TextInput(attrs={'placeholder': 'School'}),
            'email': EmailInput(attrs={'placeholder': 'Email'}),
            'phone': TextInput(attrs={'placeholder': 'Phone'})
        }
