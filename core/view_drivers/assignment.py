from django.http import HttpResponseNotFound
from django.shortcuts import render

from core.forms.assignment import AssignmentForm
from core.models import Assignment, AssignmentQuestionsList, SubjectRoom
from core.routing.urlnames import UrlNames
from core.utils.toast import redirect_with_success_toast
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.assignment import AssignmentBody
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import TeacherSidebar


class AssignmentDriver(GroupDrivenViewCommonTemplate):
    def __init__(self, request, override=False):
        super(AssignmentDriver, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENT
        self.override = override

    def student_endpoint(self):
        return HttpResponseNotFound()

    def parent_endpoint(self):
        return HttpResponseNotFound()

    def admin_endpoint(self):
        return HttpResponseNotFound()


class AssignmentGet(AssignmentDriver):
    def teacher_endpoint(self):
        # form to create assignment from assignmentquestionslist
        form = AssignmentForm(self.user, self.override)
        return render(self.request, self.template, AuthenticatedBase(TeacherSidebar(self.user), AssignmentBody(form))
                      .as_context() )


class AssignmentPost(AssignmentDriver):
    def teacher_endpoint(self):
        # form to create assignment from assignmentquestionslist
        form = AssignmentForm(self.user, self.override, self.request.POST)
        if form.is_valid():
            assignmentQuestionsList = AssignmentQuestionsList.objects.get(pk=form.get_aql_pk())
            subjectRoom = SubjectRoom.objects.get(pk=form.get_subjectroom_pk())
            assigned = form.cleaned_data['assigned']
            due = form.cleaned_data['due']
            new_assignment = Assignment.objects.create(assignmentQuestionsList=assignmentQuestionsList,
                                                       subjectRoom=subjectRoom, assigned=assigned, due=due)
            return redirect_with_success_toast(self.request,
                                               'Assignment (%s) was created successfully.' % new_assignment)

        else:
            return render(self.request, self.template,
                          AuthenticatedBase(TeacherSidebar(self.user),AssignmentBody(form)).as_context() )
