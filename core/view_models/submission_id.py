###
#
# This file contains all the submission-related viewmodels used in the core hwcentral templates. for datamodels which
# are used by the logic, look at the data_models module
#
###
from cabinet import cabinet
from core.forms.submission import ReadOnlySubmissionForm
from core.routing.urlnames import UrlNames
from core.utils.labels import get_fraction_label
from core.view_models.base import FormBody, ReadOnlyFormBody


class CorrectedSubmissionIdBody(ReadOnlyFormBody):
    def __init__(self, submission):
        submission_dm = cabinet.get_submission(submission)
        super(CorrectedSubmissionIdBody, self).__init__(ReadOnlySubmissionForm(submission_dm))


class UncorrectedSubmissionIdBody(FormBody):
    def __init__(self, submission_form, submission_db):
        self.submission_id = submission_db.pk
        self.submission_completion = get_fraction_label(submission_db.completion)
        # TODO: later is probably better to create a submission vm which takes in a subset of the dm data rather than protecting dm
        submission_form.submission_dm.protect_solutions()
        submission_form.submission_dm.protect_targets()
        super(UncorrectedSubmissionIdBody, self).__init__(submission_form, UrlNames.SUBMISSION_ID.name)
