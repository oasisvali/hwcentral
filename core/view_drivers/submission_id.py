import django
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import render, redirect

from cabinet import cabinet_api
from core.forms.submission import SubmissionForm
from core.models import Announcement
from core.routing.urlnames import UrlNames
from core.utils.assignment import get_student_assignment_submission_type, is_student_assignment, \
    get_open_assignment_subjectroom
from core.utils.constants import HWCentralAssignmentType, HWCentralStudentAssignmentSubmissionType
from core.utils.open_student import OpenStudentUtils
from core.utils.references import HWCentralOpen
from core.utils.toast import render_with_success_toast, render_with_error_toast, redirect_with_success_toast
from core.utils.user_checks import is_parent_child_relationship
from core.view_drivers.base import GroupDrivenViewTypeDrivenTemplate
from core.view_drivers.chart import is_subjectroom_classteacher_relationship
from core.view_models.base import AuthenticatedVM
from core.view_models.sidebar import ProficiencyClass
from core.view_models.submission_id import UncorrectedSubmissionIdBody, SubmissionVMUnprotected, \
    SubmissionVMProtected, CorrectedSubmissionIdBodyDifferentUser, CorrectedSubmissionIdBodySubmissionUser, \
    AssignmentInfo, RevisionSubmissionIdBody
from edge.edge_api import calculate_edge_data
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


class SubmissionIdGetStudent(SubmissionIdDriver):
    def __init__(self, request, submission):
        super(SubmissionIdGetStudent, self).__init__(request, submission)
        submission_type = get_student_assignment_submission_type(submission)
        if submission_type == HWCentralStudentAssignmentSubmissionType.CORRECTED:
            self.type = HWCentralAssignmentType.CORRECTED  # a corrected student assignment uses the same template as the regular corrected assignment
        elif submission_type == HWCentralStudentAssignmentSubmissionType.UNCORRECTED:
            self.type = HWCentralAssignmentType.STUDENT
        else:
            raise InvalidHWCentralAssignmentTypeError(submission_type)

    def parent_endpoint(self):
        raise Http404

    def teacher_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404

    def render_corrected_submission(self, categorization):
        submission_vm = SubmissionVMUnprotected(cabinet_api.get_submission(self.submission))
        return render(self.request, self.template,
                      AuthenticatedVM(self.user,
                                      CorrectedSubmissionIdBodySubmissionUser(self.user, self.submission,
                                                                              submission_vm, categorization))
                      .as_context())

    def render_uncorrected_submission(self, categorization):
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
                                                                                               categorization)).as_context())

    def common_student_endpoint(self, categorization):
        """
        Handles both practice (for student) and open (for open student) assignments
        """
        if self.type == HWCentralAssignmentType.CORRECTED:
            return self.render_corrected_submission(categorization)

        elif self.type == HWCentralAssignmentType.STUDENT:  # assignment is currently active
            if not self.submission.revised:
                return render(self.request, UrlNames.SUBMISSION_ID.get_template('revision'),
                              AuthenticatedVM(self.user, RevisionSubmissionIdBody(self.user, self.submission,
                                                                                  categorization)).as_context())
            return self.render_uncorrected_submission(categorization)
        else:
            raise InvalidHWCentralAssignmentTypeError(self.type)

    def open_student_endpoint(self):
        if not self.student_valid():
            raise Http404

        return self.common_student_endpoint(AssignmentInfo.CAT_OPEN)

    def student_endpoint(self):
        if not self.student_valid():
            raise Http404

        return self.common_student_endpoint(AssignmentInfo.CAT_PRACTICE)


