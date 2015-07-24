from fractions import Fraction

from core.utils.json import JSONModel


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
        self.choice = int(data)
        assert MCQAnswer.valid_choice(self.choice)


class MCMAQAnswer(MCQAnswer):
    def __init__(self, data):
        super(MCMAQAnswer, self).__init__()
        self.choices = []
        for elem in data:
            choice = int(elem)
            assert MCQAnswer.valid_choice(choice)
            self.choices.append(choice)


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

    def __init__(self, data):
        super(NumericAnswer, self).__init__()
        self.value = data  # Not casting to float because fraction inputs are to be saved as string and only
        # evaluated during checking


class TextualAnswer(SubpartAnswer):
    def __init__(self, data):
        super(TextualAnswer, self).__init__()
        self.value = data


class ConditionalAnswer(SubpartAnswer):
    """
    By default this looks for numeric answers, but can also be used for specifying a number of correct text out of a set
    of correct text
    """

    def __init__(self, data):
        super(ConditionalAnswer, self).__init__()
        for value in data:
            assert NumericAnswer.valid_numeric(value)
        self.values = data
