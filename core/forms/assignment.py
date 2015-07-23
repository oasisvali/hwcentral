from django import forms
from django.forms.widgets import SplitDateTimeWidget
from core.models import  SubjectRoom, AssignmentQuestionsList, ClassRoom
class AssignmentForm(forms.Form):
    def __init__(self,teacher,*args,**kwargs):
        super(AssignmentForm,self).__init__(*args,**kwargs)
        aql_options_list =[]
        separator = "_"
        self.fields['subjectroom'] =forms.ModelChoiceField(queryset=SubjectRoom.objects.filter(teacher=teacher))
        for subjectroom in SubjectRoom.objects.filter(teacher__id=teacher.pk):
            subject_id =subjectroom.subject_id
            classroom_id = subjectroom.pk
            standard_id = ClassRoom.objects.get(id=classroom_id).standard_id
            for assignmentql in AssignmentQuestionsList.objects.filter(subject_id=subject_id,standard_id=standard_id):
                aql_options_list.append(
                    (separator.join([str(standard_id), str(subject_id), assignmentql.description, str(assignmentql.pk)]),
                     str(assignmentql)))

        #options list format : standardid_subjectid_description;assignemntsubject-assignmentnumber
        self.fields['questionlists'] = forms.ChoiceField(choices=aql_options_list)

    assigned = forms.DateTimeField(widget=SplitDateTimeWidget())
    due = forms.DateTimeField(widget=SplitDateTimeWidget())