class SubmissionIdPostStudent(SubmissionIdDriver):
    def __init__(self, request, submission):
        super(SubmissionIdPostStudent, self).__init__(request, submission)
        assert HWCentralStudentAssignmentSubmissionType.UNCORRECTED == get_student_assignment_submission_type(
            submission)

        self.type = HWCentralAssignmentType.STUDENT

    def parent_endpoint(self):
        raise Http404

    def teacher_endpoint(self):
        raise Http404

    def admin_endpoint(self):
        raise Http404

    def create_proficiency_increase_notification(self, subjectroom, proficiency_class):
        Announcement.objects.create(
            object_id=self.user.pk,
            content_type=ContentType.objects.get_for_model(User),
            timestamp=django.utils.timezone.now(),
            announcer=HWCentralOpen.refs.SCHOOL.admin,
            message=ProficiencyClass.create_message(proficiency_class, subjectroom.classRoom.standard.number,
                                                    subjectroom.subject.name)
        )

    def process_form(self):
        # we can assume at this point that a shell submission exists at the very least
        # get the submission data from the cabinet
        submission_dm = cabinet_api.get_submission(self.submission)
        submission_vm = SubmissionVMProtected(submission_dm)
        submission_form = SubmissionForm(submission_vm, False, self.request.POST)
        return submission_dm, submission_form

    def update_submission(self, submission_dm, submission_form):
        # update the submission data with the form data
        submission_dm.update_answers(submission_form.get_answers())
        # update the submission data in cabinet
        cabinet_api.update_submission(self.submission, submission_dm)
        # update the submission in db
        self.submission.timestamp = django.utils.timezone.now()
        self.submission.completion = submission_dm.calculate_completion()
        self.submission.save()

    def update_assignment(self, register_ticks):
        """
        Only done on correction, not on save
        """
        grade(self.submission, register_ticks)
        assignment = self.submission.assignment
        assignment.average = self.submission.marks
        assignment.completion = self.submission.completion
        assignment.due = django.utils.timezone.now()
        assignment.save()

    @classmethod
    def build_corrected_message(cls, is_practice):
        return "Your " + ("practice " if is_practice else "") + "assignment has been corrected successfully"

    def update_badges(self, subjectroom, new_proficiency, old_proficiency):
        if new_proficiency == old_proficiency:
            return

        if old_proficiency.name is None:
            if new_proficiency >= ProficiencyClass.PAWN:
                self.create_proficiency_increase_notification(subjectroom,
                                                              ProficiencyClass.PAWN)
            if new_proficiency >= ProficiencyClass.KNIGHT:
                self.create_proficiency_increase_notification(subjectroom,
                                                              ProficiencyClass.KNIGHT)
            if new_proficiency == ProficiencyClass.KING:
                self.create_proficiency_increase_notification(subjectroom,
                                                              ProficiencyClass.KING)
        elif old_proficiency == ProficiencyClass.PAWN:
            if new_proficiency >= ProficiencyClass.KNIGHT:
                self.create_proficiency_increase_notification(subjectroom,
                                                              ProficiencyClass.KNIGHT)
            if new_proficiency == ProficiencyClass.KING:
                self.create_proficiency_increase_notification(subjectroom,
                                                              ProficiencyClass.KING)
        elif old_proficiency == ProficiencyClass.KNIGHT:
            if new_proficiency == ProficiencyClass.KING:
                self.create_proficiency_increase_notification(subjectroom,
                                                              ProficiencyClass.KING)
        else:
            InvalidStateError(
                "Invalid proficiency increase: %s to %s" % (old_proficiency, new_proficiency))

    def open_student_endpoint(self):
        if not self.student_valid():
            raise Http404

        if not self.submission.revised:
            # make sure that the revised flag is POSTed
            return handle_unrevised_post(self.request, self.submission)

        submission_dm, submission_form = self.process_form()
        if submission_form.is_valid():
            self.update_submission(submission_dm, submission_form)
            if 'correct' in self.request.POST:
                # log the old proficiency
                utils = OpenStudentUtils(self.user)
                subjectroom = get_open_assignment_subjectroom(self.submission.assignment)
                old_proficiency = utils.get_proficiency(subjectroom)
                old_proficiency = ProficiencyClass(old_proficiency)

                self.update_assignment(True)

                calculate_edge_data()

                # check if proficiency has improved
                new_proficiency = utils.get_proficiency(subjectroom)
                new_proficiency = ProficiencyClass(new_proficiency)

                self.update_badges(subjectroom, new_proficiency, old_proficiency)

                return redirect_with_success_toast(self.request,
                                                   SubmissionIdPostStudent.build_corrected_message(False),
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
                                                                    self.submission,
                                                                    AssignmentInfo.CAT_OPEN)).as_context())

    def student_endpoint(self):
        if not self.student_valid():
            raise Http404

        if not self.submission.revised:
            # make sure that the revised flag is POSTed
            return handle_unrevised_post(self.request, self.submission)

        submission_dm, submission_form = self.process_form()

        if submission_form.is_valid():
            self.update_submission(submission_dm, submission_form)
            if 'correct' in self.request.POST:
                self.update_assignment(False)
                return redirect_with_success_toast(self.request,
                                                   SubmissionIdPostStudent.build_corrected_message(True),
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
                                                                    self.submission,
                                                                    AssignmentInfo.CAT_PRACTICE)).as_context())

