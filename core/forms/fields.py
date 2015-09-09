from django.core.exceptions import ValidationError
from django.forms import CharField, TypedMultipleChoiceField, TypedChoiceField, RadioSelect, CheckboxSelectMultiple
from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from core.data_models.answer import TextualAnswer, NumericAnswer
from core.forms.widgets import CustomSelect
from core.utils.helpers import merge_dicts








# NOTE: The validation taking place in this module should be question-agnostic and only depend on the expected answer format
# The validation done here is used by the custom submission form fields as well

TEXTINPUT_MAX_LENGTH = 255

HELP_TEXT_CONTEXT = {'max_char': TEXTINPUT_MAX_LENGTH}

NUMERIC_HELP_TEXT = mark_safe(
    loader.render_to_string('authenticated/question/numeric_help_text.html', HELP_TEXT_CONTEXT))

TEXTUAL_HELP_TEXT = mark_safe(
    loader.render_to_string('authenticated/question/textual_help_text.html', HELP_TEXT_CONTEXT))

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
    'max_length': TEXTINPUT_MAX_LENGTH
}


class MCSAQFormField(TypedChoiceField):
    DROPDOWN_EMPTY_CHOICE = (-1, '-----')

    def __init__(self, choices, use_dropdown_widget, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, MCQ_KWARGS, MCSAQ_KWARGS, kwargs])
        widget = CustomSelect if use_dropdown_widget else RadioSelect
        if use_dropdown_widget:
            choices.insert(0, MCSAQFormField.DROPDOWN_EMPTY_CHOICE)
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


class TextInputFormField(CharField):
    def __init__(self, **kwargs):
        super(TextInputFormField, self).__init__(**kwargs)
        self.widget.attrs['class'] = 'disable_clipboard'


class NumericFormField(TextInputFormField):
    def __init__(self, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, INPUT_KWARGS, kwargs])
        super(NumericFormField, self).__init__(help_text=NUMERIC_HELP_TEXT, **kw_args)
        self.validators.append(numeric_validator)


class TextualFormField(TextInputFormField):
    def __init__(self, show_toolbox, **kwargs):
        kw_args = merge_dicts([SUBMISSION_FIELD_KWARGS, INPUT_KWARGS, kwargs])
        super(TextualFormField, self).__init__(help_text=TEXTUAL_HELP_TEXT, **kw_args)
        if show_toolbox:
            self.widget.attrs['class'] += ' math_toolbox_enabled'
        self.validators.append(textual_validator)

# NOTE: Conditional Form Field just uses multiple Numeric/Textual Form Fields
