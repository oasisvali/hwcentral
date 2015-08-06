from django.forms import forms


class SubmissionFormField(forms.Field):
    """
    Abstract class for setting useful default behaviour
    """

    def __init__(self):
        super(SubmissionFormField, self).__init__(required=False)


class MCQFormField(SubmissionFormField):
    def __init__(self):
        super(MCQFormField, self).__init__()

class SubmissionForm(forms.Form):
    """
    Contains a flattened list of assignment answers as fields on the form
    """

    def __init__(self, submission_dm, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        # create a form field for each subpart


    def get_answers(self):
        return None