class SubmissionIdGetCorrected(SubmissionIdDriver):
    def __init__(self, request, submission):
        super(SubmissionIdGetCorrected, self).__init__(request, submission)
        assert not is_student_assignment(submission.assignment)
        self.type = HWCentralAssignmentType.CORRECTED
        self.submission_vm = SubmissionVMUnprotected(cabinet_api.get_submission(submission))
        self.categorization = AssignmentInfo.CAT_DUE

    def student_endpoint(self):
        if not self.student_valid():
            raise Http404
        return render(self.request, self.template,
                      AuthenticatedVM(self.user,
                                      CorrectedSubmissionIdBodySubmissionUser(self.user, self.submission,
                                                                              self.submission_vm, self.categorization))
                      .as_context())

    def parent_endpoint(self):
        if not self.parent_valid():
            raise Http404
        return render(self.request, self.template,
                      AuthenticatedVM(self.user,
                                      CorrectedSubmissionIdBodyDifferentUser(self.submission, self.submission_vm,
                                                                             self.user,
                                                                             self.categorization)).as_context())

    def admin_endpoint(self):
        if not self.admin_valid():
            raise Http404
        return render(self.request, self.template,
                      AuthenticatedVM(self.user,
                                      CorrectedSubmissionIdBodyDifferentUser(self.submission, self.submission_vm,
                                                                             self.user,
                                                                             self.categorization)).as_context())

    def teacher_endpoint(self):
        if not self.teacher_valid():
            raise Http404
        return render(self.request, self.template,
                      AuthenticatedVM(self.user,
                                      CorrectedSubmissionIdBodyDifferentUser(self.submission, self.submission_vm,
                                                                             self.user,
                                                                             self.categorization)).as_context())


class SubmissionIdUncorrected(SubmissionIdDriver):
    def __init__(self, request, submission):
        super(SubmissionIdUncorrected, self).__init__(request, submission)
        assert not is_student_assignment(submission.assignment)
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

        if not self.submission.revised:
            return render(self.request, UrlNames.SUBMISSION_ID.get_template('revision'),
                          AuthenticatedVM(self.user, RevisionSubmissionIdBody(self.user, self.submission,
                                                                              AssignmentInfo.CAT_DUE)).as_context())

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
                                                                                               AssignmentInfo.CAT_DUE)).as_context())


def handle_unrevised_post(request, submission):
    # make sure that the revised flag is POSTed
    if 'revised' in request.POST:
        submission.timestamp = django.utils.timezone.now()
        submission.revised = True
        submission.save()

    return redirect(UrlNames.SUBMISSION_ID.name, submission.pk)

class SubmissionIdPostUncorrected(SubmissionIdUncorrected):
    def student_endpoint(self):
        if not self.student_valid():
            raise Http404

        if not self.submission.revised:
            # make sure that the revised flag is POSTed
            return handle_unrevised_post(self.request, self.submission)

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
                                        UncorrectedSubmissionIdBody(self.user,
                                                                    submission_form,
                                                                    self.submission,
                                                                    AssignmentInfo.CAT_DUE)).as_context())
