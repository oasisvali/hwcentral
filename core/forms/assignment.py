from django import forms
from django.db import models
from core.models import Assignment, SubjectRoom, AssignmentQuestionsList, ClassRoom


class AssignmentForm(forms.Form):

    def __init__(self,teacher,*args,**kwargs):
        super(AssignmentForm,self).__init__(*args,**kwargs)
        OPTIONS_LIST =[]

        self.fields['subjectroom'] =forms.ModelChoiceField(queryset=SubjectRoom.objects.filter(teacher_id=teacher.pk))

        for subjectroom in SubjectRoom.objects.filter(teacher__id=teacher.pk):
            subject_id =subjectroom.subject_id
            for subject in teacher.subjects_managed_set.all():
                classroom_id = subject.classRoom_id
                standard_id = ClassRoom.objects.get(id=classroom_id).standard_id
                for assignmentql in AssignmentQuestionsList.objects.filter(subject_id=subject_id,standard_id=standard_id):

                    OPTIONS_LIST.append((str(standard_id)+"_"+str(subject_id)+"_"+str(assignmentql.description)+"_"+str(assignmentql.id),str(assignmentql.subject)+
                                         "-"+str(assignmentql)))

        #options list format : standardid_subjectid_description;assignemntsubject-assignmentnumber

        self.fields['questionlists'] = forms.ChoiceField(choices=OPTIONS_LIST)
    assigned = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    due = forms.DateTimeField(widget=forms.DateInput(attrs={'class':'timepicker'}))
