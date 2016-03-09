import django
from django import forms
from django.contrib.contenttypes.models import ContentType

from core.forms.fields import CustomLabelModelChoiceField
from core.forms.widgets import ChosenNoSearchSelect
from core.models import AssignmentQuestionsList, Submission, SubjectRoom
from core.utils.labels import get_aql_label, get_subject_label


class PracticeForm(forms.Form):
    def __init__(self, student, *args, **kwargs):
        super(PracticeForm, self).__init__(*args, **kwargs)

        subjectrooms = student.subjects_enrolled_set.all()
        accessible_aqls = Submission.objects.filter(
            student=student,
            assignment__due__lte=django.utils.timezone.now(),
            assignment__content_type=ContentType.objects.get_for_model(SubjectRoom)
        ).values_list("assignment__assignmentQuestionsList__pk", flat=True).distinct()

        self.fields['question_set'] = CustomLabelModelChoiceField(get_aql_label,
                                                                  widget=forms.Select(
                                                                      attrs={'class': 'hidden'}),
                                                                  queryset=AssignmentQuestionsList.objects.filter(
                                                                      pk__in=accessible_aqls),
                                                                  help_text="Select the question set for the new homework")

        # TODO:  Technically, subjectroom is not required as part of this form
        self.fields['subjectroom'] = CustomLabelModelChoiceField(get_subject_label,
                                                                 widget=ChosenNoSearchSelect,
                                                                 queryset=subjectrooms,
                                                                 help_text="Select the subject which you wish to practice")

    def clean(self):

        if len(self.errors) > 0:
            return

        # check that the aql selected is valid for the selected subjectroom (front-end logic should prevent this,
        # but better to be safe)

        assignmentQuestionsList = self.cleaned_data['question_set']
        subjectRoom = self.cleaned_data['subjectroom']

        if assignmentQuestionsList.subject != subjectRoom.subject:
            raise forms.ValidationError("Subject for Question set and SubjectRoom do not match.")
        if (assignmentQuestionsList.standard != subjectRoom.classRoom.standard):
            raise forms.ValidationError("Standard for Question set and SubjectRoom do not match.")

        return self.cleaned_data