from core.view_models.question import QuestionElem


class Answer(object):
    """
    Base Answer wrapper
    """

    def check(self, user_answer):
        """
        Checks if user_answer is correct and returns true/false
        """
        raise NotImplementedError("Subclass of Answer class needs to implement checking logic")


class MCQAnswer(Answer):
    def __init__(self, data):
        self.incorrect = [QuestionElem(op) for op in data["incorrect"]]


class MCSAQAnswer(MCQAnswer):
    def __init__(self, data):
        super(MCSAQAnswer, self).__init__(data)
        self.correct = QuestionElem(data["correct"])

    def check(self, user_answer):
        pass


class MCMAQAnswer(MCQAnswer):
    def __init__(self, data):
        super(MCSAQAnswer, self).__init__(data)
        self.correct = [QuestionElem(op) for op in data["correct"]]


class RegularNumericAnswer(Answer):
    def __init__(self, data):
        self.value = data["value"]
        self.tolerance = data.get("tolerance", None)


class RegularTextAnswer(Answer):
    def __init__(self, data):
        assert type(data) is str
        self.value = data
