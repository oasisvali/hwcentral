from fractions import Fraction

from core.utils.constants import HWCentralConditionalAnswerFormat, HWCentralQuestionType
from core.utils.json import JSONModel
from hwcentral.exceptions import InvalidHWCentralConditionalAnswerFormatError, \
    InvalidHWCentralQuestionTypeError, \
    EvalSanitizationError


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
        raise InvalidHWCentralQuestionTypeError(answer_type)

class SubpartAnswer(JSONModel):
    """
    Abstract class for all kinds of subpart answers
    """

    @classmethod
    def from_data(cls, data):
        return data['correct']

    def __init__(self, correct):
        # a boolean value (or in the case of conditional type answers, a list of boolean values) to denote whether
        # the answer is correct. Initially, this is set to None and ONLY TO BE UPDATED BY THE GRADER
        self.correct = correct

    def calculate_completion(self):
        """
        returns a fraction value between 0 and 1 representing the amount of completion of the answer object
        """
        raise NotImplementedError("Subclass of SubpartAnswer must implement calculate_completion")

    def calculate_mark(self):
        """
        returns a fraction value between 0 and 1 representing the marks obtained by the answer. Prior checking required
        """
        if self.correct:
            return 1
        else:
            return 0

    def check_answer(self, subpart_question):
        """
        checks the answer with respect to the given subpart question and updates its correct field
        """
        raise NotImplementedError("Subclass of SubpartAnswer must implement check_answer")


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
        from core.forms.fields import MCSAQFormField
        if choice == MCSAQFormField.DROPDOWN_EMPTY_CHOICE[0]:
            choice = None
        return cls(choice, None)

    @classmethod
    def from_data(cls, data):
        choice = data['choice']
        assert MCSAQAnswer.valid_choice(choice)
        return cls(choice, super(MCSAQAnswer, cls).from_data(data))

    def __init__(self, choice, correct):
        super(MCSAQAnswer, self).__init__(correct)
        self.choice = choice

    def calculate_completion(self):
        if self.choice is None:
            return 0
        else:
            return 1

    def check_answer(self, subpart_question):
        if self.choice is None:
            self.correct = False
            return

        # note that the correct option is always the first element of the combined options list
        self.correct = (subpart_question.options.order[self.choice] == 0)


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

    def __init__(self, choices, correct):
        super(MCMAQAnswer, self).__init__(correct)
        self.choices = choices

    def calculate_completion(self):
        if len(self.choices) > 0:
            return 1
        else:
            return 0

    def check_answer(self, subpart_question):
        # note that the correct options are always put at the start of the combined options list
        chosen_options = []
        for choice in self.choices:
            chosen_options.append(subpart_question.options.order[choice])

        correct_options = xrange(len(subpart_question.options.correct))

        self.correct = (
            set(correct_options) == set(
                chosen_options))  # using unordered comparison because ordering of selected choices
        # is handled by django


class TextInputAnswer(SubpartAnswer):
    @classmethod
    def coerce_textinput(cls, textinput):
        textinput = textinput.strip()
        if textinput == '':
            return None
        return textinput

    def __init__(self, value, correct):
        super(TextInputAnswer, self).__init__(correct)
        self.value = value

    @classmethod
    def from_form_field(cls, value):
        # no validation required here as the form fields already apply the same validation at field level using validators
        return cls(TextInputAnswer.coerce_textinput(value), None)

    @classmethod
    def build_shell(cls):
        return cls(None, None)

    def calculate_completion(self):
        if self.value is None:
            return 0
        else:
            return 1


class NumericAnswer(TextInputAnswer):

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

        # these check to prevent form field validator from blowing up
        if answer == None:
            return None
        answer = answer.strip()
        if answer == '':
            return None

        value_parts = answer.split('|')
        if len(value_parts) > 2:
            raise ValueError('Invalid mixed fraction form %s' % answer)

        value_multiplier = 1
        if value_parts[0][0] == '-':
            value_parts[0] = value_parts[0][1:]
            value_multiplier = -1

        return value_multiplier * (float(sum(Fraction(s) for s in value_parts)))

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

    def check_answer(self, subpart_question):
        if self.value is None:
            self.correct = False
            return

        value = NumericAnswer.evaluate(self.value)
        if subpart_question.answer.tolerance is None:
            self.correct = (value == subpart_question.answer.value)
        else:
            self.correct = (abs(value - subpart_question.answer.value) <= subpart_question.answer.tolerance)

class TextualAnswer(TextInputAnswer):

    @classmethod
    def valid_textual(cls, answer):
        return True  # no validation for textual right now - anything goes (answer is to be lowercased only during checking))

    @classmethod
    def from_data(cls, data):
        value = data['value']
        assert TextualAnswer.valid_textual(value)
        return cls(value, super(TextualAnswer, cls).from_data(data))

    def check_answer(self, subpart_question):
        if self.value is None:
            self.correct = False
            return
        self.correct = (self.value.lower() == subpart_question.answer)


class ConditionalAnswer(SubpartAnswer):
    """
    Depending on the answer format, it uses numeric validation or no validation (for textual)
    """

    @classmethod
    def build_shell(cls):
        return cls([], None)

    @classmethod
    def from_form_field(cls, values):
        # no validation required here as the form fields already apply the same validation at field level using validators
        return cls([TextInputAnswer.coerce_textinput(value) for value in values], None)

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
            raise InvalidHWCentralConditionalAnswerFormatError(conditional_answer_format)

        return cls(values, super(ConditionalAnswer, cls).from_data(data))

    @classmethod
    def sanitize_for_eval(cls, value):
        """
        Sanitizes user input for eval. The following are not allowed:
        lambda ^ \n <whitespace> _ { } ( ) : [ ]
        """

        DISALLOWED = ['lambda', '^', '\n', ' ', '_', '{', '}', '(', ')', ':', '[', ']']

        for disallowed in DISALLOWED:
            if disallowed in value:
                raise EvalSanitizationError('Found disallowed \'%s\' in %s' % (disallowed, value))

        return value

    @classmethod
    def safe_eval(cls, value, condition):
        return eval(condition, {'__builtins__': {}}, {'value': value})

    def __init__(self, values, correct):
        super(ConditionalAnswer, self).__init__(correct)
        self.values = values

    def calculate_completion(self):
        if len(self.values) == 0:
            return 0
        else:
            completed_values = 0
            for value in self.values:
                if value is not None:
                    completed_values += 1
            return float(completed_values) / len(self.values)

    def calculate_mark(self):
        assert len(self.correct) > 0
        return sum(self.correct) / float(len(self.correct))

    def check_answer(self, subpart_question):
        self.correct = []
        if len(self.values) == 0:
            self.correct = [False] * subpart_question.answer.num_answers
            return

        assert len(self.values) == subpart_question.answer.num_answers
        for value in self.values:
            if value is None:
                self.correct.append(False)
                continue

            if subpart_question.answer.answer_format == HWCentralConditionalAnswerFormat.NUMERIC:
                value = NumericAnswer.evaluate(value)
            elif subpart_question.answer.answer_format == HWCentralConditionalAnswerFormat.TEXTUAL:
                try:
                    value = value.lower()
                    value = ConditionalAnswer.sanitize_for_eval(value)
                except EvalSanitizationError:
                    self.correct.append(False)
                    continue
            else:
                raise InvalidHWCentralConditionalAnswerFormatError(subpart_question.answer.answer_format)

            self.correct.append(ConditionalAnswer.safe_eval(value, subpart_question.answer.condition))
