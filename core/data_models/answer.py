from fractions import Fraction

from core.utils.constants import HWCentralConditionalAnswerFormat
from core.utils.json import JSONModel


# NOTE: The validation taking place in this module should be question-agnostic and only depend on the expected answer format
# The validation done here is used by the custom submission form fields as well

from hwcentral.exceptions import InvalidHWCentralConditionalAnswerFormatException


class SubpartAnswer(JSONModel):
    """
    Base class for all kinds of subpart answers
    """

    def __init__(self):
        # a float value to describe how correct (as a value from 0-1) the answer is
        # this is set to None and ONLY TO BE UPDATED BY THE GRADER
        self.correct_ratio = None


class MCQAnswer(SubpartAnswer):
    @classmethod
    def valid_choice(cls, choice):
        assert choice >= 0


class MCSAQAnswer(MCQAnswer):
    def __init__(self, data):
        super(MCSAQAnswer, self).__init__()
        self.choice = data
        assert MCQAnswer.valid_choice(self.choice)


class MCMAQAnswer(MCQAnswer):
    def __init__(self, data):
        super(MCMAQAnswer, self).__init__()
        self.choices = []
        for elem in data:
            assert MCQAnswer.valid_choice(elem)
            self.choices.append(elem)


class NumericAnswer(SubpartAnswer):
    @classmethod
    def evaluate(cls, answer):
        """
        Accepted numeric answer formats:
            int
            float
            fraction - negative sign only on the numerator
            mixed fraction - fraction and whole seperated by '|' e.g. -1|-2/3
            scientific notation - e.g. 1.35e+10 or 1.35e10 or 1.35e-10 uppercase E will also work

        @param answer: string entered by the student as numeric answer
        @return: evaluated float value
        @throws: ValueError, if answer is not in correct format (see supported formats above)
        """
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

    def __init__(self, data):
        super(NumericAnswer, self).__init__()
        assert NumericAnswer.valid_numeric(data)
        self.value = data  # Not casting to float because fraction inputs are to be saved as string and only
        # evaluated during checking


class TextualAnswer(SubpartAnswer):
    @classmethod
    def valid_textual(cls, answer):
        return True  # no validation for textual right now - anything goes (answer is to be lowercased only during checking))

    def __init__(self, data):
        super(TextualAnswer, self).__init__()
        assert TextualAnswer.valid_textual(data)
        self.value = data


class ConditionalAnswer(SubpartAnswer):
    """
    Depending on the answer format, it uses numeric validation or no validation (for textual)
    """

    def __init__(self, data, format):
        super(ConditionalAnswer, self).__init__()
        if format == HWCentralConditionalAnswerFormat.NUMERIC:
            for value in data:
                assert NumericAnswer.valid_numeric(value)
        elif format == HWCentralConditionalAnswerFormat.TEXTUAL:
            for value in data:
                assert TextualAnswer.valid_textual(value)
        else:
            raise InvalidHWCentralConditionalAnswerFormatException(format)
        self.values = data
