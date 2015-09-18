from django.http import Http404
from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.view_drivers.assignment_id import build_readonly_submission_form
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.assignment_id import AssignmentPreviewIdBody
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import TeacherSidebar


class AssignmentPreviewIdGet(GroupDrivenViewCommonTemplate):
    def render_preview_assignment(self):
        authenticated_body = AssignmentPreviewIdBody(self.user, self.assignment_questions_list,
                                                     build_readonly_submission_form(self.user,
                                                                                    self.assignment_questions_list))

        return render(self.request, self.template,
                      AuthenticatedBase(TeacherSidebar(self.user), authenticated_body).as_context())

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
