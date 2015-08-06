from django import template

register = template.Library()


@register.filter('lettered_numbering')
def lettered_numbering_lowercase(value):
    assert (value > 0 and value <= 26)

    return chr(value + 96)