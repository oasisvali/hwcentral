import random
import time

from core.utils.constants import HWCentralQuestionType
from core.view_models.assignment_id import AssignmentQuestionsListRandomized, AssignmentQuestionsListRandomizedDealt
from core.view_models.question import MCSAOptions, MCMAOptions
from hwcentral.exceptions import InvalidHWCentralOptionTypeException


def randomize_for_seed(seed, collection):
    """
    Shuffles the given collection IN-PLACE into a random order using the given seed
    """
    random.seed(seed)
    random.shuffle(collection)
    return collection


def randomize_for_time(collection):
    random.seed(time.time())
    random.shuffle(collection)
    return collection


# TODO: this doesnt belong in croupier
def get_option_count(options):
    if isinstance(options, MCSAOptions):
        return len(options.incorrect_options) + 1
    elif isinstance(options, MCMAOptions):
        return len(options.incorrect_options) + len(options.correct_options)
    else:
        raise InvalidHWCentralOptionTypeException(type(options))


def shuffle(user, assignment_questions_list):
    """
    Shuffles the given assignment_questions_list as well as the options of any MCQs in the list using the given user's pk
    """

    # first shuffle question order
    randomize_for_seed(user.pk, assignment_questions_list.questions)

    for question in assignment_questions_list.questions:
        for subpart in question.subparts:
            # check if the subpart has options whose order can be shuffled
            if subpart.type == HWCentralQuestionType.MCMA or subpart.type == HWCentralQuestionType.MCSA:
                subpart.option_order = randomize_for_seed(user.pk, range(get_option_count(subpart.options)))

    return AssignmentQuestionsListRandomized(assignment_questions_list.questions)


def deal(user, assignment_questions_list_randomized):
    return AssignmentQuestionsListRandomizedDealt(assignment_questions_list_randomized.questions)