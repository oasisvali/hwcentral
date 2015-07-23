from django.forms import forms


class SubmissionForm(forms.Form):
    def __init__(self, submission_db, submission_dm, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)

    def get_answers(self):
        return None