from django import forms
from core.models import School,ClassRoom, SubjectRoom

class BaseAnnouncementForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(BaseAnnouncementForm,self).__init__(*args,**kwargs)
    message = forms.CharField(widget=forms.Textarea)

class AdminAnnouncementForm(BaseAnnouncementForm):
    pass
class ClassAnnouncementForm(BaseAnnouncementForm):
    def __init__(self,classteacher,*args,**kwargs):
        super(ClassAnnouncementForm,self).__init__(*args,**kwargs)
        self.fields['classroom'] = forms.ModelChoiceField(queryset=ClassRoom.objects.filter(classTeacher=classteacher))

class SubjectAnnouncementForm(BaseAnnouncementForm):
    def __init__(self,classteacher,*args,**kwargs):
        super(SubjectAnnouncementForm,self).__init__(*args,**kwargs)
        self.fields['subjectroom'] =forms.ModelChoiceField(queryset=SubjectRoom.objects.filter(teacher=classteacher))

class ClassSubjectAnnouncementForm(BaseAnnouncementForm):
    def __init__(self,classteacher,*args,**kwargs):
        super(ClassSubjectAnnouncementForm,self).__init__(*args,**kwargs)
        options_list =[]
        for subject in SubjectRoom.objects.filter(teacher=classteacher):
            temp_list = "s"+str(subject.subject_id),str(subject)
            options_list.append(temp_list)
        for classes in ClassRoom.objects.filter(classTeacher=classteacher):
            temp_list = "c"+str(classes.classTeacher_id),str(classes)
            options_list.append(temp_list)
            self.fields['targets'] =forms.ChoiceField(choices=options_list)

