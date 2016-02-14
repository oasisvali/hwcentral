import django
from django.http import Http404
from django.shortcuts import render

from core.forms.practice import PracticeForm
from core.models import Assignment
from core.routing.urlnames import UrlNames
from core.utils.toast import redirect_with_success_toast
from core.view_drivers.assignment_id import create_shell_submission
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.base import AuthenticatedVM
from core.view_models.practice import PracticeBody


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


class PracticePost(PracticeDriver):
    def student_endpoint(self):
        form = PracticeForm(self.user, self.request.POST)
        if form.is_valid():
            assignmentQuestionsList = form.cleaned_data['question_set']
            assigned = django.utils.timezone.now()
            due = assigned  # NOTE: HACK!!!
            number = Assignment.get_new_practice_number(assignmentQuestionsList, self.user)
            new_assignment = Assignment.objects.create(assignmentQuestionsList=assignmentQuestionsList,
                                                       content_object=self.user, assigned=assigned, due=due,
                                                       number=number)
            # generate shell submission and redirect
            shell_submission_db = create_shell_submission(new_assignment, self.user, new_assignment.assigned)
            return redirect_with_success_toast(self.request,
                                               '<div>Practice assignment %s has been created successfully!</div><div>You can save your progress by clicking on the SAVE button in the bottom right corner</div><div>Once completed, click on the SUBMIT button in the bottom right corner to check your answers and view solutions.</div>' % new_assignment.get_title(),
                                               [UrlNames.SUBMISSION_ID.name, shell_submission_db.pk])

        else:
            return render(self.request, self.template,
                          AuthenticatedVM(self.user, PracticeBody(form)).as_context())
