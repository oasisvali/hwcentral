class QuestionElem(object):
    """
    Wrapper around the building block of a question. text + optional image
    """

    def __init__(self, data):
        assert ( ('text' in data) or ('img' in data) )
        self.text = data.get('text', None)
        self.img = data.get('img', None)


class QuestionContainer(object):
    """
    Wrapper around the data that resides in a question container file
    """

    def __init__(self, data):
        self.content = QuestionElem(data['content']) if 'content' in data else None
        self.hint = QuestionElem(data['hint']) if 'hint' in data else None

        self.subparts = data['subparts']


class QuestionPart(object):
    """
    Wrapper around the data that resides in a raw question file
    """

    def __init__(self, data):
        self.type = data['type']
        self.content = QuestionElem(data['content'])
        self.subpart_index = data['sub_part_index']

        self.hint = QuestionElem(data["hint"]) if "hint" in data else None
        self.solution = QuestionElem(data["solution"]) if "solution" in data else None

        # from core.view_models.answer import MCSAQAnswer, MCMAQAnswer, RegularNumericAnswer, RegularTextAnswer
        #
        # if self.type == HWCentralQuestionType.MCSA:
        # self.answer = MCSAQAnswer(data["options"])
        # elif self.type == HWCentralQuestionType.MCMA:
        #     self.answer = MCMAQAnswer(data["options"])
        # elif self.type == HWCentralQuestionType.REGULAR_NUMERIC:
        #     self.answer = RegularNumericAnswer(data["answer"])
        # elif self.type == HWCentralQuestionType.REGULAR_TEXT:
        #     self.answer = RegularTextAnswer(data["answer"])
        # else:
        #     raise InvalidHWCentralQuestionTypeException(self.type)


class GradedQuestion(object):
    """
    Contains the question with its metadata and user's answer - the options are in the user's custom order
    """

    def __init__(self, question_meta, user_answer):
        self.question_meta = question_meta
        self.user_answer = user_answer
        self.is_correct = self.question_meta.answer.check(user_answer)
