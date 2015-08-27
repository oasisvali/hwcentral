import copy

from core.models import Question
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


class QuestionDM(JSONModel):
    """
    Overall wrapper on cabinet question data
    """

    @classmethod
    def from_data(cls, data):
        subparts = []
        for subpart_data in data['subparts']:
            subparts.append(build_question_part_from_data(subpart_data))

        return cls(data['pk'], QuestionContainer(data['container']), subparts)

    def __init__(self, pk, container, subparts):
        self.pk = pk
        self.container = container
        self.subparts = subparts

    def build_img_urls(self, user):
        question = Question.objects.get(pk=self.pk)
        self.container.build_img_urls(user, question)
        for subpart in self.subparts:
            subpart.build_img_urls(user, question)

    def change_img_urls(self, user):
        question = Question.objects.get(pk=self.pk)
        self.container.change_img_urls(user, question)
        for subpart in self.subparts:
            subpart.change_img_urls(user, question)

    def get_protected_subparts(self, include_solutions):
        return [subpart.get_protected(include_solutions) for subpart in self.subparts]



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

    def change_img_urls(self, user, question):
        self.build_img_urls(user, question)


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

    def build_img_urls_common(self, user, question):
        self.content.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)
        if self.hint is not None:
            self.hint.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)

    def build_img_urls(self, user, question):
        self.build_img_urls_common(user, question)
        if self.solution is not None:
            self.content.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)

    def change_img_urls(self, user, question):
        self.build_img_urls_common(user, question)

    def get_protected(self, include_solution):
        self_copy = copy.deepcopy(self)
        if not include_solution:
            delattr(self_copy, 'solution')
        return self_copy


class MCOptions(JSONModel):
    """
    This is an abstract class
    """
    def __init__(self, data):
        self.incorrect = [QuestionElem.from_data(option) for option in data['incorrect']]
        self.order = data.get('order', None)

    def get_option_count(self):
        return len(self.incorrect)

    def build_img_urls(self, user, question):
        for option in self.incorrect:
            option.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)

    def change_img_urls(self, user, question):
        for option in self.combined:
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

    def get_combined_options(self):
        return [self.correct] + self.incorrect

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

    def get_combined_options(self):
        return self.correct + self.incorrect

    def get_option_count(self):
        # NOTE: correct option before incorrect
        return len(self.correct) + super(MCMAOptions, self).get_option_count()

    def build_img_urls(self, user, question):
        super(MCMAOptions, self).build_img_urls(user, question)
        for option in self.correct:
            option.build_img_url(user, question, HWCentralQuestionDataType.SUBPART)


class MCQuestionPart(QuestionPart):
    def build_img_urls(self, user, question):
        super(MCQuestionPart, self).build_img_urls(user, question)
        self.options.build_img_urls(user, question)

    def change_img_urls(self, user, question):
        # this method will only be called after the current object is in 'protected' state
        super(MCQuestionPart, self).change_img_urls(user, question)
        self.options.change_img_urls(user, question)

    def get_protected(self, include_solution):
        self_copy = super(MCQuestionPart, self).get_protected(include_solution)
        setattr(self_copy.options, 'combined', self_copy.options.get_combined_options())
        delattr(self_copy.options, 'correct')
        delattr(self_copy.options, 'incorrect')
        return self_copy


class MCSAQuestionPart(MCQuestionPart):
    def __init__(self, data):
        super(MCSAQuestionPart, self).__init__(data)
        self.options = MCSAOptions(data['options'])


class MCMAQuestionPart(MCQuestionPart):
    def __init__(self, data):
        super(MCMAQuestionPart, self).__init__(data)
        self.options = MCMAOptions(data['options'])


class NumericTarget(JSONModel):
    def __init__(self, data):
        self.value = data['value']
        self.tolerance = data.get('tolerance')


class InputQuestionPart(QuestionPart):
    def get_protected(self, include_solution):
        self_copy = super(InputQuestionPart, self).get_protected(include_solution)
        delattr(self_copy, 'answer')
        return self_copy


class TextualQuestionPart(InputQuestionPart):
    def __init__(self, data):
        super(TextualQuestionPart, self).__init__(data)
        self.answer = data['answer']
        self.show_toolbox = data.get('show_toolbox', False)  # disable by default

        assert self.answer.islower()


class NumericQuestionPart(InputQuestionPart):
    def __init__(self, data):
        super(NumericQuestionPart, self).__init__(data)
        self.answer = NumericTarget(data['answer'])

class ConditionalTarget(JSONModel):
    FORMATS = HWCentralConditionalAnswerFormat  # associating enum with this dm so that it is available in templates

    def __init__(self, data):
        self.num_answers = data['num_answers']
        self.conditions = data['conditions']
        self.answer_format = data['answer_format']
        if self.answer_format == ConditionalTarget.FORMATS.TEXTUAL:
            self.show_toolbox = data.get('show_toolbox', False)  # disable by default


class ConditionalQuestionPart(QuestionPart):
    def __init__(self, data):
        super(ConditionalQuestionPart, self).__init__(data)
        self.answer = ConditionalTarget(data['answer'])

    def get_protected(self, include_solution):
        self_copy = super(ConditionalQuestionPart, self).get_protected(include_solution)
        delattr(self_copy.answer, 'conditions')
        return self_copy
