from core.utils.constants import HWCentralQuestionType
from core.data_models.answer import MCSAQAnswer, MCMAQAnswer, NumericAnswer, TextualAnswer, ConditionalAnswer
from core.view_models.json import JSONViewModel
from core.data_models.question import Question
from hwcentral.exceptions import InvalidHWCentralQuestionTypeException


###
#
# This file contains all the submission-related datamodels used in the core hwcentral logic. for viewmodels which are
#   used by templates, look at submission_id
#
###

class ShellSubmission(JSONViewModel):
    def __init__(self, aql_randomized_dealt):
        self.questions = aql_randomized_dealt
        self.answers = []
        for question in aql_randomized_dealt:
            self.answers.append([None] * len(question.subparts))


class Submission(JSONViewModel):
    def __init__(self, data):
        # NOTE: A saved submission already has its questions and options ordered (subparts are ALWAYS ordered)
        self.questions = [Question.from_data(x) for x in data['questions']]

        answers = data['answers']
        assert len(self.questions) == len(answers)

        self.answers = [[]] * len(answers)

        for i, answer in enumerate(answers):
            assert len(answer) == len(self.questions[i].subparts)
            for j, subpart_answer in enumerate(answer):
                subpart_type = self.questions[i].subparts[j].type

                if subpart_type == HWCentralQuestionType.MCSA:
                    self.answers[i].append(MCSAQAnswer(subpart_answer))
                elif subpart_type == HWCentralQuestionType.MCMA:
                    self.answers[i].append(MCMAQAnswer(subpart_answer))
                elif subpart_type == HWCentralQuestionType.NUMERIC:
                    self.answers[i].append(NumericAnswer(subpart_answer))
                elif subpart_type == HWCentralQuestionType.TEXTUAL:
                    self.answers[i].append(TextualAnswer(subpart_answer))
                elif subpart_type == HWCentralQuestionType.CONDITIONAL:
                    self.answers[i].append(ConditionalAnswer(subpart_answer))
                else:
                    raise InvalidHWCentralQuestionTypeException(subpart_type)

    def update_answers(self, answers):
        self.answers = answers

    def calculate_completion(self):
        return None

