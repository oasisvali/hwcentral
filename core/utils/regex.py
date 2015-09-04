import re

# Contains all the helper methods that use regex to allow for tag checking, substitution etc
from hwcentral.exceptions import TagMismatchError


class SubstitutionTag(object):
    OPEN = re.compile(r'_\{')
    CLOSE = re.compile(r'\}_')
    FULL = re.compile(r'_\{(.+?)\}_')


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
    return get_tag_contents(SubstitutionTag, string)


def get_evaluation_tag_contents(string):
    return get_tag_contents(EvaluationTag, string)


def check_substitution_tags(string):
    check_tags(SubstitutionTag, string)


def check_evaluation_tags(string):
    check_tags(EvaluationTag, string)


def check_tags(tag, string):
    indices_opening_tag = [(match.end() - 1) for match in tag.OPEN.finditer(string)]  # take the last index of the match
    indices_closing_tag = [match.start() for match in tag.CLOSE.finditer(string)]

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
