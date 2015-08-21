from fractions import Fraction

from core.utils.constants import HWCentralConditionalAnswerFormat, HWCentralQuestionType
from core.utils.json import JSONModel
from hwcentral.exceptions import InvalidHWCentralConditionalAnswerFormatException, InvalidHWCentralQuestionTypeException


def build_shell_answer(answer_type):
    if answer_type == HWCentralQuestionType.MCSA:
        return MCSAQAnswer.build_shell()
    elif answer_type == HWCentralQuestionType.MCMA:
        return MCMAQAnswer.build_shell()
    elif answer_type == HWCentralQuestionType.NUMERIC:
        return NumericAnswer.build_shell()
    elif answer_type == HWCentralQuestionType.TEXTUAL:
        return TextualAnswer.build_shell()
    elif answer_type == HWCentralQuestionType.CONDITIONAL:
        return ConditionalAnswer.build_shell()
    else:
        raise InvalidHWCentralQuestionTypeException(answer_type)

class SubpartAnswer(JSONModel):
    """
    Abstract class for all kinds of subpart answers
    """

    @classmethod
    def from_data(cls, data):
        return data['correct_ratio']

    def __init__(self, correct_ratio):
        # a float value (or in the case of conditional type answers, a list of float values) to describe how correct
        # (as a value from 0-1) the answer is this is set to None and ONLY TO BE UPDATED BY THE GRADER
        self.correct_ratio = correct_ratio


class MCQAnswer(SubpartAnswer):
    """
    Abstract class to reduce duplication b/w MCQ-type answers
    """
    pass


class MCSAQAnswer(MCQAnswer):

    @classmethod
    def valid_choice(cls, choice):
        return (choice is None) or (choice >= 0)

    @classmethod
    def build_shell(cls):
        return cls(None, None)

    @classmethod
    def from_form_field(cls, choice):
        return cls(choice, None)

    @classmethod
    def from_data(cls, data):
        choice = data['choice']
        assert MCSAQAnswer.valid_choice(choice)
        return cls(choice, super(MCSAQAnswer, cls).from_data(data))

    def __init__(self, choice, correct_ratio):
        super(MCSAQAnswer, self).__init__(correct_ratio)
        self.choice = choice


class MCMAQAnswer(MCQAnswer):
    @classmethod
    def build_shell(cls):
        return cls([], None)

    @classmethod
    def from_form_field(cls, choices):
        return cls(choices, None)

    @classmethod
    def valid_choices(cls, choices):
        for choice in choices:
            if choice < 0:
                return False
        return True

    @classmethod
    def from_data(cls, data):
        choices = data['choices']
        assert MCMAQAnswer.valid_choices(choices)
        return cls(choices, super(MCMAQAnswer, cls).from_data(data))

    def __init__(self, choices, correct_ratio):
        super(MCMAQAnswer, self).__init__(correct_ratio)
        self.choices = choices


class TextInputAnswer(SubpartAnswer):
    @classmethod
    def coerce_textinput(cls, textinput):
        if textinput == '':
            return None
        return textinput


class NumericAnswer(TextInputAnswer):
    @classmethod
    def build_shell(cls):
        return cls(None, None)

    @classmethod
    def from_form_field(cls, value):
        # no validation required here as the form fields already apply the same validation at field level using validators
        return cls(NumericAnswer.coerce_textinput(value), None)

    @classmethod
    def evaluate(cls, answer):
        """
        Accepted numeric answer formats:
            int
            float
            fraction - negative sign only on the numerator
            mixed fraction - fraction and whole seperated by '|' e.g. -1|-2/3
            scientific notation - e.g. 1.35e+10 or 1.35e10 or 1.35e-10 uppercase E will also work

        Special Case: empty string evaluates to None

        @param answer: string entered by the student as numeric answer
        @return: evaluated float value
        @throws: ValueError, if answer is not in correct format (see supported formats above)
        """
        if answer == '':
            return None
        value_parts = answer.split('|')
        if len(value_parts) > 2:
            raise ValueError('Invalid mixed fraction form %s' % answer)
        return float(sum(Fraction(s) for s in value_parts))

    @classmethod
    def valid_numeric(cls, answer):
        try:
            NumericAnswer.evaluate(answer)
            return True
        except ValueError:
            return False
        except ZeroDivisionError:  # fraction with denominator 0
            return False

    @classmethod
    def from_data(cls, data):
        value = data['value']  # Not casting to float because fraction inputs are to be saved as string and only
        # evaluated during checking
        assert NumericAnswer.valid_numeric(value)

        return cls(value, super(NumericAnswer, cls).from_data(data))

    def __init__(self, value, correct_ratio):
        super(NumericAnswer, self).__init__(correct_ratio)
        self.value = value


class TextualAnswer(TextInputAnswer):

    @classmethod
    def build_shell(cls):
        return cls(None, None)

    @classmethod
    def from_form_field(cls, value):
        # no validation required here as the form fields already apply the same validation at field level using validators
        return cls(TextualAnswer.coerce_textinput(value), None)

    @classmethod
    def valid_textual(cls, answer):
        return True  # no validation for textual right now - anything goes (answer is to be lowercased only during checking))

    @classmethod
    def from_data(cls, data):
        value = data['value']
        assert TextualAnswer.valid_textual(value)
        return cls(value, super(TextualAnswer, cls).from_data(data))

    def __init__(self, value, correct_ratio):
        super(TextualAnswer, self).__init__(correct_ratio)
        self.value = value


class ConditionalAnswer(TextInputAnswer):
    """
    Depending on the answer format, it uses numeric validation or no validation (for textual)
    """

    @classmethod
    def build_shell(cls):
        return cls([], None)

    @classmethod
    def from_form_field(cls, values):
        # no validation required here as the form fields already apply the same validation at field level using validators
        return cls([ConditionalAnswer.coerce_textinput(value) for value in values], None)

    @classmethod
    def from_data(cls, data, conditional_answer_format):
        values = data['values']
        if conditional_answer_format == HWCentralConditionalAnswerFormat.NUMERIC:
            for value in values:
                assert NumericAnswer.valid_numeric(value)
        elif conditional_answer_format == HWCentralConditionalAnswerFormat.TEXTUAL:
            for value in values:
                assert TextualAnswer.valid_textual(value)
        else:
            raise InvalidHWCentralConditionalAnswerFormatException(conditional_answer_format)

        return cls(values, super(ConditionalAnswer, cls).from_data(data))

    def __init__(self, values, correct_ratio):
        super(ConditionalAnswer, self).__init__(correct_ratio)
        self.values = values
