###
#
# This file contains all the submission-related viewmodels used in the core hwcentral templates. for datamodels which
# are used by the logic, look at the data_models module
#
###
from cabinet import cabinet
from core.forms.base import FormBody
from core.view_models.base import AuthenticatedBody


class CorrectedSubmissionBody(AuthenticatedBody):
    def __init__(self, submission):
        submission_dm = cabinet.get_submission(submission)
        self.questions = submission_dm.questions
        self.answers = submission_dm.answers


class UncorrectedSubmissionBody(FormBody):
    def __init__(self, submission, submission_form):
        super(UncorrectedSubmissionBody, self).__init__(submission_form)