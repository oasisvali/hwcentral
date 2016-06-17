import django
from django.http import Http404
from django.shortcuts import render

from cabinet import cabinet_api
from core.forms.submission import SubmissionForm
from core.routing.urlnames import UrlNames
from core.utils.assignment import get_student_assignment_submission_type
from core.utils.constants import HWCentralAssignmentType, HWCentralStudentAssignmentSubmissionType
from core.utils.toast import render_with_success_toast, render_with_error_toast, redirect_with_success_toast
from core.utils.user_checks import is_parent_child_relationship
from core.view_drivers.base import GroupDrivenViewTypeDrivenTemplate
from core.view_drivers.chart import is_subjectroom_classteacher_relationship
from core.view_models.base import AuthenticatedVM
from core.view_models.submission_id import UncorrectedSubmissionIdBody, SubmissionVMUnprotected, \
    SubmissionVMProtected, CorrectedSubmissionIdBodyDifferentUser, CorrectedSubmissionIdBodySubmissionUser
from grader.grader_api import grade
from hwcentral.exceptions import InvalidHWCentralAssignmentTypeError, InvalidStateError


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
        return is_parent_child_relationship(self.user, self.submission.student)

    def teacher_valid(self):
        # teacher should only see the submission if it was created by a student in his/her classroom or subjectroom
        return is_subjectroom_classteacher_relationship(self.submission.assignment.get_subjectroom(), self.user) or (
            (self.submission.assignment.get_subjectroom()).teacher == self.user)

    def admin_valid(self):
        # admin should only see the submission if it was created by a student of the same school
        return self.user.userinfo.school == (self.submission.assignment.get_subjectroom()).classRoom.school


class SubmissionIdGetPractice(SubmissionIdDriver):
    def __init__(self, request, submission):
        super(SubmissionIdGetPractice, self).__init__(request, submission)
        submission_type = get_student_assignment_submission_type(submission)
        if submission_type == HWCentralStudentAssignmentSubmissionType.CORRECTED:
            self.type = HWCentralAssignmentType.CORRECTED
        elif submission_type == HWCentralStudentAssignmentSubmissionType.UNCORRECTED:
            self.type = HWCentralAssignmentType.PRACTICE
        else:
            raise InvalidHWCentralAssignmentTypeError(submission_type)

    def parent_endpoint(self):
        raise Http404

    def teacher_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404

    def student_endpoint(self):
        if not self.student_valid():
            raise Http404

        if self.type == HWCentralAssignmentType.CORRECTED:
            submission_vm = SubmissionVMUnprotected(cabinet_api.get_submission(self.submission))
            return render(self.request, self.template,
                          AuthenticatedVM(self.user,
                                          CorrectedSubmissionIdBodySubmissionUser(self.user, self.submission,
                                                                                  submission_vm, True))
                          .as_context())
        elif self.type == HWCentralAssignmentType.PRACTICE:
            # we can assume at this point that a shell submission exists at the very least
            # get the submission data from the cabinet
            submission_dm = cabinet_api.get_submission(self.submission)
            # get a 'protected' version of the submission data (without solutions and targets)
            submission_vm = SubmissionVMProtected(submission_dm)
            # build the submission form using the submission data
            submission_form = SubmissionForm(submission_vm, True)
            return render(self.request, self.template, AuthenticatedVM(self.user,
                                                                       UncorrectedSubmissionIdBody(self.user,
                                                                                                   submission_form,
                                                                                                   self.submission,
                                                                                                   True)).as_context())
        else:
            raise InvalidHWCentralAssignmentTypeError(self.type)


