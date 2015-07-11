import json

from core.models import Submission
from core.view_models.base import AuthenticatedBody


class AssignmentIdBody(AuthenticatedBody):
    """
    Abstract class that is used to store any common data between the bodies of all the assignment id views
    """

    def __init__(self):
        pass


class StudentAssignmentIdBody(AssignmentIdBody):
    """
    Construct the viewmodel for the student assignment id page body here. Information needed:
    1. Assignment name
    2. Assignment due date
    3. Assignment submission date
    4. Graded submission viewmodel
    5. Score
    """

    def __init__(self, user, assignment):
        self.assignment = assignment
        self.submission = Submission.objects.get(student=user, assignment=assignment)
        self.graded_submission = GradedSubmission(user, self.submission)


class ParentAssignmentIdBody(AssignmentIdBody):
    def __init__(self, user, assignment):
        raise


class AdminAssignmentIdBody(AssignmentIdBody):
    def __init__(self, user, assignment):
        raise


class TeacherAssignmentIdBody(AssignmentIdBody):
    def __init__(self, user, assignment):
        raise


class GradedSubmission(object):
    """
    Contains a list of graded questions in the user's custom order
    """

    def __init__(self, student, submission):
        self.graded_questions = []

        # read the submission from its serialized form
        with open(submission.meta, 'r') as f:
            data = json.load(f)

            # # first recreate the question ordering from the assignment for this user
            # custom_questions_order = get_question_ordering_for_student(student, submission.assignment)
            # for question in custom_questions_order:
            # # if user did not answer the question, answer = None
            #     user_answer = data.get(str(question.pk), None)
            #     question_meta = QuestionMeta(question)
            #     self.graded_questions.append(GradedQuestion(question_meta, user_answer))
