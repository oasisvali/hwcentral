from django.core.exceptions import ValidationError
from django.forms import forms, RadioSelect, CheckboxSelectMultiple, TextInput, TypedChoiceField, \
    TypedMultipleChoiceField, CharField, Select
from django.utils.translation import ugettext_lazy as _

from core.data_models.answer import NumericAnswer, TextualAnswer, ConditionalAnswer, MCSAQAnswer, MCMAQAnswer
from core.forms.base import ReadOnlyForm
from core.utils.constants import HWCentralQuestionType, HWCentralConditionalAnswerFormat
from hwcentral.exceptions import InvalidHWCentralConditionalAnswerFormatException, InvalidHWCentralQuestionTypeException


TEXTINPUT_MAX_LENGTH = 255

NUMERIC_HELP_TEXT = (
                        'Enter a number in any of these formats:'
                        '<br/>'
                        'Integer -> -4'
                        '<br/>'
                        'Decimal -> 4.23'
                        '<br/>'
                        'Fraction -> 2/35 (negative sign only allowed on numerator)'
                        '<br/>'
                        'Mixed Fraction -> 1|5/7 (whole and fraction parts seperated by |)'
                        '<br/>'
                        'Scientific Notation -> 1.35e-10 (base 10 exponent)'
                        '<br/><br/>'
                        '(Max %s characters)'
                    ) % TEXTINPUT_MAX_LENGTH

TEXTUAL_HELP_TEXT = 'Enter the answer which will be checked by a case-insensitive comparison (Max %i characters)' % TEXTINPUT_MAX_LENGTH

SUBMISSION_FIELD_KWARGS = {
    'required': False  # assignment fields may be left empty in a valid submission
}

MCQ_KWARGS = {
    'coerce': int,
    'empty_value': None,
    'label': ''
}

INPUT_KWARGS = {
    'label': 'Ans',
    'widget': TextInput,
    'max_length': TEXTINPUT_MAX_LENGTH
}


def merge_dicts(dict_list):
    """
    dict with higher index overwrites dict with lower index in case of matching key
    """
    merged_dict = {}
    for dictionary in dict_list:
        merged_dict.update(dictionary)
    return merged_dict


def coerce_textinput(textinput):
    if textinput == '':
        return None
    return textinput


class MCSAQFormField(TypedChoiceField):
    def __init__(self, choices, use_dropdown_widget, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, MCQ_KWARGS, kwargs])
        widget = Select if use_dropdown_widget else RadioSelect
        super(MCSAQFormField, self).__init__(widget=widget,
                                             choices=choices,
                                             **kw_args)


class MCMAQFormField(TypedMultipleChoiceField):
    def __init__(self, choices, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, MCQ_KWARGS, kwargs])
        super(MCMAQFormField, self).__init__(widget=CheckboxSelectMultiple,
                                             choices=choices,
                                             **kw_args)


def numeric_validator(value):
    if not NumericAnswer.valid_numeric(value):
        raise ValidationError(
            _('Invalid value: %(value)s. Numeric answer must be in one of the accepted formats listed under \'?\''),
            code='invalid',
            params={'value': value}
        )


def textual_validator(value):
    if not TextualAnswer.valid_textual(value):
        raise ValidationError(
            _('Invalid value: %(value)s. Textual answer must be in the accepted format listed under \'?\''),
            code='invalid',
            params={'value': value}
        )


class NumericFormField(CharField):
    def __init__(self, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, INPUT_KWARGS, kwargs])
        super(NumericFormField, self).__init__(help_text=NUMERIC_HELP_TEXT, **kw_args)
        self.validators.append(numeric_validator)


class TextualFormField(CharField):
    def __init__(self, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, INPUT_KWARGS, kwargs])
        super(TextualFormField, self).__init__(help_text=TEXTUAL_HELP_TEXT, **kw_args)
        self.validators.append(textual_validator)


# NOTE: Conditional Form Field just uses multiple Numeric/Textual Form Fields

