from django.http import HttpResponseNotFound
from django.shortcuts import render

from core.routing.urlnames import UrlNames
from core.utils import cabinet
from core.view_drivers.base import GroupDriven
from core.view_models.assignment_id import ReadonlyAssignmentBody
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import TeacherSidebar
from croupier import croupier


def render_readonly_assignment(request, user, sidebar, assignment_questions_list):
    """
    Renders an assignment (read-only) with the user's username as randomization key
    """
    # first we grab the question data to build the assignment from the cabinet
    aql = cabinet.build_assignment(assignment_questions_list)

    # then we use croupier to randomize the order
    aql_randomized = croupier.shuffle(user, aql)

    # then we use croupier to deal the values
    aql_randomized_dealt = croupier.deal(aql_randomized)

    render(request, UrlNames.ASSIGNMENT_ID.get_template(),
           AuthenticatedBase(sidebar, ReadonlyAssignmentBody(aql_randomized_dealt)).as_context())


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
                classRoom__standard__number=self.assignment_questions_list.standard.number,
                subject__pk=self.assignment_questions_list.subject.pk).exists():
            return render_readonly_assignment(self.request, self.user, TeacherSidebar(self.user),
                                              self.assignment_questions_list)

        return HttpResponseNotFound()