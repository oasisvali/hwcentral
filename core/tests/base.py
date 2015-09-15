from collections import namedtuple

class TCData(object):
    def __init__(self, input, expected_output=None):
        self.input = input
        self.expected_output = expected_output
