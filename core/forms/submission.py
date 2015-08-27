from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.safestring import mark_safe

from core.data_models.answer import NumericAnswer, TextualAnswer, ConditionalAnswer, MCSAQAnswer, MCMAQAnswer
from core.forms.base import ReadOnlyForm
from core.forms.fields import TextualFormField, NumericFormField, MCSAQFormField, MCMAQFormField
from core.utils.constants import HWCentralQuestionType, HWCentralConditionalAnswerFormat
from hwcentral.exceptions import InvalidHWCentralConditionalAnswerFormatException, InvalidHWCentralQuestionTypeException


class SubmissionForm(forms.Form):

    """
    Contains a flattened list of assignment subparts as fields on the form
    """

    FIELD_KEY_SEPERATOR = '_'
    NON_FIELD_ERROR_MESSAGE = "Some of the answers were invalid. Please fix the errors below and try again."

    @classmethod
    def build_subpart_field_key(cls, question_index, subpart_index):
        return "%(question_index)i%(separator)s%(subpart_index)i" % {
            'question_index': question_index,
            'subpart_index': subpart_index,
            'separator': SubmissionForm.FIELD_KEY_SEPERATOR
        }

    @classmethod
    def build_conditional_subfield_key(cls, question_index, subpart_index, subfield_index):
        return "%(question_index)i%(separator)s%(subpart_index)i%(separator)s%(subfield_index)i" % {
            'question_index': question_index,
            'subpart_index': subpart_index,
            'subfield_index': subfield_index,
            'separator': SubmissionForm.FIELD_KEY_SEPERATOR
        }

    @classmethod
    def build_img_choice_tag(cls, img_url):
        return "<img src=\"%(img_url)s\" />" % {
            'img_url': img_url
        }

    @classmethod
    def build_choices(cls, combined_options, option_order):
        """
        looks at option ordering (NOTE: this requires that the passed in options have been shuffled) and builds a 2-tuple list
        containing (index, value) tuples.
        """
        assert len(option_order) == len(combined_options)
        choices = []
        for i, option_index in enumerate(option_order):
            option = combined_options[option_index]
            value = []
            if option.text is not None:
                # needs to be escaped so that the whole choice can be displayed unescaped (hence rendering the img tag
                # if it exists)
                value.append(escape(option.text))
            if option.img_url is not None:
                value.append(SubmissionForm.build_img_choice_tag(option.img_url))

            choices.append((i, mark_safe(''.join(value))))

        return choices

    def __init__(self, submission_vm, use_dm_answers=True, *args, **kwargs):
        """
        NOTE: use_dm_answers should only be false when the request.POST QueryDict is also passed in
        """
        self.submission_vm = submission_vm

        form_fields = {}
        if use_dm_answers:
            bound_data = {}

        # create a form field for each subpart
        for i, question in enumerate(self.submission_vm.questions):
            for j, subpart in enumerate(question.subparts):
                if subpart.type == HWCentralQuestionType.CONDITIONAL:
                    for k in xrange(subpart.answer.num_answers):
                        field_key = SubmissionForm.build_conditional_subfield_key(i, j, k)

                        conditional_format = subpart.answer.answer_format

                        if conditional_format == HWCentralConditionalAnswerFormat.NUMERIC:
                            field = NumericFormField()
                        elif conditional_format == HWCentralConditionalAnswerFormat.TEXTUAL:
                            field = TextualFormField(subpart.answer.show_toolbox)
                        else:
                            raise InvalidHWCentralConditionalAnswerFormatException(conditional_format)

                        form_fields[field_key] = field
                        if use_dm_answers:
                            try:
                                bound_data[field_key] = self.submission_vm.answers[i][j].values[k]
                            except IndexError:
                                pass

                else:
                    field_key = SubmissionForm.build_subpart_field_key(i, j)

                    if subpart.type == HWCentralQuestionType.MCSA:
                        choices = SubmissionForm.build_choices(subpart.options.combined, subpart.options.order)
                        field = MCSAQFormField(choices, subpart.options.use_dropdown_widget)
                        if use_dm_answers:
                            bound_data[field_key] = self.submission_vm.answers[i][j].choice
                    elif subpart.type == HWCentralQuestionType.MCMA:
                        choices = SubmissionForm.build_choices(subpart.options.combined, subpart.options.order)
                        field = MCMAQFormField(choices)
                        if use_dm_answers:
                            bound_data[field_key] = self.submission_vm.answers[i][j].choices
                    elif subpart.type == HWCentralQuestionType.NUMERIC:
                        field = NumericFormField()
                        if use_dm_answers:
                            bound_data[field_key] = self.submission_vm.answers[i][j].value
                    elif subpart.type == HWCentralQuestionType.TEXTUAL:
                        field = TextualFormField(subpart.show_toolbox)
                        if use_dm_answers:
                            bound_data[field_key] = self.submission_vm.answers[i][j].value

                    else:
                        raise InvalidHWCentralQuestionTypeException(subpart.type)

                    form_fields[field_key] = field

        # allows us to create a bound submission form by default
        if use_dm_answers:
            super(SubmissionForm, self).__init__(bound_data, *args, **kwargs)
        else:
            super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields.update(form_fields)

    def get_field_count(self):
        """
        Calculates how many fields should be in this form based on the submission data model associated with it
        """
        field_count = 0

        for question in self.submission_vm.questions:
            for subpart in question.subparts:
                if subpart.type == HWCentralQuestionType.CONDITIONAL:
                    field_count += subpart.answer.num_answers
                else:
                    field_count += 1

        return field_count

    def clean(self):
        """
        We perform validation here that involves more context than just a single field such as validation
        that needs to know the associated submission data model
        """

        # most top level check is to make sure the right number of fields exists on the form
        # so first we check if the right number of fields are on the form and then we check if each expected field is there
        # this way we thoroughly check the form for any missing/extra fields

        if len(self.errors) > 0:
            raise ValidationError(SubmissionForm.NON_FIELD_ERROR_MESSAGE)

        expected_field_count = self.get_field_count()
        actual_field_count = len(self.cleaned_data)
        if actual_field_count != expected_field_count:
            raise ValidationError(
                'Field count mismatch. expected: %s found: %s' % (expected_field_count, actual_field_count),
                'field_count_mismatch')

        for i, question in enumerate(self.submission_vm.questions):
            for j, subpart in enumerate(question.subparts):
                if subpart.type == HWCentralQuestionType.CONDITIONAL:

                    for k in xrange(subpart.answer.num_answers):
                        field_key = SubmissionForm.build_conditional_subfield_key(i, j, k)
                        if field_key not in self.cleaned_data:
                            raise ValidationError('Missing field %s' % field_key, 'missing_field')
                else:
                    field_key = SubmissionForm.build_subpart_field_key(i, j)
                    if field_key not in self.cleaned_data:
                        raise ValidationError('Missing field %s' % field_key, 'missing_field')

    def get_answers(self):
        """
        This method should only be called after validation.
        """
        # go through associated submission data model to find out the expected fields in the form
        # build 2-D answer list for every subpart answer

        answers = []  # building a new list to store lists of Answer data models

        for i, question in enumerate(self.submission_vm.questions):
            subparts_answers = []
            for j, subpart in enumerate(question.subparts):

                if subpart.type == HWCentralQuestionType.CONDITIONAL:
                    conditional_subpart_answers = []
                    for k in xrange(subpart.answer.num_answers):
                        field_key = SubmissionForm.build_conditional_subfield_key(i, j, k)
                        conditional_subpart_answers.append(self.cleaned_data[field_key])

                    subpart_answer = ConditionalAnswer.from_form_field(conditional_subpart_answers)
                else:
                    field_key = SubmissionForm.build_subpart_field_key(i, j)
                    subpart_answer_data = self.cleaned_data[field_key]

                    if subpart.type == HWCentralQuestionType.MCSA:
                        subpart_answer = MCSAQAnswer.from_form_field(subpart_answer_data)
                    elif subpart.type == HWCentralQuestionType.MCMA:
                        subpart_answer = MCMAQAnswer.from_form_field(subpart_answer_data)
                    elif subpart.type == HWCentralQuestionType.NUMERIC:
                        subpart_answer = NumericAnswer.from_form_field(subpart_answer_data)
                    elif subpart.type == HWCentralQuestionType.TEXTUAL:
                        subpart_answer = TextualAnswer.from_form_field(subpart_answer_data)
                    else:
                        raise InvalidHWCentralQuestionTypeException(subpart.type)

                subparts_answers.append(subpart_answer)
            answers.append(subparts_answers)

        return answers


