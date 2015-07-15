from core.view_models.base import AuthenticatedBody


class AssignmentQuestionsList(object):
    """
    Contains a collection of questions - order undefined, undealt by croupier
    """

    def __init__(self, questions):
        self.questions = questions


class AssignmentQuestionsListRandomized(object):
    """
    Contains a collection of questions - order randomized, undealt by croupier
    """

    def __init__(self, questions):
        self.questions = questions


class AssignmentQuestionsListRandomizedDealt(object):
    """
    Contains a collection of questions - order randomized, dealt by croupier
    """

    def __init__(self, questions):
        self.questions = questions


class ReadonlyAssignmentBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the assignment id views
    """

    def __init__(self, aql_randomized_dealt):
        self.aql = aql_randomized_dealt
