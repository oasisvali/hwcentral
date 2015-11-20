from decimal import Decimal, InvalidOperation
from unittest import TestCase

from mock import NonCallableMagicMock, MagicMock

from core.data_models.answer import SubpartAnswer, MCSAQAnswer, MCMAQAnswer, TextInputAnswer, NumericAnswer, \
    TextualAnswer, ConditionalAnswer
from core.forms.fields import MCSAQFormField
from core.tests.base import TCData
from core.utils.constants import HWCentralConditionalAnswerFormat
from hwcentral.exceptions import EvalSanitizationError


class SubpartAnswerTest(TestCase):
    def test_calculate_mark(self):
        test_cases = [
            TCData(True, 1),
            TCData(False, 0)
        ]
        for test_case in test_cases:
            self.assertEqual(SubpartAnswer(test_case.input).calculate_mark(), test_case.expected_output)


class MCSAQAnswerTest(TestCase):
    def test_valid_choice(self):
        test_cases = [
            TCData(None, True),
            TCData(0, True),
            TCData(3, True),
            TCData(-1, False)
        ]
        for test_case in test_cases:
            self.assertEqual(MCSAQAnswer.valid_choice(test_case.input), test_case.expected_output)

    def test_from_form_field(self):
        test_cases = [
            TCData(MCSAQFormField.DROPDOWN_EMPTY_CHOICE[0], None),
            TCData(1, 1),
            TCData(0, 0),
            TCData(2, 2)
        ]
        for test_case in test_cases:
            mcsaq_answer = MCSAQAnswer.from_form_field(test_case.input)
            self.assertEqual(mcsaq_answer.choice, test_case.expected_output)
            self.assertEqual(mcsaq_answer.correct, None)

    def test_calculate_completion(self):
        test_cases = [
            TCData(None, 0),
            TCData(0, 1),
            TCData(1, 1),
            TCData(3, 1)
        ]
        for test_case in test_cases:
            mcsaq_answer = MCSAQAnswer(test_case.input, None)
            self.assertEqual(mcsaq_answer.calculate_completion(), test_case.expected_output)

    def test_check_answer(self):
        test_cases = [
            TCData(([0, 3, 1, 2], 0), True),
            TCData(([2, 1, 0], 2), True),
            TCData(([2, 0, 1], None), False),
            TCData(([3, 1, 2, 0], 2), False)
        ]

        for test_case in test_cases:
            subpart_question_mock = NonCallableMagicMock(spec_set=['options'])
            subpart_question_mock.options = NonCallableMagicMock(spec_set=['order'])
            subpart_question_mock.options.order = test_case.input[0]

            mcsaq_answer = MCSAQAnswer(test_case.input[1], None)
            mcsaq_answer.check_answer(subpart_question_mock)
            self.assertEqual(mcsaq_answer.correct, test_case.expected_output)


class MCMAQAnswerTest(TestCase):
    def test_valid_choices(self):
        test_cases = [
            TCData([], True),
            TCData([0], True),
            TCData([0, 3], True),
            TCData([0, -1, 3], False),
            TCData([-2, -1], False)
        ]
        for test_case in test_cases:
            self.assertEqual(MCMAQAnswer.valid_choices(test_case.input), test_case.expected_output)

    def test_calculate_completion(self):
        test_cases = [
            TCData([], 0),
            TCData([1], 1),
            TCData([0, 2], 1),
            TCData([0, 1, 2, 3], 1)
        ]
        for test_case in test_cases:
            mcmaq_answer = MCMAQAnswer(test_case.input, None)
            self.assertEqual(mcmaq_answer.calculate_completion(), test_case.expected_output)

    def test_check_answer(self):
        test_cases = [
            TCData(([0, 3, 1, 2], 2, [0, 2]), True),
            TCData(([2, 1, 0], 2, [1, 2]), True),
            TCData(([2, 0, 1], 1, [1]), True),
            TCData(([3, 1, 2, 0], 2, [1, 3]), True),
            TCData(([3, 1, 2, 0], 2, [3, 1]), True),
            TCData(([3, 1, 2, 0], 4, [3, 1, 0, 2]), True),
            TCData(([3, 1, 2, 0], 4, [3, 1, 2, 0]), True),

            TCData(([0, 3, 1, 2], 1, [0, 1]), False),
            TCData(([2, 1, 0], 2, []), False),
            TCData(([2, 0, 1], 1, [0, 2]), False),
            TCData(([3, 1, 2, 0], 1, [1]), False),
            TCData(([1, 3, 2, 0], 2, [3, 1]), False),
            TCData(([3, 1, 2, 0], 4, [1, 2, 0]), False)
        ]

        for test_case in test_cases:
            subpart_question_mock = NonCallableMagicMock(spec_set=['options'])
            subpart_question_mock.options = NonCallableMagicMock(spec_set=['order', 'correct'])
            subpart_question_mock.options.order = test_case.input[0]
            subpart_question_mock.options.correct = NonCallableMagicMock(spec_set=['__len__'])
            subpart_question_mock.options.correct.__len__ = MagicMock(return_value=test_case.input[1])

            mcmaq_answer = MCMAQAnswer(test_case.input[2], None)
            mcmaq_answer.check_answer(subpart_question_mock)
            self.assertEqual(mcmaq_answer.correct, test_case.expected_output)