class ReadOnlySubmissionForm(ReadOnlyForm, SubmissionForm):
    def __init__(self, submission_vm, disable_dropdowns, use_dm_answers=True, *args, **kwargs):
        super(ReadOnlySubmissionForm, self).__init__(submission_vm, use_dm_answers, *args, **kwargs)
        self.make_readonly(disable_dropdowns)

    def make_readonly(self, disable_dropdowns):
        for field_key in self.fields:
            field_key_elems = field_key.split(SubmissionForm.FIELD_KEY_SEPERATOR)
            question_index = int(field_key_elems[0])
            subpart_index = int(field_key_elems[1])
            subpart = self.submission_vm.questions[question_index].subparts[subpart_index]

            field = self.fields[field_key]

            if subpart.type == HWCentralQuestionType.MCSA:
                if not subpart.options.use_dropdown_widget:
                    ReadOnlySubmissionForm.make_field_disabled(field)
                else:
                    if disable_dropdowns:
                        ReadOnlySubmissionForm.make_dropdown_disabled(field.widget)
            elif subpart.type == HWCentralQuestionType.MCMA:
                ReadOnlySubmissionForm.make_field_disabled(field)
            elif subpart.type == HWCentralQuestionType.NUMERIC:
                ReadOnlySubmissionForm.make_field_readonly(field)
            elif subpart.type == HWCentralQuestionType.TEXTUAL:
                ReadOnlySubmissionForm.make_field_readonly(field)
            elif subpart.type == HWCentralQuestionType.CONDITIONAL:
                ReadOnlySubmissionForm.make_field_readonly(field)
            else:
                raise InvalidHWCentralQuestionTypeException(subpart.type)

        # since this is a readonly form, also disable all math toolboxes
        for question in self.submission_vm.questions:
            for subpart in question.subparts:
                if subpart.type == HWCentralQuestionType.TEXTUAL:
                    subpart.show_toolbox = False
                elif subpart.type == HWCentralQuestionType.CONDITIONAL:
                    if subpart.answer.answer_format == HWCentralConditionalAnswerFormat.TEXTUAL:
                        subpart.answer.show_toolbox = False
