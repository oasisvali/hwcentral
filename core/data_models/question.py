from core.utils.constants import HWCentralQuestionDataType, HWCentralQuestionType, HWCentralConditionalAnswerFormat
from core.utils.json import JSONModel
from hwcentral.exceptions import InvalidHWCentralQuestionTypeException


def no_tex(text):
    TEX_MARKERS = ['\[', '\]', '\(', '\)']
    return not any(tex_marker in text for tex_marker in TEX_MARKERS)

class QuestionElem(JSONModel):
    """
    Wrapper around the building block of a question. text + image (at least one must exist)
    """

    @classmethod
    def from_data(cls, data):
        if data is None:
            return None

        assert ( ('text' in data) or ('img' in data) )
        return cls(data.get('text'), data.get('img'), data.get('img_url'))

    def __init__(self, text, img, img_url):
        self.text = text
        self.img = img
        self.img_url = img_url

    def build_img_url(self, user, question, question_data_type):
        """
        This is done as a seperate step and not during initialization so that the QuestionElem creation is not dependant
        on extra contextual data such as user that the cabinet needs to build the secure url
        """
        if self.img is not None:
            from cabinet import cabinet

            self.img_url = cabinet.get_question_img_url_secure(user, question, question_data_type, self.img)

        else:
            self.img_url = None

    def is_plaintext(self):
        """
        Checks whether this QuestionElem contains plain text ONLY (no tex or img)
        """
        return (self.img is None) and no_tex(self.text)


def build_question_part_from_data(subpart_data):
    """
    Checks the provided data object (dictionary) for the type of the subpart and builds a Python object of the right type
    """
    subpart_type = subpart_data['type']

    if subpart_type == HWCentralQuestionType.MCSA:
        question_part = MCSAQuestionPart(subpart_data)
    elif subpart_type == HWCentralQuestionType.MCMA:
        question_part = MCMAQuestionPart(subpart_data)
    elif subpart_type == HWCentralQuestionType.NUMERIC:
        question_part = NumericQuestionPart(subpart_data)
    elif subpart_type == HWCentralQuestionType.TEXTUAL:
        question_part = TextualQuestionPart(subpart_data)
    elif subpart_type == HWCentralQuestionType.CONDITIONAL:
        question_part = ConditionalQuestionPart(subpart_data)
    else:
        raise InvalidHWCentralQuestionTypeException(subpart_type)

    return question_part

class Question(JSONModel):
    """
    Overall wrapper on cabinet question data
    """

    @classmethod
    def from_data(cls, data):
        subparts = []
        for subpart_data in data['subparts']:
            subparts.append(build_question_part_from_data(subpart_data))

        return cls(QuestionContainer(data['container']), subparts)

    def __init__(self, container, subparts):
        self.container = container
        self.subparts = subparts

    def build_img_urls(self, user, question):
        self.container.build_img_urls(user, question)
        for subpart in self.subparts:
            subpart.build_img_urls(user, question)


class QuestionContainer(JSONModel):
    """
    Wrapper around the data that resides in a question container file
    """

    def __init__(self, data):
        self.hint = QuestionElem.from_data(data.get("hint"))
        self.content = QuestionElem.from_data(data.get("content"))

        self.subparts = data['subparts']

    def build_img_urls(self, user, question):
        if self.hint is not None:
            self.hint.build_img_url(user, question, HWCentralQuestionDataType.CONTAINER)
        if self.content is not None:
            self.content.build_img_url(user, question, HWCentralQuestionDataType.CONTAINER)


class QuestionPart(JSONModel):
    """
    Wrapper around the data that resides in a raw question file
    """

    TYPES = HWCentralQuestionType  # associating enum with this dm so that it is available in templates

    def __init__(self, data):
        self.type = data['type']
        self.content = QuestionElem.from_data(data['content'])
        self.subpart_index = data['subpart_index']

        self.hint = QuestionElem.from_data(data.get("hint"))
        self.solution = QuestionElem.from_data(data.get("solution"))

    def build_img_urls(self, user, question):
        self.content.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)
        if self.hint is not None:
            self.hint.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)
        if self.solution is not None:
            self.content.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)


class MCOptions(JSONModel):
    def __init__(self, data):
        self.incorrect = [QuestionElem.from_data(option) for option in data['incorrect']]
        self.order = data.get('order', None)

    def get_option_count(self):
        return len(self.incorrect)

    def build_img_urls(self, user, question):
        for option in self.incorrect:
            option.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)


class MCSAOptions(MCOptions):
    def __init__(self, data):
        super(MCSAOptions, self).__init__(data)
        self.correct = QuestionElem.from_data(data['correct'])
        self.use_dropdown_widget = data.get('use_dropdown_widget', False)  # disable by default
        if self.use_dropdown_widget:
            assert self.all_options_plaintext()

    def build_img_urls(self, user, question):
        super(MCSAOptions, self).build_img_urls(user, question)
        self.correct.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)

    def get_option_count(self):
        # NOTE: correct option before incorrect
        return 1 + super(MCSAOptions, self).get_option_count()

    def all_options_plaintext(self):
        """
        Checks whether all the option QuestionElems for this Options object are text-only (no tex no img)
        @return: boolean result of check
        """
        for option in self.incorrect:
            if not option.is_plaintext():
                return False

        return self.correct.is_plaintext()

class MCMAOptions(MCOptions):
    def __init__(self, data):
        super(MCMAOptions, self).__init__(data)
        self.correct = [QuestionElem.from_data(option) for option in data['correct']]

    def get_option_count(self):
        # NOTE: correct option before incorrect
        return len(self.correct) + super(MCMAOptions, self).get_option_count()

    def build_img_urls(self, user, question):
        super(MCMAOptions, self).build_img_urls(user, question)
        for option in self.correct:
            option.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)

class MCSAQuestionPart(QuestionPart):
    def __init__(self, data):
        super(MCSAQuestionPart, self).__init__(data)
        self.options = MCSAOptions(data['options'])

    def build_img_urls(self, user, question):
        super(MCSAQuestionPart, self).build_img_urls(user, question)
        self.options.build_img_urls(user, question)


class MCMAQuestionPart(QuestionPart):
    def __init__(self, data):
        super(MCMAQuestionPart, self).__init__(data)
        self.options = MCMAOptions(data['options'])

    def build_img_urls(self, user, question):
        super(MCMAQuestionPart, self).build_img_urls(user, question)
        self.options.build_img_urls(user, question)


class TextualQuestionPart(QuestionPart):
    def __init__(self, data):
        super(TextualQuestionPart, self).__init__(data)
        self.answer = data['answer']
        assert self.answer.islower()


class NumericTarget(JSONModel):
    def __init__(self, data):
        self.value = data['value']
        self.tolerance = data.get('tolerance')


class NumericQuestionPart(QuestionPart):
    def __init__(self, data):
        super(NumericQuestionPart, self).__init__(data)
        self.answer = NumericTarget(data['answer'])
        self.show_toolbox = data.get('show_toolbox', False)  # disable by default


class ConditionalTarget(JSONModel):
    FORMATS = HWCentralConditionalAnswerFormat  # associating enum with this dm so that it is available in templates

    def __init__(self, data):
        self.num_answers = data['num_answers']
        self.conditions = data['conditions']
        self.answer_format = data['answer_format']
        if self.answer_format == ConditionalTarget.FORMATS.NUMERIC:
            self.show_toolbox = data.get('show_toolbox', False)  # disable by default


class ConditionalQuestionPart(QuestionPart):
    def __init__(self, data):
        super(ConditionalQuestionPart, self).__init__(data)
        self.answer = ConditionalTarget(data['answer'])