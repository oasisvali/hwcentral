from core.utils.constants import HWCentralQuestionType
from core.data_models.answer import MCSAQAnswer, MCMAQAnswer, NumericAnswer, TextualAnswer, ConditionalAnswer, \
    build_shell_answer
from core.utils.json import JSONModel
from core.data_models.question import QuestionDM
from hwcentral.exceptions import InvalidHWCentralQuestionTypeException


###
#
# This file contains all the submission-related datamodels used in the core hwcentral logic. for viewmodels which are
#   used by templates, look at submission_id
#
###


class SubmissionDM(JSONModel):
    @classmethod
    def build_shell_submission(cls, aql_randomized_dealt):
        questions = aql_randomized_dealt

        answers = []  # building a new list to store lists of Answer data models

        for i in xrange(len(questions)):
            subparts_answers = []
            for question_subpart in questions[i].subparts:
                subparts_answers.append(build_shell_answer(question_subpart.type))
            answers.append(subparts_answers)
        return cls(questions, answers)

    @classmethod
    def build_from_data(cls, data):
        # NOTE: A saved submission already has its questions and options ordered (subparts are ALWAYS ordered)
        questions = [QuestionDM.from_data(x) for x in data['questions']]

        answers_data = data['answers']
        assert len(questions) == len(answers_data)

        answers = []  # building a new list to store lists of Answer data models

        for i, answer_data in enumerate(answers_data):
            subparts_answers = []
            assert len(answer_data) == len(questions[i].subparts)

            for j, subpart_answer_data in enumerate(answer_data):
                subpart_answer = None
                subpart_type = questions[i].subparts[j].type

                if subpart_type == HWCentralQuestionType.MCSA:
                    subpart_answer = MCSAQAnswer.from_data(subpart_answer_data)
                elif subpart_type == HWCentralQuestionType.MCMA:
                    subpart_answer = MCMAQAnswer.from_data(subpart_answer_data)
                elif subpart_type == HWCentralQuestionType.NUMERIC:
                    subpart_answer = NumericAnswer.from_data(subpart_answer_data)
                elif subpart_type == HWCentralQuestionType.TEXTUAL:
                    subpart_answer = TextualAnswer.from_data(subpart_answer_data)
                elif subpart_type == HWCentralQuestionType.CONDITIONAL:
                    subpart_answer = ConditionalAnswer.from_data(subpart_answer_data,
                                                                 questions[i].subparts[j].answer.answer_format)
                else:
                    raise InvalidHWCentralQuestionTypeException(subpart_type)

                subparts_answers.append(subpart_answer)
            answers.append(subparts_answers)

        return cls(questions, answers)

    def __init__(self, questions, answers):
        self.answers = answers
        self.questions = questions

    def update_answers(self, answers):
        self.answers = answers

    def calculate_completion(self):
        """
        Returns a fraction value between 0-1 that denotes the amount of completion for this submission
        """

        # go through all the answers and the subpart answers
        total_subpart_answers = 0
        subpart_answers_completed = 0

        for answer in self.answers:
            for subpart_answer in answer:
                total_subpart_answers += 1
                subpart_answers_completed += subpart_answer.calculate_completion()

        return float(subpart_answers_completed) / total_subpart_answers

    def check_amswers(self):
        # go through every question subpart
        for i, question in enumerate(self.questions):
            assert len(question.subparts) == len(self.answers[i])

            for j, subpart_question in enumerate(question.subparts):
                subpart_answer = self.answers[i][j]
                subpart_answer.check_answer(subpart_question)

    def calculate_marks(self):
        """
        Returns a fraction value between 0-1 that denotes the marks awarded for this submission. Also performs correction
        """
        self.check_amswers()

        total_subpart_answers = 0
        subpart_answers_correct = 0

        for i, answer in enumerate(self.answers):
            for j, subpart_answer in enumerate(answer):
                total_subpart_answers += 1
                subpart_answers_correct += subpart_answer.calculate_mark()

        return float(subpart_answers_correct) / total_subpart_answers

    def get_protected_questions(self):
        return [QuestionDM(question.pk, question.container, question.get_protected_subparts()) for
                question in self.questions]