class SubmissionIdPostPractice(SubmissionIdDriver):
    def __init__(self, request, submission):
        super(SubmissionIdPostPractice, self).__init__(request, submission)
        assert HWCentralStudentAssignmentSubmissionType.UNCORRECTED == get_student_assignment_submission_type(
            submission)

        self.type = HWCentralAssignmentType.PRACTICE

    def parent_endpoint(self):
        raise Http404

    def teacher_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404

    def student_endpoint(self):
        if not self.student_valid():
            raise Http404

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
            # update the submission in db
            self.submission.timestamp = django.utils.timezone.now()
            self.submission.completion = submission_dm.calculate_completion()
            self.submission.save()

            if 'correct' in self.request.POST:
                grade(self.submission, False)
                practice_assignment = self.submission.assignment
                practice_assignment.average = self.submission.marks
                practice_assignment.completion = self.submission.completion
                practice_assignment.save()
                return redirect_with_success_toast(self.request,
                                                   "Your practice assignment has been checked successfully.",
                                                   [UrlNames.SUBMISSION_ID.name, self.submission.pk])
            elif 'save' in self.request.POST:
                renderer = render_with_success_toast
                message = "Your submission has been saved."
            else:
                raise InvalidStateError


        else:
            renderer = render_with_error_toast
            message = 'Some of the answers were invalid. Please fix the errors below and try again.'

        return renderer(self.request, message, self.template,
                        AuthenticatedVM(self.user,
                                        UncorrectedSubmissionIdBody(self.user, submission_form,
                                                                    self.submission, True)).as_context())

class SubmissionIdGetCorrected(SubmissionIdDriver):
    def __init__(self, request, submission):
        super(SubmissionIdGetCorrected, self).__init__(request, submission)
        self.type = HWCentralAssignmentType.CORRECTED
        self.submission_vm = SubmissionVMUnprotected(cabinet_api.get_submission(submission))

    def student_endpoint(self):
        if not self.student_valid():
            raise Http404
        return render(self.request, self.template,
                      AuthenticatedVM(self.user,
                                      CorrectedSubmissionIdBodySubmissionUser(self.user, self.submission,
                                                                                self.submission_vm))
                      .as_context())

    def parent_endpoint(self):
        if not self.parent_valid():
            raise Http404
        return render(self.request, self.template,
                      AuthenticatedVM(self.user,
                                      CorrectedSubmissionIdBodyDifferentUser(self.submission, self.submission_vm,
                                                                               self.user)).as_context())

    def admin_endpoint(self):
        if not self.admin_valid():
            raise Http404
        return render(self.request, self.template,
                      AuthenticatedVM(self.user,
                                      CorrectedSubmissionIdBodyDifferentUser(self.submission, self.submission_vm,
                                                                               self.user)).as_context())

    def teacher_endpoint(self):
        if not self.teacher_valid():
            raise Http404
        return render(self.request, self.template,
                      AuthenticatedVM(self.user,
                                      CorrectedSubmissionIdBodyDifferentUser(self.submission, self.submission_vm,
                                                                               self.user)).as_context())


class SubmissionIdUncorrected(SubmissionIdDriver):
    def __init__(self, request, submission):
        super(SubmissionIdUncorrected, self).__init__(request, submission)
        self.type = HWCentralAssignmentType.UNCORRECTED

    def parent_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404

    def teacher_endpoint(self):
        raise Http404


class SubmissionIdGetUncorrected(SubmissionIdUncorrected):
    def student_endpoint(self):
        if not self.student_valid():
            raise Http404
        # we can assume at this point that a shell submission exists at the very least
        # get the submission data from the cabinet
        submission_dm = cabinet_api.get_submission(self.submission)
        # get a 'protected' version of the submission data (without solutions and targets)
        submission_vm = SubmissionVMProtected(submission_dm)
        # build the submission form using the submission data
        submission_form = SubmissionForm(submission_vm, True)
        return render(self.request, self.template, AuthenticatedVM(self.user,
                                                                   UncorrectedSubmissionIdBody(self.user,
                                                                                                 submission_form,
                                                                                                 self.submission)).as_context())


class SubmissionIdPostUncorrected(SubmissionIdUncorrected):
    def student_endpoint(self):
        if not self.student_valid():
            raise Http404
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

            renderer = render_with_success_toast
            message = "Your submission has been saved."
        else:
            renderer = render_with_error_toast
            message = 'Some of the answers were invalid. Please fix the errors below and try again.'

        return renderer(self.request, message, self.template,
                        AuthenticatedVM(self.user,
                                        UncorrectedSubmissionIdBody(self.user, submission_form,
                                                                      self.submission)).as_context())