class TextInputAnswerTest(TestCase):
    def test_coerce_textinput(self):
        test_cases = [
            TCData(' ', None),
            TCData('', None),
            TCData('\t ', None),
            TCData(' foo ', 'foo'),
            TCData('  bar', 'bar')
        ]
        for test_case in test_cases:
            self.assertEqual(TextInputAnswer.coerce_textinput(test_case.input), test_case.expected_output)

    def test_calculate_completion(self):
        test_cases = [
            TCData(None, 0),
            TCData('foo', 1),
            TCData('bar', 1)
        ]

        for test_case in test_cases:
            text_input_answer = TextInputAnswer(test_case.input, None)
            self.assertEqual(text_input_answer.calculate_completion(), test_case.expected_output)


class NumericAnswerTest(TestCase):
    def test_evaluate(self):
        test_cases = [
            TCData(None, None),
            TCData(' ', None),
            TCData('', None),
            TCData(' \t', None),
            TCData('23', Decimal(23)),
            TCData('-43', Decimal(-43)),
            TCData('0', Decimal(0)),
            TCData('-34.12', Decimal('-34.12')),
            TCData(' - 10', Decimal(-10)),
            TCData('-  45.21 ', Decimal('-45.21')),
            TCData('0.005', Decimal('0.005')),
            TCData('0.00', Decimal(0)),
            TCData('34/7', Decimal(34) / Decimal(7)),
            TCData('- 45 / 44', Decimal(-45) / Decimal(44)),
            TCData('-46/51', Decimal(-46) / Decimal(51)),
            TCData(' 10/ 2', Decimal(5)),
            TCData('0/11', Decimal(0))
        ]

        for test_case in test_cases:
            self.assertEqual(NumericAnswer.evaluate(test_case.input), test_case.expected_output)

    def test_evaluate_exceptions(self):
        test_cases = [
            TCData('foo', InvalidOperation),
            TCData('450o', InvalidOperation),
            TCData('1e45', ValueError),
            TCData('-3.1 E-45', ValueError),
            TCData('0.1/23', ValueError),
            TCData('21e-45', ValueError),
            TCData('-34e2', ValueError),
            TCData('1e5/-0.45', ValueError),
            TCData('17/-4', ValueError),
            TCData('- 5/-6', ValueError),
            TCData('7/0', ValueError),
            TCData('0/0', ValueError),
            TCData('45/5/6', ValueError)
        ]

        for test_case in test_cases:
            with self.assertRaises(test_case.expected_output):
                NumericAnswer.evaluate(test_case.input)

    def test_check_answer(self):
        test_cases = [
            TCData(('12', None, '11.99'), False),
            TCData(('1', None, '1001/1000'), False),
            TCData(('19.45', None, '19.455'), False),
            TCData(('19.45', None, '19.4500'), True),
            TCData(('6.25', None, '25/4'), True),
            TCData(('6.25', None, '6.25'), True),
            TCData(('19.45000000', None, '19.450'), True),

            TCData(('-1.7', 0.05, '- 10/6'), True),
            TCData(('1.47', 0.01, '1.459'), True),
            TCData((str(Decimal(22) / Decimal(7)), 0.02, '3.129'), True),
            TCData(('1.292', 0.005, '1.2983'), False),
            TCData(('1.292', 0.005, '1.2857'), False),
            TCData(('1.292', 0.005, '1.29299'), True),
        ]

        for test_case in test_cases:
            subpart_question_mock = NonCallableMagicMock(spec_set=['answer'])
            subpart_question_mock.answer = NonCallableMagicMock(spec_set=['tolerance', 'value'])
            subpart_question_mock.answer.value = test_case.input[0]
            subpart_question_mock.answer.tolerance = test_case.input[1]

            numeric_answer = NumericAnswer(test_case.input[2], None)
            numeric_answer.check_answer(subpart_question_mock)
            self.assertEqual(numeric_answer.correct, test_case.expected_output)


class TextualAnswerTest(TestCase):

    def test_check_answer(self):
        test_cases = [
            TCData((' JawAHArLal  Nehru ', 'Jawaharlal Nehru'), True),
            TCData(('jawaharlalnehru', 'Jawaharlal Nehru'), False),
            TCData(('\t\t FooBAR ', 'foobar'), True),
            TCData((None, 'foobar'), False),
            TCData(('banana', 'foobar'), False),
            TCData(('foobar', 'FooBar'), True),
            TCData(('Jawaharlal nehroo', 'Jawaharlal Nehru'), False),
            TCData(('jawaharlal\tnehru', 'Jawaharlal Nehru'), True),
        ]

        for test_case in test_cases:
            subpart_question_mock = NonCallableMagicMock(spec_set=['answer'])
            subpart_question_mock.answer = test_case.input[1]

            textual_answer = TextualAnswer(test_case.input[0], None)
            textual_answer.check_answer(subpart_question_mock)
            self.assertEqual(textual_answer.correct, test_case.expected_output)


