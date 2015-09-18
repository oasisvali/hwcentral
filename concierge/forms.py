from django.forms import ModelForm, TextInput, EmailInput

from concierge.models import Enquirer


class EnquirerForm(ModelForm):
    class Meta:
        model = Enquirer
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'name'}),
            'school': TextInput(attrs={'placeholder': 'school'}),
            'email': EmailInput(attrs={'placeholder': 'email'}),
            'phone': TextInput(attrs={'placeholder': 'phone'})
        }