class SubmissionForm(forms.Form, ReadOnlyForm):

    """
    Contains a flattened list of assignment subparts as fields on the form
    """

    @classmethod
    def build_subpart_field_key(cls, question_index, subpart_index):
        return "%(question_index)i_%(subpart_index)i" % {
            'question_index': question_index,
            'subpart_index': subpart_index,
        }

    @classmethod
    def build_conditional_subfield_key(cls, question_index, subpart_index, subfield_index):
        return "%(question_index)i_%(subpart_index)i_%(subfield_index)i" % {
            'question_index': question_index,
            'subpart_index': subpart_index,
            'subfield_index': subfield_index
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
                value.append(option.text)
            if option.img_url is not None:
                value.append(SubmissionForm.build_img_choice_tag(option.img_url))

            choices.append((i, ''.join(value)))

        return choices

    def __init__(self, submission_dm, *args, **kwargs):
        self.submission = submission_dm
        super(SubmissionForm, self).__init__(*args, **kwargs)
        # create a form field for each subpart
        for i, question in enumerate(self.submission.questions):
            for j, subpart in enumerate(question.subparts):
                if subpart.type == HWCentralQuestionType.CONDITIONAL:
                    for k in xrange(subpart.answer.num_answers):
                        field_key = SubmissionForm.build_conditional_subfield_key(i, j, k)

                        conditional_format = subpart.answer.answer_format

                        if conditional_format == HWCentralConditionalAnswerFormat.NUMERIC:
                            field = NumericFormField()
                        elif conditional_format == HWCentralConditionalAnswerFormat.TEXTUAL:
                            field = TextualFormField()
                        else:
                            raise InvalidHWCentralConditionalAnswerFormatException(conditional_format)

                        self.fields[field_key] = field
                else:
                    field_key = SubmissionForm.build_subpart_field_key(i, j)

                    if subpart.type == HWCentralQuestionType.MCSA:
                        combined_options = [subpart.options.correct_option]
                        combined_options.extend(subpart.options.incorrect_options)
                        choices = SubmissionForm.build_choices(combined_options, subpart.options.order)
                        field = MCSAQFormField(choices, subpart.options.use_dropdown_widget)
                    elif subpart.type == HWCentralQuestionType.MCMA:
                        combined_options = subpart.options.correct_options
                        combined_options.extend(subpart.options.incorrect_options)
                        choices = SubmissionForm.build_choices(combined_options, subpart.options.order)
                        field = MCMAQFormField(choices)
                    elif subpart.type == HWCentralQuestionType.NUMERIC:
                        field = NumericFormField()
                    elif subpart.type == HWCentralQuestionType.TEXTUAL:
                        field = TextualFormField()

                    else:
                        raise InvalidHWCentralQuestionTypeException(subpart.type)

                    self.fields[field_key] = field

    def get_field_count(self):
        """
        Calculates how many fields should be in this form based on the submission data model associated with it
        """
        field_count = 0

        for question in self.submission.questions:
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

        expected_field_count = self.get_field_count()
        actual_field_count = len(self.cleaned_data)
        if actual_field_count != expected_field_count:
            raise ValidationError(
                'Field count mismatch. expected: %s found: %s' % (expected_field_count, actual_field_count),
                'field_count_mismatch')

        for i, question in enumerate(self.submission.questions):
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

        answers = [[]] * len(self.submission.questions)  # building a new list to store lists of Answer data models

        for i, question in enumerate(self.submission.questions):
            for j, subpart in enumerate(question.subparts):

                if subpart.type == HWCentralQuestionType.CONDITIONAL:
                    conditional_subpart_answers = []
                    for k in xrange(subpart.answer.num_answers):
                        field_key = SubmissionForm.build_conditional_subfield_key(i, j, k)
                        conditional_subanswer_data = coerce_textinput(self.cleaned_data[field_key])

                        conditional_subpart_answers.append(conditional_subanswer_data)

                    subpart_answer = ConditionalAnswer(conditional_subpart_answers, subpart.answer.answer_format)
                else:
                    field_key = SubmissionForm.build_subpart_field_key(i, j)
                    subpart_answer_data = self.cleaned_data[field_key]

                    if subpart.type == HWCentralQuestionType.MCSA:
                        subpart_answer = MCSAQAnswer(subpart_answer_data)
                    elif subpart.type == HWCentralQuestionType.MCMA:
                        subpart_answer = MCMAQAnswer(subpart_answer_data)
                    elif subpart.type == HWCentralQuestionType.NUMERIC:
                        subpart_answer = NumericAnswer(coerce_textinput(subpart_answer_data))
                    elif subpart.type == HWCentralQuestionType.TEXTUAL:
                        subpart_answer = TextualAnswer(coerce_textinput(subpart_answer_data))
                    else:
                        raise InvalidHWCentralQuestionTypeException(subpart.type)

                answers[i].append(subpart_answer)

        return answers



