from django import template
from django.template.defaultfilters import stringfilter

from hwcentral.exceptions import InvalidHWCentralGroupException

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
@stringfilter  # this will cast value to str
def add_str(value, arg):
    """
    casts both the value and argument to string and returns their concatenation
    @param value: the prefix string
    @param arg: the suffix string
    @return: value + arg
    """

    return value + str(arg)


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
def throw_InvalidHWCentralGroupException(value):
    """
    Hacky way to throw an exception in template
    @param value: the invalid group object
    """
    raise InvalidHWCentralGroupException(value.name)
