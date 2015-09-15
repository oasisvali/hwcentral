from django import template
from django.template.defaultfilters import stringfilter

from core.utils.constants import HWCentralQuestionType
from hwcentral.exceptions import InvalidHWCentralGroupError, InvalidHWCentralQuestionTypeError

register = template.Library()


@register.filter(is_safe=True)
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)


@register.filter(is_safe=True)
@stringfilter  # this will cast value to unicode
def add_str(value, arg):
    """
    casts both the value and argument to unicode and returns their concatenation
    @param value: the prefix string
    @param arg: the suffix string
    @return: value + arg
    """

    return value + unicode(arg)


@register.filter(is_safe=True)
def get_form_field(value, arg):
    """
    Looks up the arg key in the value form's fields and returns it
    @param value: form from which to extract the field
    @param arg: field key which corresponds to the name of the field
    """
    assert arg in value.fields
    return value[arg]  # using form's special getitem logic instead of pulling the field straight from the fields dict


@register.filter(is_safe=True)
def get_list_elem(value, arg):
    """
    Returns the element in collection value at index arg
    @param value: The collection from which the element is to be looked up
    @param arg:  The index of the required element
    @return: The element in value at index arg
    """
    assert arg < len(value)
    return value[arg]

@register.filter(is_safe=True)
def answer_wrong(value, arg):
    """
    Checks if the given answer is wrong (even a single wrong subanswer makes the whole answer wrong)
    @param value: subpart answer's correct attribute
    @param arg: type of the subpart
    @return: True if answer is wrong, False otherwise
    """
    if arg == HWCentralQuestionType.CONDITIONAL:
        return (False in value)
    else:
        return not value


@register.filter(is_safe=True)
def is_correct_option_index_sa(value, arg):
    """
    Checks if the index specified in value is the index for the correct option for the given option order in arg
    @param value: index which is to be checked for correct option
    @param arg: option ordering for the mcsa subpart
    @return: True if the index in value corresponds to the correct option. False otherwise
    """
    assert value < len(arg)
    return (arg[value] == 0)    # since the correct option comes first in combined options, shuffled options have
                                # correct option at value = 0


@register.filter(is_safe=True)
def is_correct_option_index_ma(value, arg):
    """
    Checks if the index specified in value is the index for one of the correct options for the given options in arg
    @param value: index which is to be checked for correct option
    @param arg: options object for the mcsa subpart
    @return: True if the index in value corresponds to a correct option. False otherwise
    """
    assert value < len(arg.order)

    # since the correct options come first in combined options, shuffled options have
    # correct options at value < number of correct options
    return (arg.order[value] < len(arg.correct))


@register.filter(is_safe=True)
def throw_InvalidHWCentralGroupError(value):
    """
    Hacky way to throw an exception in template
    @param value: the invalid group object
    """
    raise InvalidHWCentralGroupError(value.name)


@register.filter(is_safe=True)
def throw_InvalidHWCentralQuestionTypeError(value):
    """
    Hacky way to throw an exception in template
    @param value: the invalid question type
    """
    raise InvalidHWCentralQuestionTypeError(value)
