from fractions import Fraction
import re

# Contains all the helper methods that use regex to allow for tag checking, substitution etc
from core.utils.helpers import merge_dicts
from croupier.exceptions import InvalidSubstitutionTagContentError
from hwcentral.exceptions import TagMismatchError


class SubstitutionTag(object):
    OPEN = re.compile(r'_\{[^\{]')
    CLOSE = re.compile(r'[^\}]\}_')
    FULL = re.compile(r'_\{(.+?)\}_')  # NOTE: this will also match evaluation tags, so make sure eval tags are subbed
    # out before subbing substitution tags


class EvaluationTag(object):
    OPEN = re.compile(r'_\{\{')
    CLOSE = re.compile(r'\}\}_')
    FULL = re.compile(r'_\{\{(.+?)\}\}_')


def replacer(replacements):
    replacements = iter(replacements)

    def replacer_callback(matchobj):
        return replacements.next()

    return replacer_callback


def sub_tags(tag, string, replacements):
    return tag.FULL.sub(replacer(replacements), string)


def sub_substitution_tags(string, replacements):
    return sub_tags(SubstitutionTag, string, replacements)


def sub_evaluation_tags(string, replacements):
    return sub_tags(EvaluationTag, string, replacements)


def get_tag_contents(tag, string):
    return [match.group(1) for match in tag.FULL.finditer(string)]


def get_substitution_tag_contents(string):
    substitution_tag_contents = get_tag_contents(SubstitutionTag, string)
    # substitution tag contents must only be a single variable
    for i in xrange(len(substitution_tag_contents)):
        split_contents = substitution_tag_contents[i].split()
        if len(split_contents) != 1:
            raise InvalidSubstitutionTagContentError()
        substitution_tag_contents[i] = split_contents[0]

    return substitution_tag_contents


def get_evaluation_tag_contents(string):
    return get_tag_contents(EvaluationTag, string)


def check_all_tags(string):
    check_substitution_tags(string)
    check_evaluation_tags(string)

def check_substitution_tags(string):
    check_tags(SubstitutionTag, string, 1, 1)


def check_evaluation_tags(string):
    check_tags(EvaluationTag, string)


def check_tags(tag, string, opening_offset=0, closing_offset=0):
    indices_opening_tag = [(match.end() - (opening_offset + 1)) for match in
                           tag.OPEN.finditer(string)]  # take the last index of the match
    indices_closing_tag = [(match.start() + closing_offset) for match in tag.CLOSE.finditer(string)]

    check_matching_tags(indices_opening_tag, indices_closing_tag)


def check_matching_tags(indices_opening_tag, indices_closing_tag):
    """
    Checks if the index positions of the opening and closing tags are matching
    @throws: TagMismatchError
    """

    if len(indices_opening_tag) != len(indices_closing_tag):
        raise TagMismatchError()

    opening_index = 0
    closing_index = 0
    prev_opening_index = -1
    prev_closing_index = -1
    for i in xrange(len(indices_opening_tag)):
        opening_index = indices_opening_tag[i]
        closing_index = indices_closing_tag[i]

        if (opening_index >= closing_index) or (opening_index <= prev_opening_index) or (
            closing_index <= prev_closing_index):
            raise TagMismatchError()

        prev_closing_index = closing_index
        prev_opening_index = opening_index


EVAL_HELPERS = {
    'Fraction': Fraction
}


def eval_no_globals(expression, variables):
    return eval(expression, {}, merge_dicts([EVAL_HELPERS, variables]))


def format_value_for_sub(value):
    if isinstance(value, Fraction):  # TODO: might be better approach to subclass fraction and override tostring
        return "\\frac{%s}{%s}" % (value.numerator, value.denominator)

    if value < 0:
        return '(%s)' % value

    return str(value)


def evaluate_substitute(text, variable_values):
    check_all_tags(text)
    # first sub evaluate
    eval_tag_contents = get_evaluation_tag_contents(text)
    replacements = [format_value_for_sub(eval_no_globals(expression, variable_values)) for expression in
                    eval_tag_contents]
    text = sub_evaluation_tags(text, replacements)
    # then sub substitutions
    substitution_tag_contents = get_substitution_tag_contents(text)
    replacements = [format_value_for_sub(variable_values[variable]) for variable in substitution_tag_contents]
    return sub_substitution_tags(text, replacements)
