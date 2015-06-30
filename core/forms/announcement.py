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
            j =[]
            for subject in SubjectRoom.objects.filter(teacher=classteacher):
                k = "s"+str(subject.subject_id),str(subject)
                j.append(k)
            for classes in ClassRoom.objects.filter(classTeacher=classteacher):
                k = "c"+str(classes.classTeacher_id),str(classes)
                j.append(k)
            self.fields['targets'] =forms.ChoiceField(choices=j)

