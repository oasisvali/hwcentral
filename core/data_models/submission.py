from core.utils.constants import HWCentralQuestionType
from core.data_models.answer import MCSAQAnswer, MCMAQAnswer, NumericAnswer, TextualAnswer, ConditionalAnswer, \
    build_shell_answer
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

        answers = [[]] * len(questions)  # building a new list to store lists of Answer data models

        for i, answer in enumerate(answers):
            # at this point answer is an empty list. remember to only append and not reassign to answer to have the
            # changes reflected in answers

            for question_subpart in questions[i].subparts:
                answer.append(build_shell_answer(question_subpart.type))

        return cls(questions, answers)

    @classmethod
    def build_from_data(cls, data):
        # NOTE: A saved submission already has its questions and options ordered (subparts are ALWAYS ordered)
        questions = [Question.from_data(x) for x in data['questions']]

        answers_data = data['answers']
        assert len(questions) == len(answers_data)

        answers = [[]] * len(answers_data)  # building a new list to store lists of Answer data models

        for i, answer_data in enumerate(answers_data):
            assert len(answer_data) == len(questions[i].subparts)

            for j, subpart_answer_data in enumerate(answer_data):
                subpart_answer = None
                if subpart_answer_data is not None:
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

                # if subpart_answer_data is None, None will be appended to the answers list here
                answers[i].append(subpart_answer)

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

    def protect_solutions(self):
        """
        Sanitizes the data model so that the solutions are not needlessly exposed. This will prevent bugs like solutions
        being accidentally visible for uncorrected and readonly assignments
        """
        # loop through questions
        for question in self.questions:
            for subpart in question.subparts:
                subpart.solution = None
