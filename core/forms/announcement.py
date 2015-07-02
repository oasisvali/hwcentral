from django import forms
from django.contrib.contenttypes.models import ContentType
from core.models import School,ClassRoom



class AdminAnnouncementForm(forms.Form):
    message = forms.CharField()

class ClassAnnouncementForm(forms.Form):
    def __init__(self,*args,**kwargs):
        request = kwargs.pop('request')
        teacherpk = int(request.user.id)
        super(ClassAnnouncementForm,self).__init__(self,*args,**kwargs)
        self.fields['classroom'].queryset = ClassRoom.objects.filter(classTeacher_id=teacherpk)

    classroom = forms.CharField()
    message = forms.CharField()

class SubjectAnnouncementForm(forms.Form):
    message = forms.CharField()

class ClassSubjectAnnouncementForm(forms.Form):
    message = forms.CharField()

