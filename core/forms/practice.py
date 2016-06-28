import django
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from core.forms.fields import CustomLabelModelChoiceField
from core.forms.widgets import ChosenNoSearchSelect
from core.models import AssignmentQuestionsList, Submission, SubjectRoom
from core.utils.constants import HWCentralEnv
from core.utils.labels import get_aql_label, get_subject_label
from core.utils.references import HWCentralRepo, HWCentralGroup
from hwcentral.exceptions import InvalidHWCentralEnvError
from hwcentral.settings import ENVIRON


class PracticeForm(forms.Form):
    def __init__(self, student, *args, **kwargs):
        super(PracticeForm, self).__init__(*args, **kwargs)
        assert student.userinfo.group == HWCentralGroup.refs.STUDENT

        subjectrooms = student.subjects_enrolled_set.all()

        if ENVIRON == HWCentralEnv.PROD or ENVIRON == HWCentralEnv.CIRCLECI:
            accessible_aql_pks = Submission.objects.filter(
                student=student,
                assignment__due__lte=django.utils.timezone.now(),
                assignment__content_type=ContentType.objects.get_for_model(SubjectRoom)
            ).values_list("assignment__assignmentQuestionsList__pk", flat=True).distinct()
            accessible_aqls = AssignmentQuestionsList.objects.filter(
                pk__in=accessible_aql_pks)
        elif ENVIRON == HWCentralEnv.QA or ENVIRON == HWCentralEnv.LOCAL:
            school_filter = Q(school=student.userinfo.school) | Q(school=HWCentralRepo.refs.SCHOOL)
            standard_filter = Q(standard=student.classes_enrolled_set.get().standard)

            accessible_aqls = AssignmentQuestionsList.objects.filter(school_filter & standard_filter)
        else:
            raise InvalidHWCentralEnvError(ENVIRON)

        self.fields['question_set'] = CustomLabelModelChoiceField(get_aql_label,
                                                                  widget=forms.Select(
                                                                      attrs={'class': 'hidden'}),
                                                                  queryset=accessible_aqls,
                                                                  help_text="Select the question set to practice")

        # TODO:  Technically, subjectroom is not required as part of this form
        self.fields['subjectroom'] = CustomLabelModelChoiceField(get_subject_label,
                                                                 widget=ChosenNoSearchSelect,
                                                                 queryset=subjectrooms,
                                                                 help_text="Select the subject that you wish to practice")

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


class OpenAssignmentForm(forms.Form):
    def __init__(self, student, *args, **kwargs):
        super(OpenAssignmentForm, self).__init__(*args, **kwargs)
        assert student.userinfo.group == HWCentralGroup.refs.OPEN_STUDENT

        accessible_aqls = AssignmentQuestionsList.objects.filter(school=HWCentralRepo.refs.SCHOOL,
                                                                 standard=(student.classes_enrolled_set.get()).standard)

        self.fields['question_set'] = CustomLabelModelChoiceField(get_aql_label,
                                                                  widget=forms.Select(
                                                                      attrs={'class': 'hidden'}),
                                                                  queryset=accessible_aqls,
                                                                  help_text="Select Question Set")
