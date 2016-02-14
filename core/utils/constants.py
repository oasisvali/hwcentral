VIEWMODEL_KEY = 'vm'


class HWCentralRegex(object):
    NUMERIC = r'\d+'
    BASE64 = r'[\w\-]+'


class HttpMethod(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class HWCentralQuestionType(object):
    MCSA = 1
    MCMA = 2
    NUMERIC = 3
    TEXTUAL = 4
    CONDITIONAL = 5


class HWCentralAssignmentType(object):
    INACTIVE = 'inactive'
    UNCORRECTED = 'uncorrected'
    CORRECTED = 'corrected'
    PRACTICE = 'practice'


class HWCentralPracticeSubmissionType(object):
    UNCORRECTED = 'uncorrected'
    CORRECTED = 'corrected'

class HWCentralQuestionDataType(object):
    CONTAINER = 'containers'
    SUBPART = 'raw'


class HWCentralConditionalAnswerFormat(object):
    TEXTUAL = 1
    NUMERIC = 2


class HWCentralEnv(object):
    PROD = 1
    CIRCLECI = 2
    QA = 3
    LOCAL = 4
