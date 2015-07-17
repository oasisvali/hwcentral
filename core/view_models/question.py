from core.utils.constants import HWCentralQuestionDataType
from core.view_models.json import JSONViewModel


class QuestionElem(JSONViewModel):
    """
    Wrapper around the building block of a question. text + image (at least one must exist)
    """

    def __init__(self, data):
        assert ( ('text' in data) or ('img' in data) )
        self.text = data.get('text', None)
        self.img = data.get('img', None)

    def build_img_url(self, user, question, question_data_type):
        """
        This is done as a seperate step and not during initialization so that the QuestionElem creation is not dependant
        on extra contextual data such as user that the cabinet needs to build the secure url
        """
        if self.img is not None:
            from core.utils import cabinet

            self.img_url = cabinet.get_question_img_url_secure(user, question, question_data_type, self.img)


class Question(JSONViewModel):
    """
    Overall wrapper on cabinet question data
    """

    def __init__(self, container, subparts):
        self.container = container
        self.subparts = subparts

    def build_img_urls(self, user, question):
        self.container.build_img_urls(user, question)
        for subpart in self.subparts:
            subpart.build_img_urls(user, question)


class QuestionContainer(JSONViewModel):
    """
    Wrapper around the data that resides in a question container file
    """

    def __init__(self, data):
        self.hint = QuestionElem(data["hint"]) if "hint" in data else None
        self.content = QuestionElem(data["content"]) if "content" in data else None

        self.subparts = data['subparts']

    def build_img_urls(self, user, question):
        if self.hint is not None:
            self.hint.build_img_url(user, question, HWCentralQuestionDataType.CONTAINER)
        if self.content is not None:
            self.content.build_img_url(user, question, HWCentralQuestionDataType.CONTAINER)


class QuestionPart(JSONViewModel):
    """
    Wrapper around the data that resides in a raw question file
    """

    def __init__(self, data):
        self.type = data['type']
        self.content = QuestionElem(data['content'])
        self.subpart_index = data['sub_part_index']

        self.hint = QuestionElem(data["hint"]) if "hint" in data else None
        self.solution = QuestionElem(data["solution"]) if "solution" in data else None

    def build_img_urls(self, user, question):
        self.content.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)
        if self.hint is not None:
            self.hint.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)
        if self.solution is not None:
            self.content.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)


class MCOptions(JSONViewModel):
    def __init__(self, data):
        self.incorrect_options = [QuestionElem(option) for option in data['incorrect']]


class MCSAOptions(MCOptions):
    def __init__(self, data):
        super(MCSAOptions, self).__init__(data)
        self.correct_option = QuestionElem(data['correct'])


class MCMAOptions(MCOptions):
    def __init__(self, data):
        super(MCMAOptions, self).__init__(data)
        self.correct_options = [QuestionElem(option) for option in data['correct']]


class MCSAQuestionPart(QuestionPart):
    def __init__(self, data):
        super(MCSAQuestionPart, self).__init__(data)
        self.options = MCSAOptions(data['options'])


class MCMAQuestionPart(QuestionPart):
    def __init__(self, data):
        super(MCMAQuestionPart, self).__init__(data)
        self.options = MCMAOptions(data['options'])


class TextualQuestionPart(QuestionPart):
    def __init__(self, data):
        super(TextualQuestionPart, self).__init__(data)
        self.answer = data['answer']
        assert self.answer.islower()


class NumericAnswer(JSONViewModel):
    def __init__(self, data):
        self.value = data['value']
        self.tolerance = data['tolerance'] if 'tolerance' in data else None


class NumericQuestionPart(QuestionPart):
    def __init__(self, data):
        super(NumericQuestionPart, self).__init__(data)
        self.answer = NumericAnswer(data['answer'])


class ConditionalAnswer(JSONViewModel):
    def __init__(self, data):
        self.num_answers = data['num_answers']
        self.conditions = data['conditions']


class ConditionalQuestionPart(QuestionPart):
    def __init__(self, data):
        super(ConditionalQuestionPart, self).__init__(data)
        self.answer = ConditionalAnswer(data['answer'])