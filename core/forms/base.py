class ReadOnlyForm(object):
    """
    Mixin class to add-in read-only functionality to a form via the make_readonly method
    """

    def make_readonly(self):
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True