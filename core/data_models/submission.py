from core.utils.constants import HWCentralQuestionType
from core.data_models.answer import MCSAQAnswer, MCMAQAnswer, NumericAnswer, TextualAnswer, ConditionalAnswer
from core.utils.json import JSONModel
from core.data_models.question import Question
from hwcentral.exceptions import InvalidHWCentralQuestionTypeException


###
#
# This file contains all the submission-related datamodels used in the core hwcentral logic. for viewmodels which are
#   used by templates, look at submission_id
#
###


class Submission(JSONModel):
    @classmethod
    def build_shell_submission(cls, aql_randomized_dealt):
        questions = aql_randomized_dealt
        answers = []
        for question in aql_randomized_dealt:
            answers.append([None] * len(question.subparts))

        return cls(questions, answers)

    @classmethod
    def build_from_data(cls, data):
        # NOTE: A saved submission already has its questions and options ordered (subparts are ALWAYS ordered)
        questions = [Question.from_data(x) for x in data['questions']]

        answers_data = data['answers']
        assert len(questions) == len(answers_data)

        answers = [[]] * len(answers_data)

        for i, answer in enumerate(answers):
            assert len(answer) == len(self.questions[i].subparts)
            for j, subpart_answer in enumerate(answer):
                if subpart_answer is None:
                    self.answers[i].append(subpart_answer)
                    continue

                subpart_type = self.questions[i].subparts[j].type

                if subpart_type == HWCentralQuestionType.MCSA:
                    answers[i].append(MCSAQAnswer(subpart_answer_data))
                elif subpart_type == HWCentralQuestionType.MCMA:
                    answers[i].append(MCMAQAnswer(subpart_answer_data))
                elif subpart_type == HWCentralQuestionType.NUMERIC:
                    answers[i].append(NumericAnswer(subpart_answer_data))
                elif subpart_type == HWCentralQuestionType.TEXTUAL:
                    answers[i].append(TextualAnswer(subpart_answer_data))
                elif subpart_type == HWCentralQuestionType.CONDITIONAL:
                    answers[i].append(ConditionalAnswer(subpart_answer_data))
                else:
                    raise InvalidHWCentralQuestionTypeException(subpart_type)

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
                if subpart_answer is not None:
                    subpart_answers_completed += 1
        return float(subpart_answers_completed) / total_subpart_answers


