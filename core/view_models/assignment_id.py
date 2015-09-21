from core.view_models.base import ReadOnlyFormBody
from core.view_models.submission_id import AssignmentInfo, AQLInfo, Revision


class BaseAssignmentIdBody(ReadOnlyFormBody):
    def __init__(self, user, assignment_questions_list, readonly_form):
        super(BaseAssignmentIdBody, self).__init__(readonly_form)
        self.aql_info = AQLInfo(assignment_questions_list)
        self.revision = Revision(user, assignment_questions_list)

class AssignmentPreviewIdBody(BaseAssignmentIdBody):
    pass


class AssignmentIdBody(BaseAssignmentIdBody):
    def __init__(self, user, assignment, readonly_form):
        super(AssignmentIdBody, self).__init__(user, assignment.assignmentQuestionsList, readonly_form)
        self.assignment_info = AssignmentInfo(assignment)
