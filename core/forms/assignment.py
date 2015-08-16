import datetime

from django import forms
import django
from django.forms.widgets import SplitDateTimeWidget

from core.models import SubjectRoom, AssignmentQuestionsList


class AssignmentForm(forms.Form):
    SEPARATOR = "_"
    def __init__(self,teacher,*args,**kwargs):
        super(AssignmentForm,self).__init__(*args,**kwargs)
        aql_options_list =[]

        self.fields['subjectroom'] =forms.ModelChoiceField(queryset=SubjectRoom.objects.filter(teacher=teacher),
                                                           help_text="Select the class for which you wish "
                                                                     "to assign the homework")
        for subjectroom in teacher.subjects_managed_set.all():
            subject =subjectroom.subject
            standard = subjectroom.classRoom.standard
            for assignmentql in AssignmentQuestionsList.objects.filter(subject=subject,standard=standard,school=teacher.userinfo.school):
                aql_options_list.append(
                    #These will be te ID
                    (AssignmentForm.SEPARATOR.join([str(standard.pk), str(subject.pk), assignmentql.description, str(assignmentql.pk)]),
                     #This will be the display
                     str(assignmentql)))

        self.fields['question sets'] = forms.ChoiceField(choices=aql_options_list,
                                                         help_text="Select the question set for the new assignment")

    assigned = forms.DateTimeField(widget=SplitDateTimeWidget(),
                                   help_text="The date and time  when the assignment "
                                             "will become available for the students")

    due = forms.DateTimeField(widget=SplitDateTimeWidget(),
                              help_text= "Enter the due date for the assignment. This must be"
                                         "at least 24 hours from when it was assigned")

    def clean(self):

        SECONDS_BUFFER = 300
        ASSIGNMENT_MIN_ACTIVE_DAYS= 1
        cleaned_data = super(AssignmentForm, self).clean()
        if len(self.errors)>0:
            return
        assigned = cleaned_data['assigned']
        due = cleaned_data['due']
        now = django.utils.timezone.now()

        if  (assigned) < (now-datetime.timedelta(seconds = SECONDS_BUFFER)):
            raise forms.ValidationError("An assigment cannot be assigned in the past. ")

        if (due)<assigned:
            raise forms.ValidationError("An assignment cant be due before it has been assigned!")

        if (due)< now + datetime.timedelta(days=ASSIGNMENT_MIN_ACTIVE_DAYS):
            raise forms.ValidationError("Every assignment must be open for at least a day.")


