from django.http import HttpResponseNotFound
from django.shortcuts import render

from core.data_models.submission import SubmissionDM
from core.forms.submission import ReadOnlySubmissionForm
from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDriven
from core.view_models.assignment_id import ReadOnlyAssignmentBody
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import TeacherSidebar
from core.view_models.submission_id import SubmissionVM
from croupier import croupier


def render_readonly_assignment(request, user, sidebar, assignment_questions_list):
    """
    Renders an assignment (read-only) with the user's username as randomization key
    """
    questions_randomized_dealt = croupier.build_assignment_user_seed(user, assignment_questions_list)

    # finally build a shell submission
    shell_submission_dm = SubmissionDM.build_shell_submission(questions_randomized_dealt)

    # use a protected version of the submission data, and dont include solutions
    shell_submission_vm = SubmissionVM(shell_submission_dm, False)

    # and use it to build a readonly submission form which will help us easily render the assignment (False - don't disable dropdown)
    readonly_submission_form = ReadOnlySubmissionForm(shell_submission_vm, False)

    return render(request, UrlNames.ASSIGNMENT_ID.get_template(),
           AuthenticatedBase(sidebar, ReadOnlyAssignmentBody(readonly_submission_form)).as_context())


class AssignmentPreviewIdGet(GroupDriven):
    def __init__(self, request, assignment_questions_list):
        super(AssignmentPreviewIdGet, self).__init__(request)
        self.assignment_questions_list = assignment_questions_list

    def student_endpoint(self):
        return HttpResponseNotFound()

    def parent_endpoint(self):
        return HttpResponseNotFound()

    def admin_endpoint(self):
        return HttpResponseNotFound()

    def teacher_endpoint(self):
        # teacher can only see the assignment preview if he/she is a subject teacher for the standard and subject of the AQL
        if self.user.subjects_managed_set.filter(
                classRoom__standard=self.assignment_questions_list.standard,
                subject=self.assignment_questions_list.subject).exists():
            return render_readonly_assignment(self.request, self.user, TeacherSidebar(self.user),
                                              self.assignment_questions_list)

        return HttpResponseNotFound()