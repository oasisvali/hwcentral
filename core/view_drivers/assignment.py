from django.http import Http404
from django.shortcuts import render

from core.forms.assignment import AssignmentForm
from core.models import Assignment
from core.routing.urlnames import UrlNames
from core.utils.labels import get_subjectroom_label
from core.utils.toast import redirect_with_success_toast
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.assignment import AssignmentBody
from core.view_models.base import AuthenticatedVM


class AssignmentDriver(GroupDrivenViewCommonTemplate):
    def __init__(self, request, override=False):
        super(AssignmentDriver, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENT
        self.override = override

    def student_endpoint(self):
        raise Http404

    def parent_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404


class AssignmentGet(AssignmentDriver):
    def teacher_endpoint(self):
        # form to create assignment from assignmentquestionslist
        form = AssignmentForm(self.user, self.override)
        return render(self.request, self.template, AuthenticatedVM(self.user,
                                                                   AssignmentBody(form))
                      .as_context())


class AssignmentPost(AssignmentDriver):
    def teacher_endpoint(self):
        # form to create assignment from assignmentquestionslist
        form = AssignmentForm(self.user, self.override, self.request.POST)
        if form.is_valid():
            assignmentQuestionsList = form.cleaned_data['question_set']
            subjectRoom = form.cleaned_data['subjectroom']
            assigned = form.cleaned_data['assigned']
            due = form.cleaned_data['due']
            # check if same aql has been assigned in this subjectroom before, if yes increase number
            number = Assignment.get_new_assignment_number(assignmentQuestionsList, subjectRoom)
            new_assignment = Assignment.objects.create(assignmentQuestionsList=assignmentQuestionsList,
                                                       content_object=subjectRoom, assigned=assigned, due=due,
                                                       number=number)
            return redirect_with_success_toast(self.request,
                                               'Assignment %s for SubjectRoom %s was assigned successfully.' % (
                                                   new_assignment.get_title(),
                                                   get_subjectroom_label(new_assignment.get_subjectRoom())))

        else:
            return render(self.request, self.template,
                          AuthenticatedVM(self.user, AssignmentBody(form)).as_context())
