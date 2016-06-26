import datetime

import django
from django import forms
from django.db.models import Q

from core.forms.base import DATE_INPUT_FORMAT
from core.forms.base import TIME_INPUT_FORMAT
from core.forms.fields import CustomLabelModelChoiceField
from core.forms.widgets import ChosenNoSearchSelect
from core.models import AssignmentQuestionsList
from core.utils.labels import get_subjectroom_label, get_aql_label
from core.utils.references import HWCentralRepo


class AssignmentForm(forms.Form):
    SECONDS_BUFFER = 300
    ASSIGNMENT_MIN_ACTIVE_DAYS = 1

    ENFORCE_DUE_TIME = datetime.time(22)

    def __init__(self, teacher, question_set_override, *args, **kwargs):
        super(AssignmentForm,self).__init__(*args,**kwargs)

        self.question_set_override = question_set_override

        school_filter = Q(school=teacher.userinfo.school) | Q(school=HWCentralRepo.refs.SCHOOL)

        subjectrooms = teacher.subjects_managed_set.all()

        standard_subject_filter = Q()

        for subjectroom in subjectrooms:
            subject = subjectroom.subject
            standard = subjectroom.classRoom.standard
            if self.question_set_override:
                standard_subject_filter = standard_subject_filter | (
                Q(subject=subject) & Q(standard__number__lte=standard.number))

            else:
                standard_subject_filter = standard_subject_filter | (Q(subject=subject) & Q(standard=standard))

        self.fields['question_set'] = CustomLabelModelChoiceField(get_aql_label,
                                                                  widget=forms.Select(
                                                                          attrs={'class': 'hidden'}),
                                                                  queryset=AssignmentQuestionsList.objects.filter(school_filter, standard_subject_filter),
                                                                  help_text="Select the question set for the new homework")

        self.fields['subjectroom'] = CustomLabelModelChoiceField(get_subjectroom_label,
                                                                 widget=ChosenNoSearchSelect,
                                                                 queryset=subjectrooms,
                                                                 help_text="Select the subjectroom for which you wish "
                                                                     "to assign the homework")

    assigned = forms.SplitDateTimeField(input_date_formats=DATE_INPUT_FORMAT,
                                        input_time_formats=TIME_INPUT_FORMAT,
                                        help_text="The date and time  when the homework "
                                             "will become available for the students")

    due = forms.SplitDateTimeField(input_date_formats=DATE_INPUT_FORMAT,
                                   input_time_formats=TIME_INPUT_FORMAT,
                                   help_text="Enter the due date for the homework. This must be "
                                         "at least 24 hours from when it was assigned")

    def clean_due(self):
        due = self.cleaned_data['due']
        if due.time() != AssignmentForm.ENFORCE_DUE_TIME:
            raise forms.ValidationError("A homework must be due at %s hrs." % AssignmentForm.ENFORCE_DUE_TIME)

        return due

    def clean(self):

        if len(self.errors)>0:
            return
        assigned = self.cleaned_data['assigned']
        due = self.cleaned_data['due']
        now = django.utils.timezone.now()

        if assigned < (now - datetime.timedelta(seconds=AssignmentForm.SECONDS_BUFFER)):
            raise forms.ValidationError("A homework cannot be assigned in the past.")

        if due < assigned:
            raise forms.ValidationError("A homework can't be due before it has been assigned.")

        if due < (now + datetime.timedelta(days=AssignmentForm.ASSIGNMENT_MIN_ACTIVE_DAYS)):
            raise forms.ValidationError("Every homework must be open for at least a day.")

        # finally, check that the aql selected is valid for the selected subjectroom (front-end logic should prevent this,
        # but better to be safe)

        assignmentQuestionsList = self.cleaned_data['question_set']
        subjectRoom = self.cleaned_data['subjectroom']

        if assignmentQuestionsList.subject != subjectRoom.subject:
            raise forms.ValidationError("Subject for Question set and SubjectRoom do not match.")

        if not self.question_set_override:
            if (assignmentQuestionsList.standard != subjectRoom.classRoom.standard):
                raise forms.ValidationError("Standard for Question set and SubjectRoom do not match.")
        else:
            if (assignmentQuestionsList.standard.number > subjectRoom.classRoom.standard.number):
                raise forms.ValidationError("Cannot assign Question set for %s standard to class of %s standard!" % (assignmentQuestionsList.standard.number, subjectRoom.classRoom.standard.number))


        return self.cleaned_data
