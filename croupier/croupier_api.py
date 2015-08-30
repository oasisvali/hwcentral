import random
import time

from cabinet import cabinet_api
from core.utils.constants import HWCentralQuestionType


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


def shuffle_for_user(user, questions):
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
                # storing a separate option order rather than ordering a list of options so that we can still easily
                # identify the correct and incorrect options based on the human-readable template format
                subpart.options.order = technique(range(subpart.options.get_option_count()), *args)

    return questions


def deal_for_user(user, questions):
    return questions


def deal_for_time(questions):
    return questions


def build_assignment_user_seed(user, assignment_questions_list):
    # first we grab the question data to build the assignment from the cabinet
    questions = cabinet_api.build_assignment(user, assignment_questions_list)

    # then we use croupier to randomize the order
    questions_randomized = shuffle_for_user(user, questions)

    # then we use croupier to deal the values
    return deal_for_user(user, questions_randomized)


def build_assignment_time_seed(student, assignment_questions_list):
    # first we grab the question data to build the assignment from the cabinet
    questions = cabinet_api.build_assignment(student, assignment_questions_list)

    # then we use croupier to randomize the order
    questions_randomized = shuffle_for_time(questions)

    # then we use croupier to deal the values
    return deal_for_time(questions_randomized)