TIME_INPUT_FORMAT = ('%H:%M',)  # 14:30
DATE_INPUT_FORMAT = ('%d %b %Y',)  # 25 Oct 2015

class ReadOnlyForm(object):
    """
    Mixin class to add-in read-only functionality to a form via the make_readonly method
    """

    @classmethod
    def make_field_readonly(cls, field):
        field.widget.attrs['readonly'] = True

    @classmethod
    def make_field_disabled(cls, field):
        field.widget.attrs['disabled'] = True

    def make_readonly(self):
        raise NotImplementedError("Subclass of ReadOnlyForm must implement make_readonly")
