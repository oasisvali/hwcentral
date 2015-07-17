import random
import time

from core.utils.constants import HWCentralQuestionType
from core.view_models.question import MCSAOptions, MCMAOptions
from hwcentral.exceptions import InvalidHWCentralOptionTypeException


def randomize_for_seed(collection, seed):
    """
    Shuffles the given collection IN-PLACE into a random order using the given seed. Also returns modified collection
    """
    random.seed(seed)
    random.shuffle(collection)
    return collection

def randomize_for_time(collection):
    """
    Shuffles the given collection IN-PLACE into a random order using the current tick counter as seed. Also returns
    modified collection
    """
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


def shuffle_for_user(questions, user):
    """
    Shuffles the given list of questions as well as the options of any MCQs in the list using the given user's pk
    """

    return _shuffle(randomize_for_seed, questions, user.pk)


def shuffle_for_time(questions):
    """
    Shuffles the given list of questions as well as the options of any MCQs in the list using the current tick counter
    """
    return _shuffle(randomize_for_time, questions)


def _shuffle(technique, questions, *args):
    """
    Shuffles the given list of questions as well as the options of any MCQs in the list using the given technique
    """
    # first shuffle question order
    technique(questions, *args)

    for question in questions:
        for subpart in question.subparts:
            # check if the subpart has options whose order can be shuffled
            if subpart.type == HWCentralQuestionType.MCMA or subpart.type == HWCentralQuestionType.MCSA:
                subpart.option_order = technique(range(get_option_count(subpart.options)), *args)

    return questions


def deal_for_user(user, questions):
    return questions


def deal_for_time(questions):
    return questions