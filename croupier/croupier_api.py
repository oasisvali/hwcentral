import random
import time

from datadog import statsd
from django.core.signing import Signer

from cabinet import cabinet_api
from core.data_models.question import QuestionContainer
from core.utils.constants import HWCentralQuestionType
from croupier.data_models import UndealtQuestionDM

SIGNER = Signer()

def deal(undealt_questions):
    """
    This method takes undealt questions, deals them (variable value selection, substitution and evaluation) and then
    returns just the dealt questions as regular data models
    """
    dealt_questions = []
    for undealt_question in undealt_questions:
        undealt_question.deal()
        dealt_questions.append(undealt_question.question_data)
    return dealt_questions


def shuffle(undealt_questions):
    """
    Shuffles the given list of questions as well as the options of any MCQs in the list using the given technique
    """
    # first shuffle question order (IN PLACE)
    random.shuffle(undealt_questions)

    for undealt_question in undealt_questions:
        for subpart in undealt_question.question_data.subparts:
            # check if the subpart has options whose order can be shuffled
            if subpart.type == HWCentralQuestionType.MCMA or subpart.type == HWCentralQuestionType.MCSA:
                # storing a separate option order rather than ordering a list of options so that we can still easily
                # identify the correct and incorrect options based on the human-readable template format
                options_order = range(subpart.options.get_option_count())
                random.shuffle(options_order)
                subpart.options.order = options_order

def build_assignment_user_seed(user, assignment_questions_list):
    return build_assignment(user.pk, user, assignment_questions_list)


def build_assignment_time_seed(student, assignment_questions_list):
    return build_assignment(time.time(), student, assignment_questions_list)


@statsd.timed('croupier.build_assignment')
def build_assignment(seed, user, assignment_questions_list):

    # first we grab the question data to build the assignment from the cabinet
    undealt_questions = cabinet_api.build_undealt_assignment(user, assignment_questions_list)

    # setup random with the seed for this round of building the assignment
    seed = SIGNER.sign(seed)
    random.seed(seed)

    # then we use croupier to shiffle and deal the values
    shuffle(undealt_questions)
    return deal(undealt_questions)


def deal_subpart(subpart, variable_constraints):
    # first initialize this dealer run with timestamp
    random.seed(time.time())

    # now we must create a shell UndealtQuestionDM since that is what croupier expects, but we only have a single subpart
    undealt_question = UndealtQuestionDM(0, QuestionContainer({'subparts': [0]}), [subpart], [variable_constraints])
    undealt_question.deal()

    return undealt_question.question_data.subparts[0]
