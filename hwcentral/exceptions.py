class InvalidStateError(Exception):
    pass

class InvalidHWCentralError(InvalidStateError):
    def __init__(self, label, value, *args, **kwargs):
        super(InvalidHWCentralError, self).__init__("Invalid OpenShiksha %s: %s" % (label, value))


class InvalidHWCentralTypeError(InvalidHWCentralError):
    def __init__(self, label, value, *args, **kwargs):
        super(InvalidHWCentralTypeError, self).__init__(label + ' type', value)


class InvalidHWCentralGroupError(InvalidHWCentralError):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralGroupError, self).__init__('group', value)


class InvalidHWCentralEnvError(InvalidHWCentralError):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralEnvError, self).__init__('environ', value)

class InvalidHWCentralAssignmentTypeError(InvalidHWCentralTypeError):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralAssignmentTypeError, self).__init__('assignment', value)

class InvalidContentTypeError(InvalidHWCentralTypeError):
    def __init__(self, value, *args, **kwargs):
        super(InvalidContentTypeError, self).__init__('content', value)

class InvalidHWCentralQuestionTypeError(InvalidHWCentralTypeError):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralQuestionTypeError, self).__init__('question', value)


class InvalidHWCentralOptionTypeError(InvalidHWCentralTypeError):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralOptionTypeError, self).__init__('option', value)


class InvalidHWCentralContentTypeError(InvalidHWCentralTypeError):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralContentTypeError, self).__init__('content', value)

class InvalidHWCentralConditionalAnswerFormatError(InvalidHWCentralError):
    def __init__(self, value, *args, **kwargs):
        super(InvalidHWCentralConditionalAnswerFormatError, self).__init__('conditional answer format', value)


class NoneArgumentError(Exception):
    def __init__(self, argument, *args, **kwargs):
        super(NoneArgumentError, self).__init__("Unexpected None argument: %s" % argument)


# TODO: better error messages
class EvalSanitizationError(Exception):
    pass


class TagMismatchError(Exception):
    pass

class UncorrectedSubmissionError(InvalidStateError):
    def __init__(self, *args, **kwargs):
        super(UncorrectedSubmissionError, self).__init__("Tried to render uncorrected submission as corrected")


class SubmissionFormError(InvalidStateError):
    pass