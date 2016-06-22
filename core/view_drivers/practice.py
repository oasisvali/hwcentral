import django
from django.http import Http404
from django.shortcuts import render, redirect

from core.forms.practice import PracticeForm, OpenAssignmentForm
from core.models import Assignment
from core.routing.urlnames import UrlNames
from core.utils.references import HWCentralGroup
from core.utils.toast import redirect_with_success_toast
from core.view_drivers.assignment_id import create_shell_submission
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.base import AuthenticatedVM
from core.view_models.home import OpenStudentHomeBody
from core.view_models.practice import PracticeBody
from hwcentral.settings import LOGIN_REDIRECT_URL


class PracticeDriver(GroupDrivenViewCommonTemplate):
    def __init__(self, request):
        super(PracticeDriver, self).__init__(request)
        self.urlname = UrlNames.PRACTICE

    def teacher_endpoint(self):
        raise Http404

    def parent_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404


class PracticeGet(PracticeDriver):
    def student_endpoint(self):
        form = PracticeForm(self.user)
        return render(self.request, self.template, AuthenticatedVM(self.user,
                                                                   PracticeBody(form))
                      .as_context())

    def open_student_endpoint(self):
        return redirect(LOGIN_REDIRECT_URL)


class PracticePost(PracticeDriver):
    def create_new_student_assignment(self, aql):
        assigned = django.utils.timezone.now()
        due = assigned  # NOTE: HACK!!!
        number = Assignment.get_new_practice_number(aql, self.user)
        new_assignment = Assignment.objects.create(assignmentQuestionsList=aql,
                                                   content_object=self.user, assigned=assigned, due=due,
                                                   number=number)
        # generate shell submission
        shell_submission_db = create_shell_submission(new_assignment, self.user, new_assignment.assigned)
        return shell_submission_db

    def build_success_message(self, label):
        return '%s has been created successfully! Check out the chapter summary below and click <b>Begin Assignment</b> to start.' % label

    def open_student_endpoint(self):
        form = OpenAssignmentForm(self.user, self.request.POST)
        if form.is_valid():
            assignmentQuestionsList = form.cleaned_data['question_set']
            submission = self.create_new_student_assignment(assignmentQuestionsList)
            return redirect_with_success_toast(self.request,
                                               self.build_success_message(
                                                   'Assignment %s' % submission.assignment.get_title()),
                                               [UrlNames.SUBMISSION_ID.name, submission.pk])

        else:
            return render(self.request, UrlNames.HOME.get_template(HWCentralGroup.refs.OPEN_STUDENT),
                          AuthenticatedVM(self.user, OpenStudentHomeBody(self.user, form)).as_context())

    def student_endpoint(self):
        form = PracticeForm(self.user, self.request.POST)
        if form.is_valid():
            assignmentQuestionsList = form.cleaned_data['question_set']
            submission = self.create_new_student_assignment(assignmentQuestionsList)
            return redirect_with_success_toast(self.request,
                                               self.build_success_message(
                                                   'Practice Assignment %s' % submission.assignment.get_title()),
                                               [UrlNames.SUBMISSION_ID.name, submission.pk])

        else:
            return render(self.request, self.template,
                          AuthenticatedVM(self.user, PracticeBody(form)).as_context())
