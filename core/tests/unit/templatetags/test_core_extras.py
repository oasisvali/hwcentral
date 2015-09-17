from unittest import TestCase
from mock import MagicMock
from core.templatetags.core_extras import get_range, add_str, get_form_field, get_list_elem, answer_wrong, \
    is_correct_option_index_sa, is_correct_option_index_ma, throw_InvalidHWCentralGroupError, \
    throw_InvalidHWCentralQuestionTypeError
from core.tests.base import TCData
from core.utils.constants import HWCentralQuestionType
from hwcentral.exceptions import InvalidHWCentralGroupError, InvalidHWCentralQuestionTypeError, \
    UncorrectedSubmissionError


class CoreExtrasTest(TestCase):
    def test_get_range(self):
        test_cases = [
            TCData(0),
            TCData(1),
            TCData(5)
        ]
        for test_case in test_cases:
            self.assertEqual(test_case.input, len(get_range(test_case.input)))

    def test_add_str(self):
        test_cases = [
            TCData( (0, 1), u'01' ),
            TCData( (None, 'foo'), u'Nonefoo' ),
            TCData( ('bar', -4.56), u'bar-4.56' ),
            TCData( ([1,2,3], (None, [3.4,],45)), u'[1, 2, 3](None, [3.4], 45)' )
        ]
        for test_case in test_cases:
            actual_output = add_str(test_case.input[0], test_case.input[1])
            self.assertEqual(test_case.expected_output, actual_output)
            self.assertIsInstance(actual_output, unicode)

    def test_get_form_field(self):
        test_case = TCData( ({'field_key': 'field_val', 'foo': 'bar'}, 'field_key'), 'field_val' )
        # setup mock object
        mock_form = MagicMock(spec_set=['fields', '__getitem__'])   #MagicMock will create __getitem__ magic method by default
        mock_form.fields = test_case.input[0]
        mock_form.__getitem__.side_effect = mock_form.fields.__getitem__  #mocking some form functionality here

        self.assertEqual(test_case.expected_output, get_form_field(mock_form, test_case.input[1]))
        with self.assertRaises(AssertionError):
            get_form_field(mock_form, 'not_form_field_key')


    def test_get_list_elem(self):
        test_case = TCData( (['first', 'second', 'third'], 1), 'second' )

        self.assertEqual(test_case.expected_output, get_list_elem(test_case.input[0], test_case.input[1]))
        with self.assertRaises(AssertionError):
            get_list_elem(test_case.input[0], len(test_case.input[0]))  # invalid index


    def test_answer_wrong(self):
        test_cases = [
            TCData( (False, HWCentralQuestionType.MCMA), True ),
            TCData( (False, HWCentralQuestionType.MCSA), True ),
            TCData( (False, HWCentralQuestionType.NUMERIC), True ),
            TCData( (False, HWCentralQuestionType.TEXTUAL), True ),
            TCData( (True, HWCentralQuestionType.MCMA), False ),
            TCData( (True, HWCentralQuestionType.MCSA), False ),
            TCData( (True, HWCentralQuestionType.NUMERIC), False ),
            TCData( (True, HWCentralQuestionType.TEXTUAL), False ),
            TCData( ([False], HWCentralQuestionType.CONDITIONAL), True ),
            TCData( ([False, False], HWCentralQuestionType.CONDITIONAL), True ),
            TCData( ([False, True, False], HWCentralQuestionType.CONDITIONAL), True ),
            TCData( ([True, False, True, False], HWCentralQuestionType.CONDITIONAL), True ),
            TCData( ([True, True, True], HWCentralQuestionType.CONDITIONAL), False ),
        ]

        for test_case in test_cases:
            self.assertEqual(test_case.expected_output, answer_wrong(test_case.input[0], test_case.input[1]))

    def test_answer_wrong_assertion(self):
        test_cases = [
            TCData( (None, HWCentralQuestionType.MCMA) ),
            TCData( (None, HWCentralQuestionType.MCSA) ),
            TCData( (None, HWCentralQuestionType.NUMERIC) ),
            TCData( (None, HWCentralQuestionType.TEXTUAL) ),
            TCData( (None, HWCentralQuestionType.CONDITIONAL) ),
        ]
        for test_case in test_cases:
            with self.assertRaises(UncorrectedSubmissionError):
                answer_wrong(test_case.input[0], test_case.input[1])

    def test_is_correct_option_index_sa(self):
        test_cases = [
            TCData( (0, [0]), True ),
            TCData( (2, [0,1,2,3]), False ),
            TCData( (1, [3,1,2,0]), False ),
            TCData( (1, [3,0,2,1]), True ),
            TCData( (2, [1,2,0]), True)
        ]

        for test_case in test_cases:
            self.assertEqual(test_case.expected_output, is_correct_option_index_sa(test_case.input[0], test_case.input[1]))

    def test_is_correct_option_index_sa_assertion(self):
        test_cases = [
            TCData( (1, [0]) ),
            TCData( (3, [1,0]) )
        ]
        for test_case in test_cases:
            with self.assertRaises(AssertionError):
                is_correct_option_index_sa(test_case.input[0], test_case.input[1])

    def test_is_correct_option_index_ma(self):
        test_cases = [
            TCData( (0, [0], 1), True ),
            TCData( (0, [0], 0), False ),
            TCData( (0, [1,0], 1), False ),
            TCData( (0, [1,0], 0), False ),
            TCData( (1, [1,0], 1), True ),
            TCData( (1, [1,0], 0), False ),
            TCData( (2, [2,0,3,1], 3), False ),
            TCData( (0, [2,3,0,1], 3), True ),
            TCData( (3, [2,0,3,1], 2), True ),
            TCData( (0, [2,1,3,0,4], 2), False ),
        ]

        for test_case in test_cases:
            #set up mock options object
            mock_options = self.build_mock_mcma_options(test_case.input[1], test_case.input[2])
            self.assertEqual(test_case.expected_output, is_correct_option_index_ma(test_case.input[0], mock_options))

    def build_mock_mcma_options(self, order, correct_len = None):
        mock_options = MagicMock(spec_set=['order', 'correct'])
        mock_options.order = order
        if correct_len is not None:
            mock_options.correct.__len__.return_value = correct_len
        return mock_options

    def test_is_correct_option_index_ma_assertion(self):
        test_cases = [
            TCData( (1, [0]) ),
            TCData( (3, [1,0]) )
        ]
        for test_case in test_cases:
            with self.assertRaises(AssertionError):
                mock_options = self.build_mock_mcma_options(test_case.input[1])
                is_correct_option_index_ma(test_case.input[0], mock_options)

    def test_throw_InvalidHWCentralGroupError(self):
        with self.assertRaises(InvalidHWCentralGroupError):
            throw_InvalidHWCentralGroupError(MagicMock())

    def test_throw_InvalidHWCentralQuestionTypeError(self):
        with self.assertRaises(InvalidHWCentralQuestionTypeError):
            throw_InvalidHWCentralQuestionTypeError(MagicMock())