import django
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import render

from cabinet import cabinet_api
from core.forms.submission import SubmissionForm
from core.routing.urlnames import UrlNames
from core.utils.constants import HWCentralAssignmentType
from core.utils.toast import render_with_toast
from core.view_drivers.base import GroupDrivenViewTypeDrivenTemplate
from core.view_drivers.chart import is_subjectroom_classteacher_relationship
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import StudentSidebar, AdminSidebar, ParentSidebar, TeacherSidebar
from core.view_models.submission_id import UncorrectedSubmissionIdBody, SubmissionVMUnprotected, \
    SubmissionVMProtected, CorrectedSubmissionIdBodyDifferentUser, CorrectedSubmissionIdBodySubmissionUser


class SubmissionIdDriver(GroupDrivenViewTypeDrivenTemplate):
    def __init__(self, request, submission):
        super(SubmissionIdDriver, self).__init__(request)
        self.urlname = UrlNames.SUBMISSION_ID
        self.submission = submission

    # TODO: the checks performed here are fairly common logic (e.g. same validations used for charts also). Try refactor
    def student_valid(self):
        # student should only see the submission if it was created by them
        return self.user == self.submission.student

    def parent_valid(self):
        # parent should only see the submission if one of their students created it
        for child in self.user.home.children.all():
            if child == self.submission.student:
                return True

        return False

    def teacher_valid(self):
        # teacher should only see the submission if it was created by a student in his/her classroom or subjectroom
        return is_subjectroom_classteacher_relationship(self.submission.assignment.subjectRoom, self.user) or (
        self.submission.assignment.subjectRoom.teacher == self.user)

    def admin_valid(self):
        # admin should only see the submission if it was created by a student of the same school
        return self.user.userinfo.school == self.submission.assignment.subjectRoom.classRoom.school


class SubmissionIdGetCorrected(SubmissionIdDriver):
    def __init__(self, request, submission):
        super(SubmissionIdGetCorrected, self).__init__(request, submission)
        self.type = HWCentralAssignmentType.CORRECTED
        self.submission_vm = SubmissionVMUnprotected(cabinet_api.get_submission(submission))

    def student_endpoint(self):
        if not self.student_valid():
            return HttpResponseNotFound()
        return render(self.request, self.template,
                      AuthenticatedBase(StudentSidebar(self.user),
                                        CorrectedSubmissionIdBodySubmissionUser(self.user, self.submission,
                                                                                self.submission_vm))
                      .as_context())

    def parent_endpoint(self):
        if not self.parent_valid():
            return HttpResponseNotFound()
        return render(self.request, self.template,
                      AuthenticatedBase(ParentSidebar(self.user),
                                        CorrectedSubmissionIdBodyDifferentUser(self.submission, self.submission_vm,
                                                                  self.user)).as_context())

    def admin_endpoint(self):
        if not self.admin_valid():
            return HttpResponseNotFound()
        return render(self.request, self.template,
                      AuthenticatedBase(AdminSidebar(self.user),
                                        CorrectedSubmissionIdBodyDifferentUser(self.submission, self.submission_vm,
                                                                  self.user)).as_context())

    def teacher_endpoint(self):
        if not self.teacher_valid():
            return HttpResponseNotFound()
        return render(self.request, self.template,
                      AuthenticatedBase(TeacherSidebar(self.user),
                                        CorrectedSubmissionIdBodyDifferentUser(self.submission, self.submission_vm,
                                                                  self.user)).as_context())


class SubmissionIdUncorrected(SubmissionIdDriver):
    def __init__(self, request, submission):
        super(SubmissionIdUncorrected, self).__init__(request, submission)
        self.type = HWCentralAssignmentType.UNCORRECTED

    def parent_endpoint(self):
        return HttpResponseNotFound()

    def admin_endpoint(self):
        return HttpResponseNotFound()

    def teacher_endpoint(self):
        return HttpResponseNotFound()


class SubmissionIdGetUncorrected(SubmissionIdUncorrected):
    def student_endpoint(self):
        if not self.student_valid():
            return HttpResponseNotFound()
        # we can assume at this point that a shell submission exists at the very least
        # get the submission data from the cabinet
        submission_dm = cabinet_api.get_submission(self.submission)
        # get a 'protected' version of the submission data (without solutions and targets)
        submission_vm = SubmissionVMProtected(submission_dm)
        # build the submission form using the submission data
        submission_form = SubmissionForm(submission_vm, True)
        return render(self.request, self.template, AuthenticatedBase(StudentSidebar(self.user),
                                                                     UncorrectedSubmissionIdBody(self.user,
                                                                                                 submission_form,
                                                                                                 self.submission)).as_context())


class SubmissionIdPostUncorrected(SubmissionIdUncorrected):
    def student_endpoint(self):
        if not self.student_valid():
            return HttpResponseNotFound()
        # we can assume at this point that a shell submission exists at the very least
        # get the submission data from the cabinet
        submission_dm = cabinet_api.get_submission(self.submission)
        submission_vm = SubmissionVMProtected(submission_dm)
        submission_form = SubmissionForm(submission_vm, False, self.request.POST)
        if submission_form.is_valid():
            # update the submission data with the form data
            submission_dm.update_answers(submission_form.get_answers())
            # update the submission data in cabinet
            cabinet_api.update_submission(self.submission, submission_dm)
            # update the submisssion in db
            self.submission.timestamp = django.utils.timezone.now()
            self.submission.completion = submission_dm.calculate_completion()
            self.submission.save()

            message_level = messages.SUCCESS
            message = "Your submission has been saved.",
        else:
            message_level = messages.ERROR
            message = 'Some of the answers were invalid. Please fix the errors below and try again.'

        return render_with_toast(self.request, message_level, message, self.template,
                                 AuthenticatedBase(StudentSidebar(self.user),
                                                   UncorrectedSubmissionIdBody(self.user, submission_form,
                                                                               self.submission)).as_context())
