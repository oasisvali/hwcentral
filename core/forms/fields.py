from django.core.exceptions import ValidationError
from django.forms import CharField, TypedMultipleChoiceField, TypedChoiceField, RadioSelect, Select, \
    CheckboxSelectMultiple, TextInput
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from core.data_models.answer import TextualAnswer, NumericAnswer
from core.utils.helpers import merge_dicts



# NOTE: The validation taking place in this module should be question-agnostic and only depend on the expected answer format
# The validation done here is used by the custom submission form fields as well

TEXTINPUT_MAX_LENGTH = 255

NUMERIC_HELP_TEXT = mark_safe((
                        'Enter a number in any of these formats:'
                        '<br/>'
                        'Integer -&gt; -4'
                        '<br/>'
                        'Decimal -&gt; 4.23'
                        '<br/>'
                        'Fraction -&gt; 2/35 (negative sign only allowed on numerator)'
                        '<br/>'
                        'Mixed Fraction -&gt; 1|5/7 (whole and fraction parts seperated by |)'
                        '<br/>'
                        'Scientific Notation -&gt; 1.35e-10 (base 10 exponent)'
                        '<br/><br/>'
                        '(Max %s characters)'
                              ) % TEXTINPUT_MAX_LENGTH)

TEXTUAL_HELP_TEXT = mark_safe('Answer is case-insensitive (Max %i characters)' % TEXTINPUT_MAX_LENGTH)

SUBMISSION_FIELD_KWARGS = {
    'required': False,  # assignment fields may be left empty in a valid submission
    'label': ''
}

MCQ_KWARGS = {
    'coerce': int
}

MCSAQ_KWARGS = {
    'empty_value': None
}

MCMAQ_KWARGS = {
    'empty_value': []
}

INPUT_KWARGS = {
    'widget': TextInput,
    'max_length': TEXTINPUT_MAX_LENGTH
}


class MCSAQFormField(TypedChoiceField):
    def __init__(self, choices, use_dropdown_widget, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, MCQ_KWARGS, MCSAQ_KWARGS, kwargs])
        widget = Select if use_dropdown_widget else RadioSelect
        super(MCSAQFormField, self).__init__(widget=widget,
                                             choices=choices,
                                             **kw_args)


class MCMAQFormField(TypedMultipleChoiceField):
    def __init__(self, choices, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, MCQ_KWARGS, MCMAQ_KWARGS, kwargs])
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
    def __init__(self, show_toolbox, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, INPUT_KWARGS, kwargs])
        super(NumericFormField, self).__init__(help_text=NUMERIC_HELP_TEXT, **kw_args)
        if show_toolbox:
            self.widget.attrs['class'] = 'math_toolbox_enabled'
        self.validators.append(numeric_validator)


class TextualFormField(CharField):
    def __init__(self, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, INPUT_KWARGS, kwargs])
        super(TextualFormField, self).__init__(help_text=TEXTUAL_HELP_TEXT, **kw_args)
        self.validators.append(textual_validator)


        # NOTE: Conditional Form Field just uses multiple Numeric/Textual Form Fields
