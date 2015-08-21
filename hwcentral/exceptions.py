class InvalidStateException(Exception):
    pass


class InvalidHWCentralException(InvalidStateException):
    def __init__(self, label, value, *args, **kwargs):
        super(InvalidHWCentralException, self).__init__("Invalid HWCentral %s: %s" % (label, value))


class InvalidHWCentralTypeException(InvalidHWCentralException):
    def __init__(self, label, value, *args, **kwargs):
        super(InvalidHWCentralTypeException).__init__(self, label + ' type', value)


class InvalidHWCentralGroupException(InvalidHWCentralException):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralGroupException).__init__(self, 'group', value)


class InvalidHWCentralAssignmentTypeException(InvalidHWCentralTypeException):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralAssignmentTypeException).__init__(self, 'assignment', value)


class InvalidHWCentralQuestionTypeException(InvalidHWCentralTypeException):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralQuestionTypeException).__init__(self, 'question', value)


class InvalidHWCentralOptionTypeException(InvalidHWCentralTypeException):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralOptionTypeException).__init__(self, 'option', value)


class InvalidHWCentralConditionalAnswerFormatException(InvalidHWCentralException):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralOptionTypeException).__init__(self, 'conditional answer format', value)


class NoneArgumentException(Exception):
    def __init__(self, argument, *args, **kwargs):
        super(NoneArgumentException, self).__init__("Unexpected None argument: %s" % argument)


class CabinetSubmissionExistsException(Exception):
    pass


class CabinetSubmissionMissingException(Exception):
    pass