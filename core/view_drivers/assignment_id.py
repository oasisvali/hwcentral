import django
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from core.forms.submission import ReadOnlySubmissionForm
from core.models import Submission
from core.data_models.submission import SubmissionDM
from core.routing.urlnames import UrlNames
from cabinet import cabinet_api
from core.utils.user_checks import is_student_assignment_relationship, \
    is_assignment_teacher_relationship
from core.view_drivers.base import GroupDrivenViewCommonTemplate
from core.view_models.assignment_id import AssignmentIdBody
from core.view_models.base import AuthenticatedBase
from core.view_models.sidebar import TeacherSidebar, AdminSidebar, ParentSidebar
from core.view_models.submission_id import SubmissionVMProtected
from croupier import croupier_api
from hwcentral.exceptions import InvalidStateError


class AssignmentIdGet(GroupDrivenViewCommonTemplate):
    def __init__(self, request, assignment):
        super(AssignmentIdGet, self).__init__(request)
        self.urlname = UrlNames.ASSIGNMENT_ID
        self.assignment = assignment

    def render_readonly_assignment(self, sidebar):
        """
        Renders an assignment (read-only) with the user's username as randomization key
        """
        authenticated_body = AssignmentIdBody(self.assignment,
                                              build_readonly_submission_form(self.user,
                                                                             self.assignment.assignmentQuestionsList))

        return render(self.request, self.template,
                      AuthenticatedBase(sidebar, authenticated_body).as_context())


class AssignmentIdGetInactive(AssignmentIdGet):

    def student_endpoint(self):
        return HttpResponseNotFound()
    def parent_endpoint(self):
        return HttpResponseNotFound()

    def admin_endpoint(self):
        # admin can only see this inactive assignment if it belongs to his/her school
        if self.assignment.subjectRoom.classRoom.school != self.user.userinfo.school:
            return HttpResponseNotFound()
        return self.render_readonly_assignment(AdminSidebar(self.user))

    def teacher_endpoint(self):
        # teacher can only see this inactive assignment if it was created by them or if it belongs to their classroom
        if is_assignment_teacher_relationship(self.assignment, self.user):
            return self.render_readonly_assignment(TeacherSidebar(self.user))

        return HttpResponseNotFound()


def create_shell_submission(assignment, student, timestamp):
    """
    Creates shell submission both in database and in the cabinet
    """
    questions_randomized_dealt = croupier_api.build_assignment_time_seed(student, assignment.assignmentQuestionsList)


    shell_submission_db = Submission.objects.create(assignment=assignment, student=student,
                                                    timestamp=timestamp,
                                                    completion=0.0)

    cabinet_api.build_submission(shell_submission_db, SubmissionDM.build_shell(questions_randomized_dealt))

    return shell_submission_db


def build_readonly_submission_form(user, assignment_questions_list):
    questions_randomized_dealt = croupier_api.build_assignment_user_seed(user, assignment_questions_list)

    # finally build a shell submission
    shell_submission_dm = SubmissionDM.build_shell(questions_randomized_dealt)

    # use a protected version of the submission data
    shell_submission_vm = SubmissionVMProtected(shell_submission_dm)

    # and use it to build a readonly submission form which will help us easily render the assignment
    return ReadOnlySubmissionForm(shell_submission_vm)

class AssignmentIdGetUncorrected(AssignmentIdGet):

    def student_endpoint(self):
        # student can only see this assignment if he/she belongs to the subjectroom the assignment is for
        if not is_student_assignment_relationship(self.user, self.assignment):
            return HttpResponseNotFound()

        # check if a submission already exists for this user for this assignment. if it exists, just redirect to that active submission
        try:
            submission = Submission.objects.get(student=self.user, assignment=self.assignment)
            return redirect(UrlNames.SUBMISSION_ID.name, submission.pk)
        except MultipleObjectsReturned:
            raise InvalidStateError(
                'Multiple submissions for user %s for assignment %s' % (self.user, self.assignment))
        except Submission.DoesNotExist:
            # generate shell submission and redirect
            shell_submission_db = create_shell_submission(self.assignment, self.user, django.utils.timezone.now())
            return redirect(UrlNames.SUBMISSION_ID.name, shell_submission_db.pk)


    def parent_endpoint(self):
        # parent can only see this assignment if it is assigned to one of their children
        for child in self.user.home.children.all():
            if is_student_assignment_relationship(child, self.assignment):
                return self.render_readonly_assignment(ParentSidebar(self.user))

        return HttpResponseNotFound()

    def admin_endpoint(self):
        # admin can only see this uncorrected assignment if it belongs to his/her school
        if self.assignment.subjectRoom.classRoom.school != self.user.userinfo.school:
            return HttpResponseNotFound()
        return self.render_readonly_assignment(AdminSidebar(self.user))

    def teacher_endpoint(self):
        # teacher can only see this uncorrected assignment if it was created by them or if it belongs to their classroom
        if is_assignment_teacher_relationship(self.assignment, self.user):
            return self.render_readonly_assignment(TeacherSidebar(self.user))

        return HttpResponseNotFound()
