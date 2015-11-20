from unittest import TestCase

from core.tests.base import TCData
from core.utils.helpers import make_string_lean


class HelpersTest(TestCase):
    def test_make_string_lean(self):
        test_cases = [
            TCData(' FoO', 'FoO'),
            TCData('foo  Bar ', 'foo Bar'),
            TCData('banana Dr. Gru ', 'banana Dr. Gru'),
            TCData('  Banana \tDr. gru ', 'Banana Dr. gru'),
            TCData('banana    Dr.   GRU', 'banana Dr. GRU'),
            TCData('\t\tbaNAna  Dr. GRU', 'baNAna Dr. GRU')
        ]

        for test_case in test_cases:
            self.assertEqual(make_string_lean(test_case.input), test_case.expected_output)