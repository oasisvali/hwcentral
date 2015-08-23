class InvalidStateException(Exception):
    pass


class InvalidHWCentralException(InvalidStateException):
    def __init__(self, label, value, *args, **kwargs):
        super(InvalidHWCentralException, self).__init__("Invalid HWCentral %s: %s" % (label, value))


class InvalidHWCentralTypeException(InvalidHWCentralException):
    def __init__(self, label, value, *args, **kwargs):
        super(InvalidHWCentralTypeException, self).__init__(label + ' type', value)


class InvalidHWCentralGroupException(InvalidHWCentralException):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralGroupException, self).__init__('group', value)


class InvalidHWCentralAssignmentTypeException(InvalidHWCentralTypeException):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralAssignmentTypeException, self).__init__('assignment', value)


class InvalidHWCentralQuestionTypeException(InvalidHWCentralTypeException):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralQuestionTypeException, self).__init__('question', value)


class InvalidHWCentralOptionTypeException(InvalidHWCentralTypeException):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralOptionTypeException, self).__init__('option', value)


class InvalidHWCentralConditionalAnswerFormatException(InvalidHWCentralException):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralConditionalAnswerFormatException, self).__init__('conditional answer format', value)


class NoneArgumentException(Exception):
    def __init__(self, argument, *args, **kwargs):
        super(NoneArgumentException, self).__init__("Unexpected None argument: %s" % argument)


class CabinetSubmissionExistsException(Exception):
    pass


class CabinetSubmissionMissingException(Exception):
    pass