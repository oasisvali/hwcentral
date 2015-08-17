TIME_INPUT_FORMAT = ('%H:%M',)  # 14:30
DATE_INPUT_FORMAT = ('%d %b %Y',)  # 25 Oct 2015

class ReadOnlyForm(object):
    """
    Mixin class to add-in read-only functionality to a form via the make_readonly method
    """

    def make_readonly(self):
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True