from bs4 import BeautifulSoup
from django.forms import Select
from django.utils.safestring import mark_safe


class LockableSelect(Select):
    def __init__(self, attrs=None, choices=()):
        super(LockableSelect, self).__init__(attrs, choices)
        self.disable_unselected_options = False

    def render_option(self, selected_choices, option_value, option_label):
        rendered_option = super(LockableSelect, self).render_option(selected_choices, option_value, option_label)
        if not self.disable_unselected_options:
            return rendered_option

        option_tag = BeautifulSoup(rendered_option, 'html.parser').option
        if 'selected' in option_tag.attrs:
            return rendered_option

        option_tag.attrs['disabled'] = 'disabled'
        return mark_safe(str(option_tag))

    def lock_to_selected(self):
        self.disable_unselected_options = True


class ChosenNoSearchSelect(Select):
    CLASS_ATTR = 'chosen-no-search'

    def __init__(self, attrs=None, choices=()):
        if attrs is not None:
            if 'class' in attrs:
                attrs['class'] += ' ' + ChosenNoSearchSelect.CLASS_ATTR
            else:
                attrs['class'] = ChosenNoSearchSelect.CLASS_ATTR
        else:
            attrs = {'class': ChosenNoSearchSelect.CLASS_ATTR}
        super(ChosenNoSearchSelect, self).__init__(attrs, choices)
