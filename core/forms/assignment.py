import datetime
from django import forms
import django
from django.forms.widgets import SplitDateTimeWidget
from core.models import  SubjectRoom, AssignmentQuestionsList, ClassRoom
class AssignmentForm(forms.Form):
    def __init__(self,teacher,*args,**kwargs):
        super(AssignmentForm,self).__init__(*args,**kwargs)
        aql_options_list =[]
        SEPARATOR = "_"
        self.fields['subjectroom'] =forms.ModelChoiceField(queryset=SubjectRoom.objects.filter(teacher=teacher))
        for subjectroom in teacher.subjects_managed_set.all():
            subject =subjectroom.subject
            standard = ClassRoom.objects.get(pk=subjectroom.classRoom.pk).standard
            for assignmentql in AssignmentQuestionsList.objects.filter(subject=subject,standard=standard,school=teacher.userinfo.school):
                aql_options_list.append(
                    (SEPARATOR.join([str(standard.pk), str(subject.pk), assignmentql.description, str(assignmentql.pk)]),
                     str(assignmentql)))

        #options list format : standardid_subjectid_description;assignemntsubject-assignmentnumber
        self.fields['question sets'] = forms.ChoiceField(choices=aql_options_list)

    assigned = forms.DateTimeField(widget=SplitDateTimeWidget())
    due = forms.DateTimeField(widget=SplitDateTimeWidget())

    def clean(self):

        SECONDS_BUFFER = 300
        ASSIGNMENT_MIN_ACTIVE_DAYS= 1
        cleaned_data = super(AssignmentForm, self).clean()
        if len(self.errors)>0:
            return
        assigned = cleaned_data['assigned']
        due = cleaned_data['due']
        now = django.utils.timezone.now()

        if  assigned < now-datetime.timedelta(seconds = SECONDS_BUFFER):
            raise forms.ValidationError("An assigment cannot be assigned in the past. ")

        if due<assigned:
            raise forms.ValidationError(" An assignment cant be due before it has been assigned! ")

        if due< now + datetime.timedelta(days=ASSIGNMENT_MIN_ACTIVE_DAYS):
            raise forms.ValidationError(" Every assignment must be open for at least a day. ")


