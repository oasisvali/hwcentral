###
#
# This file contains all the submission-related viewmodels used in the core hwcentral templates. for datamodels which
# are used by the logic, look at the data_models module
#
###
from core.forms.submission import ReadOnlySubmissionForm
from core.routing.urlnames import UrlNames
from core.utils.labels import get_fraction_label
from core.view_models.base import FormBody, ReadOnlyFormBody


class CorrectedSubmissionIdBody(ReadOnlyFormBody):
    def __init__(self, submission_db, submission_vm, user=None):
        self.submission_completion = get_fraction_label(submission_db.completion)
        if user is not None:
            # customize submission viewmodel for the given user
            submission_vm.change_img_urls_for_user(user)

        # build a readonly form representation of the submission so it is easier to render. True- disable dropdowns
        readonly_form = ReadOnlySubmissionForm(submission_vm, True)
        super(CorrectedSubmissionIdBody, self).__init__(readonly_form)

class UncorrectedSubmissionIdBody(FormBody):
    def __init__(self, submission_form, submission_db):
        self.submission_id = submission_db.pk
        self.submission_completion = get_fraction_label(submission_db.completion)
        super(UncorrectedSubmissionIdBody, self).__init__(submission_form, UrlNames.SUBMISSION_ID.name)


class SubmissionVM(object):
    """
    Contains data from the submission data model that is used by the submission id pages
    """

    def __init__(self, submission_dm, include_solutions):
        self.questions = submission_dm.get_protected_questions(include_solutions)
        self.answers = submission_dm.answers

    def change_img_urls_for_user(self, user):
        for question in self.questions:
            question.change_img_urls(user)

