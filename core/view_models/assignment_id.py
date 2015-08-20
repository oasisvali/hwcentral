from core.view_models.base import ReadOnlyFormBody


class ReadOnlyAssignmentBody(ReadOnlyFormBody):
    def __init__(self, readonly_submission_form):
        readonly_submission_form.submission_dm.protect_solutions()
        super(ReadOnlyAssignmentBody, self).__init__(readonly_submission_form)
