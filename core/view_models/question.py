import json

from core.utils.constants import HWCentralQuestionType
from hwcentral.exceptions import InvalidHWCentralQuestionTypeException


class QuestionElem(object):
    """
    Wrapper around the building block of a question. text + optional image
    """

    def __init__(self, data):
        # elem must have at least one of text/img
        assert ("text" in data) or ("img" in data)
        self.text = data.get("text", None)
        self.img = data.get("img", None)


class QuestionContainer(object):
    """
    Wrapper around the data that resides in a question container file
    """

    def __init__(self, question):
        # read container from its serialized form
        with open(question.meta, 'r') as f:
            data = json.load(f)

        self.type = data["type"]
        self.content = QuestionElem(data["content"])

        self.hint = QuestionElem(data["hint"]) if "hint" in data else None
        self.solution = QuestionElem(data["solution"]) if "solution" in data else None

        from core.view_models.answer import MCSAQAnswer, MCMAQAnswer, RegularNumericAnswer, RegularTextAnswer

        if self.type == HWCentralQuestionType.MCSA:
            self.answer = MCSAQAnswer(data["options"])
        elif self.type == HWCentralQuestionType.MCMA:
            self.answer = MCMAQAnswer(data["options"])
        elif self.type == HWCentralQuestionType.REGULAR_NUMERIC:
            self.answer = RegularNumericAnswer(data["answer"])
        elif self.type == HWCentralQuestionType.REGULAR_TEXT:
            self.answer = RegularTextAnswer(data["answer"])
        else:
            raise InvalidHWCentralQuestionTypeException(self.type)

class QuestionMeta(object):
    """
    Wrapper around the data that resides in a question metadata file. Built from the database model
    """

    def __init__(self, question):
        # read metadata from its serialized form
        with open(question.meta, 'r') as f:
            data = json.load(f)

        self.type = data["type"]
        self.content = QuestionElem(data["content"])

        self.hint = QuestionElem(data["hint"]) if "hint" in data else None
        self.solution = QuestionElem(data["solution"]) if "solution" in data else None

        from core.view_models.answer import MCSAQAnswer, MCMAQAnswer, RegularNumericAnswer, RegularTextAnswer

        if self.type == HWCentralQuestionType.MCSA:
            self.answer = MCSAQAnswer(data["options"])
        elif self.type == HWCentralQuestionType.MCMA:
            self.answer = MCMAQAnswer(data["options"])
        elif self.type == HWCentralQuestionType.REGULAR_NUMERIC:
            self.answer = RegularNumericAnswer(data["answer"])
        elif self.type == HWCentralQuestionType.REGULAR_TEXT:
            self.answer = RegularTextAnswer(data["answer"])
        else:
            raise InvalidHWCentralQuestionTypeException(self.type)


class GradedQuestion(object):
    """
    Contains the question with its metadata and user's answer - the options are in the user's custom order
    """

    def __init__(self, question_meta, user_answer):
        self.question_meta = question_meta
        self.user_answer = user_answer
        self.is_correct = self.question_meta.answer.check(user_answer)
