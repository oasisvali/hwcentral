import datetime

import django
from django import forms
from django.db.models import Q

from core.forms.base import DATE_INPUT_FORMAT
from core.forms.base import TIME_INPUT_FORMAT
from core.models import SubjectRoom, AssignmentQuestionsList
from core.utils.labels import get_subjectroom_label
from core.utils.references import HWCentralRepo


class AssignmentForm(forms.Form):
    SEPARATOR = "_"
    AQL_INDEX_IN_ID = -2

    SECONDS_BUFFER = 300
    ASSIGNMENT_MIN_ACTIVE_DAYS = 1

    ENFORCE_DUE_TIME = datetime.time(22)

    @classmethod
    def build_question_set_id(cls, subject_pk, standard, aql_pk, aql_desc):
        return AssignmentForm.SEPARATOR.join([str(subject_pk), str(standard), str(aql_pk), aql_desc])

    @classmethod
    def build_subjectroom_id(cls, subjectroom, standard_override=None):
        if not standard_override:
            standard = str(subjectroom.classRoom.standard)
        else:
            standard = standard_override
        return AssignmentForm.SEPARATOR.join([str(subjectroom.subject.pk), standard, str(subjectroom.pk)])

    @classmethod
    def build_question_set_label(cls, aql):
        return "%s - %s - %s" % (aql.standard.number, aql.subject.name, aql.get_title())

    def get_aql_pk(self):
        return long(self.cleaned_data['question_set'].split(AssignmentForm.SEPARATOR)[AssignmentForm.AQL_INDEX_IN_ID])

    def get_subjectroom_pk(self):
        return long(self.cleaned_data['subjectroom'].split(AssignmentForm.SEPARATOR)[-1])

    def __init__(self, teacher, question_set_override=False, *args, **kwargs):
        super(AssignmentForm,self).__init__(*args,**kwargs)

        self.question_set_override = question_set_override

        school_filter = Q(school=teacher.userinfo.school) | Q(school=HWCentralRepo.refs.SCHOOL)

        subjectrooms = teacher.subjects_managed_set.all()

        standard_subject_filter = Q()

        subjectroom_options_list = []
        for subjectroom in subjectrooms:
            subject = subjectroom.subject
            standard = subjectroom.classRoom.standard
            if self.question_set_override:
                # TODO: rather than looping over all subjects to make this list, better to do this in one query
                subjectroom_options_list.append((  # This will be the id
                                                   AssignmentForm.build_subjectroom_id(subjectroom, '*'),
                                                   # This will be the value
                                                   get_subjectroom_label(subjectroom)
                                                   ))

                standard_subject_filter = standard_subject_filter | (
                Q(subject=subject) & Q(standard__number__lte=standard.number))


            else:
                subjectroom_options_list.append((  # This will be the id
                                                   AssignmentForm.build_subjectroom_id(subjectroom),
                                                   # This will be the value
                                                   get_subjectroom_label(subjectroom)
                                                   ))
                standard_subject_filter = standard_subject_filter | (Q(subject=subject) & Q(standard=standard))

        aql_options_list = []

        for aql in AssignmentQuestionsList.objects.filter(school_filter, standard_subject_filter):
            subject = aql.subject
            standard = '*' if self.question_set_override else aql.standard

            aql_options_list.append(
                # These will be te ID
                (AssignmentForm.build_question_set_id(subject.pk, standard, aql.pk, aql.description),
                 # This will be the display
                 AssignmentForm.build_question_set_label(aql)))

        self.fields['question_set'] = forms.ChoiceField(choices=aql_options_list,
                                                        help_text="Select the question set for the new homework")

        self.fields['subjectroom'] = forms.ChoiceField(choices=subjectroom_options_list,
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

        assignmentQuestionsList = AssignmentQuestionsList.objects.get(pk=self.get_aql_pk())
        subjectRoom = SubjectRoom.objects.get(pk=self.get_subjectroom_pk())

        if assignmentQuestionsList.subject != subjectRoom.subject:
            raise forms.ValidationError("Subject for Question set and SubjectRoom do not match.")
        if not self.question_set_override:
            if (assignmentQuestionsList.standard != subjectRoom.classRoom.standard):
                raise forms.ValidationError("Standard for Question set and SubjectRoom do not match.")

        return self.cleaned_data
