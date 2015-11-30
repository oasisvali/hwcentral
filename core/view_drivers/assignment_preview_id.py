from django.http import Http404
from django.shortcuts import render
from core.data_models.submission import SubmissionDM
from core.forms.submission import ReadOnlySubmissionFormPreview

from core.routing.urlnames import UrlNames
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.assignment_id import AssignmentPreviewIdBody
from core.view_models.base import AuthenticatedVM
from core.view_models.sidebar import TeacherSidebar
from core.view_models.submission_id import SubmissionVMUnprotected
from croupier import croupier_api


class AssignmentPreviewIdGet(GroupDrivenViewCommonTemplate):

    def render_preview_assignment(self):
        questions_randomized_dealt = croupier_api.build_assignment_user_seed(self.user, self.assignment_questions_list)

        # now build a shell submission
        shell_submission_dm = SubmissionDM.build_shell(questions_randomized_dealt)

        # use an unprotected version of the submission data
        shell_submission_vm = SubmissionVMUnprotected(shell_submission_dm)

        # and use it to build a readonly submission form which will help us easily render the assignment
        assignment_preview_form = ReadOnlySubmissionFormPreview(shell_submission_vm)

        authenticated_body = AssignmentPreviewIdBody(self.user, self.assignment_questions_list,
                                                     assignment_preview_form)

        return render(self.request, self.template,
                      AuthenticatedVM(self.user, authenticated_body).as_context())

    def __init__(self, request, assignment_questions_list):
        super(AssignmentPreviewIdGet, self).__init__(request)
        self.assignment_questions_list = assignment_questions_list
        self.urlname = UrlNames.ASSIGNMENT_ID  # because the preview template is only a slight variation of the assignment_id template

    def student_endpoint(self):
        raise Http404

    def parent_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404

    def teacher_endpoint(self):
        # teacher can only see the assignment preview if he/she is a subject teacher for the standard and subject of the AQL
        if self.user.subjects_managed_set.filter(
                classRoom__standard=self.assignment_questions_list.standard,
                subject=self.assignment_questions_list.subject).exists():
            return self.render_preview_assignment()

        raise Http404
