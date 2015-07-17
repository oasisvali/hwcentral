from core.view_models.base import AuthenticatedBody


class ReadonlyAssignmentBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the assignment id views
    """

    def __init__(self, questions):
        self.questions = questions