class ConditionalAnswerTest(TestCase):
    def test_sanitize_for_eval(self):
        test_cases = [
            TCData('lambda', True),
            TCData('foo\nbar', True),
            TCData('__import__', True),
            TCData('def fun():\n\texit()', True),

            TCData('12*3', False),
            TCData('1.89', False),
            TCData('34/57', False),
            TCData('-56', False),
            TCData('Jawaharlal Nehru', False)
        ]

        for test_case in test_cases:
            if test_case.expected_output:
                with self.assertRaises(EvalSanitizationError):
                    ConditionalAnswer.sanitize_for_eval(test_case.input)
            else:
                self.assertEqual(ConditionalAnswer.sanitize_for_eval(test_case.input), test_case.input)

    def test_safe_eval(self):
        test_cases = [
            TCData((Decimal(12), '_value_ < 15'), True),
            TCData((Decimal('1.05'), '_value_ - 1 == Decimal(str(0.05))'), True),
            TCData(('foobar', 'len(_value_) > 0'), True),

            TCData(('foobar', '_value_.isupper()'), False),
            TCData((Decimal('1.666'), '_value_ > 1.5 and _value_ < 1.6'), False),
            TCData(('banana', "_value_ in set(['watermelon', 'orange'])"), False)
        ]

        for test_case in test_cases:
            self.assertEqual(ConditionalAnswer.safe_eval(test_case.input[0], test_case.input[1]),
                             test_case.expected_output)

    def test_safe_eval_error(self):
        test_cases = [
            TCData("__import__('os')", "_value_")
        ]

        for test_case in test_cases:
            with self.assertRaises(NameError):
                ConditionalAnswer.safe_eval(test_case.input[0], test_case.input[1])

    def test_calculate_completion(self):
        test_cases = [
            TCData([], 0),
            TCData(['1', '1', '0'], 1),
            TCData([None, None, None], 0),
            TCData([None, '0', None, '1'], 0.5),
            TCData(['0', None, None, None], 0.25)
        ]

        for test_case in test_cases:
            conditional_answer = ConditionalAnswer(test_case.input, None)
            self.assertEqual(conditional_answer.calculate_completion(), test_case.expected_output)

    def test_calculate_mark(self):
        test_cases = [
            TCData([True, True, True], 1),
            TCData([False, False, False], 0),
            TCData([True, True, False, False], 0.5),
            TCData([True, False, False, False], 0.25),
            TCData([False, False, True, False], 0.25),
            TCData([False, True, True, False, True, False], 0.5)
        ]

        for test_case in test_cases:
            conditional_answer = ConditionalAnswer(None, test_case.input)
            self.assertEqual(conditional_answer.calculate_mark(), test_case.expected_output)

    def test_check_answer(self):
        test_cases = [
            TCData((HWCentralConditionalAnswerFormat.NUMERIC, 1, '_value_ < 10', []), [False]),
            TCData((HWCentralConditionalAnswerFormat.NUMERIC, 3, '_value_ < 10', []), [False, False, False]),
            TCData((HWCentralConditionalAnswerFormat.NUMERIC, 3, '_value_ < 10', ['5.1', '3/10', '- 5 / 56']),
                   [True, True, True]),
            TCData((HWCentralConditionalAnswerFormat.NUMERIC, 1, '_value_ < 10', ['11.1']), [False]),
            TCData((HWCentralConditionalAnswerFormat.NUMERIC, 3, '_value_ < 10', [None, '9', None]),
                   [False, True, False]),

            TCData((HWCentralConditionalAnswerFormat.TEXTUAL, 1, '_value_.isupper()', []), [False]),
            TCData((HWCentralConditionalAnswerFormat.TEXTUAL, 3, '_value_.isupper()', []), [False, False, False]),
            TCData((HWCentralConditionalAnswerFormat.TEXTUAL, 3, '_value_.isupper()',
                    [' FOO  BAR\t ', 'BANANA', 'W A T\t\t E   RMELON']), [True, True, True]),
            TCData((HWCentralConditionalAnswerFormat.TEXTUAL, 1, '_value_.isupper()', ['foobar']), [False]),
            TCData((HWCentralConditionalAnswerFormat.TEXTUAL, 3, '_value_.isupper()', [None, '  FU BAR', None]),
                   [False, True, False])
        ]

        for test_case in test_cases:
            subpart_question_mock = NonCallableMagicMock(spec_set=['answer'])
            subpart_question_mock.answer = NonCallableMagicMock(spec_set=['answer_format', 'num_answers', 'condition'])
            subpart_question_mock.answer.answer_format = test_case.input[0]
            subpart_question_mock.answer.num_answers = test_case.input[1]
            subpart_question_mock.answer.condition = test_case.input[2]

            conditional_answer = ConditionalAnswer(test_case.input[3], None)
            conditional_answer.check_answer(subpart_question_mock)
            self.assertEqual(conditional_answer.correct, test_case.expected_output)
